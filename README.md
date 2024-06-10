# Description
Python project for retrieving Google ratings.

When you run the script and provide the search term, Chromedriver will open and scroll all the way to the bottom of the page, checking for the 'more results' button. If it exists, the script will click it until no more buttons are available.

![image](https://github.com/h10n3/get_google_ratings/assets/99500478/df449799-d8cd-4a93-99ec-390c3a6f4a17)

The script looks for company name, website, and rating:

![image](https://github.com/h10n3/get_google_ratings/assets/99500478/70733644-efa3-4d0b-b1bd-63fb6f5387f2)

It collects all the necessary information and includes it if the rating is 4 or less:

![image](https://github.com/h10n3/get_google_ratings/assets/99500478/9e2dba5e-151c-4f36-a155-1546c010bb99)

Finally, it saves the results to a ```csv``` file in the same directory:

![image](https://github.com/h10n3/get_google_ratings/assets/99500478/56fdc0c8-d9e1-477e-82a7-dfb064f537e7)


# Install

Download the repository
```bash
git clone https://github.com/h10n3/get_google_ratings.git
```

Install the required modules
```bash
pip install -U requests beautifulsoup4 selenium webdriver-manager
```

I added a Win64 Chromedriver, but always check for the correct [chromedriver version](https://googlechromelabs.github.io/chrome-for-testing/) for your system.


# Usage

Run the script:
```sh
$ python3 get_rating.py
What do you want to search?
>>
```

Or just run the [```.exe```](https://github.com/h10n3/get_google_ratings/tree/main/Windows_Executablehttps://github.com/h10n3/get_google_ratings/tree/main/Windows_Executable) file. 

Provide a query for the search.

Wait until it finishes. If you want, you can continue with a new query or exit.

![image](https://github.com/h10n3/get_google_ratings/assets/99500478/df600647-1459-47e7-9448-242c4e08aa9e)



The results will be saved to a ```csv``` file named ```Companies.csv``` in the same directory.

#Example CSV File
Here is an example of what the Companies.csv file might look like:

```csv
Title,Link,Snippet
Company A,https://companya.com,3.8
Company B,https://companyb.com,3.9
```

# Requirements
Python 3.6 or higher
Google Chrome browser

# Troubleshooting
If you encounter issues with Chromedriver, ensure it matches your Chrome browser version.
Common errors and solutions:
```selenium.common.exceptions.WebDriverException: Check Chromedriver compatibility```.

# Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.
