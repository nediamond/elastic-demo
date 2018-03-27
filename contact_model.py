
class ContactModel:
	def __init__(self, name, phone=None, email=None):
		self.attrs = {}
		self.attrs['name'] = name
		self.name = name
		if phone:
			if len(phone) < 7 or len(phone) > 15:
				raise ValueError("Invalid Phone Number")
			else:
				self.attrs['phone'] = phone
 
		if email:
			if len(email) < 6 or len(email) > 35:
				raise ValueError("Invalid Email")
			else:
				self.attrs['email'] = email

	def __repr__(self):
		return repr(self.attrs)
