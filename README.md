
# NhaTot.com Data Crawler Tool

A custom web scraping tool designed to extract data from [NhaTot.com](https://nhatot.com), a popular real estate website in Vietnam.<br>
This tool helps automate the process of collecting real estate data for research, analysis, or data enrichment purposes.

> ⚠️ **Disclaimer**: This tool is for educational and research purposes only. Make sure you comply with NhaTot.com's Terms of Service before using it.

---

## 📦 Features

- Scrape listing data (title, price, location, description, etc.)
- Logging and error handling
- Easy to extend and customize

---

## 🛠 Installation

1. Clone the repository:

```bash
    git clone https://github.com/yourusername/nhatot-crawler.git
    cd nhatot-crawler
```

2. Create and activate a virtual environment (optional but recommended):

```bash
    python -m venv .venv
    source venv/bin/activate  # on Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
    pip install -r requirements.txt
```

---

## 📁 Folder Structure

```
nhatot-crawler/
│
├── crawler/               # Main crawler logic
│   ├── __init__.py
│   ├── fetcher.py         # Handles HTTP requests and responses
│   ├── parser.py          # Extracts data from HTML pages
│   └── config.py          # Configuration for URLs, headers, delays
│
├── data/                  # Scraped data output (CSV, JSON, etc.)
│
├── logs/                  # Log files for monitoring and debugging
│
├── utils/                 # Utility functions (e.g., formatters, validators)
│
├── main.py                # Entry point for running the crawler
├── requirements.txt       # Python package dependencies
└── README.md              # Project documentation
```

---

## 🚀 Usage

Run the crawler with default settings:

    python main.py

Optional arguments (if applicable):

    python main.py --category=real-estate --max-pages=10 --output=data/real_estate.csv

You can adjust headers, delays, and selectors in the config.py file if the structure of NhaTot.com changes.

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
- Email: yourname@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for more information.
