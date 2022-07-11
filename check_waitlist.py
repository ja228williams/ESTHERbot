import os
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from send_email import send_email


def clean_schedule_text(strs):
    """
    :return: tuple of waitlisted classes w/info (in form of strings)
    """
    courses = []
    course = ""
    for str in strs:
        if re.search(' - [A-Z]{4} [0-9]{3} - [0-9]{3}', str):
            courses.append(course)
            course = str
        else:
            course += str
    courses.append(course)

    waitlisted_courses = []
    for course in courses:
        if 'Waitlist' in course:
            course_info = []
            course_str_rows = course.split('\n')
            course_info.append(course_str_rows[0])
            for txt in course_str_rows:
                if 'Waitlist' in txt or 'Assigned Instructor' in txt or ' am ' in txt or ' pm ' in txt:
                    course_info.append(txt)
            try:
                loc = course_info[len(course_info)-1].rindex('20') + 4
                course_info[len(course_info)-1] = course_info[len(course_info)-1][:loc]
            except:
                pass
            waitlisted_courses.append("\n".join(course_info))

    return waitlisted_courses


def check_waitlist(username, password):
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

    # student detail schedule
    print("navigating to student detail schedule...")
    driver.get("https://esther.rice.edu/selfserve/bwskfshd.P_CrseSchdDetl")

    # term selection
    print("selecting term...\n")
    term_select = Select(WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "term_id"))))
    term_select.select_by_value("202310")
    term_submit = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[@class='pagebodydiv']/form/input[1]"))
    )
    term_submit.click()

    # iterate through tables
    print("reading through courses...")
    tables = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "datadisplaytable")))
    strs = []
    for row in tables:
        strs.append(row.text)
    waitlisted_classes = clean_schedule_text(strs)
    for course in waitlisted_classes:
        print(course)
        print()

    driver.quit()

    return waitlisted_classes


def send_update_email(username, password, sender_email, email_password, receiver_email):
    send_email(sender_email, email_password, "\n\n".join(check_waitlist(username, password)), receiver_email,
               "Waitlisted Courses Update")

# esther info
esther_username = os.environ.get("esther_username")
esther_password = os.environ.get("esther_password")

# email info
sender_email = os.environ.get("sender_email")
email_password = os.environ.get("email_password")
receiver_email = os.environ.get("receiver_email")

send_update_email(esther_username, esther_password, sender_email, email_password, receiver_email)
