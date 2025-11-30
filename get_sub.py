from playwright.sync_api import sync_playwright
import time
import re

def main():
    with sync_playwright() as p:
        print("启动无头浏览器...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 打开页面
        page.goto("https://openproxylist.com/v2ray/")
        page.wait_for_load_state("networkidle")
        print("页面加载完成")

        # 【关键】精准定位你提供的真实输入框
        page.wait_for_selector('input[name="response"]', timeout=60000)
        page.fill('input[name="response"]', "50")   # 改成 50
        print("已设置最大延迟 ≤ 50ms")

        # 点击 Search 按钮
        page.click('button:has-text("Search")')
        print("正在搜索，请稍等 10 秒让表格加载完...")
        page.wait_for_load_state("networkidle")
        time.sleep(10)   # 必须等够，表格是动态渲染的

        # 点击右上角 V2Ray Subscription（弹出新窗口）
        with page.expect_popup() as popup_info:
            page.click('text="V2Ray Subscription"')
        popup = popup_info.value

        # 提取 base64 订阅内容
        sub_base64 = popup.text_content().strip()
        sub_base64 = re.sub(r'\s+', '', sub_base64)  # 去除所有空白

        # 保存
        with open("subscription.txt", "w", encoding="utf-8") as f:
            f.write(sub_base64)

        # 粗略统计节点数量
        import base64
        try:
            decoded = base64.b64decode(sub_base64).decode('utf-8', errors='ignore')
            node_count = len(re.findall(r'(vmess|vless|trojan|ss)://', decoded))
        except:
            node_count = "未知"

        print(f"成功！共获取约 {node_count} 个节点（延迟 ≤ 50ms）")
        print(f"订阅长度：{len(sub_base64)} 字符")
        print(f"前100字符预览：{sub_base64[:100]}...")

        browser.close()

if __name__ == "__main__":
    main()
