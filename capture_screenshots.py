from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent / 'docs' / 'screenshots'
root.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})

    page.goto('http://127.0.0.1:5000', wait_until='networkidle', timeout=30000)
    page.screenshot(path=str(root / 'dashboard.png'), full_page=True)

    page.goto('http://127.0.0.1:5000/login', wait_until='networkidle', timeout=30000)
    page.screenshot(path=str(root / 'login.png'), full_page=True)

    page.goto('http://127.0.0.1:5000/admin', wait_until='networkidle', timeout=30000)
    page.screenshot(path=str(root / 'admin.png'), full_page=True)

    browser.close()

    print('Captured screenshots:')
    for item in sorted(root.iterdir()):
        print(item.name)
