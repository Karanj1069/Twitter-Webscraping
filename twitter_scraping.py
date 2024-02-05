#!/usr/bin/env python
# coding: utf-8

# In[29]:


import os
import yaml
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def log_event(event):
    logging.info(event)

def read_yaml_file(file_path):
    with open(file_path) as f:
        data = yaml.safe_load(f)
        return data

def setup_driver(chromedriver_path):
    s = Service(chromedriver_path)
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    return driver

def login_to_twitter(driver, username, password):
    url = 'https://twitter.com/login'
    driver.get(url)

    time.sleep(3)
    username_input = driver.find_element(By.XPATH, username_input_xpath)
    username_input.send_keys(username)

    next_button = driver.find_element(By.XPATH, next_button_xpath)
    next_button.click()

    time.sleep(3)
    password_input = driver.find_element(By.XPATH, password_input_xpath)
    password_input.send_keys(password)

    log_in = driver.find_element(By.XPATH, log_in_xpath)
    log_in.click()
    log_event(f"Crawled {url}")

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, search_box_xpath)))
    time.sleep(3)

def search_for_subject(driver, subject):
    search_box = driver.find_element(By.XPATH, search_box_xpath)
    search_box.send_keys(subject)
    search_box.send_keys(Keys.ENTER)
    log_event(f"Searched for {subject}")

    people = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, people_xpath)))
    people.click()
    time.sleep(5)

    log_event(f"Searched for people related to {subject}")
    driver.execute_script("window.scrollBy(0, 500);")

def scrape_twitter_profiles(driver, tweet_article_xpath):
    usernames = []
    user_tags = []
    user_bio = []
    tweet_article = driver.find_element(By.XPATH, tweet_article_xpath)
    tweets = tweet_article.find_elements(By.XPATH, './/section/div/div/div/div/div')

    for i, tweet in enumerate(tweets):
        try:
            time.sleep(4)
            tweet_text = tweet.find_element(By.XPATH, './/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]').text
            tweet_tag = tweet.find_element(By.XPATH, f'{tweet_article_xpath}/section/div/div/div/div/div[{i+1}]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span').text

            usernames.append(tweet_text)
            user_tags.append(tweet_tag)

            user_bio_xpath = f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div/div/div[{i+1}]/div/div/div/div/div[2]/div[2]'
            User_bio_elements = driver.find_elements(By.XPATH, user_bio_xpath)
            for element in User_bio_elements:
                user_bio.append(element.text)
            time.sleep(4)
            
            log_event(f"Crawled through profile of {tweet_text}")
        except Exception as e:
            log_event(f"Error while crawling a profile: {str(e)}")

    return usernames, user_tags, user_bio

def save_data_to_csv(subject, usernames, user_tags, user_bio):
    df = pd.DataFrame({'Username': usernames, 'UserTags': user_tags, 'UserBio': user_bio})
    current_dir = os.getcwd()
    csv_path = os.path.join(current_dir, f'{subject}.csv')
    df.to_csv(csv_path, index=False)
    os.system(f'start "excel" "{csv_path}"')
    log_event("Updated the data in CSV")
    log_event(f"Finished scraping. CSV file created at: {csv_path}")

if __name__ == '__main__':
    xpath_config_path = "xpath_config.yml"
    xpath_config = read_yaml_file(xpath_config_path)

    username_input_xpath = xpath_config["username_input"]
    next_button_xpath = xpath_config["next_button"]
    password_input_xpath = xpath_config["password_input"]
    log_in_xpath = xpath_config["log_in"]
    search_box_xpath = xpath_config["search_box"]
    people_xpath = xpath_config["people"]
    tweet_article_xpath = xpath_config["tweet_article"]

    logging.basicConfig(filename="twitter_scraper.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    config_path = "config.yml"
    config = read_yaml_file(config_path)

    username = config["username"]
    password = config["password"]
    subject = config["subject"]

    driver = setup_driver("path_to_chromedriver")
    login_to_twitter(driver, username, password)
    search_for_subject(driver, subject)
    scraped_usernames, scraped_user_tags, scraped_user_bio = scrape_twitter_profiles(driver, tweet_article_xpath)
    save_data_to_csv(subject, scraped_usernames, scraped_user_tags, scraped_user_bio)

    driver.quit()


# In[ ]:




