import csv
import time
from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Input and Output file paths
input_file = r""
output_file = r""

def scrape_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            headless=False
        )
        page = browser.new_page()

        # Navigate with longer timeout
        try:
            page.goto(url, timeout=60000)
        except Exception as e:
            print(f"[!] Error loading {url}: {e}")
            browser.close()
            return None

        # Dismiss any pop-up by clicking center
        try:
            w = page.evaluate("() => window.innerWidth")
            h = page.evaluate("() => window.innerHeight")
            page.mouse.click(w/2, h/2)
            time.sleep(1)
        except:
            pass

        # Click "Xem thêm"
        try:
            xem_them = page.query_selector('button:has-text("Xem thêm")')
            if xem_them:
                page.evaluate("(el) => el.scrollIntoView()", xem_them)
                xem_them.click(timeout=10000)
                time.sleep(2)
        except:
            pass

        # Helper to extract text or 'N/A'
        def text_of(sel):
            el = page.query_selector(sel)
            return el.inner_text().strip() if el else 'N/A'

        # Scrape fields
        data = {
            "Title":           text_of('h1'),
            "Type":            text_of('.a3jfi3v[itemprop="house_type"]'),
            "Price":           text_of('.pyhk1dv'),
            "Price/m2":        text_of('.brnpcl3'),
            "Area":            text_of('.a3jfi3v[itemprop="size"]'),
            "Living Area":     text_of('.a3jfi3v[itemprop="living_size"]'),
            "Legal Documents": text_of('.a3jfi3v[itemprop="property_legal_document"]'),
            "Rooms":           text_of('.a3jfi3v[itemprop="rooms"]'),
            "Toilets":         text_of('.a3jfi3v[itemprop="toilets"]'),
            "Address":         text_of('.bwq0cbs.flex-1'),
        }

        # Print out everything for debugging
        print(f"\n=== Data for {url} ===")
        for k, v in data.items():
            print(f"{k}: {v}")
        print("=" * 40)

        browser.close()
        return data

# Main
with open(input_file, newline='', encoding='utf-8') as infile:
    urls = [row[0] for row in csv.reader(infile)]

# Match fieldnames exactly to the keys above:
fieldnames = [
    "Title",
    "Type",
    "Price",
    "Price/m2",
    "Area",
    "Living Area",
    "Legal Documents",
    "Rooms",
    "Toilets",
    "Address"
]

with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for url in urls:
        print(f"\nProcessing {url}")
        record = scrape_data(url)
        if not record:
            print(f"  Skipped {url} due to load error.")
            continue

        # Skip writing if any field is N/A
        if any(v == 'N/A' for v in record.values()):
            print(f"  Skipped {url} due to missing data.")
            continue

        writer.writerow(record)

print(f"\n🎉 All done — data saved to: {output_file}")
