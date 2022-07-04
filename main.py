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
from register_classes import register_classes

############################################################
my_netid = ""
my_username = ""
my_password = ""
crn_list = ["10668", "14256"]


def main():
    # register_classes()
    print("main function not yet supported")


if __name__ == "__main__":
    # input_username = input("student id = ")
    # input_password = input("password = ")
    # input_netid = input("netid = ")
    input_username = my_username
    input_password = my_password
    input_netid = my_netid
    crn_list = crn_list
    register_classes(input_username, input_password, input_netid, crn_list)


# potential bugs / issues:
# 1) current term button from drop-down may change by semester
# 2) other notifications may need to be handled
# 3) need to check that urls / formatting isn't specific to user
# 4)
