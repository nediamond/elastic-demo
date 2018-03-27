from flask import Flask, request
import json
from contact_manager import (get_contact_page, 
							 create_contact, 
							 get_contact, 
							 put_contact, 
							 delete_contact,
							 InvalidNameException)
from contact_model import ContactModel

app = Flask(__name__)


@app.route('/contact',  methods = ['GET', 'POST'])
def contact():
	print request.method
	if request.method == "GET":
		kwargs = {
			'pageSize': request.values.get('pageSize', 25), 
			'page': request.values.get('page', 0), 
			'query': request.values.get('query', '*'),
		}
		return json.dumps(get_contact_page(**kwargs))
	elif request.method == "POST":
		try:
			contact = ContactModel(request.values['name'], 
								   request.values.get('phone'), 
								   request.values.get('email'))
			return json.dumps(create_contact(contact))
		except (KeyError, InvalidNameException, ValueError):
			return ('Bad Request', 400)



@app.route('/contact/<name>',  methods = ['GET', 'PUT', 'DELETE'])
def contact_name(name):
	try:
		if request.method == "GET":
			return json.dumps(get_contact(name))
		elif request.method == "PUT":
			try:
				newcontact = ContactModel(request.values.get('name', name), 
									   	  request.values.get('phone'), 
									   	  request.values.get('email'))
				return json.dumps(put_contact(name, newcontact))	
			except ValueError:
				return ('Bad Request', 400)
		elif request.method == "DELETE":
			return json.dumps(delete_contact(name))
	except InvalidNameException:
		return ('Bad Request', 400)


if __name__ == "__main__":
	app.run()