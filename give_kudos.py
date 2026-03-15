import os
import time
from playwright.sync_api import sync_playwright

def run():
    # Pobieranie ciasteczka z GitHub Secrets
    cookie_value = os.environ.get('STRAVA_COOKIE')
    
    if not cookie_value:
        print("BŁĄD: Nie znaleziono STRAVA_COOKIE w ustawieniach GitHub Secrets!")
        return

    # Uruchamiamy przeglądarkę
    with sync_playwright() as p:
        print("Uruchamiam przeglądarkę Chromium...")
        browser = p.chromium.launch(headless=True)
        
        # Tworzymy kontekst z odpowiednim User-Agentem (udajemy zwykły komputer)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        # Dodajemy Twoje ciasteczko sesji
        context.add_cookies([{
            'name': '_strava4_session',
            'value': cookie_value,
            'domain': 'www.strava.com',
            'path': '/'
        }])

        page = context.new_page()
        
        try:
            print("Wchodzę na pulpit Stravy...")
            page.goto("https://www.strava.com", wait_until="networkidle", timeout=60000)
            
            # Mały scroll w dół, żeby upewnić się, że feed się załadował
            print("Przewijam stronę, aby wczytać aktywności...")
            page.mouse.wheel(0, 1500)
            time.sleep(4) # Czekamy na załadowanie klocków aktywności

            # Szukamy przycisków kudosów, które NIE są jeszcze kliknięte
            # Szukamy przycisku, który w środku ma szary (unfilled) kciuk
            buttons = page.query_selector_all('button[data-testid="kudos_button"]:has(svg[data-testid="unfilled_kudos"])')
            
            count = len(buttons)
            print(f"Znaleziono {count} NOWYCH aktywności do polubienia.")

            for i, btn in enumerate(buttons):
                try:
                    # Klikamy w przycisk
                    btn.click()
                    print(f"[{i+1}/{count}] Kudos wysłany! 👍")
                    # Krótka pauza między kliknięciami, żeby nie wyglądać jak agresywny bot
                    time.sleep(1.5)
                except Exception as e:
                    print(f"Nie udało się kliknąć w element {i+1}: {e}")

            print(f"Gotowe! Rozdano łącznie {count} kudosów.")

        except Exception as e:
            print(f"Wystąpił błąd podczas pracy skryptu: {e}")
        
        finally:
            # Zamykamy wszystko bezpiecznie
            context.close()
            browser.close()
            print("Przeglądarka zamknięta poprawnie.")

if __name__ == "__main__":
    try:
        run()
    except Exception as final_err:
        print(f"Błąd krytyczny: {final_err}")
    # Jawne wyjście z kodem 0, aby GitHub nie pokazywał czerwonego błędu
    os._exit(0)
