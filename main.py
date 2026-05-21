from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import json
import re
import urllib.parse
from bs4 import BeautifulSoup

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class FetchRequest(BaseModel):
    url: str
    password: str = ""

class FetchResult(BaseModel):
    success: bool
    type: str = ""
    file_url: str = ""
    filename: str = ""
    platform: str = ""
    error: str = ""

def detect_platform(url: str) -> str:
    for platform, pattern in {
        "risu":  r"risu\.(io|cc)/",
        "myppt": r"myppt\.cc/",
        "lurl":  r"lurl\.cc/",
        "imgus": r"imgus\.net/",
        "ppt":   r"ppt\.cc/",
    }.items():
        if re.search(pattern, url, re.IGNORECASE):
            return platform
    return ""

def curl_get(url: str, referer: str = "", cookies: str = "") -> str:
    """用 curl 模擬真實瀏覽器，繞過 Cloudflare 基本保護"""
    cmd = [
        "curl", "-sL",
        "-A", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "-H", "Accept-Language: zh-TW,zh;q=0.9,en;q=0.8",
        "-H", "Accept-Encoding: gzip, deflate, br",
        "-H", "Connection: keep-alive",
        "--compressed",
        "--max-time", "20",
    ]
    if referer:
        cmd += ["-H", f"Referer: {referer}"]
    if cookies:
        cmd += ["-b", cookies]
    cmd.append(url)

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    return result.stdout

def curl_post(url: str, data: dict, referer: str = "") -> str:
    """POST 表單（用於密碼提交）"""
    form_data = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in data.items())
    cmd = [
        "curl", "-sL",
        "-A", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "-H", "Accept-Language: zh-TW,zh;q=0.9,en;q=0.8",
        "-H", "Content-Type: application/x-www-form-urlencoded",
        "-H", f"Referer: {referer or url}",
        "--compressed",
        "--max-time", "20",
        "-d", form_data,
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    return result.stdout

def make_absolute(src: str, base_url: str) -> str:
    if src.startswith("http"):
        return src
    parsed = urllib.parse.urlparse(base_url)
    if src.startswith("//"):
        return f"{parsed.scheme}:{src}"
    if src.startswith("/"):
        return f"{parsed.scheme}://{parsed.netloc}{src}"
    return urllib.parse.urljoin(base_url, src)

def extract_media(html: str, base_url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # 影片
    for video in soup.find_all("video"):
        src = video.get("src") or (video.find("source") or {}).get("src", "")
        if src and not src.startswith("blob:"):
            return {"type": "video", "file_url": make_absolute(src, base_url)}

    # 音檔
    for audio in soup.find_all("audio"):
        src = audio.get("src") or (audio.find("source") or {}).get("src", "")
        if src:
            return {"type": "audio", "file_url": make_absolute(src, base_url)}

    # script 裡的媒體 URL
    for script in soup.find_all("script"):
        text = script.string or ""
        m = re.search(r'["\']((https?://)[^"\']+\.(mp4|m3u8|jpg|jpeg|png|gif|webp|mp3|ogg)(\?[^"\']*)?)["\']', text)
        if m:
            src = m.group(1)
            ext = m.group(3).lower()
            t = "video" if ext in ("mp4", "m3u8") else "audio" if ext in ("mp3", "ogg") else "image"
            return {"type": t, "file_url": src}

    # og:image
    og = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "og:image"})
    if og and og.get("content"):
        src = og["content"]
        if src and "placeholder" not in src and "logo" not in src.lower():
            return {"type": "image", "file_url": make_absolute(src, base_url)}

    # img tags
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and src.startswith("http") and not any(x in src.lower() for x in ["logo", "icon", "avatar", "favicon", "banner"]):
            return {"type": "image", "file_url": src}

    return {}

def guess_filename(url: str, media_type: str) -> str:
    path = urllib.parse.urlparse(url).path
    name = path.rstrip("/").split("/")[-1]
    if "." not in name:
        ext = {"image": "jpg", "video": "mp4", "audio": "mp3"}.get(media_type, "bin")
        name = f"backup_{name}.{ext}"
    return name or f"backup.{media_type}"

def submit_password(html: str, page_url: str, password: str) -> str:
    """找到密碼表單並提交"""
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find("form")
    if not form:
        return html

    action = form.get("action", page_url)
    if not action.startswith("http"):
        parsed = urllib.parse.urlparse(page_url)
        action = f"{parsed.scheme}://{parsed.netloc}{action}" if action.startswith("/") else urllib.parse.urljoin(page_url, action)

    data = {}
    for inp in form.find_all("input"):
        name = inp.get("name")
        if name:
            data[name] = inp.get("value", "")

    # 自動填密碼欄位
    for key in list(data.keys()):
        if any(x in key.lower() for x in ["pass", "pw", "password", "pwd", "secret"]):
            data[key] = password

    method = (form.get("method") or "post").lower()
    if method == "post":
        return curl_post(action, data, referer=page_url)
    else:
        qs = urllib.parse.urlencode(data)
        return curl_get(f"{action}?{qs}", referer=page_url)

def needs_password(html: str) -> bool:
    lower = html.lower()
    return any(x in lower for x in [
        'type="password"', "type='password'",
        "請輸入密碼", "enter password", "password required",
        "密碼", "password"
    ]) and "input" in lower

@app.post("/api/fetch", response_model=FetchResult)
def fetch_media(req: FetchRequest):
    url = req.url.strip()
    if not url.startswith("http"):
        url = "https://" + url

    platform = detect_platform(url)
    if not platform:
        raise HTTPException(400, "無法辨識平台，請確認網址格式")

    try:
        # 第一次抓頁面
        html = curl_get(url)
        if not html:
            return FetchResult(success=False, platform=platform, error="無法連線到目標網站，請稍後再試")

        # 需要密碼就提交
        if req.password and needs_password(html):
            html = submit_password(html, url, req.password)

        media = extract_media(html, url)

        if not media or not media.get("file_url"):
            # 嘗試找頁面裡的直接連結
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if re.search(r'\.(mp4|jpg|jpeg|png|gif|webp|mp3|ogg)(\?|$)', href, re.I):
                    ext = re.search(r'\.(mp4|jpg|jpeg|png|gif|webp|mp3|ogg)', href, re.I).group(1).lower()
                    t = "video" if ext == "mp4" else "audio" if ext in ("mp3","ogg") else "image"
                    return FetchResult(
                        success=True,
                        type=t,
                        file_url=make_absolute(href, url),
                        filename=guess_filename(href, t),
                        platform=platform,
                    )

            return FetchResult(success=False, platform=platform,
                error="查無媒體內容，連結可能已過期或密碼錯誤")

        file_url = media["file_url"]
        media_type = media["type"]

        return FetchResult(
            success=True,
            type=media_type,
            file_url=file_url,
            filename=guess_filename(file_url, media_type),
            platform=platform,
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(504, "請求逾時，請稍後再試")
    except Exception as e:
        raise HTTPException(500, f"抓取失敗: {str(e)}")

@app.get("/api/health")
def health():
    return {"status": "ok"}
