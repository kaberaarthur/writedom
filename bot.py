from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from cryptography.fernet import Fernet
from bs4 import BeautifulSoup
from datetime import date
import datetime
import time
import smtplib
import time
import requests
import random
import os
import socket

def test_connection():
    try:
        socket.create_connection(('Google.com', 80))
        return True
    except OSError:
        return False

def checker():
    num_file = open("num.txt", "r")
    number = str(num_file.read().rstrip("\n"))
    number = int(number)
    if number == 1:
        browser.close()

# Crypto Key
key = "HQKre9MwJLt8v2PmfaNYW9UP4_xKTsjjyuNAn4Y5_7w="

#######################
######  Trial #########
#######################
date_file = open("token.txt", "r")
expiry_date_str = str(date_file.read().rstrip("\n"))

# Decryt Expiry date
f = Fernet(key)
encoded = expiry_date_str.encode()
decrypted = f.decrypt(encoded)
decoded = decrypted.decode()
expiry_date_str = decoded
#print(decoded)

expiry_date = datetime.datetime.strptime(expiry_date_str, '%d/%m/%y')
current_date = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
current_date = datetime.datetime.strptime(current_date, '%y-%m-%d %H:%M:%S')


cwd = str(os.getcwd())
driver_path = cwd + "\chromedriver.exe"
driver_path = driver_path.replace(os.sep, '/')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')

browser = webdriver.Chrome(executable_path = driver_path, chrome_options = chrome_options)
browser.implicitly_wait(25)

# Security Guards
email_file = open("email.txt", "r")
email_encrypted = str(email_file.read().rstrip("\n"))
f = Fernet(key)
email_encrypted = email_encrypted.encode()
email_decrypted = f.decrypt(email_encrypted)
email_address = email_decrypted.decode()



# Sending Email credentials
sender_email = "arthurkabera@gmail.com"
rec_email = email_address
email_password = str("gE4jiApK5sCdBx4")
message = """\
Subject: Writedom Message

Hello, you have a new message from writedom, possibly a New Order."""


pass_file = open("password.txt", "r")
the_password = str(pass_file.read().rstrip("\n"))

time_file = open("time.txt", "r")
sleep_time = int(time_file.read().rstrip("\n"))

#Manual Scheduler
def run_kill():
    f = open("run_status.txt", "r")
    run_status = f.read()
    run_status = int(run_status)
    if run_status == 1:
        browser.quit()


count = 0
browser.get("https://writedom.com/dashboard")
browser.maximize_window()

