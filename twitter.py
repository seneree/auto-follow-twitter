import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import random

from selenium.webdriver.chrome.service import Service as ChromeService

COOKIES_RAW_FILE = "cookies.txt"
CLEANED_FILE = "cookies.json"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/125.0.0.0 Mobile/15E148 Safari/604.1",
]

def clean_raw_cookies():
    if not os.path.exists(COOKIES_RAW_FILE):
        print("❌ File 'cookies.txt' tidak ditemukan.")
        return

    with open(COOKIES_RAW_FILE, "r", encoding="utf-8") as f:
        raw = f.read()

    blocks = [b.strip() for b in raw.split("\n\n") if b.strip()]
    cleaned = []

    for i, block in enumerate(blocks, 1):
        try:
            data = json.loads(block)
            if isinstance(data, list):
                cookie_dict = {item["name"]: item["value"] for item in data if "name" in item and "value" in item}
                cleaned.append(cookie_dict)
        except Exception as e:
            print(f"⚠️ Skip blok {i}, error: {e}")

    with open(CLEANED_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ {len(cleaned)} cookies berhasil dibersihkan ke '{CLEANED_FILE}'")

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1366,768")
    options.add_argument("--log-level=3")
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    random_user_agent = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={random_user_agent}")
    
    chrome_service = ChromeService(log_level='3') 
    
    driver = webdriver.Chrome(service=chrome_service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def follow_with_cookie(cookie, target_url):
    driver = None
    try:
        driver = setup_driver()
        # Navigate to X.com home page first to set cookies
        driver.get("https://x.com/") 

        for name, value in cookie.items():
            try:
                if isinstance(value, str):
                    driver.add_cookie({"name": name, "value": value, "domain": ".x.com"})
            except Exception as e:
                continue
        
        # Now navigate to the target profile
        driver.get(target_url)
        print(f"Mengunjungi: {target_url}")
        time.sleep(random.uniform(5, 10))

        # --- Penanganan pop-up login/modal ---
        try:
            close_button = WebDriverWait(driver, 7).until(
                EC.element_to_be_clickable((By.XPATH, 
                    '//div[@aria-label="Tutup" or @aria-label="Close"] | '
                    '//span[contains(text(),"Not now") or contains(text(),"Nanti saja")]/ancestor::div[@role="button"]'
                ))
            )
            close_button.click()
            print("✅ Pop-up/modal berhasil ditutup.")
            time.sleep(random.uniform(1, 3)) 
        except:
            pass 

        follow_button_xpath = [
            '//div[@data-testid="UserFollowButton"]', 
            '//div[@data-testid="placementTracking"]//span[contains(text(),"Follow") or contains(text(),"Ikuti")]',
            '//div[@data-testid="PrimaryButton"]//span[contains(text(),"Follow") or contains(text(),"Ikuti")]',
            '//span[contains(text(),"Follow")]/ancestor::div[contains(@data-testid, "User")]',
            '//div[@data-testid="userActions"]//span[contains(text(),"Follow") or contains(text(),"Ikuti")]',
            '//div[@role="button" and (.//span[contains(text(), "Follow")] or .//span[contains(text(), "Ikuti")])]',
            '//div[contains(@aria-label, "Follow")]',
            '//div[contains(@data-testid, "UserFollowButton")]/div/div/span[contains(text(),"Follow") or contains(text(),"Ikuti")]',
            '//div[@data-testid="unfollow"]', 
        ]

        follow_status_message = "⚠️ Gagal: Tidak menemukan tombol 'Follow/Ikuti' yang dapat diklik atau sudah diikuti."
        
        try:
            follow_btn = None
            for xpath in follow_button_xpath:
                try:
                    follow_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    break 
                except:
                    continue

            if follow_btn:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", follow_btn)
                time.sleep(random.uniform(1, 2))

                button_text = follow_btn.text.strip().lower()

                if "mengikuti" in button_text or "following" in button_text or "unfollow" in button_text:
                    follow_status_message = "✅ Sudah diikuti atau akun terkunci (tombol: '{}').".format(button_text)
                elif "follow" in button_text or "ikuti" in button_text:
                    # --- KLIK MENGGUNAKAN JAVASCRIPT UNTUK LEBIH ANDAL ---
                    driver.execute_script("arguments[0].click();", follow_btn) 
                    print(f"✅ Berhasil mengklik tombol 'Follow/Ikuti' menggunakan JS.")
                    time.sleep(random.uniform(3, 5)) 
                    
                    # --- VERIFIKASI SETELAH KLIK ---
                    try:
                        # Refresh halaman untuk verifikasi status yang lebih pasti
                        driver.refresh()
                        time.sleep(random.uniform(5, 8)) # Tunggu refresh selesai

                        # Cari lagi tombol setelah refresh untuk verifikasi
                        verified_status_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, 
                                '//div[@data-testid="UserFollowButton"]//span[contains(text(),"Mengikuti") or contains(text(),"Following")] | '
                                '//div[@data-testid="unfollow"]'
                            ))
                        )
                        verified_text = verified_status_element.text.strip().lower()
                        if "mengikuti" in verified_text or "following" in verified_text or "unfollow" in verified_text:
                            follow_status_message = "✅ Berhasil follow dan diverifikasi setelah refresh!"
                        else:
                            follow_status_message = "❌ Status tidak berubah setelah refresh. Mungkin gagal follow."

                    except Exception as e_verify:
                        follow_status_message = f"❌ Gagal memverifikasi follow setelah klik dan refresh. Error: {e_verify}. Mungkin akun dibatasi."
                else:
                    follow_status_message = f"DEBUG: Tombol ditemukan, tapi teksnya tidak 'Follow/Ikuti': '{button_text}'."
            else:
                follow_status_message = "⚠️ Gagal: Tidak menemukan tombol 'Follow/Ikuti' yang dapat diklik."

        except Exception as e:
            follow_status_message = f"❌ Terjadi error saat mencoba follow {target_url}: {e}"
        
        print(follow_status_message)

    except Exception as e:
        print(f"❌ Terjadi error umum saat follow {target_url}: {e}")
    finally:
        if driver:
            driver.quit()

