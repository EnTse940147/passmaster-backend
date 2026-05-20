"""
PassMaster 後端 - Python FastAPI
支援平台: Risu, MyPPT, Lurl, Imgus, PPt.cc
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup
import re
import urllib.parse

app = FastAPI(title="PassMaster API")

# 允許所有前端來源（部署時可改為你的前端網址）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
}

class FetchRequest(BaseModel):
    url: str
    password: str = ""

class FetchResult(BaseModel):
    success: bool
    type: str = ""        # image | video | audio | link
    file_url: str = ""
    filename: str = ""
    platform: str = ""
    error: str = ""


def detect_platform(url: str) -> str:
    patterns = {
        "risu":  r"risu\.(io|cc)/",
        "myppt": r"myppt\.cc/",
        "lurl":  r"lurl\.cc/",
        "imgus": r"imgus\.net/",
        "ppt":   r"ppt\.cc/",
        "mork":  r"mork\.cc/",
    }
    for platform, pattern in patterns.items():
        if re.search(pattern, url, re.IGNORECASE):
            return platform
    return ""


async def fetch_page(url: str, password: str = "") -> str:
    """取得頁面 HTML，自動處理密碼表單提交"""
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=15) as client:
        resp = await client.get(url)
        html = resp.text

        # 若頁面有密碼表單且有提供密碼，POST 提交
        if password and ("password" in html.lower() or "密碼" in html):
            soup = BeautifulSoup(html, "html.parser")
            form = soup.find("form")
            if form:
                action = form.get("action", url)
                if not action.startswith("http"):
                    base = urllib.parse.urlparse(url)
                    action = f"{base.scheme}://{base.netloc}{action}"
                data = {}
                for inp in form.find_all("input"):
                    name = inp.get("name")
                    val = inp.get("value", "")
                    if name:
                        data[name] = val
                # 自動填入密碼
                for key in list(data.keys()):
                    if "pass" in key.lower() or "pw" in key.lower():
                        data[key] = password
                resp = await client.post(action, data=data)
                html = resp.text

        return html


def extract_media(html: str, base_url: str) -> dict:
    """從 HTML 中找出媒體元素"""
    soup = BeautifulSoup(html, "html.parser")

    # 影片
    video = soup.find("video")
    if video:
        src = video.get("src") or ""
        if not src:
            source = video.find("source")
            if source:
                src = source.get("src", "")
        if src:
            if src.startswith("blob:"):
                # blob URL 需要後端另外處理，這邊先回傳提示
                return {"type": "video", "file_url": src, "note": "blob"}
            return {"type": "video", "file_url": make_absolute(src, base_url)}

    # 音檔
    audio = soup.find("audio")
    if audio:
        src = audio.get("src") or ""
        if not src:
            source = audio.find("source")
            if source:
                src = source.get("src", "")
        if src:
            return {"type": "audio", "file_url": make_absolute(src, base_url)}

    # 圖片 (og:image 優先，通常是原圖)
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        src = og["content"]
        if src and not src.endswith("logo") and "placeholder" not in src:
            return {"type": "image", "file_url": make_absolute(src, base_url)}

    # 頁面內 img
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and src.startswith("http") and not any(x in src for x in ["logo", "avatar", "icon", "favicon"]):
            return {"type": "image", "file_url": src}

    return {}


def make_absolute(src: str, base_url: str) -> str:
    if src.startswith("http"):
        return src
    parsed = urllib.parse.urlparse(base_url)
    if src.startswith("//"):
        return f"{parsed.scheme}:{src}"
    if src.startswith("/"):
        return f"{parsed.scheme}://{parsed.netloc}{src}"
    return urllib.parse.urljoin(base_url, src)


def guess_filename(url: str, media_type: str) -> str:
    path = urllib.parse.urlparse(url).path
    name = path.rstrip("/").split("/")[-1]
    if "." not in name:
        ext = {"image": "jpg", "video": "mp4", "audio": "mp3"}.get(media_type, "bin")
        name = f"backup_{name}.{ext}"
    return name or f"backup.{media_type}"


# ── 各平台解析器 ──────────────────────────────────────────

async def parse_risu(url: str, password: str) -> dict:
    html = await fetch_page(url, password)
    media = extract_media(html, url)
    if media:
        return media
    # Risu 影片可能以 blob 提供；嘗試找 data-src 或 script 裡的 URL
    soup = BeautifulSoup(html, "html.parser")
    for script in soup.find_all("script"):
        text = script.string or ""
        m = re.search(r'["\'](https?://[^"\']+\.(mp4|m3u8|jpg|png|gif|webp|mp3|ogg))["\']', text)
        if m:
            src = m.group(1)
            ext = m.group(2)
            t = "video" if ext in ("mp4", "m3u8") else "audio" if ext in ("mp3", "ogg") else "image"
            return {"type": t, "file_url": src}
    return {}


async def parse_myppt(url: str, password: str) -> dict:
    html = await fetch_page(url, password)
    return extract_media(html, url)


async def parse_lurl(url: str, password: str) -> dict:
    html = await fetch_page(url, password)
    return extract_media(html, url)


async def parse_imgus(url: str, password: str) -> dict:
    html = await fetch_page(url, password)
    soup = BeautifulSoup(html, "html.parser")
    # Imgus 通常把圖片放在 .img-fluid 或 #main-image
    for selector in ["#main-image", ".img-fluid", "img[id*='image']"]:
        el = soup.select_one(selector)
        if el and el.get("src"):
            return {"type": "image", "file_url": make_absolute(el["src"], url)}
    return extract_media(html, url)


async def parse_ppt(url: str, password: str) -> dict:
    html = await fetch_page(url, password)
    soup = BeautifulSoup(html, "html.parser")
    # PPt.cc 直接重導向或顯示媒體
    meta_refresh = soup.find("meta", attrs={"http-equiv": "refresh"})
    if meta_refresh:
        content = meta_refresh.get("content", "")
        m = re.search(r"url=(.+)", content, re.IGNORECASE)
        if m:
            redirect = m.group(1).strip().strip("'\"")
            return {"type": "link", "file_url": redirect}
    return extract_media(html, url)


PARSERS = {
    "risu":  parse_risu,
    "myppt": parse_myppt,
    "lurl":  parse_lurl,
    "imgus": parse_imgus,
    "ppt":   parse_ppt,
}


# ── API 端點 ──────────────────────────────────────────────

@app.post("/api/fetch", response_model=FetchResult)
async def fetch_media(req: FetchRequest):
    url = req.url.strip()
    if not url.startswith("http"):
        url = "https://" + url

    platform = detect_platform(url)
    if not platform:
        raise HTTPException(400, "無法辨識平台，請確認網址格式")
    if platform == "mork":
        raise HTTPException(503, "Mork 平台目前暫無服務")

    parser = PARSERS.get(platform)
    if not parser:
        raise HTTPException(400, f"尚未支援此平台: {platform}")

    try:
        result = await parser(url, req.password)
    except httpx.TimeoutException:
        raise HTTPException(504, "請求逾時，請稍後再試")
    except Exception as e:
        raise HTTPException(500, f"抓取失敗: {str(e)}")

    if not result or not result.get("file_url"):
        return FetchResult(success=False, platform=platform, error="查無內容，連結可能已過期或密碼錯誤")

    file_url = result["file_url"]
    media_type = result.get("type", "image")
    filename = guess_filename(file_url, media_type)

    return FetchResult(
        success=True,
        type=media_type,
        file_url=file_url,
        filename=filename,
        platform=platform,
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}
