from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pyautogui as pg
import time
from tkinter import Tk

#todo:fix verification on this method
#todo: may have to change to googel chrome browser
#todo: fix timeing on the whole application(try to reduce time)
def wait5sec(driver):
    try:
        element_present = EC.presence_of_element_located((By.ID, 'element_id'))
        WebDriverWait(driver, 5).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

def bluestacks():
    #close any bluestacks process
    #open /click duo
    #close bluestacks
    pg.hotkey('winleft')
    time.sleep(3)
    pg.typewrite('duo\n', .5)
    time.sleep(40)
    pg.typewrite('b',.5)
    time.sleep(1)





def login():
    #create browser instance
    driver = webdriver.Firefox()
    pg.hotkey('winleft')
    time.sleep(3)
    pg.typewrite('duo\n', .5)
    #navigate to wolfware home page
    driver.get("https://wolfware.ncsu.edu/")

    #click on login button
    driver.find_element_by_link_text("Log in").click()
    wait5sec(driver)

    #input username and password
    elem = driver.find_element_by_name("j_username")
    elem.clear()
    elem.send_keys("psengo")
    elem2 = driver.find_element_by_name("j_password")
    elem2.clear()
    elem2.send_keys("uvZx4e@27vKy")
    driver.find_element_by_id("formSubmit").click()
    wait5sec(driver)
    #now on duo authentication page
    iframe = driver.find_element_by_id("duo_iframe")

    #navigate into duo frame
    driver.switch_to.frame(iframe)

    #select device for authentication
    select = Select(driver.find_element_by_name('device'))
    select.select_by_value('phone2')

    #click on duo push button(can change later)
    z = driver.find_elements_by_tag_name('button')
    current_url = driver.current_url
    time.sleep(25)
    z[2].click()
    time.sleep(5)
    pg.hotkey('ctrl','alt','2')
    time.sleep(20)
    #bluestacks()

    #section to authenticate manually
    #todo: add code to open up bluestacks and auto click allow for duo transmission
    WebDriverWait(driver, 15).until(EC.url_changes(current_url))
    driver.refresh()
    #--------------------------------


    #redirect to page to accept data transmitted
    driver.find_element_by_name("_eventId_proceed").click()
    wait5sec(driver)
    #go to my dashboard page
    driver.get("https://moodle-courses2021.wolfware.ncsu.edu/my/")
    wait5sec(driver)
    # redirect to page to accept data transmitted
    driver.find_element_by_name("_eventId_proceed").click()
    wait5sec(driver)
    #navigate to grades page
    driver.find_element_by_id("action-menu-toggle-1").click()
    driver.find_element_by_link_text('Grades').click()

    #at grades page
    elems = driver.find_elements_by_xpath("//td/a")

    #todo: iterate through the for loop for each
    current_url = elems[0].get_attribute("href")


    #todo: close bluestacks application
    #close the browser
    driver.close()


if __name__ == "__main__":
    #bluestacks()
    login()





