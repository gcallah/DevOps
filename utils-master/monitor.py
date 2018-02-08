"""
Very simple monitor to see if our servers are up.
"""

import sys
from html.parser import HTMLParser
import smtplib
import requests

HTTP_SUCCESS = "200"
SMTP_SERVER = 'smtp.mail.me.com'
PORT = 587
LOGIN_NAME = "gcallah@mac.com"
PASSWD = "jkhjkhjkhjkh"

url = ""

if len(sys.argv) < 2:
    print("Must supply server URL to check.")
    exit(ARG_ERROR)
else:
    url = sys.argv[1]

page = requests.get(url)
# if we need the content, it is in: page.content

if HTTP_SUCCESS not in str(page):
    print("Failed to fetch page.")
    server = smtplib.SMTP(SMTP_SERVER, PORT)
    server.connect(SMTP_SERVER, PORT)
    server.login(LOGIN_NAME, PASSWD)
    msg = "\nServer " + url + " failed to respond."
    server.sendmail(LOGIN_NAME, LOGIN_NAME, msg)
else:
    print("Page fetch successful.")
