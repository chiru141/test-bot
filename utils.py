from wit import Wit

wit_access_token = "GPOOEJ2VHEGD5BA5C5EFZ3GZ4YYFTBZ2"


def wit_response(message_text):
	resp = client.message(message_text)               
	entity = None
	value = None 
	
	try:
		entity = list(resp['entities'])[0]                     #why 0 ? 
		value = resp['entities'][entity][0]['value']
	except:
		pass	
	return(entity, value)
	
	
def first_entity_value(entities, entity):
	if entity not in entities:
		return None
		
	val = entities[entity][0]["value"]
	if not val:
		return None
	return val["value"] if isinstance(val, dict) else val 

def send(request, response):
    print(response['text'])
	
def setCuisine(request):
	#print('entity : ',request['entities'])
	context=request['context']
	entities=request['entities']
	
	cuisine = first_entity_value(entities, "cuisine")
	
	context['cuisine']=cuisine
	return context
	
	
def setLocation(request):
	#print("received location from user ",request['entities'])
	context=request['context']
	entities=request['entities']
	location = first_entity_value(entities, "location")
	
	context['location']=location
	return context

def setPreference(request):
	#print("received preference from user ",request['entities'])
	context=request['context']
	entities=request['entities']
	
	preference = first_entity_value(entities, 'preference')
		
	context['preference']=preference
	return context
	
def fetchReview(request):
	print("received from user ",request['text'])
	context=request['context']
	entities=request['entities']
	
	preference = first_entity_value(entities, 'restaurant_name')
		
	context['restaurant_name']=restaurant_name
	return context
		
def findRestaurant(request): 
		print("received from user ",request['entities'])
		
#def my_action(request):
 #   print('Received from user...', request['text'])


		
actions = {
    'send': send,
	'setCuisine':setCuisine,
   # 'my_action': my_action,
	'setLocation':setLocation,
	'setPreference':setPreference,
	'fetchReview':fetchReview,
	'findRestaurant':findRestaurant
}
	
client = Wit(access_token = wit_access_token)