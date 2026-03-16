from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import time
import os

# 自动读取 GitHub 密钥
USER = os.getenv("HNA_ACCOUNT")
PWD = os.getenv("HNA_PASSWORD")
TOKEN = os.getenv("PUSHPLUS_TOKEN")

# 航班查询配置
FROM = "长沙"
TO = "北京"
DATE = "2026-04-06"

# PushPlus 微信推送
def send(title, content):
    try:
        requests.post("http://www.pushplus.plus/send", json={
            "token": TOKEN,
            "title": title,
            "content": content
        })
    except:
        pass

# 主监控程序
def monitor():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    wait = WebDriverWait(driver, 25)

    try:
        print("✅ 正在打开海南航空官网...")
        driver.get("https://www.hnair.com/")
        time.sleep(3)

        # 登录
        print("🔐 准备登录...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='登录']"))).click()
        time.sleep(2)

        driver.find_element(By.ID, "username").send_keys(USER)
        driver.find_element(By.ID, "password").send_keys(PWD)
        driver.find_element(By.XPATH, "//button[text()='登录']").click()
        time.sleep(7)

        # 进入国内机票
        print("✈️ 进入机票查询页面...")
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "国内机票"))).click()
        time.sleep(3)

        # 填写出发地、目的地、日期
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
        print(f"🔍 查询：{FROM}→{TO} {DATE}")
        driver.find_element(By.XPATH, "//button[text()='查询']").click()
        time.sleep(8)

        # 判断是否有 199 特价票
        page = driver.page_source
        if "199" in page and "海航PLUS" in page:
            msg = f"🎉 发现特价票！\n{FROM}→{TO}\n日期：{DATE}\n价格：海航PLUS 199元"
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
