import os
import re
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from send_email import send_email

# FALL SEMESTER CODE = 202310- CHANGE FOR FUTURE SEMESTERS
# can access at https://esther.rice.edu/selfserve/bwskfshd.P_CrseSchdDetl under <select> element of html code
# with id = "term_id"
semester_code = "202310"

def clean_schedule_text(strs):
    """
    Reformats the string representing information about the classes into a tuple of strings

    :param strs: list of strings representing the raw text from ESTHER describing the classes

    :return: tuple of waitlisted classes w/info (in form of strings)
    """
    # builds list of courses
    courses = []
    course = ""
    for str in strs:
        # splits if str is the title line of the course
        if re.search(' - [A-Z]{4} [0-9]{3} - [0-9]{3}', str):
            courses.append(course)
            course = str
        else:
            course += str
    courses.append(course)

    # constructs list of waitlisted courses from courses found from strs
    waitlisted_courses = []
    for course in courses:
        if 'Waitlist' in course:
            course_info = []
            course_str_rows = course.split('\n')
            course_info.append(course_str_rows[0])
            for txt in course_str_rows:
                # only adds important lines from the course description
                if 'Waitlist' in txt or 'Assigned Instructor' in txt or ' am ' in txt or ' pm ' in txt:
                    course_info.append(txt)
            # removes less relevant words from final line
            try:
                loc = course_info[len(course_info)-1].rindex('20') + 4
                course_info[len(course_info)-1] = course_info[len(course_info)-1][:loc]
            except:
                pass
            waitlisted_courses.append("\n".join(course_info))

    return waitlisted_courses


def check_waitlist(username, password):
    """
    Checks ESTHER for information on waitlisted courses, including waitlist position. Prints and returns a list of
    strings describing currently waitlisted courses.

    :param username: ESTHER username (student ID of form SXXXXXXXX)
    :param password: ESTHER password

    :return: list of strings describing currently waitlisted courses
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    orig_url = "https://esther.rice.edu/selfserve/twbkwbis.P_WWWLogin"
    driver.get(orig_url)

    # accesses login page
    print("logging in...")
    user_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "UserID")))
    user_box.send_keys(username)
    password_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "PIN")))
    password_box.send_keys(password)
    login = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[@class='pagebodydiv']/form/p/input[1]")))
    login.click()

    # accesses student detail schedule
    print("navigating to student detail schedule...")
    driver.get("https://esther.rice.edu/selfserve/bwskfshd.P_CrseSchdDetl")

    # selects term
    print("selecting term...\n")
    term_select = Select(WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "term_id"))))
    term_select.select_by_value(semester_code)
    term_submit = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[@class='pagebodydiv']/form/input[1]"))
    )
    term_submit.click()

    # iterates through tables representing courses
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
    """
    Sends an update email for waitlisted courses for the given account.

    :param username: ESTHER username (student ID of form SXXXXXXXX)
    :param password: ESTHER password
    :param sender_email: Name of the email account being used to send the update email.
    :param email_password: Password for the email account being used to send the update email.
    :param receiver_email: Name of the email account receiving the update email.
    """
    # calls check_waitlist method and handles relevant errors if necessary
    try:
        message = "\n\n".join(check_waitlist(username, password))
        subject = "Waitlisted Courses Update"
    except:
        # if error is encountered in check_waitlist method, then the email includes the error's traceback.
        message = "Error accessing class information from ESTHER.\n\n" + str(traceback.format_exc())
        print(message)
        subject = "Error accessing ESTHER"

    # sends an email and handles relevant errors if necessary
    try:
        send_email(sender_email, email_password, message, receiver_email, subject)
    except:
        print("Failed to send email.")
        print(traceback.format_exc())


# environmental variables

# esther info
esther_username = os.environ.get("esther_username")
esther_password = os.environ.get("esther_password")

# email info
sender_email = os.environ.get("sender_email")
email_password = os.environ.get("email_password")
receiver_email = os.environ.get("receiver_email")

send_update_email(esther_username, esther_password, sender_email, email_password, receiver_email)
