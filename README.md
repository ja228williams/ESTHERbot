# ESTHERbot
ESTHERbot has three tasks- checking course availability, checking waitlist position, and course auto-registration for classes at Rice University. The first two of these may be set up to be automated for updates on a weekly (or daily, hourly, etc.) basis. For best use, ESTHERbot can be set up to send update emails for these at any desired frequency. Descriptions of and instructions for utilization of any of these tasks, as well as editing the necessary settings and setting up update emails, can be found below.

## Course Availability Updates
check_availability.py 

### Setting Environmental Variables:
Windows: https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html

Mac/Linux: https://www.youtube.com/watch?v=5iWhQWVXosU&ab_channel=CoreySchafer

## Waitlist Updates
check_waitlist.py 

## Sending Emails
send_email.py accesses the Gmail SMTP server, logs into the user's account and sends an email with a message and (optionally) a subject.

To set this up, 

## Course Registration
NOTE: This task only currently functions for time periods during add/drop, and outside of the hour-long period each semester where 15-minute time periods are allotted to each group (freshmen/sophomores/etc.), as this form of the website includes an extra screen that's inaccessible outside of this time period that requires the last 6 digits of the student's ID to be entered- but stay tuned for updates in future semesters. 

## Course Code Dictionary
code_course_dict.py holds a dictionary mapping 4-letter codes to their corresponding departments (for example, 'COMP': 'Computer Science')  

### _________________________________________________________________________________________________________________________
For any other questions/suggestions/issues, email jaw15developer@gmail.com.
