import os
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from send_email import send_email


def reformat_class_string(class_str):
    """
    Reformats the string for a given class into a cleaner form.

    :param class_str: The raw input class string

    :return: A string consisting of the course's title, format, professor, time, type, and number of remaining seats.
    """

    # organizes class_str into components
    components = class_str.split('\n')
    title = components[0]
    prof_format_block = components[1]

    # separates format from professor within line
    try:
        format = prof_format_block[:prof_format_block.index(' ')]
        prof = prof_format_block[prof_format_block.index(' ') + 1:]
        prof_format_block = format + "\n" + prof
    except ValueError:
        prof_format_block = prof_format_block + "\nNo currently assigned professor."

    # isolates other relevant components
    time_type = components[9]
    time = time_type[:time_type.rindex(' Type:')]
    type = time_type[time_type.rindex('Type:'):]
    seats = components[-1]

    new_class_str = title + '\n' + prof_format_block + '\n' + time + '\n' + type + '\n' + seats

    return new_class_str


def check_availability(username, password, course_name):
    """
    Checks ESTHER for availability of sections for a given course.

    :param username: ESTHER username (student ID of form SXXXXXXXX)
    :param password: ESTHER password
    :param course_name: Name of the course in the form of the name of the department and course number (ex. MUSI 117)

    :return: list of strings describing available course sections, including the course's name, type, professor, time,
             and number of remaining seats.
    """
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    except PermissionError:
        # attempts to avoid collision with other process
        time.sleep(61)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    orig_url = "https://esther.rice.edu/selfserve/twbkwbis.P_WWWLogin"
    driver.get(orig_url)

    # parses subject and course number
    subject = course_name[0:4]
    course_number = course_name[-3:]

    # accesses login page
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

    # switches tabs to registration home page
    print("switching tabs...")
    second_window = driver.window_handles[1]
    driver.switch_to.window(second_window)

    # navigates to "browse course schedule"
    print("navigating to 'browse course schedule'...")
    browse_schedule = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "classSearchLink")))
    browse_schedule.click()

    # selects newest (default) term
    print("selecting term...")
    term_selection = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "select2-chosen-1")))
    term_selection.click()
    fall_sem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "202310")))
    fall_sem.click()
    term_cont = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "term-go")))
    term_cont.click()

    # inputs subject
    print("inputting class information...")
    subject_name_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "s2id_txt_subject")))
    subject_name_box.click()

    subject_name_word_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "s2id_autogen1")))
    subject_name_word_box.send_keys(subject)

    subject_name_selection = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, subject)))
    subject_name_selection.click()

    # inputs course number
    course_number_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "txt_courseNumber")))
    course_number_input.send_keys(course_number)

    # searches for crn
    crn_search = WebDriverWait(driver, 30).until((EC.presence_of_element_located((By.ID, "search-go"))))
    crn_search.click()

    # analyzes course table
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


def send_update_email(username, password, course_name, sender_email, email_password, receiver_email):
    """
    Sends an email update about available sections of a course. Prints the message sent to the receiving email or the
    backtrace of an error if one occurs.

    :param username: ESTHER username (student ID of form SXXXXXXXX)
    :param password: ESTHER password
    :param course_name: Name of the course in the form of the name of the department and course number (ex. MUSI 117)
    :param sender_email: Name of the email account being used to send the update email.
    :param email_password: Password for the email account being used to send the update email.
    :param receiver_email: Name of the email account receiving the update email.
    """
    available_courses = []

    # finds available courses via check_availability function
    try:
        available_courses = check_availability(username, password, course_name)
    except:
        # handles errors from check_availability funciton
        message = "Error accessing class information from ESTHER.\n\n" + str(traceback.format_exc())
        print(message)
        subject = "Error accessing ESTHER"
        send_email(sender_email, email_password, message, receiver_email, subject)
        quit(2)

    # defines subject and message
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


# environmental variables

# esther login info
esther_username = os.environ.get("esther_username")
esther_password = os.environ.get("esther_password")
course_name = os.environ.get("course_name")

# email info
sender_email = os.environ.get("sender_email")
email_password = os.environ.get("email_password")
receiver_email = os.environ.get("receiver_email")

send_update_email(esther_username, esther_password, course_name, sender_email, email_password, receiver_email)
