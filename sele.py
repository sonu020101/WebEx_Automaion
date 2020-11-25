from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


participants_info = {}


def joiner(name_now, driver, frame):
    print(frame)
    driver.switch_to.frame(frame)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="meetingSimpleContainer"]/div[2]/div[2]/input')))
        namer = driver.find_element_by_xpath('//*[@id="meetingSimpleContainer"]/div[2]/div[2]/input')
        namer.clear()
        namer.send_keys(name_now)
        emailer = driver.find_element_by_xpath('//*[@id="meetingSimpleContainer"]/div[2]/div[3]/input')
        emailer.clear()
        emailer.send_keys(participants_info[name_now])
        emailer.send_keys(Keys.RETURN)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div[1]/button')))
            driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div/div/div[1]/button').click()
        except:
            print("No extra key")
        driver.find_element_by_xpath('//*[@id="meetingSimpleContainer"]/div[3]/div[2]/div[1]/div/button').click()
        driver.find_element_by_xpath('//*[@id="interstitial_join_btn"]').click()

    except:
        print("Unable to find element")


def leave(driver):
    driver.close()


if __name__ == '__main__':
    n = int(input("Enter number of participants: "))
    for i in range(n):
        name_in = input(f"Enter name of participant {i + 1}: ")
        email_in = input(f"Enter email of participant {i + 1}: ")
        try:
            participants_info[name_in] = email_in
        except Exception as e:
            print(f"Error: {e}")

    time.sleep(3)
    sec=int(input("Enter amount of time in seconds that a person should stay in meeting: "))
    path = input("Enter path of chrome driver: ")
    link=input("Link of meeting: ")
    for name_now in participants_info.keys():
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_argument("--disable-infobars")
        options.add_experimental_option("prefs", { \
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_setting_values.notifications": 1
        })

        driver = webdriver.Chrome(path, options=options)
        driver.get(link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pb_iframecontainer"]')))
        main_div = driver.find_elements_by_xpath('//*[@id="pb_iframecontainer"]')
        print(main_div)
        for elem in main_div:
            print(elem.get_attribute("iframe"))
        size = driver.find_elements_by_tag_name("iframe")
        print(len(size))

        for elem in size:
            print(elem)

        joiner(name_now, driver, size[3].get_attribute("id"))
        time.sleep(sec)
        leave(driver)
