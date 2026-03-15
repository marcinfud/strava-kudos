import requests
import re
import os

SESSION_COOKIE = os.environ.get('STRAVA_COOKIE')

headers = {
    "Cookie": f"_strava4_session={SESSION_COOKIE}",
    "User-Agent": "Strava/350.11 (iPhone; iOS 17.4.1; Scale/3.00)", # Udajemy iPhone'a
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def run():
    # Używamy innego adresu - mobilnego dashboardu
    url = "https://www.strava.com"
    r = requests.get(url, headers=headers)
    
    # Szukamy ID w szerszym zakresie (same cyfry w kontekście aktywności)
    ids = re.findall(r'activity/(\d{9,12})', r.text)
    unique_ids = list(set(ids))
    
    if not unique_ids:
        print("Nadal 0. Strava całkowicie blokuje ten dostęp.")
        # Sprawdźmy czy w ogóle jesteśmy zalogowani w tej sesji
        if "login" in r.url or "Log In" in r.text:
            print("STATUS: Wylogowany. Ciasteczko wygasło!")
        return

    print(f"Sukces! Znaleziono {len(unique_ids)} ID aktywności przez widok mobilny.")
    # ... tutaj reszta kodu z pętlą POST (tak jak wcześniej)
