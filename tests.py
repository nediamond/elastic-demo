import unittest

from contact_model import ContactModel
from contact_manager import *

class TestContactModel(unittest.TestCase):
	def test_phone_cleaning(self):
		mod = ContactModel('a', phone='(123)-456-7890')
		self.assertEqual(mod.attrs['phone'], '1234567890')

		mod = ContactModel('a', phone='+1(123).456.7890')
		self.assertEqual(mod.attrs['phone'], '11234567890')

		mod = ContactModel('a', phone='456 7890')
		self.assertEqual(mod.attrs['phone'], '4567890')

	def test_phone_validation(self):
		with self.assertRaises(ValueError):
			mod = ContactModel('a', phone='(123)-456-7890-1234')

		with self.assertRaises(ValueError):
			mod = ContactModel('a', phone='(123)-456')

		with self.assertRaises(ValueError):
			mod = ContactModel('a', phone='1')

		with self.assertRaises(ValueError):
			mod = ContactModel('a', phone='abc')

		with self.assertRaises(ValueError):
			mod = ContactModel('a', phone='123456789012')

		with self.assertRaises(ValueError):
			mod = ContactModel('a', phone='a234567890')

		with self.assertRaises(ValueError):
			mod = ContactModel('a', phone='(123)-456-7890a')

		with self.assertRaises(ValueError):
			mod = ContactModel('a', phone='(123)-45a6-7890')

	def test_email_validation(self):
		with self.assertRaises(ValueError):
			mod = ContactModel('a', email='a')

		with self.assertRaises(ValueError):
			mod = ContactModel('a', email='12345')

		with self.assertRaises(ValueError):
			mod = ContactModel('a', email='abcdefghijklmopqrstuvwzyz@abcdefghijklmopqrstuvwzyz.abcdefghijklmopqrstuvwzyz')

		mod = ContactModel('a', email='rand.user@gmail.com')
		self.assertEqual(mod.attrs['email'], 'rand.user@gmail.com')


class TestContactManager(unittest.TestCase):	
	def test_get_contact_page(self):
		self.pam = ContactModel('Pam', email='pam@dundermifflin.com', phone='123-456-7890')
		try:
			create_contact(self.pam)
		except InvalidNameException:
			delete_contact('Pam')
			create_contact(self.pam)

		self.jim = ContactModel('Jim', email='tuna@dundermifflin.com', phone='(123)-456-7890')
		try:
			create_contact(self.jim)
		except InvalidNameException:
			delete_contact('Jim')
			create_contact(self.jim)

		self.dwight = ContactModel('Dwight', email='shrute@dundermifflin.com', phone='+1(123)456-7890')
		try:
			create_contact(self.dwight)
		except InvalidNameException:
			delete_contact('Dwight')
			create_contact(self.dwight)

		self.michael = ContactModel('Michael', email='boss@dundermifflin.com', phone='1234567')
		try:
			create_contact(self.michael)
		except InvalidNameException:
			delete_contact('Michael')
			create_contact(self.michael)

		time.sleep(2)

		self.assertEqual(get_contact_page(-1,20,'*'), [])
		self.assertEqual(get_contact_page(20,-1,'*'), [])

		self.assertEqual(get_contact_page(25,100,'*'), [])
		self.assertEqual(get_contact_page(25,100000000000,'*'), [])


		page = get_contact_page(25,0,'*')
		self.assertIn(self.pam.attrs, page)
		self.assertIn(self.jim.attrs, page)
		self.assertIn(self.dwight.attrs, page)
		self.assertIn(self.michael.attrs, page)

		self.assertTrue(len(get_contact_page(1,0,'*')) == 1)
		self.assertTrue(len(get_contact_page(3,0,'*')) == 3)
		self.assertTrue(len(get_contact_page(2,1,'*')) == 2)

		for x in ['Jim','Pam','Michael','Dwight']: 
			delete_contact(x)

	def test_contact_CRUD(self):
		self.pam = ContactModel('Pam', email='pam@dundermifflin.com', phone='123-456-7890')
		try:
			create_contact(self.pam)
		except InvalidNameException:
			pass

		with self.assertRaises(InvalidNameException):
			mod = ContactModel('Pam', email='pam@dundermifflin.com', phone='123-456-7890')
			create_contact(mod)

		karen = ContactModel('Karen', email='karen@dundermifflin.com', phone='123-456-7890')
		self.assertEqual(create_contact(karen), karen.attrs)

		self.assertEqual(get_contact('Karen'), karen.attrs)
		self.assertEqual(delete_contact('Karen'), karen.attrs)
		with self.assertRaises(InvalidNameException):
			delete_contact('Karen')

		self.assertEqual(put_contact('Pam', karen), karen.attrs)
		self.assertEqual(get_contact('Karen'), karen.attrs)
		with self.assertRaises(InvalidNameException):
			get_contact('Pam')

		self.assertEqual(put_contact('Karen', self.pam), self.pam.attrs)
		self.assertEqual(get_contact('Pam'), self.pam.attrs)
		with self.assertRaises(InvalidNameException):
			get_contact('Karen')

		delete_contact('Pam')

if __name__ == '__main__':
	unittest.main()