import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os

# ===================== 自动读取GitHub加密配置 =====================
USER = os.getenv("HNA_ACCOUNT")
PWD = os.getenv("HNA_PASSWORD")
TOKEN = os.getenv("PUSHPLUS_TOKEN")

# 固定查询：长沙 → 北京 4月6日 海航PLUS199
FROM = "长沙"
TO = "北京"
DATE = "2026-04-06"
# =================================================================

def send(title, content):
    """推送微信消息"""
    try:
        requests.post("http://www.pushplus.plus/send", json={
            "token": TOKEN, "title": title, "content": content
        })
    except:
        pass

def monitor():
    """全自动监控主程序"""
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options)
    driver.set_page_load_timeout(30)
    wait = WebDriverWait(driver, 25)

    try:
        print("✅ 启动成功，正在访问海航官网...")
        driver.get("https://www.hnair.com/")
        time.sleep(3)

        # 自动点击登录
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='登录']"))).click()
            time.sleep(2)
        except:
            pass

        # 自动输入账号密码
        driver.find_element(By.ID, "username").send_keys(USER)
        driver.find_element(By.ID, "password").send_keys(PWD)
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[text()='登录']").click()
        print("🔐 已提交登录，自动过验证中...")
        time.sleep(7)

        # 自动进入国内机票
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "国内机票"))).click()
        time.sleep(3)

        # 自动填写行程
        dep = driver.find_element(By.ID, "depCity")
        dep.clear()
        dep.send_keys(FROM)
        time.sleep(1)

        arr = driver.find_element(By.ID, "arrCity")
        arr.clear()
        arr.send_keys(TO)
        time.sleep(1)

        # 自动填日期
        driver.execute_script(f"document.getElementById('depDate').value='{DATE}'")
        time.sleep(2)

        # 自动查询
        driver.find_element(By.XPATH, "//button[text()='查询']").click()
        print(f"🔍 查询中：{FROM}→{TO} {DATE}")
        time.sleep(8)

        # 自动识别PLUS 199特价票
        page = driver.page_source
        if "199" in page and "海航PLUS" in page:
            msg = f"🎉 抢到特价票！\n{FROM}→{TO}\n日期：{DATE}\n价格：海航PLUS 199元"
            send("海航特价票提醒", msg)
            print("✅ 查到特价票！已推送微信！")
        else:
            print("ℹ️ 暂无199特价票")

    except Exception as e:
        print(f"⚠️ 运行异常：{str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    monitor()
