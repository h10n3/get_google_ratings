# Description
Python project for getting google ratings.

When you run the script and give the search term, chromedriver will be opened, 
It waits 5 seconds in case cookie approval is required,

![image](https://github.com/h10n3/get_google_ratings/assets/99500478/c99b981c-82aa-4ba0-9dcb-a547d0eb9024)


After acceptance, it scrolls all the way to the bottom of the page and checks the possible 'more results' button,
If exists clicks it until there is no more button.

![image](https://github.com/h10n3/get_google_ratings/assets/99500478/df449799-d8cd-4a93-99ec-390c3a6f4a17)

Look for compony name, website and the raiting:

![image](https://github.com/h10n3/get_google_ratings/assets/99500478/70733644-efa3-4d0b-b1bd-63fb6f5387f2)

Gets all needed information and if the raiting is 4 or more it includes it,

![image](https://github.com/h10n3/get_google_ratings/assets/99500478/9e2dba5e-151c-4f36-a155-1546c010bb99)

Finally, save the results in same directory with the name of the searched term:

![image](https://github.com/h10n3/get_google_ratings/assets/99500478/56fdc0c8-d9e1-477e-82a7-dfb064f537e7)


# Install

Download the repository
```bash
git clone https://github.com/h10n3/get_google_ratings.git
```

Install the required modules
```bash
pip install -U requests beautifulsoup4 selenium webdriver-manager csv
```

I added a win64 chromedriver but always check the right [chromedriver version](https://googlechromelabs.github.io/chrome-for-testing/) for your own.


# Usage

Run the script:
```sh
$ python3 get_rating.py
What do you want to search?
>>
```

Accept the coookies and wait until finish.

![image](https://github.com/h10n3/get_google_ratings/assets/99500478/0d632381-df2c-4803-b896-b7891cfd920d)


The resuls will be saved to a ```csv``` file with the name of queried term in the same directory.
