import time
import random
import csv
from playwright.sync_api import sync_playwright

def safe_goto(page, url, retries=3, timeout=60000):
    for attempt in range(retries):
        try:
            print(f"[+] Đang mở {url} (thử lần {attempt + 1})...")
            page.goto(url, timeout=timeout, wait_until="domcontentloaded")
            return True
        except Exception as e:
            print(f"[!] Lỗi khi mở {url}: {e}")
            time.sleep(2)
    print(f"[!] Thất bại khi mở {url} sau {retries} lần.")
    return False

def random_user_agent():
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    ]
    return random.choice(ua_list)

def crawl_nhatot_links(output_file='', max_pages=10):
    with sync_playwright() as p:
        headless = False
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(user_agent=random_user_agent())
        page = context.new_page()

        if not safe_goto(page, 'https://www.nhatot.com/mua-ban-nha-dat'):
            return

        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            current_page = 1
            while current_page <= max_pages:
                print(f"\n==== Đang xử lý trang {current_page} ====")

                try:
                    page.wait_for_selector("li[itemprop='itemListElement']", timeout=10000)
                except Exception:
                    print("[!] Timeout đợi tin đăng.")
                    headless = not headless
                    print(f"[+] Đổi headless thành {headless}")
                    browser.close()
                    browser = p.chromium.launch(headless=headless)
                    context = browser.new_context(user_agent=random_user_agent())
                    page = context.new_page()
                    if not safe_goto(page, f'https://www.nhatot.com/mua-ban-nha-dat?page={current_page}'):
                        break
                    continue

                items = page.locator("li[itemprop='itemListElement']")
                count = items.count()
                print(f"→ Tổng cộng {count} tin trên trang {current_page}")

                for i in range(count):
                    try:
                        item = items.nth(i)
                        link_element = item.locator("a").first
                        link = link_element.get_attribute("href") if link_element.count() > 0 else ""

                        if not link:
                            print(f"[i] Bỏ qua tin {i+1}: không tìm thấy link.")
                            continue

                        full_link = f"https://www.nhatot.com{link}" if link.startswith("/") else link

                        if full_link.strip() == "https://www.nhatot.com":
                            print(f"[i] Bỏ qua tin {i+1}: Link là trang chủ.")
                            continue

                        print(f"{i+1:02d}. {full_link}")
                        writer.writerow([full_link])
                    except Exception as e:
                        print(f"[!] Bỏ qua tin {i+1}: {e}")
                        continue

                current_page += 1
                if current_page > max_pages:
                    break
                new_url = f"https://www.nhatot.com/mua-ban-nha-dat?page={current_page}"
                if not safe_goto(page, new_url):
                    print("[!] Không thể chuyển sang trang tiếp theo. Dừng crawl.")
                    break
                print(f"[+] Đã chuyển sang trang {current_page}.")
                time.sleep(random.uniform(3, 6))

        browser.close()

if __name__ == "__main__":
    crawl_nhatot_links(output_file='', max_pages=5)
