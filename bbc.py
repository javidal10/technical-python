import os
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the URLs for the sections of interest
sections = {
    "business": "https://www.bbc.com/news/business",
    "technology": "https://www.bbc.com/news/technology",
}

# Define the CSS selectors for relevant article content
selectors = {
    "business": ".gs-c-promo-body",
    "technology": ".gs-c-promo-body",
}

# Set Chrome options and configure the WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
driver_path = os.getenv("CHROMEDRIVER_PATH")  # add path to .env file
service = Service(driver_path)

# Create a folder to store the downloaded articles
output_folder = "bbc_articles"
os.makedirs(output_folder, exist_ok=True)

# Load the list of already downloaded articles
downloaded_articles = set()
if os.path.exists("downloaded_articles.txt"):
    with open("downloaded_articles.txt", "r") as file:
        downloaded_articles = set(file.read().splitlines())

# Iterate over the sections
for section, url in sections.items():
    # Start the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    sleep(5)  # Wait for the page to load (adjust the sleep time if needed)

    # Find all the articles
    articles = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selectors[section]))
    )

    # Process each article
    for article in articles:
        # Extract the title and body
        title = article.find_element(By.CSS_SELECTOR, "h3").text.strip()
        body = article.find_element(By.CSS_SELECTOR, "p").text.strip()

        # Generate a unique filename based on the article title
        filename = os.path.join(output_folder, f"{title[:50]}.json")

        # Check if the article has already been downloaded
        if filename in downloaded_articles:
            continue

        # Create a dictionary with the article content
        article_data = {"title": title, "body": body}

        # Save the article as a JSON file
        with open(filename, "w") as file:
            json.dump(article_data, file, indent=4)

        # Add the filename to the set of downloaded articles
        downloaded_articles.add(filename)

    # Close the WebDriver for the current section
    driver.quit()

# Save the updated list of downloaded articles
with open("downloaded_articles.txt", "w") as file:
    file.write("\n".join(downloaded_articles))
