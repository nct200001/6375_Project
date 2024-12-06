from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Initialize the Selenium WebDriver (use the appropriate driver for your browser)
driver = webdriver.Chrome()  # Replace with your WebDriver (e.g., ChromeDriver)
url = 'https://www.ratemyprofessors.com/search/professors/1273?q=*'

# Open the webpage
driver.get(url)

# Wait for the page to load and dynamically load content
wait = WebDriverWait(driver, 10)
count = 0

# Keep clicking "Show More" until all professors are loaded
while count < 10000:
    try:
        # Wait for the "Show More" button to be clickable and then click it
        show_more_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'PaginationButton__StyledPaginationButton-txi1dr-1'))
        )
        show_more_button.click()
        count = count + 1
        time.sleep(100)  # Small delay to allow content to load
    except Exception:
        # If "Show More" button is not found or clickable, assume all content is loaded
        break

# Get the page source after loading all content
html_content = driver.page_source

# Close the Selenium driver
driver.quit()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all professor links
professor_links = soup.find_all('a', class_='TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx')

# Collect the full URLs of each professor's page
professor_urls = []
base_url = 'https://www.ratemyprofessors.com'

for link in professor_links:
    href = link.get('href')
    if href:
        # Concatenate base URL with the relative href
        professor_urls.append(base_url + href)

# Write the collected URLs to a text file
with open('professor_urls.txt', 'w') as file:
    for url in professor_urls:
        file.write(url + '\n')

print(f"Collected {len(professor_urls)} professor URLs. Data has been written to 'professor_urls.txt'.")
