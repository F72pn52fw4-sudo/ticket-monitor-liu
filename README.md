# ticket-monitor-liu
# -*- coding: utf-8 -*-
import requests

# 你的 PushPlus Token
PUSHPLUS_TOKEN = "0af69c1298824342be163af0f50fb0fc"
TARGET_PRICE = 199

# 航班信息
DEP_CITY = "长沙"
ARR_CITY = "北京"
DATE = "2026-04-06"

def check_ticket():
    # 这里是模拟查询，后续我帮你换成真实接口
    return {
        "success": True,
        "price": 199,
        "dep": DEP_CITY,
        "arr": ARR_CITY,
        "date": DATE,
        "channel": "海航小程序"
    }

def send_wechat(title, content):
    url = "https://www.pushplus.plus/send"
    data = {
        "token": PUSHPLUS_TOKEN,
        "title": title,
        "content": content,
        "template": "markdown"
    }
    try:
        requests.post(url, json=data, timeout=10)
    except:
        pass

if __name__ == "__main__":
    ticket = check_ticket()
    if ticket and ticket.get("success"):
        price = ticket["price"]
        print(f"价格：{price} 元")
        if price <= TARGET_PRICE:
            content = f"""### ✈️ 特价机票放票提醒
- 航线：{DEP_CITY} → {ARR_CITY}
- 日期：{DATE}
- 价格：**{price} 元**
- 渠道：海航小程序
"""
            send_wechat("✈️ 低价机票已放票！", content)
            print("已推送微信")
