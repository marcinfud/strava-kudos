import os
import time
from playwright.sync_api import sync_playwright

def run():
    cookie_value = os.environ.get('STRAVA_COOKIE')
    if not cookie_value:
        print("Brak ciasteczka!")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        
        # Wstrzykujemy ciasteczko sesji
        context.add_cookies([{
            'name': '_strava4_session',
            'value': cookie_value,
            'domain': 'www.strava.com',
            'path': '/'
        }])

        page = context.new_page()
        print("Otwieram Stravę...")
        page.goto("https://www.strava.com", wait_until="networkidle")
        
        # Przewijamy kawałek, żeby załadować feed
        page.mouse.wheel(0, 2000)
        time.sleep(3)

        # Szukamy nieklikniętych kciuków
        buttons = page.query_selector_all('button[data-testid="kudos_button"]:has(svg[data-testid="unfilled_kudos"])')
        print(f"Znaleziono {len(buttons)} nowych aktywności.")

        for btn in buttons:
            btn.click()
            print("Kudos wysłany! 👍")
            time.sleep(1)

        browser.close()

if __name__ == "__main__":
    run()
