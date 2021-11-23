"""
Mailing list Manager that keep track of email address categorized into named groups. 
When it's time to send a message, we can pick a group and send the message to all email 
address assigned to that group. 

"""

import smtplib
from email.mime.text import MIMEText
from collections import defaultdict
from contextlib import suppress

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
    def __init__(self, data_file):
        self.data_file = data_file
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


    def save(self):
        with open(self.data_file, "w") as file:
            for email, groups in self.email_map.items():
                file.write("{} {}\n".format(email, ",".join(groups)))


    def load(self):
        self.email_map = defaultdict(set) 
        with suppress(IOError):
            with open(self.data_file) as file:
                for line in file:
                    email, groups = line.strip().split(" ")
                    groups = set(groups.split(","))
                    self.email_map[email] = groups
    

    def __enter__(self):
        self.load()
        return self 

    
    def __exit__(self, type, value, tb):
        self.save()