from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://localhost:8000/00%20-%20Comece%20Aqui.html')
    page.screenshot(path='screenshot.png', full_page=True)
    browser.close()
