import re

# Source: emailregex.com
EMAIL_REGEX = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

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
            if not (re.compile(r'^\d+$').match(phone) and len(phone) in [7,10,11]):
                raise ValueError("Invalid Phone Number")
            else:
                self.attrs['phone'] = phone
 
        if email:
            if not (re.compile(EMAIL_REGEX).match(email) and len(email) < 50): 
                raise ValueError("Invalid Email")
            else:
                self.attrs['email'] = email

    def __repr__(self):
        return repr(self.attrs)
