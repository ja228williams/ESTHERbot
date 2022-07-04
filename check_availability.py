import os
import sys
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from html_code_cleaner import code_to_course
from send_email import send_email
from email.message import EmailMessage


def reformat_class_string(class_str):
    new_class_str = ""

    # organize class_str
    components = class_str.split('\n')
    title = components[0]
    prof_format_block = components[1]
    try:
        format = prof_format_block[:prof_format_block.index(' ')]
        prof = prof_format_block[prof_format_block.index(' ') + 1:]
        prof_format_block = format + "\n" + prof
    except ValueError:
        prof_format_block = prof_format_block + "\nNo currently assigned professor."
    time_type = components[9]
    time = time_type[:time_type.rindex(' Type:')]
    type = time_type[time_type.rindex('Type:'):]
    seats = components[-1]

    new_class_str += title + '\n' + prof_format_block + '\n' + time + '\n' + type + '\n' + seats

    return new_class_str


def check_availability(username, password, netid, course_name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    orig_url = "https://esther.rice.edu/selfserve/twbkwbis.P_WWWLogin"
    driver.get(orig_url)

    # parse subject and course number
    subject = course_name[0:4]
    course_number = course_name[-3:]

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

    # navigate to "browse course schedule"
    print("navigating to 'browse course schedule'...")
    browse_schedule = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "classSearchLink")))
    browse_schedule.click()

    # select newest (default) term
    print("selecting term...")
    term_selection = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "select2-chosen-1")))
    term_selection.click()
    fall_sem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "202310")))
    fall_sem.click()
    term_cont = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "term-go")))
    term_cont.click()

    print("inputting class information...")
    # input subject
    subject_name_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "s2id_txt_subject")))
    subject_name_box.click()

    subject_name_word_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "s2id_autogen1")))
    subject_name_word_box.send_keys(subject)

    subject_name_selection = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, subject)))
    subject_name_selection.click()

    # input course number
    course_number_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "txt_courseNumber")))
    course_number_input.send_keys(course_number)

    # search for crn
    crn_search = WebDriverWait(driver, 30).until((EC.presence_of_element_located((By.ID, "search-go"))))
    crn_search.click()

    # analyze course table
    courses = []
    available_courses = []
    course_table = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "table1")))
    for row in course_table.find_elements(By.CSS_SELECTOR, 'tr'):
        row_str = row.text
        if row_str == "Title\nInstructor\nMeeting Times\nStatus":
            continue
        if 'FULL' not in row_str:
            available_courses.append(row_str)
        courses.append(row_str)

    for course in courses:
        print('\n' + reformat_class_string(course))
    print()

    driver.quit()

    return available_courses


def send_update_email(username, password, netid, course_name, sender_email, email_password, receiver_email):
    available_courses = []

    try:
        available_courses = check_availability(username, password, netid, course_name)
    except Exception as e:
        message = "Error accessing class information from ESTHER.\n\n" + str(traceback.format_exc())
        subject = "Error accessing ESTHER"
        send_email(sender_email, email_password, message, receiver_email, subject)
        quit(1)

    if len(available_courses) == 0:
        message = "No sections of " + course_name + " are currently available. "
        subject = message
    else:
        message = str(len(available_courses)) + " section" + (
            's' if len(available_courses) > 1 else '') + " of " + course_name + " are available. "
        subject = message
        for course in available_courses:
            message += 2 * '\n' + reformat_class_string(course)
    print(message)

    send_email(sender_email, email_password, message, receiver_email, subject)


# esther login info
my_netid = ""
my_username = ""
my_password = ""
course_name = "MUSI 117"

# email info
sender_email = ""
email_password = ""
receiver_email = ""

# check_availability(my_username, my_password, my_netid, course_name)
# send_update_email(my_username, my_password, my_netid, course_name, sender_email, email_password, receiver_email)

# to-do:
# 1) setup scheduling email schedule