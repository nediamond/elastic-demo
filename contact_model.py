import re

# Source: emailregex.com
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

PHONE_REGEX = re.compile(r'^\d+$')

class ContactModel:
    def __init__(self, name, phone=None, email=None):
        self.attrs = {}

        if not name or len(name) > 40: 
                raise ValueError("Invalid Name")
        self.attrs['name'] = name
        self.name = name

        if phone:
            for c in '()-. +':
                phone = phone.replace(c, '')
            if not (PHONE_REGEX.match(phone) and len(phone) in [7,10,11]):
                raise ValueError("Invalid Phone Number")
            else:
                self.attrs['phone'] = phone
 
        if email:
            if not (EMAIL_REGEX.match(email) and len(email) < 50): 
                raise ValueError("Invalid Email")
            else:
                self.attrs['email'] = email

    def __repr__(self):
        return repr(self.attrs)