def menu_follow():
    if not os.path.exists(CLEANED_FILE):
        print(f"❌ File '{CLEANED_FILE}' tidak ditemukan. Silakan bersihkan cookies terlebih dahulu (menu 2).")
        return

    with open(CLEANED_FILE, "r") as f:
        cookies = json.load(f)

    if not cookies:
        print("❌ Tidak ada cookie yang ditemukan di 'cleaned.json'. Pastikan Anda sudah membersihkan cookies.")
        return

    target_input = input("🔗 Masukkan link profil X target (contoh: https://x.com/username): ").strip()
    
    parsed_url = urlparse(target_input)
    if parsed_url.netloc not in ("x.com", "www.x.com") or not parsed_url.path or parsed_url.path == '/':
        print("❌ Link X tidak valid. Pastikan formatnya https://x.com/username.")
        return
    
    target_username = parsed_url.path.split('/')[-1]
    if not target_username:
        print("❌ Tidak dapat mengekstrak username dari link yang diberikan. Pastikan link valid.")
        return

    print(f"\n🔁 Memulai follow {target_username} dengan {len(cookies)} akun...\n")

    for i, cookie in enumerate(cookies, 1):
        print(f"\n--- Menggunakan akun ke-{i} ---")
        follow_with_cookie(cookie, target_input)
        time.sleep(random.uniform(7, 15))

    print("\n✅ Proses follow selesai.")

def main():
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Auto Follow dari cleaned.json (Selenium Headless)")
        print("2. Bersihkan cookies.txt ke cleaned.json")
        print("0. Keluar")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            menu_follow()
        elif pilih == "2":
            clean_raw_cookies()
        elif pilih == "0":
            print("👋 Keluar.")
            break
        else:
            print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    main()