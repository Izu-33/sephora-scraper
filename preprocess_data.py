from bs4 import BeautifulSoup
import pandas as pd
import json

# Load HTML from saved file
with open("products_raw_html_2.txt", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Find all product containers
product_divs = soup.find_all("div", class_="Product")

# Prepare list to hold structured data
products = []

for product in product_divs:
    # SKU
    sku = product.get("data-sku", "")

    # Discount
    discount = ""
    discount_tag = product.select_one("b.Product-discount")
    if discount_tag:
        discount = discount_tag.get_text(strip=True)

    # Product info from data-feelunique-datalayer-push
    link = product.select_one("a.Product-link")
    name = brand = price = product_url = image_url = ""
    if link and link.has_attr("data-feelunique-datalayer-push"):
        try:
            data = json.loads(link["data-feelunique-datalayer-push"])
            prod_info = data.get("click", {}).get("ecommerce", {}).get("click", {}).get("products", [{}])[0]
            name = prod_info.get("name", "")
            brand = prod_info.get("brand", "")
            price = prod_info.get("price", "")
        except json.JSONDecodeError:
            pass

    # Product URL
    if link and link.has_attr("href"):
        product_url = "https://www.sephora.co.uk" + link["href"]

    # Image URL
    img_tag = product.select_one("img.Product-image")
    if img_tag:
        image_url = "https:" + img_tag.get("src", "")

    # Rating
    rating = ""
    rating_tag = product.select_one("span.Rating-average")
    if rating_tag:
        rating = rating_tag.get("data-aggregate-rating", "")

    # Review Count
    review_count = ""
    review_tag = product.select_one("span.Rating-count")
    if review_tag:
        review_count = review_tag.get("data-review-count", "")

    # Append structured info as a dict
    products.append({
        "sku": sku,
        "name": name,
        "brand": brand,
        "price": price,
        "discount": discount,
        "rating": rating,
        "review_count": review_count,
        "image_url": image_url,
        "product_url": product_url,
    })

# Convert to DataFrame
df = pd.DataFrame(products)

# Save to CSV
df.to_csv("sephora_products.csv", index=False, encoding="utf-8-sig")
print(f"Saved {len(df)} products to sephora_products.csv")
