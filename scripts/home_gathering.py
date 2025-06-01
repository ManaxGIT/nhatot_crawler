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

def crawl_nhatot(output_file='nhatot_data.csv', max_pages=10):
    with sync_playwright() as p:
        headless = False
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(user_agent=random_user_agent())
        page = context.new_page()

        if not safe_goto(page, 'https://www.nhatot.com/mua-ban-bat-dong-san'):
            return

        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Land Type", "Price", "Price per m2", "Area", "City"])

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
                    if not safe_goto(page, f'https://www.nhatot.com/mua-ban-bat-dong-san?page={current_page}'):
                        break
                    continue

                items = page.locator("li[itemprop='itemListElement']")
                count = items.count()
                print(f"→ Tổng cộng {count} tin trên trang {current_page}")

                for i in range(count):
                    try:
                        item = items.nth(i)

                        # Lấy loại đất
                        land_type_element = item.locator("span.tle2ik0").first
                        land_type = land_type_element.inner_text().strip() if land_type_element.count() > 0 else ""

                        # Lấy giá
                        price_element = item.locator("span.bfe6oav").nth(0)
                        price = price_element.inner_text().strip() if price_element.count() > 0 else ""

                        # Lấy giá/m2
                        price_per_m2_element = item.locator("span.bfe6oav").nth(1)
                        price_per_m2 = price_per_m2_element.inner_text().strip() if price_per_m2_element.count() > 0 else ""

                        # Lấy diện tích
                        area_element = item.locator("span.bfe6oav").nth(2)
                        area = area_element.inner_text().strip() if area_element.count() > 0 else ""

                        # Lấy tên thành phố
                        location_element = item.locator("span.c1u6gyxh").first
                        if location_element.count() > 0:
                            location_text = location_element.inner_text().strip()
                            city = location_text.split('•')[0].strip()
                        else:
                            city = ""

                        if land_type or price or area:
                            print(f"{i+1:02d}. {land_type} | {price} | {price_per_m2} | {area} | {city}")
                            writer.writerow([land_type, price, price_per_m2, area, city])
                        else:
                            print(f"[i] Bỏ qua tin {i+1}: thiếu dữ liệu quan trọng.")
                    except Exception as e:
                        print(f"[!] Bỏ qua tin {i+1}: {e}")
                        continue

                # Sang trang tiếp theo
                current_page += 1
                if current_page > max_pages:
                    break
                new_url = f"https://www.nhatot.com/mua-ban-bat-dong-san?page={current_page}"
                if not safe_goto(page, new_url):
                    print("[!] Không thể chuyển sang trang tiếp theo. Dừng crawl.")
                    break
                print(f"[+] Đã chuyển sang trang {current_page}.")
                time.sleep(random.uniform(3, 6))

        browser.close()

def random_user_agent():
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    ]
    return random.choice(ua_list)

if __name__ == "__main__":
    crawl_nhatot(output_file='nhatot_data_4.csv', max_pages=100)
