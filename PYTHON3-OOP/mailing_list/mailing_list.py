"""
Mailing list Manager that keep track of email address categorized into named groups. 
When it's time to send a message, we can pick a group and send the message to all email 
address assigned to that group. 

"""

import smtplib
from email.mime.text import MIMEText
from collections import defaultdict

def send_email(subject, message, from_addr, *to_addrs, host="localhost", port=1025, headers=None):
    headers = headers if headers else {}
    email = MIMEText(message) 
    email["Subject"] = subject 
    email["From"] = from_addr
    for header, value in headers.items(): # header is a dict
        email[header] =  value 
    sender = smtplib.SMTP(host, port) 
    for addr in to_addrs: # to_addrs is a list 
        del email["To"] 
        email["To"] = addr 
        sender.sendmail(from_addr, addr, email.as_string()) 
    sender.quit()


class MailingList:
    """Manage groups of e-mail addresses for sending e-mails."""
    def __init__(self):
        self.email_map = defaultdict(set)

    def add_to_group(self, email, group):
        self.email_map[email].add(group)

    def emails_in_groups(self, *groups):
        groups = set(groups) 
        emails = set() 
        for email, group in self.email_map.items():
            if group & groups: # can be group.intersection(groups)
                emails.add(email) 
        return emails 

    def send_mailing(self, subject, message, from_addr, *groups, headers=None):
        emails = self.emails_in_groups(*groups) 
        send_email(subject, message, from_addr, *emails, headers=headers)