'''
Save all your Favorited TikToks before the goberment takes them away

Usage:
    python ttdl-faves.py -u <username> -o <output_directory>

Arguments:
    -u, --handle: The handle of the user whos favorites you want to save.
    -o, --output: The output directory to save the TikToks to (optional, defaults 'out')

You will need some dependencies. See the README for more info.

Enjoy.
'''

import argparse
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyktok as pyk
import os
import subprocess
import io
import contextlib


def main():
    # argparse setup
    parser = argparse.ArgumentParser(description='Save all your Favorited TikToks')
    parser.add_argument('-u', '--handle', type=str, required=True, help='The handle of the user whos favorites you want to save.')
    # parser.add_argument('-p', '--profile', type=str, help='Chrome profile in which you are logged into tiktok. find by navigating to `chrome://version/` in chrome and looking for the `Profile Path`. Paste with quite marks (ie "C:\\Users\\username\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1").')
    parser.add_argument('-o', '--output', type=str, default='out', help='The output directory to save the TikToks to (default: out)')
    args = parser.parse_args()
    user_handle = args.handle
    print(f"Saving {user_handle}'s Favrites...")

    # tiktok stuff setup
    pyk.specify_browser('chrome')
    save_url = f'https://www.tiktok.com/@{user_handle}'

    # Selenium setup
    # profile_directory = args.profile # not using profile for now
    options = webdriver.ChromeOptions()

    # not using specific profile for now...
    # options.add_argument(f"--user-data-dir={'/'.join(profile_directory.split('/')[0:-1])}")  # Path to your Chrome user data directory
    # options.add_argument(f"--profile-directory={profile_directory.split('/')[-1]}")  # Profile directory

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # the internet says this helps
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")  # Uncomment for headless mode

    driver.get(save_url)
    time.sleep(5)

    # wait for the user to sign in
    ndots = 0
    while driver.find_elements(By.ID, "header-login-button"):
        print("Please sign in to TikTok" + "." * ndots, end="\r")
        ndots = (ndots + 1) % 4
        
        time.sleep(0.1)

    print("Signed in! Continuing...")
    time.sleep(5)

    # click on the favorites tab
    favorites_tab = driver.find_element(By.XPATH, "//*[contains(@class, 'PFavorite')]")
    favorites_tab.click()
    time.sleep(5)

    # scroll to the bottom of the page to load all the favorites
    print('Loading all of your favorites...')
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_content = driver.page_source

    # beautiful soup setup
    soup = BeautifulSoup(html_content, 'html.parser')
    favorites_container = soup.find('div', {'data-e2e': 'favorites-item-list'})
    favorites = favorites_container.find_all(recursive=False) if favorites_container else []

    output_directory = args.output
    if output_directory:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

    for favorite in favorites:
        a_element = favorite.find('a', recursive=True)
        if a_element:
            print(a_element['href'])
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    curr_tiktok = pyk.save_tiktok(a_element['href'],
                        True,
                        'video_data.csv',
                        'chrome',
                        return_fns=True)
                
                subprocess.run(f"mv {curr_tiktok["video_fn"]} {output_directory}", shell=True)
            except Exception as e:
                print(f"Error saving {a_element['href']}: {e}")
                print("Continuing...")
                continue

if __name__ == "__main__":
    main()