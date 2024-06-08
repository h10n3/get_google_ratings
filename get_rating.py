import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def google_search(query):
    try:
        url = f"https://www.google.com/search?q={query}&sca_esv=4ce04de13f7e18f6&udm=1&biw=855&bih=919&ei=Ci9jZurcI4-Xi-gPh-f2qQU&ved=0ahUKEwjqia3k7smGAxWPywIHHYezPVUQ4dUDCBA&uact=5&oq=makelaar+alkmaar&gs_lp=Egxnd3Mtd2l6LXNlcnAiEG1ha2VsYWFyIGFsa21hYXIyBRAAGIAEMgUQABiABDIFEAAYgAQyBhAAGBYYHjIGEAAYFhgeMggQABgWGB4YDzIIEAAYFhgeGA8yCBAAGBYYHhgPMggQABgWGB4YDzIGEAAYFhgeSI0TUOIHWMAQcAJ4AJABAJgBN6ABtQKqAQE3uAEDyAEA-AEBmAIJoALzAsICBhAAGAcYHsICCxAAGIAEGLEDGIMBwgIIEAAYgAQYogSYAwCIBgGSBwE5oAe2KA&sclient=gws-wiz-serp#ip=1"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url}: {str(e)}")
        return None

def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='VkpGBb'):
        title = g.find('span', class_='OSrXXb').text if g.find('span', class_='OSrXXb') else 'No Company Name'
        link = g.find('a', class_="yYlJEf Q7PwXb L48Cpd brKmxb")['href'] if g.find('a', "yYlJEf Q7PwXb L48Cpd brKmxb") else 'No link'
        snippet = g.find('span', class_='yi40Hd YrbPuc').text if g.find('span', 'yi40Hd YrbPuc') else 'No Raiting'

        # Check the value of 'snippet' and see if it is 4 or higher
        try:
            snippet_value = float(snippet.replace(',', '.'))
            if snippet_value >= 4.0:
                results.append({'title': title, 'link': link, 'snippet': snippet_value})
        except ValueError:
            continue 

    return results
# Save the results to 'results.csv'
def save_to_csv(results):
    with open('bedrijven.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'link', 'snippet'])
        writer.writeheader()
        for result in results:
            writer.writerow(result)

def scroll_and_collect_results(driver):
    results = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        # Wait for the page to load
        time.sleep(3)  # You can adjust this time according to your internet speed
        # Get new page height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If 'Load more' options exists try to click it
            try:
                more_results_button = driver.find_element(By.XPATH, "//div[@class='GNJvt ipz2Oe']")
                more_results_button.click()
                time.sleep(2)  # You can adjust this time according to your internet speed
            except Exception as e:
                print(f"Could not load more results: {str(e)}")
            break  # If the height hasn't changed, we've reached the end
        last_height = new_height
        # Collect results from the current page
        page_html = driver.page_source
        new_results = parse_results(page_html)
        results.extend(new_results)
    return results

def main():
    # Get search term
    query = urllib.parse.quote_plus(input("What do you want to search?\n> "))

    # Set up the Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(f"https://www.google.com/search?q={query}&sca_esv=4ce04de13f7e18f6&udm=1&biw=855&bih=919&ei=Ci9jZurcI4-Xi-gPh-f2qQU&ved=0ahUKEwjqia3k7smGAxWPywIHHYezPVUQ4dUDCBA&uact=5&oq=makelaar+alkmaar&gs_lp=Egxnd3Mtd2l6LXNlcnAiEG1ha2VsYWFyIGFsa21hYXIyBRAAGIAEMgUQABiABDIFEAAYgAQyBhAAGBYYHjIGEAAYFhgeMggQABgWGB4YDzIIEAAYFhgeGA8yCBAAGBYYHhgPMggQABgWGB4YDzIGEAAYFhgeSI0TUOIHWMAQcAJ4AJABAJgBN6ABtQKqAQE3uAEDyAEA-AEBmAIJoALzAsICBhAAGAcYHsICCxAAGIAEGLEDGIMBwgIIEAAYgAQYogSYAwCIBgGSBwE5oAe2KA&sclient=gws-wiz-serp#ip=1")

    # Wait for the user to manually handle the cookie consent
    # input("Please handle the cookie consent and press Enter to continue...")
    time.sleep(5)

    # Scroll and collect results
    results = scroll_and_collect_results(driver)

    # Close the browser
    driver.quit()

    # Save results to CSV
    save_to_csv(results)


if __name__ == "__main__":
    main()
