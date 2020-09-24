from bs4 import BeautifulSoup, NavigableString, Tag
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import password

# import pyautogui as pg
import time
import subprocess
from tkinter import Tk
import csv

# todo:fix verification on this method
# todo: may have to change to googel chrome browser
# todo: fix timeing on the whole application(try to reduce time)
def wait5sec(driver):
    try:
        element_present = EC.presence_of_element_located((By.ID, "element_id"))
        WebDriverWait(driver, 5).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")


def bluestacks():
    # opens and run duo veriification
    # subprocess.Popen('"C:\Program Files\BlueStacks\HD-RunApp.exe" -json "{\"app_icon_url\":\"\",\"app_name\":\"Duo Mobile\",\"app_url\":\"\",\"app_pkg\":\"com.duosecurity.duomobile\"}"')
    player = subprocess.Popen("C:\ProgramData\BlueStacks\Client\Bluestacks.exe")
    # macro in bluestacks runs
    time.sleep(60)
    # player.terminate()


def read(pagesource, textTitle):
    # used for scraping in text file.
    # with open("scraped.txt") as fp:
    #   soup = BeautifulSoup(fp, "html5lib")
    # go to page

    soup = BeautifulSoup(pagesource, "html.parser")

    table = soup.find("table")

    # table header(collumn values)
    column = []
    for thead in table.find_all("thead"):
        theadText = thead.get_text("/", strip=True)
        column = theadText.split("/")
    column.append("Category")
    rows = []
    category = "-"
    # todo: project not showing due to no feedback/ coursetotal format messed up due to first column string being split in two rows.
    # todo: add extension for multiple categories
    # get the table body
    for tbody in table.find_all("tbody"):
        # get the table row
        for tr in tbody.find_all("tr"):
            # trText = tr.get_text("/", strip = True)
            # row = trText.split('/')
            row = []
            for child in tr.children:
                if isinstance(child, NavigableString):
                    continue
                if isinstance(child, Tag):
                    if child.get_text() == "":
                        row.append("-")
                    else:
                        row.append(child.get_text())

            # if row has values for each column
            if len(row) == (len(column) - 1):
                row.append(category)
                rows.append(row)
            # if row doesn't have values for each column
            else:
                # if row is not a category
                if not tr.find("i"):
                    print("droped")
                # if the row specifies the category
                else:
                    if tr.find("i")["aria-label"] == "Category":
                        category = row[1]
    # inserts column into row
    rows.insert(0, column)
    # writes out the rows to csv
    with open("grades/" + textTitle + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def login():
    # create browser instance
    driver = webdriver.Firefox()
    ##pg.hotkey('winleft')
    time.sleep(3)
    ##pg.typewrite('duo\n', .5)
    # navigate to wolfware home page
    driver.get("https://wolfware.ncsu.edu/")

    # click on login button
    driver.find_element_by_link_text("Log in").click()
    wait5sec(driver)

    # input username and password
    elem = driver.find_element_by_name("j_username")
    elem.clear()
    elem.send_keys(password.username)
    elem2 = driver.find_element_by_name("j_password")
    elem2.clear()
    elem2.send_keys(password.password)
    driver.find_element_by_id("formSubmit").click()
    wait5sec(driver)
    # now on duo authentication page
    iframe = driver.find_element_by_id("duo_iframe")

    # navigate into duo frame
    driver.switch_to.frame(iframe)

    # select device for authentication
    select = Select(driver.find_element_by_name("device"))
    select.select_by_value("phone2")

    # click on duo push button(can change later)
    z = driver.find_elements_by_tag_name("button")
    current_url = driver.current_url
    # time.sleep(25)
    z[2].click()
    # time.sleep(5)
    # pg.hotkey('ctrl','alt','2')
    # time.sleep(5)
    # pg.hotkey('alt','f4')
    # time.sleep(20)
    # bluestacks()
    time.sleep(10)
    WebDriverWait(driver, 15).until(EC.url_changes(current_url))
    driver.refresh()
    # --------------------------------

    # redirect to page to accept data transmitted
    driver.find_element_by_name("_eventId_proceed").click()
    wait5sec(driver)
    # go to my dashboard page
    driver.get("https://moodle-courses2021.wolfware.ncsu.edu/my/")
    wait5sec(driver)
    # redirect to page to accept data transmitted
    driver.find_element_by_name("_eventId_proceed").click()
    wait5sec(driver)
    # navigate to grades page
    driver.find_element_by_id("action-menu-toggle-1").click()
    driver.find_element_by_link_text("Grades").click()

    # at grades page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    tbody = soup.find("tbody")
    elemst = {}
    for a in tbody.find_all("a", href=True):
        elemst[a.get_text()] = a["href"]

    # elems = driver.find_elements_by_xpath("//td/a")

    # todo: iterate through the for loop for each
    count = 0
    for title, link in elemst.items():
        textTitle = title[:7]
        textTitle = textTitle.strip()
        textTitle = textTitle.replace(" ", "_")
        driver.get(link)
        pagesource = driver.page_source
        read(pagesource, textTitle)

    # close the browser
    driver.close()


if __name__ == "__main__":
    login()

