
# Nhatot.com Data Crawler Tool

A custom web scraping tool designed to extract data from [Nhatot.com](https://nhatot.com), a popular real estate website in Vietnam.<br>
This tool helps automate the process of collecting real estate data for research, analysis, or data enrichment purposes.

> ⚠️ **Disclaimer**: This tool is for educational and research purposes only. Make sure you comply with NhaTot.com's Terms of Service before using it.

---

## 📦 Features

- Scrape listing data (title, price, location, description, etc.)
- Easy to extend and customize

---

## 🛠 Installation

<b>1. Clone the repository:</b>

```bash
    git clone https://github.com/ManaxGIT/nhatot_crawler
    cd nhatot_crawler
```

<b>2. Create and activate a virtual environment:</b>
*(optional but strongly recommended)*

* create virtual environment
```bash
    python -m venv .venv
```
* run virtual environment
    * MacOS/Linux user
        ```bash
        source .venv/bin/activate
        ```
    * Window user
        ```bash
        venv\Scripts\activate.bat
        ```

<b>3. Install dependencies:</b>

```bash
    pip install -r requirements.txt
```

---

## 📁 Folder Structure

```
nhatot-crawler/
│
├── scripts/               # Include all crawl script files
│   ├── home_gathering.py  # Use to crawl informations on home page
│   ├── link_gathering.py  # Use to crawl links on home page
│   ├── output_can_ho.py   # Crawl Can Ho informations
│   ├── output_dat.py      # Crawl Dat informations 
│   └── output_nha_o.py    # Crawl Nha O informations
│
├── link_output/           # link-output location
│
├── scraped_data/          # real estate data output location
│
├── thread/                # Contain logic to increase productivity
│
├── GUI.py                 # GUI of the tool
├── requirements.txt       # Python package dependencies
├── INSTRUCTION.docx       # Tool logic explaination
└── README.md              # Project guide
```

---

## 🚀 Use manual

* run the GUI
```bash
    python3 GUI.py
```

* <b>If you don't have the link file (which you usually are)</b>
  - Access [Nhatot.com](https://nhatot.com). From *Danh mục*, select either *căn hộ/chung cư*, *nhà ở*, *đẩt*. Copy the link
  - Input the link into *Link danh mục tin*.
  - Choose number of pages you want to get data from in *Số trang cần crawl*.
  - Input the name of the output link file into *Tên file CSV của link*. This could be reuse later.
  - Input the name of the file which data are saved into *Tên file sau khi scrape*.
  - Select *Loại dữ liệu* same as the website link you copied before.
  - Click *Bắt đầu* button

* <b>If you already have the link file</b>
  - Change mode to *Chỉ scrape từ link đã có*.
  - Input link file location into *Tên file CSV của link*
  - Input the name of the file which data are saved into *Tên file sau khi scrape*.
  - Select *Loại dữ liệu* same as the inputted link file.
  - Click *Bắt đầu* button

---

## ⚖️ Legal & Ethical Considerations

This tool is intended **only for educational, academic, or personal research use**. Web scraping may violate a website’s terms of service. It is your responsibility to ensure that your use of this tool does not breach:

- NhaTot.com’s [Terms of Use](https://nhatot.com/terms)
- Vietnamese or international data privacy laws
- The rights of any third party

Avoid aggressive crawling to reduce the risk of IP bans and server overload.

---

## 📧 Contact

For questions or collaboration:
- Email: mancv.22it@vku.udn.vn | huycq.22it@vku.udn.vn
- GitHub: [Manax](https://github.com/ManaxGIT/) | [Hy](https://github.com/huycq2004)

