# graphical-facebook
This is a library to pull posts from facebook and analyze them as a whole

Before running the script you need to install the library referenced in the repo, called "facebook-scraper" and implement some changes.
The changes are mentioned in a file called "facebook-scraper.diff", which can be run on the repo locally or implemented mannually.
If requested, a guide will be added in the future.

To get new posts, put a facebook cookie file in the path "facebook.com_cookies.txt", and run:
```
python3 main.py <page_name>
```

note that posts are added to the csv file if it exists, so make sure to avoid duplicates.

