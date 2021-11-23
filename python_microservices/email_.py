from datetime import datetime
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from email.utils import format_datetime


def render_email_(**data):
    template = Jinja2Templates(directory="templates")
    return template.TemplateResponse("email_template.html", **data)


def render_email(**data):
    with open('templates/email_template.eml') as f:
        template = Template(f.read())
    return template.render(**data)


data = {
    'date': format_datetime(datetime.now()),
    'to': 'bob@example.com',
    'from': 'tarek@ziade.org',
    'subject': "Your Tarek's Burger order",
    'name': 'Bob',
    'items': [{'name': 'Cheeseburger', 'price': 4.5},
    {'name': 'Fries', 'price': 2.},
    {'name': 'Root Beer', 'price': 3.}]}

print(render_email(**data))