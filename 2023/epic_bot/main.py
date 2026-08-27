#//*[@id="create-icon"]
#//*[@id="text-item-0"]
#//*[@id="content"]
#//*[@id="next-button"]
#//*[@id="done-button"]
#//*[@id="next-button"]
#//*[@id="close-button"]
#//*[@id="close-button"]/div
#Imports
from selenium.webdriver import *
from selenium.webdriver.common.by import *
import time
import os
#Settings
chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" #Go to chrome://version to get these
profilePath = "C:\\Users\\Morgan\\AppData\\Local\\Google\\Chrome\\User Data\\" #Go to chrome://version to get these and remove everything after user data

#Setup
Settings = ChromeOptions()

Settings.add_argument(f"user-data-dir={profilePath}")
Settings.binary_location = chromePath



#Main loop
while True:
    for file in os.listdir("E:\\memes\\finel"):
        chromeInstance = Chrome(options=Settings)
        chromeInstance.get("https://studio.youtube.com")
        chromeInstance.find_element(by=By.XPATH, value='//*[@id="create-icon"]').click()
        chromeInstance.find_element(by=By.XPATH, value='//*[@id="text-item-0"]').click()
        chromeInstance.find_element(by=By.XPATH, value='//*[@id="content"]/input').send_keys(f"E:\\memes\\finel\{file}")
        time.sleep(10)
        for i in range(3):
            chromeInstance.find_element(by=By.XPATH, value='//*[@id="next-button"]').click()
        time.sleep(1)
        chromeInstance.find_element(by=By.XPATH, value='//*[@id="done-button"]').click()
        time.sleep(8)
        chromeInstance.quit()
        time.sleep(5)        
