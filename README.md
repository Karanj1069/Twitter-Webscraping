# Twitter Scraper

## Overview
This Python script automates the process of logging in to Twitter, searching for a specified subject, and scraping profile information from the search results. The script utilizes the Selenium library for web scraping.

## Prerequisites
- Python (3.x recommended)
- Selenium library (`pip install selenium`)
- Chrome browser
- ChromeDriver (Ensure it's in your system PATH or specify the path in the script)
- YAML library (`pip install pyyaml`)

## Configuration
1. **XPath Configuration**
   - Create an `xpath_config.yml` file with the XPaths for various elements.
     ```yaml
     username_input: "//your/username/input/xpath"
     next_button: "//your/next/button/xpath"
     password_input: "//your/password/input/xpath"
     log_in: "//your/log/in/button/xpath"
     search_box: "//your/search/box/xpath"
     people: "//your/people/xpath"
     tweet_article: "//your/tweet/article/xpath"
     ```

2. **Configurations**
   - Create a `config.yml` file with your Twitter username, password, and the subject you want to search.
     ```yaml
     username: your_twitter_username
     password: your_twitter_password
     subject: your_search_subject
     ```

## Usage
1. **Execution**
   - Run the script using `python twitter.py`.
   - The script will log in to Twitter, search for the specified subject, and scrape profile information from the search results.
   - Extracted data is saved in a CSV file named `{subject}.csv`.
   - The CSV file is automatically opened in Excel for easy viewing.

## Output
- The script creates a CSV file with columns: Username, UserTags, and UserBio.
- The CSV file is saved in the same directory as the script and automatically opened in Excel.

## Notes
- The script uses explicit waits for elements to ensure proper page loading.
- Twitter may have restrictions on automated access, so use the script responsibly and in compliance with Twitter's terms of service.
- Handle exceptions gracefully to avoid disruptions during execution.

## Warning
- Automated scraping of Twitter may violate their terms of service. Use this script responsibly and at your own risk. The authors are not responsible for any misuse or violation of terms.
