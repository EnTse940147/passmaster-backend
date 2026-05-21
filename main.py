from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cloudscraper
import httpx
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

TURNSTILE_SECRET = "0x4AAAAAADTd3C2m2o09b0QBK-7tKiD-NyA"

class FetchRequest(BaseModel):
    url: str
    password: str = ""
    turnstile_token: str = ""

class FetchResult(BaseModel):
    success: bool
    type: str = ""
    file_url: str = ""
    filename: str = ""
    platform: str = ""
    error: str = ""

def verify_turnstile(token: str) -> bool:
    try:
        resp = httpx.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={"secret": TURNSTILE_SECRET, "response": token},
            timeout=10,
        )
        return resp.json().get("success", False)
    except:
        return False

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

def make_absolute(src: str, base_url: str) -> str:
    if not src:
        return ""
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

    for video in soup.find_all("video"):
        src = video.get("src", "")
        if not src:
            s = video.find("source")
            src = s.get("src", "") if s else ""
        if src and not src.startswith("blob:"):
            return {"type": "video", "file_url": make_absolute(src, base_url)}

    for audio in soup.find_all("audio"):
        src = audio.get("src", "")
        if not src:
            s = audio.find("source")
            src = s.get("src", "") if s else ""
        if src:
            return {"type": "audio", "file_url": make_absolute(src, base_url)}

    for script in soup.find_all("script"):
        text = script.string or ""
        m = re.search(
            r'["\']((https?://)[^"\']+\.(mp4|m3u8|jpg|jpeg|png|gif|webp|mp3|ogg)(\?[^"\']*)?)["\']',
            text
        )
        if m:
            src = m.group(1)
            ext = m.group(3).lower()
            t = "video" if ext in ("mp4","m3u8") else "audio" if ext in ("mp3","ogg") else "image"
            return {"type": t, "file_url": src}

    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        src = og["content"]
        if src and "placeholder" not in src and "logo" not in src.lower():
            return {"type": "image", "file_url": make_absolute(src, base_url)}

    for img in soup.find_all("img", attrs={"data-src": True}):
        src = img["data-src"]
        if src and not any(x in src.lower() for x in ["logo","icon","avatar","favicon"]):
            return {"type": "image", "file_url": make_absolute(src, base_url)}

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and not any(x in src.lower() for x in ["logo","icon","avatar","favicon","banner","placeholder"]):
            return {"type": "image", "file_url": make_absolute(src, base_url)}

    return {}

def needs_password(html: str) -> bool:
    lower = html.lower()
    return 'type="password"' in lower or "type='password'" in lower

def submit_password(scraper, html: str, page_url: str, password: str) -> str:
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
    for key in list(data.keys()):
        if any(x in key.lower() for x in ["pass","pw","password","pwd","secret"]):
            data[key] = password
    method = (form.get("method") or "post").lower()
    if method == "post":
        resp = scraper.post(action, data=data, headers={"Referer": page_url})
    else:
        resp = scraper.get(action, params=data, headers={"Referer": page_url})
    return resp.text

def guess_filename(url: str, media_type: str) -> str:
    path = urllib.parse.urlparse(url).path
    name = path.rstrip("/").split("/")[-1]
    if "." not in name:
        ext = {"image":"jpg","video":"mp4","audio":"mp3"}.get(media_type,"bin")
        name = f"backup_{name}.{ext}"
    return name or f"backup.{media_type}"

@app.post("/api/fetch", response_model=FetchResult)
def fetch_media(req: FetchRequest):
    # 驗證 Turnstile
    if not req.turnstile_token:
        raise HTTPException(400, "請完成人機驗證")
    if not verify_turnstile(req.turnstile_token):
        raise HTTPException(403, "人機驗證失敗，請重試")

    url = req.url.strip()
    if not url.startswith("http"):
        url = "https://" + url

    platform = detect_platform(url)
    if not platform:
        raise HTTPException(400, "無法辨識平台，請確認網址格式")

    try:
        scraper = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False}
        )
        resp = scraper.get(url, timeout=20)
        html = resp.text

        if not html:
            return FetchResult(success=False, platform=platform, error="無法連線到目標網站")

        if needs_password(html):
            if not req.password:
                return FetchResult(success=False, platform=platform, error="此連結需要密碼，請輸入密碼後再試")
            html = submit_password(scraper, html, url, req.password)

        media = extract_media(html, url)

        if not media or not media.get("file_url"):
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                m = re.search(r'\.(mp4|jpg|jpeg|png|gif|webp|mp3|ogg)(\?|$)', href, re.I)
                if m:
                    ext = m.group(1).lower()
                    t = "video" if ext=="mp4" else "audio" if ext in ("mp3","ogg") else "image"
                    return FetchResult(
                        success=True, type=t,
                        file_url=make_absolute(href, url),
                        filename=guess_filename(href, t),
                        platform=platform,
                    )
            return FetchResult(success=False, platform=platform,
                error="查無媒體內容，連結可能已過期或密碼錯誤")

        return FetchResult(
            success=True,
            type=media["type"],
            file_url=media["file_url"],
            filename=guess_filename(media["file_url"], media["type"]),
            platform=platform,
        )

    except Exception as e:
        raise HTTPException(500, f"抓取失敗: {str(e)}")

@app.get("/api/health")
def health():
    return {"status": "ok"}
