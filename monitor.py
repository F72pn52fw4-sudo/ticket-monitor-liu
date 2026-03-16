import requests
import time
import os
import json

# ================= 配置 =================
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN")
JSESSIONID = os.getenv("JSESSIONID")

FROM = "长沙"
TO = "北京"
DATE = "2026-04-06"
# =======================================

def send_wechat(title, content):
    """推送消息"""
    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSHPLUS_TOKEN,
        "title": title,
        "content": content
    }
    try:
        requests.post(url, json=data, timeout=10)
        print("✅ 推送成功！")
    except Exception as e:
        print(f"❌ 推送失败：{e}")

def check_flight():
    """调用海航API查询航班"""
    # 海航API接口 (模拟浏览器请求)
    url = "https://www.hnair.com/hna-web-api/flight/queryFlightList"
    
    # 请求头，模拟已登录状态
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Cookie": f"JSESSIONID={JSESSIONID}"
    }
    
    # 请求参数
    payload = {
        "depCityName": FROM,
        "arrCityName": TO,
        "depDate": DATE,
        "routeType": "OW",
        "cabinClass": "ALL",
        "flightType": "ALL",
        "pageNum": 1,
        "pageSize": 10
    }
    
    try:
        print(f"🔍 正在查询 {FROM} -> {TO} {DATE}...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        result = response.json()
        
        # 解析结果（根据实际返回结构调整）
        if result.get("data") and result["data"].get("flightList"):
            flight_list = result["data"]["flightList"]
            special_tickets = []
            
            for flight in flight_list:
                # 查找海航PLUS 199元产品
                for cabin in flight.get("cabinList", []):
                    if cabin.get("productName") and "海航PLUS" in cabin["productName"]:
                        price = cabin.get("price", {}).get("totalPrice", "未知")
                        if price == "199" or (isinstance(price, (int, float)) and price <= 199):
                            flight_info = f"航班：{flight['flightNo']}\n时间：{flight['depTime']}\n价格：{price}元"
                            special_tickets.append(flight_info)
            
            if special_tickets:
                msg = "🎉 发现海航PLUS 199特价票！\n\n" + "\n\n".join(special_tickets)
                send_wechat("海航特价票提醒", msg)
            else:
                print("ℹ️ 暂无199元特价票，继续监控...")
        else:
            print("ℹ️ 未查询到航班数据")
            
    except Exception as e:
        print(f"⚠️ 查询异常：{e}")
        # 异常时也推送一下
        send_wechat("海航监控异常", f"脚本运行出错：{e}")

if __name__ == "__main__":
    check_flight()
