# 🧴 Sephora Skincare Product Scraper

This project is a **web scraping and preprocessing pipeline** for extracting structured skincare product data from [Sephora UK](https://www.sephora.co.uk/).

It uses **Selenium with undetected-chromedriver** to bypass anti-bot detection, scrapes product listings (including dynamically loaded items), and stores the raw HTML in a text file. Later, a **preprocessing step** converts the raw HTML into a clean, structured dataset in CSV format for downstream analytics.

---

## ✨ Features

- 🚀 Automated scraping of all skincare products from Sephora UK.
- ✅ Handles cookie consent pop-ups automatically.
- 🔄 Clicks “Load More” until all products are loaded.
- 📝 Saves raw product HTML blocks into `products_raw_html_2.txt`.
- 🧹 Preprocessing pipeline parses the HTML and extracts:
  - SKU
  - Name
  - Brand
  - Price
  - Discount (if any)
  - Rating
  - Review count
  - Image URL
  - Product URL
- 📊 Clean structured data exported as `sephora_products.csv`.
- 🛡️ Uses stealth settings to mimic human browsing (avoids detection).

---

## 📂 Project Structure

```bash
sephora-scraper/
│
├── scraper_v2.py # Main scraper (uses Selenium + undetected_chromedriver)
├── preprocess_data.py # Preprocessing script (parses raw HTML -> CSV)
│
├── products_raw_html_2.txt # Raw scraped product HTML (output of scraper.py)
├── sephora_products.csv # Clean processed dataset (output of preprocess_data.py)
│
├── requirements.txt # Python dependencies
└── README.md # Documentation
```

---

## ⚙️ Installation

### 1. Clone this repo

```bash
git clone https://github.com/<your-username>/sephora-scraper.git
cd sephora-scraper
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Core libraries used:

- `selenium` (browser automation)
- `undetected-chromedriver` (evades bot detection)
- `selenium-stealth` (spoofs browser fingerprinting)
- `beautifulsoup4` (HTML parsing)
- `pandas` (data handling & CSV export)

## 🕵️ Usage

### Step 1: Run the scraper

This script will:

- Launch a Chrome browser.
- Navigate to Sephora UK skincare category.
- Accept cookie consent.
- Keep scrolling and clicking "Load More" until all products are loaded.
- Save all raw product HTML to products_raw_html_2.txt

Run:

```bash
python scraper_v2.py
```

👉 Example console output:

```bash
Navigated to page.
Accepted cookies.
Initial products loaded.
Products before click: 40
Clicked 'Load More'...
Products after click: 80
...
No more 'Load More' button.
Total products found: 1260
```

At this stage, you’ll have products_raw_html_2.txt with product blocks separated by ---.

### Step 2: Preprocess the raw HTML

This script will:

- Load products_raw_html_2.txt.
- Extract key fields (name, brand, price, SKU, discount, rating, etc).
- Convert into a structured pandas DataFrame.
- Save as sephora_products.csv.

Run:

```bash
python preprocess_data.py
```

👉 Example console output:

```bash
Saved 1260 products to sephora_products.csv
```

## 📊 Output Data

The CSV file (`sephora_products.csv`) contains:

| sku    | name                           | brand            | price  | discount | rating | review_count | image_url                  | product_url                    |
| ------ | ------------------------------ | ---------------- | ------ | -------- | ------ | ------------ | -------------------------- | ------------------------------ |
| 188373 | Advanced Night Repair Serum    | Estée Lauder     | 75.00  | -20%     | 4.8    | 215          | https://.../prod188373.jpg | https://sephora.co.uk/product1 |
| 187484 | Ultra Facial Cream             | Kiehl's          | 32.00  |          | 4.7    | 512          | https://.../prod187484.jpg | https://sephora.co.uk/product2 |
| 172470 | The Rich Cream                 | Augustinus Bader | 230.00 |          | 4.9    | 128          | https://.../prod172470.jpg | https://sephora.co.uk/product3 |
| 187551 | Hydra Zen Anti-Stress Cream    | Lancôme          | 45.00  | -10%     | 4.6    | 340          | https://.../prod187551.jpg | https://sephora.co.uk/product4 |
| 160205 | Moisture Surge 100H Auto-Repl. | Clinique         | 40.00  |          | 4.8    | 890          | https://.../prod160205.jpg | https://sephora.co.uk/product5 |

> **Note:** `image_url` and `product_url` are truncated in this table for readability.

## 👨‍💻 Author

🐙 [Izundu Dan-Ekeh](https://github.com/Izu-33)
💼 [LinkedIn](https://www.linkedin.com/in/izundu-dan-ekeh/)
