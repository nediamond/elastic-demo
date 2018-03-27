from elasticsearch import Elasticsearch, NotFoundError

#Todo: config
es = Elasticsearch(
	['localhost'],
	scheme="http",
	port=9200
)
index = "contacts"

def get_contact_page(pageSize, page, query):
	body = {
				'from': int(page)*int(pageSize), 
				'size': pageSize,
				'query': {
					'query_string' : {
						'default_field' : '*',
						'query' : query
					}
				}
			}
	try:
		return es.search(index=index, body=body)['hits']['hits']
	except NotFoundError: # No contacts have been created yet.
		return []

def create_contact(contact):
	try:
		contact = get_contact(contact.name)
	# Want exception to be raised here, means name does not yet exist.
	except (NotFoundError, InvalidNameException): 
		return es.index(index=index, doc_type="contact", body=contact.attrs)
	raise InvalidNameException()

def get_contact(name):
	body = {
				'size': 1,
				'query': {
					'query_string' : {
						'default_field' : 'name',
						'query' : name
					}
				}
			}
	res = es.search(index=index, body=body)['hits']
	if res['total'] < 1:
		raise InvalidNameException()
	return res['hits'][0]

def put_contact(name, newcontact):
	contact = get_contact(name)
	for key in contact['_source']:
		if key not in newcontact.attrs:
			newcontact.attrs[key] = contact['_source'][key]
	return es.index(index=index, doc_type="contact", id=contact['_id'], body=newcontact.attrs)

def delete_contact(name):
	contact = get_contact(name)
	return  es.delete(index=index, doc_type='contact', id=contact['_id'])


class InvalidNameException(Exception):
    pass