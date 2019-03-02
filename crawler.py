from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os
import json
import pymongo

database_url="mongodb://localhost:12345/"

def catch_main_discussions():
    # After opening the url above, Selenium clicks the specific agency link
    python_buttons = driver.find_elements_by_xpath(
        '''//*[@class='tl-cell views-field views-field-profanity-title']//a''')

    for i in range(len(python_buttons)):
        python_button = driver.find_elements_by_xpath(
            '''//*[@class='tl-cell views-field views-field-profanity-title']//a''')[i]
        python_button.click()
        soup_level1 = BeautifulSoup(driver.page_source, 'lxml')
        x = 0  # counter

        # Beautiful Soup grabs the HTML title on the thread
        all_threads = soup_level1.find_all(
            'div', {'class': 'post-content post-left-offset'})
        title = soup_level1.findAll('h3', {'class': 'post-title'})[0].text
        posts_dict = []
        main_thread = True

        for i in range(len(all_threads)):
            if main_thread:
                post_date = all_threads[i].findChildren(
                    "span", {'class': 'post-created hidden-xs'})[0].text
                main_thread = False
            else:
                post_date = all_threads[i].findChildren(
                    'span', {'class': 'post-is-reply-to'})[0].text
            post_text = all_threads[i].findChildren(
                'div', {'class': 'field-item even'})[0].text
            posts_dict.append({post_date: post_text})

        raw_data = {title: posts_dict}
        # Store the dataframe in a list
        data_list.append(raw_data)
        x += 1
        driver.back()
    return


def try_next_button():
    while(True):
        try:
            # Go to replies section first
            python_button = driver.find_elements_by_xpath(
                '''//*[@class='next last']//a''')
            python_button[0].click()

            # After opening the url above, Selenium clicks the specific agency link
            python_buttons = driver.find_elements_by_xpath(
                '''//*[@class='tl-cell views-field views-field-profanity-title']//a''')

            for i in range(len(python_buttons)):
                python_button = driver.find_elements_by_xpath(
                    '''//*[@class='tl-cell views-field views-field-profanity-title']//a''')[i]
                python_button.click()
                soup_level1 = BeautifulSoup(driver.page_source, 'lxml')
                x = 0  # counter

                # Beautiful Soup grabs the HTML title on the thread
                all_threads = soup_level1.find_all(
                    'div', {'class': 'post-content post-left-offset'})
                title = soup_level1.findAll(
                    'h3', {'class': 'post-title'})[0].text
                posts_dict = []

                for i in range(len(all_threads)):
                    try:
                        post_date = all_threads[i].findChildren(
                            "span", {'class': 'post-created hidden-xs'})[0].text
                    except IndexError:
                        post_date = all_threads[i].findChildren(
                            'span', {'class': 'post-is-reply-to'})[0].text

                    post_text = all_threads[i].findChildren(
                        'div', {'class': 'field-item even'})[0].text
                    posts_dict.append({post_date: post_text})

                raw_data = {title: posts_dict}
                # Store the dataframe in a list
                data_list.append(raw_data)
                x += 1
                driver.back()

        except:
            return False
    return


def catch_replies():
    # Go to replies section first
    python_button = driver.find_elements_by_xpath(
        '''//*[@class='']//a''')
    python_button[0].click()

    # After opening the url above, Selenium clicks the specific agency link
    python_buttons = driver.find_elements_by_xpath(
        '''//*[@class='tl-cell views-field views-field-profanity-title']//a''')

    for i in range(len(python_buttons)):
        python_button = driver.find_elements_by_xpath(
            '''//*[@class='tl-cell views-field views-field-profanity-title']//a''')[i]
        python_button.click()
        soup_level1 = BeautifulSoup(driver.page_source, 'lxml')
        x = 0  # counter

        # Beautiful Soup grabs the HTML title on the thread
        all_threads = soup_level1.find_all(
            'div', {'class': 'post-content post-left-offset'})
        title = soup_level1.findAll('h3', {'class': 'post-title'})[0].text
        posts_dict = []

        for i in range(len(all_threads)):
            try:
                post_date = all_threads[i].findChildren(
                    "span", {'class': 'post-created hidden-xs'})[0].text
            except IndexError:
                post_date = all_threads[i].findChildren(
                    'span', {'class': 'post-is-reply-to'})[0].text

            post_text = all_threads[i].findChildren(
                'div', {'class': 'field-item even'})[0].text
            posts_dict.append({post_date: post_text})

        raw_data = {title: posts_dict}
        # Store the dataframe in a list
        data_list.append(raw_data)
        x += 1
        driver.back()

    try_next_button()
    return


def push_to_database(mydict):
    myclient = pymongo.MongoClient(database_url)
    mydb = myclient["mydatabase"]
    mycol = mydb["users"]
    mycol.insert(mydict,check_keys=False)
    return


def push_to_csv(user, data):
    for post in data: 
        for thread in post:
            for item in post[thread]:
                time = list(item.keys())[0]
                text = list(item.values())[0]
                csv_data.append([user,thread,time,text])
    

# launch url
url_base = "https://www.cancerresearchuk.org/about-cancer/cancer-chat/users/"
usernames = ["lonelygirl", "billygoat", "foxdale", "andydorro1",
             "dragonfly46", "dondon0808", "anchor1707", "twintwo", "parmz"]

csv_data = []
for user in usernames:
    driver = webdriver.Firefox()    # create a new Firefox session
    driver.implicitly_wait(30)
    driver.get(url_base+user)
    data_list = []  # empty list
    catch_main_discussions()
    catch_replies()
    driver.quit()   # end the Selenium browser session
    # push_to_database({user:data_list})
    push_to_csv(user,data_list)
    time.sleep(1)

df=pd.DataFrame(csv_data, columns = ["user", "thread", "time", "text"])
df.to_csv('scraped_data/cancerUK.csv', header=True, sep=',', index=False)

print("Done crawling")