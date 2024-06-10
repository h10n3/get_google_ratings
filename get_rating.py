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
import os

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
        link = g.find('a', class_="yYlJEf Q7PwXb L48Cpd brKmxb")['href'] if g.find('a', class_="yYlJEf Q7PwXb L48Cpd brKmxb") else 'No link'
        snippet = g.find('span', class_='yi40Hd YrbPuc').text if g.find('span', 'yi40Hd YrbPuc') else 'No Raiting'

        # Check the 'snippet' value if it's 4 or less
        try:
            snippet_value = float(snippet.replace(',', '.'))
            if snippet_value < 4.0:
                results.append({'Title': title, 'Link': link, 'Raiting': snippet_value})
        except ValueError:
            continue  # If the value cannot be converted to float, skip it

    return results

def save_to_csv(results):
    # Check if the file exist
    file_exist = os.path.isfile("Companies.csv")
    with open('Companies.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Link', 'Raiting'])

        # If not exist, create and add field names
        if not file_exist:
            writer.writeheader()

        # Write the result to file
        for result in results:
            writer.writerow(result)

def scroll_and_collect_results(driver):
    results = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        try:
            # Find and click the "Load more" button
            more_results_button = driver.find_element(By.XPATH, "//div[@class='ZFiwCf']")
            more_results_button.click()
            time.sleep(20)
        except Exception:
            print("Collecting data....")

        # Scroll down to the bottom
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)  # You can adjust this time according to your internet speed

        # Get new page height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If 'Load more' options exist, try to click it
            for _ in range(15):
                try:
                    more_results_button = driver.find_element(By.XPATH, "//div[@class='GNJvt ipz2Oe']")
                    more_results_button.click()
                    time.sleep(2)  # Sayfanın yüklenmesi için kısa bir bekleme süresi
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                except Exception:
                    break
            break
        last_height = new_height

        # Collect results from the current page
        page_html = driver.page_source
        new_results = parse_results(page_html)
        results.extend(new_results)
    return results

def get_query():
    query = urllib.parse.quote_plus(input("What do you want to search?\n>> "))

    # Set up the Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(
        f"https://www.google.com/search?q={query}&sca_esv=4ce04de13f7e18f6&udm=1&biw=855&bih=919&ei=Ci9jZurcI4-Xi-gPh-f2qQU&ved=0ahUKEwjqia3k7smGAxWPywIHHYezPVUQ4dUDCBA&uact=5&oq=makelaar+alkmaar&gs_lp=Egxnd3Mtd2l6LXNlcnAiEG1ha2VsYWFyIGFsa21hYXIyBRAAGIAEMgUQABiABDIFEAAYgAQyBhAAGBYYHjIGEAAYFhgeMggQABgWGB4YDzIIEAAYFhgeGA8yCBAAGBYYHhgPMggQABgWGB4YDzIGEAAYFhgeSI0TUOIHWMAQcAJ4AJABAJgBN6ABtQKqAQE3uAEDyAEA-AEBmAIJoALzAsICBhAAGAcYHsICCxAAGIAEGLEDGIMBwgIIEAAYgAQYogSYAwCIBgGSBwE5oAe2KA&sclient=gws-wiz-serp#ip=1"
    )

    # Reject cookies
    try:
        more_results_button = driver.find_element(By.XPATH, "//div[@class='QS5gu sy4vM']")
        more_results_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error handling cookies: {e}")

    # Scroll and collect results
    results = scroll_and_collect_results(driver)

    # Close the browser
    driver.quit()

    # Save results to CSV
    save_to_csv(results)

def main():
    get_query()
    next_question = int(input("Do you want to search again?\n1- Yes\n2- Exit\n>> "))
    while next_question == 1:
        get_query()
        next_question = int(input("Do you want to search again?\n1- Yes\n2- Exit\n>> "))

    print("Exiting...\nThe results are saved to Companies.csv file\nHave a nice day")
    exit()

if __name__ == "__main__":
    main()
