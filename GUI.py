import sys
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import re
import threading

BASE_SCRIPT_DIR1 = os.path.join(os.getcwd(), "thread")
BASE_SCRIPT_DIR2 = os.path.join(os.getcwd(), "scripts")

SCRIPT_MAP = {
    "Nhà ở": os.path.join(BASE_SCRIPT_DIR1, "thread_nha.py"),
    "Căn hộ": os.path.join(BASE_SCRIPT_DIR1, "thread_can-ho.py"),
    "Đất": os.path.join(BASE_SCRIPT_DIR1, "thread_dat.py")
}

CRAWLER_SCRIPT = os.path.join(BASE_SCRIPT_DIR2, "link_gathering.py")

def run_script(selected_type, link_file_name, output_file_name, crawl_url, max_pages, mode, progress, btn):
    def task():
        folder = os.getcwd()

        link_folder = os.path.join(os.getcwd(), "link_output")
        output_folder = os.path.join(os.getcwd(), "scraped_data")

        link_file = os.path.join(link_folder, link_file_name)
        output_file = os.path.join(output_folder, output_file_name)

        if mode == "crawl_and_scrape":
            with open(CRAWLER_SCRIPT, 'r', encoding='utf-8') as f:
                crawler_content = f.read()

            crawler_content = re.sub(
                r"(output_file\s*=\s*)['\"].*?['\"]",
                lambda m: m.group(1) + repr(link_file),
                crawler_content
            )

            crawler_content = re.sub(r"max_pages\s*=\s*\d+", f"max_pages={max_pages}", crawler_content)
            crawler_content = re.sub(r"https://www\.nhatot\.com/mua-ban-nha-dat", crawl_url, crawler_content)

            crawler_script_name = os.path.basename(CRAWLER_SCRIPT)
            temp_crawler = os.path.join(folder, f"temp_{crawler_script_name}")

            with open(temp_crawler, 'w', encoding='utf-8') as f:
                f.write(crawler_content)

            try:
                print(f"▶️ Đang chạy crawler từ {crawl_url} với {max_pages} trang...")
                subprocess.run([sys.executable, temp_crawler], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Lỗi", f"Crawler lỗi:\n{e}")
                progress.stop()
                btn.config(state=tk.NORMAL)
                return
            finally:
                if os.path.exists(temp_crawler):
                    os.remove(temp_crawler)

        # Gọi script scrape
        script_file = SCRIPT_MAP[selected_type]
        with open(script_file, 'r', encoding='utf-8') as f:
            script_content = f.read()

        script_content = re.sub(
            r"input_file\s*=\s*r?['\"].*?['\"]",
            f"input_file = r{repr(link_file)}", script_content
        )

        script_content = re.sub(
            r"output_file\s*=\s*r?['\"].*?['\"]",
            f"output_file = r{repr(output_file)}", script_content
        )

        script_name = os.path.basename(script_file)
        temp_script = os.path.join(folder, f"temp_{script_name}")

        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(script_content)

        try:
            print(f"▶️ Đang scrape dữ liệu từ {link_file} ...")
            subprocess.run([sys.executable, temp_script], check=True)
            messagebox.showinfo("Thành công", f"🎉 Dữ liệu đã được lưu tại:\n{output_file_name}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Lỗi", f"Script scrape lỗi:\n{e}")
        finally:
            if os.path.exists(temp_script):
                os.remove(temp_script)
            progress.stop()
            progress.pack_forget()
            btn.config(state=tk.NORMAL)

    threading.Thread(target=task).start()

# GUI
root = tk.Tk()

root.title("Tool Crawl Dữ Liệu NhaTot.com")
root.geometry("700x550")  # giảm chiều cao vì bỏ console
root.configure(bg="#f9f9f9")

style = ttk.Style()
style.theme_use("clam")
style.configure('TLabel', font=('Segoe UI', 10))
style.configure('TButton', font=('Segoe UI', 10, 'bold'))
style.configure('TEntry', font=('Segoe UI', 10))
style.configure('TMenubutton', font=('Segoe UI', 10))

tk.Label(root, text="🏠 Crawl Dữ Liệu từ NhaTot.com", font=("Segoe UI", 16, "bold"), bg="#f9f9f9", fg="#333").pack(pady=15)

form_frame = ttk.Frame(root)
form_frame.pack(pady=10)

def add_form_row(label_text, widget, row, ref_dict):
    lbl = ttk.Label(form_frame, text=label_text)
    lbl.grid(row=row, column=0, sticky="w", padx=5, pady=8)
    widget.grid(row=row, column=1, padx=5, pady=8)
    ref_dict[label_text] = (lbl, widget)

entry_url = ttk.Entry(form_frame, width=50)
entry_pages = ttk.Entry(form_frame, width=20)
entry_pages.insert(0, "5")
entry_linkfile = ttk.Entry(form_frame, width=40)
entry_outputfile = ttk.Entry(form_frame, width=40)
selected_type = tk.StringVar(value="Nhà ở")
option_menu = ttk.OptionMenu(form_frame, selected_type, "Nhà ở", *SCRIPT_MAP.keys())

mode = tk.StringVar(value="crawl_and_scrape")
tk.Label(root, text="🔧 Chọn chế độ:").pack()
radio1 = ttk.Radiobutton(root, text="🕷️ Crawl link + scrape", variable=mode, value="crawl_and_scrape")
radio2 = ttk.Radiobutton(root, text="🔗 Chỉ scrape từ link đã có", variable=mode, value="scrape_only")
radio1.pack()
radio2.pack()

field_refs = {}
add_form_row("🔗 Link danh mục tin:", entry_url, 0, field_refs)
add_form_row("📄 Số trang cần crawl:", entry_pages, 1, field_refs)
add_form_row("📁 Tên file CSV của link:", entry_linkfile, 2, field_refs)
add_form_row("📁 Tên file sau khi scrape:", entry_outputfile, 3, field_refs)
add_form_row("🏷️ Loại dữ liệu:", option_menu, 4, field_refs)

progress = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", length=400)
progress.pack_forget()

def update_visibility(*args):
    state = mode.get()
    url_row = field_refs["🔗 Link danh mục tin:"]
    page_row = field_refs["📄 Số trang cần crawl:"]

    if state == "scrape_only":
        url_row[0].grid_remove()
        url_row[1].grid_remove()
        page_row[0].grid_remove()
        page_row[1].grid_remove()
    else:
        url_row[0].grid()
        url_row[1].grid()
        page_row[0].grid()
        page_row[1].grid()

mode.trace_add("write", update_visibility)
update_visibility()

def start():
    if not entry_linkfile.get() or not entry_outputfile.get():
        messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ tên file.")
        return
    if mode.get() == "crawl_and_scrape":
        if not entry_url.get() or not entry_pages.get():
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập link và số trang.")
            return
        try:
            int(entry_pages.get())
        except:
            messagebox.showerror("Lỗi", "Số trang phải là số nguyên.")
            return

    btn_start.config(state=tk.DISABLED)
    progress.pack(pady=10)
    progress.start(10)

    start_thread = threading.Thread(target=run_script, args=(
        selected_type.get(),
        entry_linkfile.get(),
        entry_outputfile.get(),
        entry_url.get(),
        int(entry_pages.get() or 1),
        mode.get(),
        progress,
        btn_start
    ))
    start_thread.start()

btn_start = ttk.Button(root, text="🚀 Bắt đầu", width=30, command=start)
btn_start.pack(pady=25)

tk.Label(root, text="© 2025 - Tool by Hyy ❤️", font=("Segoe UI", 9), bg="#f9f9f9", fg="#888").pack(side="bottom", pady=10)

root.mainloop()
