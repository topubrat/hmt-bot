import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 🔐 ENV VARIABLES (Railway)
BOT_TOKEN = "8639793392:AAGnSFDqp5DDyAXz7zU7QTBXZUqjFBWXPY0"
CHAT_ID = "435115317"

# 🔥 WATCH LIST
WATCHES = {
    "HMT Tareeq Quartz | Blue Sunburst | HMT.Store": "https://www.hmtwatches.store/product/6a41455b-5f12-4ee9-bec2-185c45f1d569",
    "HMT Tareeq Quartz | Turquoise blue | HMT.Store": "https://www.hmtwatches.store/product/7281c42e-604a-4bd9-b011-066aa202eddd",
    "HMT Kohinoor Quartz B1 | Maroon | HMT.store": "https://www.hmtwatches.store/product/0035cf80-48d5-4cf3-a02f-1f36b01071a5",
    "HMT Tareeq Quartz | Sunray Blue | HMT.in": "https://www.hmtwatches.in/product_overview?id=eyJpdiI6IlBlNGlVc1NjdkpiZnNQakhib3d6d2c9PSIsInZhbHVlIjoic3lDL1c5UjNvYTkvVUNJOXJIdUNMQT09IiwibWFjIjoiMTcxY2E4MTEzZjM0OWJhZGZhMWQ5NGE3NDgyYWQ3Y2Q4YjQ4ZDQwMTAwMzU4NGNlODg0ZDY1NDZmYzkyOWRiNCIsInRhZyI6IiJ9",
    "HMT Kohinoor Quartz B1 | Maroon | HMT.in": "https://www.hmtwatches.in/product_overview?id=eyJpdiI6Ik83MUNXaXNBS2ZBUkhEc2s5SkxJUnc9PSIsInZhbHVlIjoibGQ0QkExZGphVGdzYkY0UnBodHVPUT09IiwibWFjIjoiMTA5MWZlYTBjNTE3ZTI2ZDI4YzdlNzA1ODNhN2M3MGY1YTk4ZDc5NjI5NGFkNzllZjI1MTIwM2U2OTE0YWRhNSIsInRhZyI6IiJ9",
    "HMT Inox Quartz IXLL 62 | Blue | HMT.in": "https://www.hmtwatches.in/product_overview?id=eyJpdiI6InB2R2dTKr6EeffXNDX9kzYZyr5KsyfSB1v9GuZYxHVlIjoiaCtoTTNRbGV5ck05ZHI1TTNFRmU5dz09IiwibWFjIjoiODIwZGUxZDQyYjY1YzIzMGY0ZDRmMzE4OGQ4YjAxODZkNDdjMjlkOTk3ZGI2OTg0ZGYwMjA5ZDBmYzY2ZmI2YyIsInRhZyI6IiJ9",
    "HMT Inox Quartz IXLL 62 | White | HMT.in": "https://www.hmtwatches.in/product_overview?id=eyJpdiI6ImNRRFo5RjZvOXVKSmMxTG1mNCtIQ3c9PSIsInZhbHVlIjoiMkJ2VitNYngrWEdCNzRHQkU5aERMZz09IiwibWFjIjoiMDhiM2IzNGI1ZGU4NWM3Y2Q5NmNhNWEyOTVjZDg2NzMyZTZlOTk4Yjk2YTc2MzI4OTk4MGM5NzJiZDQ1NWZhMSIsInRhZyI6IiJ9",
    "(test) HMT Plus JGSL 02 | Grey | HMT.in": "https://www.hmtwatches.in/product_overview?id=eyJpdiI6IlArWnhrMTZuZ2psTkdHS3FWSHBHemc9PSIsInZhbHVlIjoiSEJ0cVJWQTVxRXEraVlRanN3dXV1Zz09IiwibWFjIjoiNTdiODhmNTI2NDhlN2FkMTQyYmYxMmFjOGZjOTVlOTM3OWU1YjYxNzRmMzJlYzFjY2YxYWJiNWM3NjA1MTgwZiIsInRhZyI6IiJ9",
}

alerted = set()

# 🔔 TELEGRAM ALERT
def send_alert(name, url, price=None):
    try:
        message = f"🔥 {name} IN STOCK!\n\n💰 {price}\n🔗 {url}"

        requests.post(
            f"https://api.telegram.org/bot{8639793392:AAGnSFDqp5DDyAXz7zU7QTBXZUqjFBWXPY0}/sendMessage",
            data={"chat_id": "435115317", "text": message},
            timeout=10
        )
    except Exception as e:
        print("Telegram error:", e)

# 💰 GET PRICE
def get_price():
    try:
        elements = driver.find_elements(By.XPATH, "//*[contains(text(),'₹')]")

        for el in elements:
            text = el.text.strip()

            if "₹" in text and any(c.isdigit() for c in text) and len(text) < 15:
                return text

        return "Price not found"
    except:
        return "Price not found"

# 🌐 BROWSER SETUP (RAILWAY SAFE)
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

from selenium.webdriver.chrome.service import Service

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)


print("🚀 RAILWAY BOT RUNNING...\n")

# 🔁 MAIN LOOP
while True:
    try:
        for name, url in WATCHES.items():

            if name in alerted:
                continue

            print(f"🔄 Checking: {name}")

            try:
                driver.set_page_load_timeout(20)
                driver.get(url)
            except:
                print(f"⚠️ Timeout loading {name}")
                continue

            time.sleep(10)

            in_stock = False

            try:
                elements = driver.find_elements(By.XPATH, "//button | //a")

                for el in elements:
                    text = el.text.strip().lower()

                    if "notify me" in text:
                        continue

                    if any(x in text for x in ["add to cart", "add to bag", "buy now"]):
                        if el.is_displayed() and el.is_enabled():
                            in_stock = True
                            break

            except Exception as e:
                print("Detection error:", e)

            # extra safety
            page = driver.page_source.lower()
            if "notify me" in page and not in_stock:
                in_stock = False

            if in_stock:
                print(f"✅ {name} IN STOCK!")

                price = get_price()
                send_alert(name, url, price)

                alerted.add(name)

            else:
                print(f"❌ {name} not available")

            driver.delete_all_cookies()

        print("\n🔁 Restarting cycle...\n")

    except Exception as e:
        print("❌ Loop Error:", e)

    time.sleep(15)
