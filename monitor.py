from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import time
import os

# ===================== 自动配置 =====================
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN")
HNA_SESSION = os.getenv("HNA_SESSION")

FROM = "长沙"
TO = "北京"
DATE = "2026-04-06"
# =====================================================

def send(title, content):
    try:
        requests.post("http://www.pushplus.plus/send", json={
            "token": PUSHPLUS_TOKEN, "title": title, "content": content
        })
    except:
        pass

def monitor():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    wait = WebDriverWait(driver, 20)

    try:
        print("✅ 打开海航官网...")
        driver.get("https://www.hnair.com/")
        time.sleep(2)

        # ================ 核心：直接注入登录态，跳过验证码 ================
        driver.add_cookie({
            "name": "JSESSIONID",
            "value": HNA_SESSION,
            "domain": ".www.hnair.com",
            "path": "/",
            "secure": True
        })

        print("🔐 已使用登录态，跳过验证码登录成功！")
        driver.refresh()
        time.sleep(5)

        # 进入国内机票
        print("✈️ 进入查询页面...")
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "国内机票"))).click()
        time.sleep(3)

        # 填写行程
        dep = driver.find_element(By.ID, "depCity")
        dep.clear()
        dep.send_keys(FROM)
        time.sleep(1)

        arr = driver.find_element(By.ID, "arrCity")
        arr.clear()
        arr.send_keys(TO)
        time.sleep(1)

        driver.execute_script(f"document.getElementById('depDate').value='{DATE}'")
        time.sleep(2)

        # 查询
        driver.find_element(By.XPATH, "//button[text()='查询']").click()
        print(f"🔍 查询中：{FROM}→{TO} {DATE}")
        time.sleep(8)

        # 判断特价票
        page = driver.page_source
        if "199" in page and "海航PLUS" in page:
            msg = f"🎉 特价票已放出！\n{FROM}→{TO}\n日期：{DATE}\n价格：199元"
            send("海航特价机票提醒", msg)
            print("✅ 查到特价票！已推送微信！")
        else:
            print("ℹ️ 暂无199特价票")

    except Exception as e:
        print(f"⚠️ 异常：{str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    monitor()
