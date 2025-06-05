import asyncio
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = FastAPI()

screenshots_dir = Path("/app/screenshots")
screenshots_dir.mkdir(exist_ok=True)
app.mount("/screenshots", StaticFiles(directory=str(screenshots_dir)), name="screenshots")

class ScreenshotRequest(BaseModel):
    url: str

def screenshot_sync_bidi(url: str):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.enable_bidi = True
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(3)
        
        filename = f"screenshot_{int(time.time() * 1000)}.png"
        filepath = screenshots_dir / filename
        driver.save_screenshot(str(filepath))
        return filename
    finally:
        driver.quit()

executor = ThreadPoolExecutor(max_workers=2)

async def screenshot(url: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, screenshot_sync_bidi, url)

@app.post("/screenshot")
async def post(request: ScreenshotRequest):
    filename = await screenshot(request.url)
    return {"filename": filename, "url": f"/screenshots/{filename}"}

@app.get("/screenshot")
async def get(url: str):
    filename = await screenshot(url)
    return {"filename": filename, "url": f"/screenshots/{filename}"}

@app.get("/")
async def root():
    return {"status": "running"}
