from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import time
from playwright.sync_api import sync_playwright

input_file = r""
output_file = r""

def scrape_single_page(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                headless=False
            )
            page = browser.new_page()

            page.goto(url, timeout=60000)

            try:
                w = page.evaluate("() => window.innerWidth")
                h = page.evaluate("() => window.innerHeight")
                page.mouse.click(w/2, h/2)
                time.sleep(1)
            except:
                pass

            try:
                xem_them = page.query_selector('button:has-text("Xem thêm")')
                if xem_them:
                    page.evaluate("(el) => el.scrollIntoView()", xem_them)
                    xem_them.click(timeout=10000)
                    time.sleep(2)
            except:
                pass

            def text_of(sel):
                el = page.query_selector(sel)
                return el.inner_text().strip() if el else 'N/A'

            data = {
                "Title":           text_of('h1'),
                "Type":            text_of('.a3jfi3v[itemprop="land_type"]'),
                "Price":           text_of('.pyhk1dv'),
                "Price/m2":        text_of('.a3jfi3v[itemprop="price_m2"]'),
                "Size":            text_of('.a3jfi3v[itemprop="size"]'),
                "Direction":       text_of('.a3jfi3v[itemprop="direction"]'),
                "Legal Documents": text_of('.a3jfi3v[itemprop="property_legal_document"]'),
                "Characteristics": text_of('.a3jfi3v[itemprop="pty_characteristics"]'),
                "Width":           text_of('.a3jfi3v[itemprop="width"]'),
                "length":          text_of('.a3jfi3v[itemprop="length"]'),
                "Address":         text_of('.bwq0cbs.flex-1'),
            }

            print(f"\n=== Data for {url} ===")
            for k, v in data.items():
                print(f"{k}: {v}")
            print("=" * 40)

            browser.close()

            if all(v != 'N/A' for v in data.values()):
                return data
            else:
                print(f"⚠️ Missing data at {url}")
                return None
    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None

def main():
    with open(input_file, newline='', encoding='utf-8') as infile:
        urls = [row[0] for row in csv.reader(infile)]

    fieldnames = [
        "Title",
        "Type",
        "Price",
        "Price/m2",
        "Size",
        "Direction",
        "Legal Documents",
        "Characteristics",
        "Width",
        "length",
        "Address"
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(scrape_single_page, url): url for url in urls}

            for future in as_completed(futures):
                result = future.result()
                if result:
                    writer.writerow(result)

    print(f"\n🎉 All done — data saved to: {output_file}")

if __name__ == "__main__":
    main()
