from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


def fetch_instagram_data(username):
    options = Options()
    options.headless = True
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.instagram.com/accounts/login/")
        wait = WebDriverWait(driver, 20)

        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")

        username_field.send_keys("denemedeneme2015")
        password_field.send_keys("burak155")
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)  # Giriş işleminin tamamlanmasını bekleyin

        driver.get(f"https://www.instagram.com/{username}/")

        def wait_for_element(locator, timeout=30):
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

        # Profil adını çekme
        try:
            profile_name = wait_for_element((By.CSS_SELECTOR, "header section div h2")).text
        except Exception as e:
            print(f"Could not fetch profile name: {e}")
            profile_name = ""

        # Açıklama çekme
        try:
            description_element = wait_for_element((By.CSS_SELECTOR, "header section div.-vDIg span"))
            description = description_element.text if description_element else ""
        except Exception as e:
            print(f"Could not fetch description: {e}")
            description = ""

        # Gönderi sayısını çekme
        try:
            posts_element = wait_for_element((By.XPATH, "//header/section/ul/li[1]/span/span"))
            posts_text = posts_element.text if posts_element else "0"
            posts = int(posts_text.replace('.', '').replace(',', ''))
        except Exception as e:
            print(f"Could not fetch number of posts: {e}")
            posts = 0

        # Takipçi sayısını çekme
        try:
            followers_element = wait_for_element((By.XPATH, "//header/section/ul/li[2]/span/span"))
            followers_text = followers_element.get_attribute("title") if followers_element else ""
            if not followers_text:
                followers_text = followers_element.text if followers_element else "0"
            followers = int(followers_text.replace('.', '').replace(',', '').replace('k', '000').replace('m', '000000'))
        except Exception as e:
            print(f"Could not fetch number of followers: {e}")
            followers = 0

        # Takip edilen sayısını çekme
        try:
            follows_element = wait_for_element((By.XPATH, "//header/section/ul/li[3]/span/span"))
            follows_text = follows_element.text if follows_element else "0"
            follows = int(follows_text.replace('.', '').replace(',', '').replace('k', '000').replace('m', '000000'))
        except Exception as e:
            print(f"Could not fetch number of follows: {e}")
            follows = 0

        kullanıcı_verileri = {
            'nums/length username': len(username),
            'fullname words': len(profile_name.split()) if profile_name else 0,
            'nums/length fullname': sum(c.isdigit() for c in profile_name) / len(profile_name) if profile_name else 0,
            'description length': len(description),
            '#posts': posts,
            '#followers': followers,
            '#follows': follows
        }

        print("Fetched User Data: ", kullanıcı_verileri)
        return kullanıcı_verileri

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

    finally:
        driver.quit()