import sys
import time
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def register_classes(username, password, netid, crn_lst):
    # driver = webdriver.Chrome("C:/Users/2020c/Downloads/chromedriver_win32/chromedriver.exe")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    orig_url = "https://esther.rice.edu/selfserve/twbkwbis.P_WWWLogin"
    driver.get(orig_url)

    # login page
    print("logging in...")
    user_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "UserID")))
    user_box.send_keys(username)
    password_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "PIN")))
    password_box.send_keys(password)
    login = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[@class='pagebodydiv']/form/p/input[1]")))
    login.click()

    # ESTHER home page
    print("entering banner...")
    banner = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "NewReg")))
    banner.click()

    # Switch tabs to registration home page
    print("switching tabs...")
    second_window = driver.window_handles[1]
    driver.switch_to.window(second_window)

    # Registration home page
    print("entering registration home page...")
    register_home_page = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "registerLink")))
    register_home_page.click()

    # checks for login verification
    if driver.title == "Rice Identity Provider":
        print("verifying identity...")
        netid_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "username")))
        netid_field.send_keys(netid)
        password_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password)
        login_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[@class='wrapper']/div[@class='container']/div["
                                                      "@class='content']/div[@class='column one']/form/div["
                                                      "@class='form-element-wrapper'][4]/button[@class='form-element "
                                                      "form-button']")))
        login_field.click()

    # selecting term (CURRENTLY FALL- MIGHT WORK FOR WHATEVER THE NEXT SEMESTER IS, BUT NEED TO VERIFY/TEST)
    print("selecting term...")
    drop_down = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html[@class=' js no-flexbox flexbox-legacy flexboxlegacy canvas "
                                                  "canvastext webgl no-touch geolocation postmessage websqldatabase "
                                                  "indexeddb hashchange history draganddrop websockets rgba hsla "
                                                  "multiplebgs backgroundsize borderimage borderradius boxshadow "
                                                  "textshadow opacity cssanimations csscolumns cssgradients "
                                                  "cssreflections csstransforms csstransforms3d csstransitions "
                                                  "fontface generatedcontent video audio localstorage sessionstorage "
                                                  "webworkers no-applicationcache svg inlinesvg smil "
                                                  "svgclippaths']/body[@class='webkit webkit537']/main[ "
                                                  "@id='content']/div[@id='inner-center']/div["
                                                  "@class='body-wrapper']/div[@class='body-content']/div["
                                                  "@id='term-date-selection']/div[@id='term-buttons']/fieldset/div["
                                                  "@id='term-window']/div[@id='term-search-combobox']/div["
                                                  "@id='s2id_txt_term']/a[@class='select2-choice']/span["
                                                  "@class='select2-arrow']/b")))
    drop_down.click()
    select_fall = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "202310")))
    select_fall.click()
    continue_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "term-go")))
    continue_button.click()

    # close out notification if it exists
    try:
        print("closing notification...")
        # change which element is being located to a different element of the website that can be found
        notif_close = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
            (By.XPATH, "/html[@class=' js no-flexbox flexbox-legacy flexboxlegacy canvas "
                       "canvastext webgl no-touch geolocation postmessage websqldatabase "
                       "indexeddb hashchange history draganddrop websockets rgba hsla "
                       "multiplebgs backgroundsize borderimage borderradius boxshadow "
                       "textshadow opacity cssanimations csscolumns cssgradients "
                       "cssreflections csstransforms csstransforms3d csstransitions "
                       "fontface generatedcontent video audio localstorage "
                       "sessionstorage webworkers no-applicationcache svg inlinesvg smil "
                       "svgclippaths']/body[@class='webkit webkit537']/header["
                       "@id='header-main-section']/div["
                       "@id='header-main-section-east-part']/div["
                       "@id='notification-center']/div["
                       "@class='notification-center-flyout "
                       "notification-center-flyout-displayed']/ul["
                       "@class='prompt-container']/li[@class='notification-item "
                       "notification-center-message-with-prompts "
                       "notification-center-message-warning']/div["
                       "@class='notification-item-prompts']/button["
                       "@class='notification-flyout-item primary']")))
        notif_close.click()
    except NoSuchElementException:
        print("no notification to be cleared")

    # add courses marked by crn to list of desired classes
    print("adding courses...")
    crn_tab = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "enterCRNs-tab")))
    crn_tab.click()

    for i in range(len(crn_lst) - 1):
        next_crn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "addAnotherCRN")))
        next_crn.click()

    for i in range(len(crn_lst)):
        crn = crn_lst[i]
        crn_entry = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "txt_crn" + str(i + 1))))
        crn_entry.send_keys(crn)

    add_to_summary = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "addCRNbutton")))
    add_to_summary.click()

    # submit courses
    print("submitting courses...")
    # submit = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "saveButton")))
    # submit.click()
    print("process completed. terminating in 30 seconds.")

    # freeze for 30 seconds and terminate
    time.sleep(25)
    print("terminating in 5... ")
    time.sleep(1)
    for i in range(4, 0, -1):
        print(str(i) + "...")
        time.sleep(1)
    print("terminating...")
    driver.quit()
