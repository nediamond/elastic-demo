from elasticsearch import Elasticsearch

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
	return es.search(index=index, body=body)['hits']['hits']

def create_contact(newname):
	try:
		contact = get_contact(newname)
	# Want exception to be raised here, means name does not yet exist.
	except InvalidNameException: 
		body = {
					'name': newname
				}
		return es.create(index=index, doc_type="contact", body=body)
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

def put_contact(name, newname):
	contact = get_contact(name)
	body = {
				'name': newname
			}
	return es.index(index=index, doc_type="contact", id=contact['_id'], body=body)

def delete_contact(name):
	contact = get_contact(name)
	return  es.delete(index=index, doc_type='contact', id=contact['_id'])


class InvalidNameException(Exception):
    pass