while count == 0:
    # Check if it is time to quit
    run_kill()

    checker()
    if test_connection() == True:
        checker()
        browser.get("https://writedom.com/dashboard")
        another_url = browser.current_url
        if another_url == "https://writedom.com/dashboard/messages":
            # Send Email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, email_password)
            server.sendmail(sender_email, rec_email, message)
            break

    run_kill()

    if current_date > expiry_date:
        print("License Expired")
        time.sleep(100)
        browser.quit()


    if test_connection() == True:
        checker()                                   # /html/body/div[3]/div/div/div/div[1]/form/div[2]/input
                                                    # /html/body/div[3]/div/div/div/div[1]/form/div[2]/input
        email_input = browser.find_elements_by_xpath("/html/body/div[3]/div/div/div/div/form/div[2]/input")
        if len(email_input) > 0:
            email_input[0].send_keys(email_address)
            time.sleep(3)
            # No need to check input twice
                                                        #/html/body/div[3]/div/div/div/div[1]/form/div[3]/div[1]/input
            pass_input = browser.find_element_by_xpath("/html/body/div[3]/div/div/div/div/form/div[3]/div[1]/input")
            pass_input.send_keys(the_password)
            time.sleep(3)
            login_button = browser.find_element_by_xpath("/html/body/div[3]/div/div/div/div/form/div[5]/button/div/span")
            login_button.click()
            time.sleep(5)

    run_kill()
    # Append database items to a list - Must be in loop
    read_database = open("database.txt", "r")
    old_links = [link.rstrip('\n') for link in read_database]
    read_database.close()

    run_kill()
    orders = []

    curr_url = browser.current_url
    if curr_url == "https://writedom.com/dashboard/available-orders":
        order_links = browser.find_elements_by_xpath("/html/body/div[3]/div/div/div/div/div/main/div/div/div/div/div/div[1]/div[2]/table/tbody/tr/td[1]/div/a[1]")

        if len(order_links) > 0:
            for link in order_links:
                link = link.get_attribute("href")
                if link in old_links:
                    continue
                else:
                    orders.append(link)

    write_db = open("database.txt", "a+")


    run_kill()
    if len(orders) > 0:
        for order in orders:
            if test_connection() == True:
                checker()
                browser.get(order)
                time.sleep(sleep_time)
                # Check Deadline

                deadline_divs = browser.find_elements_by_xpath("/html/body/div[3]/div/div/div/div/div/main/div/div/div[1]/div[2]/div/div[3]")
                if len(deadline_divs) == 1:
                    deadline = browser.find_elements_by_xpath("/html/body/div[3]/div/div/div/div/div/main/div/div/div[1]/div[2]/div/div[3]/span[2]")
                    if len(deadline) > 0:
                        deadline = deadline[0].text
                        ddln_text = deadline

                        # Check if Deadline is in Hours or Days
                        if "min" in ddln_text:
                            # Check if deadline is in minutes
                            if "hour" in ddln_text:
                                # If Deadline is in Hours
                                ddln_text = ddln_text.replace("Deadline : ", "")
                                # Remove everything after "Hour"
                                ddln_text = ddln_text.split(' hour', 1)[0]
                                #ddln_text = ddln_text[:ddln_text.find(' hour')].strip()
                                ddln_text = int(ddln_text)

                        else:
                            # If Deadline is in Days
                            ddln_text = 24

                        user_deadline = open("deadline.txt", "r")
                        user_deadline = user_deadline.read()
                        user_deadline = int(user_deadline)

                        if ddln_text < user_deadline:
                            print("Short Deadline")
                        else:
                            # Selected Subjects
                            subjects = open("subjects.txt", "r")
                            subjects = [link.rstrip('\n') for link in subjects]
                            # Check if Order is Within Desired Subjects
                            order_subject = browser.find_elements_by_xpath("/html/body/div[3]/div/div/div/div/div/main/div/div/div[1]/div[3]/div[2]/div[1]/div/div[1]/div[2]/div")
                            order_subject = order_subject[0].text
                            order_subject = order_subject.replace("Subject: ", "")
                            if order_subject in subjects:
                                # Apply
                                apply_button = browser.find_elements_by_xpath("/html/body/div[3]/div/div/div/div/div/main/div/div/div[1]/div[2]/div/div[5]/div/div/button/div")
                                if len(apply_button) > 0:
                                    apply_button[0].click()
                                    write_db.write(str(order) + "\n")
                elif len(deadline_divs) == 1:
                    #changed
                    deadline = browser.find_elements_by_xpath("/html/body/div[3]/div/div/div/div/div/main/div/div/div[1]/div[2]/div/div[3]/span[2]")
                    if len(deadline) > 0:
                        deadline = deadline[0].text
                        ddln_text = deadline
                        # Check if Deadline is in Hours or Days
                        if "min" in ddln_text:
                            # Check if deadline is in minutes
                            if "hour" in ddln_text:
                                # If Deadline is in Hours
                                ddln_text = ddln_text.replace("Deadline : ", "")
                                # Remove everything after "Hour"
                                ddln_text = ddln_text.split(' hour', 1)[0]
                                #ddln_text = ddln_text[:ddln_text.find(' hour')].strip()
                                ddln_text = int(ddln_text)
                            else:
                                ddln_text = 0
                        else:
                            # If Deadline is in Days
                            ddln_text = 24

                        run_kill()
                        user_deadline = open("deadline.txt", "r")
                        user_deadline = user_deadline.read()
                        user_deadline = int(user_deadline)

                        try:
                            user_deadline = int(ddln_text)
                        except ValueError:
                            print("Short Deadline")
                        else:
                            if ddln_text < user_deadline:
                                print("Short Deadline")
                            else:
                                # Selected Subjects
                                subjects = open("subjects.txt", "r")
                                subjects = [link.rstrip('\n') for link in subjects]
                                # Check if Order is Within Desired Subjects
                                order_subject = browser.find_elements_by_xpath("/html/body/div[3]/div/div/div/div/div/main/div/div/div[1]/div[3]/div[2]/div[1]/div/div[1]/div[2]/div")
                                order_subject = order_subject[0].text
                                order_subject = order_subject.replace("Subject: ", "")
                                if order_subject in subjects:
                                    # Apply
                                    apply_button = browser.find_elements_by_xpath("/html/body/div[3]/div/div/div/div/div/main/div/div/div[1]/div[2]/div/div[5]/div/div/button/div")
                                    if len(apply_button) > 0:
                                        apply_button[0].click()
                                        write_db.write(str(order) + "\n")

    write_db.close()
    run_kill()

time.sleep(60)
browser.close()
