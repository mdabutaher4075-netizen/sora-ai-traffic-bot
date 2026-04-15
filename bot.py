import time
import random
import threading
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# আপনার সাইট লিঙ্ক
MY_SITE = "https://sites.google.com/view/sora-ai-studio-free"

def get_residential_proxy():
    # Elite/Residential মানের প্রক্সি ফিল্টার
    api = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=yes&anonymity=elite"
    try:
        res = requests.get(api)
        proxies = [p for p in res.text.split('\r\n') if p]
        return random.choice(proxies)
    except:
        return None

def start_hit():
    proxy = get_residential_proxy()
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # র্যান্ডম ইউজার এজেন্ট (কখনো পিসি, কখনো মোবাইল)
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0",
        "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
    ]
    options.add_argument(f"user-agent={random.choice(ua_list)}")
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # ১. গুগল রিফারার মাস্কিং করে সাইটে প্রবেশ
        driver.get(f"https://www.google.com/url?q={MY_SITE}")
        time.sleep(random.randint(5, 7))

        # ২. মানুষের মতো পেজ স্ক্রল করা (বাটন খোঁজার আগে)
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)

        # ৩. বাটন ক্লিক করা (আপনার সাইটের নীল বাটনটি খুঁজে বের করবে)
        try:
            # Google Sites-এর বাটনগুলো সাধারণত 'a' ট্যাগ বা 'role=button' হিসেবে থাকে
            button = driver.find_element(By.XPATH, "//a[contains(., 'AI Video Generate Free')]")
            ActionChains(driver).move_to_element(button).perform() # মাউস হোভার
            time.sleep(1)
            button.click()
            print("Successfully clicked the Ad Button!")
        except:
            # যদি সরাসরি না পায় তবে সব লিঙ্কের মধ্যে একটিতে র্যান্ডম ক্লিক করবে
            links = driver.find_elements(By.TAG_NAME, "a")
            if links:
                random.choice(links).click()

        # ৪. অ্যাড পেজে ১৫ সেকেন্ড অ্যাকশন করা (স্ক্রল ও ক্লিক সিমুলেশন)
        # উইন্ডো হ্যান্ডেল পরিবর্তন (যদি নতুন ট্যাবে অ্যাড ওপেন হয়)
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])

        for _ in range(3):
            driver.execute_script(f"window.scrollBy(0, {random.randint(200, 500)});")
            time.sleep(random.randint(3, 5))
        
        print("View completed with full interaction.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

# একসাথে অনেকগুলো হিট পাঠানোর জন্য (১ মিনিটে ৫০+)
def run_batch():
    threads = []
    for _ in range(10): # প্রতি ব্যাচে ১০টি থ্রেড একসাথে চলবে
        t = threading.Thread(target=start_hit)
        threads.append(t)
        t.start()
        time.sleep(1) # ০.৫-১ সেকেন্ড গ্যাপ দিয়ে নতুন সেশন শুরু
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    while True:
        run_batch()
        time.sleep(random.randint(10, 20)) # প্রতি ব্যাচের মাঝে বিরতি
