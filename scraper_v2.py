import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time
import random

options = uc.ChromeOptions()
options.headless = False
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
)

driver = uc.Chrome(options=options)

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

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Accept cookies
    try:
        consent_button = WebDriverWait(driver, 20).until(
            # EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Accept all cookies")]'))
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        consent_button.click()
        print("Accepted cookies.")
        time.sleep(2)
    except:
        print("No GDPR popup found or already accepted.")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Product[data-sku]'))
    )
    print("Initial products loaded.")

    # Load all products
    total_loaded = 0
    while True:
        # Count before clicking
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        products_before = len(soup.select('div.Product[data-sku]'))
        print(f"Products before click: {products_before}")

        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(3, 6))

        try:
            load_more = WebDriverWait(driver, 15).until(
                # EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Load more")]'))
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.loadMoreButton"))
            )
            load_more.click()
            print("Clicked 'Load More'...")
        except:
            print("No more 'Load More' button.")
            break

        # Wait longer for many products to load
        time.sleep(random.uniform(5, 10))

        # Count after clicking
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        products_after = len(soup.select('div.Product[data-sku]'))
        print(f"Products after click: {products_after}")

        # Check if new products appeared
        if products_after <= products_before:
            print("No new products loaded. Exiting loop.")
            break

        # Extra scroll in case more lazy load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(3, 5))

    # Final scrape
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    products = soup.select('div.Product[data-sku]')
    print(f"Total products found: {len(products)}")

    with open("products_raw_html_2.txt", "w", encoding="utf-8") as f:
        for product in products:
            f.write(str(product))
            f.write("\n---\n")

    # Example SKUs
    for product in products[:5]:
        sku = product["data-sku"]
        print("SKU:", sku)

finally:
    driver.quit()
