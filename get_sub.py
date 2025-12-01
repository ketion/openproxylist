# get_sub.py —— 终极稳定版（只筛选延迟 ≤ 50ms，全局最优）
from playwright.sync_api import sync_playwright
import time
import re

def main():
    with sync_playwright() as p:
        print("正在启动无头 Chromium...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 打开页面
        page.goto("https://openproxylist.com/v2ray/")
        page.wait_for_load_state('domcontentloaded', timeout=60000)  # 增加到 60s，并用更宽松状态
        print("页面加载完成")

        # 精准定位你提供的真实输入框：name="response"
        page.wait_for_selector('input[name="response"]', timeout=60000)
        page.fill('input[name="response"]', "50")
        print("已设置最大延迟 ≤ 50ms")

        # 点击搜索
        page.click('button:has-text("Search")')
        print("正在搜索节点，请等待 12 秒确保表格完全加载...")
        page.wait_for_load_state('domcontentloaded', timeout=120000)  # 增加到 60s，并用更宽松状态
        time.sleep(12)  # 必须等够！这是最关键的一步

        # 点击 V2Ray Subscription（弹出新窗口）
        with page.expect_popup() as popup_info:
            page.click('text="V2Ray Subscription"')
        popup = popup_info.value

        # 正确提取弹窗内容（修复点！）
        sub_base64 = popup.locator("body").text_content().strip()
        sub_base64 = re.sub(r'\s+', '', sub_base64)  # 去掉所有空格换行

        # 保存到文件
        with open("subscription.txt", "w", encoding="utf-8") as f:
            f.write(sub_base64)

        # 统计节点数量（粗略）
        import base64
        try:
            decoded = base64.b64decode(sub_base64).decode('utf-8', errors='ignore')
            node_count = len(re.findall(r'(vmess|vless|trojan|ss)://', decoded))
        except:
            node_count = "无法统计"

        print(f"成功获取订阅！共约 {node_count} 个节点（延迟 ≤ 50ms）")
        print(f"订阅字符串长度：{len(sub_base64)} 字符")
        print(f"前 100 字符预览：{sub_base64[:100]}...")

        browser.close()

if __name__ == "__main__":
    main()
