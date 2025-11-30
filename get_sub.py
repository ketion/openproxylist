# get_sub.py
from playwright.sync_api import sync_playwright
import time
import os

def main():
    with sync_playwright() as p:
        print("正在启动 Chromium（无头模式）...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()
        
        print("正在打开 https://openproxylist.com/v2ray/")
        page.goto("https://openproxylist.com/v2ray/", timeout=60000)
        page.wait_for_load_state("networkidle")

        # 设置延迟 ≤50ms
        page.fill('input[placeholder="Response Time"]', "50")
        print("已设置延迟 ≤50ms")

        # 选择国家：Hong Kong, Japan, Singapore
        page.click("text=Select Country...")
        for country in ["Hong Kong", "Japan", "Singapore"]:
            page.check(f'input[type="checkbox"][value="{country}"]', timeout=10000)
            print(f"已勾选国家: {country}")

        # 勾选所有主流协议
        for protocol in ["VMess", "VLess", "Trojan VPN", "Shadowsocks"]:
            page.check(f'//label[contains(text(), "{protocol}")]/preceding-sibling::input', timeout=10000)
            print(f"已勾选协议: {protocol}")

        # 点击搜索
        page.click('button:has-text("Search")')
        print("正在搜索节点，请稍候...")
        page.wait_for_load_state("networkidle")
        time.sleep(8)  # 等待表格完全渲染（关键！）

        # 点击 V2Ray Subscription，捕获新窗口
        with page.expect_popup() as popup_info:
            page.click('text="V2Ray Subscription"')
        popup = popup_info.value

        # 获取 base64 订阅内容
        subscription_base64 = popup.locator("body").inner_text().strip()
        subscription_base64 = subscription_base64.replace("\n", "").replace("\r", "")

        # 保存到文件
        with open("subscription.txt", "w", encoding="utf-8") as f:
            f.write(subscription_base64)

        print("成功获取最新订阅！共 {} 字符".format(len(subscription_base64)))
        print("前100字符预览：")
        print(subscription_base64[:100] + "...")

        browser.close()

if __name__ == "__main__":
    main()
