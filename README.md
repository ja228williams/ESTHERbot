# ESTHERbot
ESTHERbot has three tasks- checking course availability, checking waitlist position, and course auto-registration for classes at Rice University. The first two of these may be set up to be automated for updates on a weekly (or daily, hourly, etc.) basis. For best use, ESTHERbot can be set up to send update emails for these at any desired frequency. Descriptions of and instructions for utilization of any of these tasks, as well as editing the necessary settings and setting up update emails, can be found below.

## Download Requirements
* **Python**: install newest version for corresponding system (Windows/Linux/Mac) at https://www.python.org/downloads/
* **pip**: open your system's terminal / command prompt and type: 
  - <ins>For Windows:</ins> py -m ensurepip --upgrade
  - <ins>For Linux / MacOS:</ins> python -m ensurepip --upgrade
* **Python packages**: open your system's terminal / command prompt and type: 
  - pip install selenium
  - pip install webdriver_manager

## Setting Environmental Variables
<ins>For Windows:</ins> https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html

<ins>For Mac/Linux:</ins> https://www.youtube.com/watch?v=5iWhQWVXosU&ab_channel=CoreySchafer

## Automation
To 

## Course Availability Updates
check_availability.py 



## Waitlist Updates
check_waitlist.py 

## Sending Emails
send_email.py accesses the Gmail SMTP server, logs into the user's account and sends an email with a message and (optionally) a subject.

To set this up, choose the Gmail account you want to use, and turn on 2-step verification (at https://myaccount.google.com/u/0/security, and make sure the right user is selected). Then, select App Passwords, and generate a new app password (with App = "Other"- can give it any name, and choose the corresponding device for your computer). This will be the password your system will use to login to your email, and should be stored as an environmental variable under the name "email_password".

## Course Registration
NOTE: This task only currently functions for time periods during add/drop, and outside of the hour-long period each semester where 15-minute time periods are allotted to each group (freshmen/sophomores/etc.), as this form of the website includes an extra screen that's inaccessible outside of this time period that requires the last 6 digits of the student's ID to be entered- but stay tuned for updates in future semesters. 



## Course Code Dictionary
code_course_dict.py holds a dictionary mapping 4-letter codes to their corresponding departments (for example, 'COMP': 'Computer Science')  

<p>&nbsp;</p>

For any other questions/suggestions/issues, or help setting up email jaw15developer@gmail.com.
