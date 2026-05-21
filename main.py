from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright
import asyncio
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

    # 影片
    for video in soup.find_all("video"):
        src = video.get("src", "")
        if not src:
            s = video.find("source")
            src = s.get("src", "") if s else ""
        if src and not src.startswith("blob:"):
            return {"type": "video", "file_url": make_absolute(src, base_url)}

    # 音檔
    for audio in soup.find_all("audio"):
        src = audio.get("src", "")
        if not src:
            s = audio.find("source")
            src = s.get("src", "") if s else ""
        if src:
            return {"type": "audio", "file_url": make_absolute(src, base_url)}

    # script 裡的媒體 URL
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

    # og:image
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        src = og["content"]
        if src and "placeholder" not in src and "logo" not in src.lower():
            return {"type": "image", "file_url": make_absolute(src, base_url)}

    # data-src
    for img in soup.find_all("img", attrs={"data-src": True}):
        src = img["data-src"]
        if src and not any(x in src.lower() for x in ["logo","icon","avatar","favicon"]):
            return {"type": "image", "file_url": make_absolute(src, base_url)}

    # 一般 img
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and not any(x in src.lower() for x in ["logo","icon","avatar","favicon","banner","placeholder"]):
            return {"type": "image", "file_url": make_absolute(src, base_url)}

    return {}

def guess_filename(url: str, media_type: str) -> str:
    path = urllib.parse.urlparse(url).path
    name = path.rstrip("/").split("/")[-1]
    if "." not in name:
        ext = {"image":"jpg","video":"mp4","audio":"mp3"}.get(media_type,"bin")
        name = f"backup_{name}.{ext}"
    return name or f"backup.{media_type}"

async def fetch_with_browser(url: str, password: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="zh-TW",
        )
        page = await context.new_page()

        # 移除 webdriver 特徵
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # 等待 Cloudflare 驗證通過（最多等 10 秒）
        for _ in range(10):
            title = await page.title()
            if "just a moment" not in title.lower():
                break
            await asyncio.sleep(1)

        # 若有密碼欄位就填入
        if password:
            pw_input = page.locator('input[type="password"]').first
            if await pw_input.count() > 0:
                await pw_input.fill(password)
                # 找提交按鈕
                submit = page.locator('button[type="submit"], input[type="submit"]').first
                if await submit.count() > 0:
                    await submit.click()
                    await page.wait_for_load_state("domcontentloaded")

        # 等待媒體載入
        await asyncio.sleep(2)
        html = await page.content()
        await browser.close()
        return html

@app.post("/api/fetch", response_model=FetchResult)
async def fetch_media(req: FetchRequest):
    url = req.url.strip()
    if not url.startswith("http"):
        url = "https://" + url

    platform = detect_platform(url)
    if not platform:
        raise HTTPException(400, "無法辨識平台，請確認網址格式")

    try:
        html = await fetch_with_browser(url, req.password)
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
