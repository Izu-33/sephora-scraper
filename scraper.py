import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time

# Optional proxy (replace with a working one or set to None)
proxy = None

# Configure Chrome options
options = uc.ChromeOptions()
options.headless = False  # Headless often gets blocked
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")

# Use a realistic User-Agent
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
)

if proxy:
    options.add_argument(f"--proxy-server={proxy}")

# Start the driver
driver = uc.Chrome(options=options)

# Apply selenium-stealth
stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

try:
    driver.get("https://www.sephora.co.uk/skin")
    print("Navigated to page.")

    # Wait for body to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Accept cookies if present
    try:
        consent_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Accept all cookies")]'))
        )
        consent_button.click()
        print("Accepted cookies.")
        time.sleep(2)
    except:
        print("No GDPR popup found or already accepted.")

    # Wait for products to appear
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Product[data-sku]'))
    )
    print("Initial products loaded.")

    # Keep loading more
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        try:
            load_more = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Load more")]'))
            )
            load_more.click()
            print("Clicked 'Load More'...")
            time.sleep(5)
        except:
            print("No more 'Load More' button.")
            break

    # Grab page source
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    products = soup.select('div.Product[data-sku]')
    print(f"Found {len(products)} products.")

    # Save raw HTML
    with open("products_raw_html.txt", "w", encoding="utf-8") as f:
        for product in products:
            f.write(str(product))
            f.write("\n---\n")

    # Print first few SKUs
    for product in products[:5]:
        sku = product["data-sku"]
        print("SKU:", sku)

finally:
    driver.quit()
