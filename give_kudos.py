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
        print("BŁĄD: Nie znaleziono zmiennej STRAVA_COOKIE w Secrets!")
        return

    url = "https://www.strava.com"
    print("Łączę ze Stravą...")
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        # Szukamy ID aktywności w kodzie strony
        ids = re.findall(r'activity/(\d{10,12})', r.text)
        unique_ids = list(set(ids))
        
        print(f"Znaleziono {len(unique_ids)} aktywności.")

        for aid in unique_ids:
            kudos_url = f"https://www.strava.com{aid}/kudos"
            res = requests.post(kudos_url, headers=headers)
            if res.status_code == 200:
                print(f"ID {aid}: Kudos wysłany! 👍")
            else:
                print(f"ID {aid}: Pominąłem (kod: {res.status_code})")
            time.sleep(2)
            
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    run()
