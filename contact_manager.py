from elasticsearch import Elasticsearch, NotFoundError
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini')

es = Elasticsearch(
    [config['ElasticSearch']['Host']],
    scheme='http',
    port=int(config['ElasticSearch']['Port'])
)
index = config['ElasticSearch']['Index']

def get_contact_page(pageSize, page, query):
    if pageSize < 0 or page < 0 or pageSize*page+pageSize > 10000:
        return []
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
        res = es.search(index=index, body=body)['hits']['hits']
        return [hit['_source'] for hit in res]
    except NotFoundError: # No contacts have been created yet.
        return []

def create_contact(contact):
    try:
        contact = _get_contact(contact.name)
    # Want exception to be raised here, means name does not yet exist.
    except (NotFoundError, InvalidNameException): 
        res = es.index(index=index, doc_type="contact", body=contact.attrs)
        if res['result'] == 'created':
            return contact.attrs
        else:
            raise ContactCreationError
    raise InvalidNameException

def _get_contact(name):
    time.sleep(1) # Deals with latency/race condition type issues.
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
        raise InvalidNameException
    return res['hits'][0]

def get_contact(name):
    return _get_contact(name)['_source']

def put_contact(name, newcontact):
    contact = _get_contact(name)
    for key in contact['_source']:
        if key not in newcontact.attrs:
            newcontact.attrs[key] = contact['_source'][key]

    res = es.index(index=index, doc_type="contact", 
                   id=contact['_id'], body=newcontact.attrs)
    if res['result'] == 'updated':
        return newcontact.attrs
    else:
        raise ContactUpdateError

def delete_contact(name):
    contact = _get_contact(name)
    res = es.delete(index=index, doc_type='contact', id=contact['_id'])
    if res['result'] == 'deleted':
        return contact['_source']
    else:
        raise ContactDeletionError

class InvalidNameException(Exception):
    pass
class ContactCreationError(Exception):
    pass
class ContactUpdateError(Exception):
    pass
class ContactDeletionError(Exception):
    pass