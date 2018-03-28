import re

class ContactModel:
    def __init__(self, name, phone=None, email=None):
        self.attrs = {}
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
            # Would write (or find) regex with more time
            if len(email) < 6 or len(email) > 35: 
                raise ValueError("Invalid Email")
            else:
                self.attrs['email'] = email

    def __repr__(self):
        return repr(self.attrs)
