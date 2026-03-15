import requests
import re
import time
import os

# Pobieramy dane z Secrets GitHuba
SESSION_COOKIE = os.environ.get('STRAVA_COOKIE')

headers = {
    "Cookie": f"_strava4_session={SESSION_COOKIE}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

def run():
    if not SESSION_COOKIE:
        print("BŁĄD: Brak STRAVA_COOKIE w Secrets!")
        return

    url = "https://www.strava.com"
    print("Łączę ze Stravą i szukam aktywności...")
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        
        # 1. Szukamy ID w danych JSON ukrytych w kodzie strony (najskuteczniejsze)
        # Strava trzyma tam informacje o wszystkich załadowanych wpisach
        ids = re.findall(r'"activity_id":(\d+)', r.text)
        
        # 2. Dodatkowo szukamy klasycznych wzorców (na wszelki wypadek)
        ids += re.findall(r'activity-(\d+)', r.text)
        ids += re.findall(r'data-activity-id="(\d+)"', r.text)
        
        unique_ids = list(set(ids))

        if not unique_ids:
            print("Nadal 0 aktywności. Możliwe, że Strava wymaga odświeżenia sesji.")
            # Opcjonalnie: wydrukuj kawałek kodu strony, żeby sprawdzić co widzi skrypt
            # print(r.text[:500]) 
            return

        print(f"Sukces! Znaleziono {len(unique_ids)} aktywności.")

        for aid in unique_ids:
            # Sprawdź, czy to nie Twoja własna aktywność (Strava nie pozwala dawać kudosów sobie)
            kudos_url = f"https://www.strava.com{aid}/kudos"
            res = requests.post(kudos_url, headers=headers)
            
            if res.status_code == 200:
                print(f"ID {aid}: Kudos wysłany! 👍")
            elif res.status_code == 429:
                print("Osiągnięto limit kudosów na dziś.")
                break
            else:
                print(f"ID {aid}: Pominięto (Status: {res.status_code})")
            time.sleep(2)
            
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    run()
