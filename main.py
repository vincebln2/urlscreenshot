import asyncio
import time
from pathlib import Path
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

async def screenshot(url: str):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    await asyncio.sleep(3)
    
    filename = f"screenshot_{int(time.time() * 1000)}.png"
    filepath = screenshots_dir / filename
    driver.save_screenshot(str(filepath))
    driver.quit()
    
    return filename

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
