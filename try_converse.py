from wit import Wit
import requests
import json
from pprint import pprint

wit_access_token = "GPOOEJ2VHEGD5BA5C5EFZ3GZ4YYFTBZ2"
zomato_api_key="bdb3b7c195a74c2b0deefe4534c6a410"

#google_api_key = 'AIzaSyCzoYCtiRMpJKOm1Qi8xWrcds6na1vHv7I'

#google_places = GooglePlaces(google_api_key)
context={}
def wit_response(sess_id,message_text,context):
	#resp = client.converse(sess_id,message_text,context)               
	context=client.run_actions(sess_id,message_text,context)
	print context
	return context 
	
	
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
	print('entity : ',request['entities'])
	context=request['context']
	entities=request['entities']
	
	cuisine = first_entity_value(entities, "cuisine")
	
	context['cuisine']=cuisine
	return context
	
	
def setLocation(request):
	print("received location from user ",request['entities'])
	context=request['context']
	entities=request['entities']
	location = first_entity_value(entities, "location")
	
	response_locationID = requests.get("https://developers.zomato.com/api/v2.1/cities?apikey=" + zomato_api_key + "&q="+location )
	data_city=response_locationID.json()
	context['location_id']= data_city['location_suggestions'][0]['id']
	#context['location_id']=location
	return context

def setPreference(request):
	print("received preference from user ",request['entities'])
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
		print("received from user ",request)
		print request['context']['cuisine']
		findRestaurantURL = "https://developers.zomato.com/api/v2.1/search?"
		URL_withAPI = findRestaurantURL + "apikey=" + zomato_api_key
		URL_withPAR = URL_withAPI + "&start=0" + "&count=10" + "&cuisines=" + request['context']['cuisine'] + "&sort=rating&entity_id=" + str(request['context']['location_id'])
		print URL_withPAR
		response = requests.get(URL_withPAR)
		#print response
		data=response.json()
		number = len(data['restaurants'])
		#print number
		for i in range(0,number):
			print(data['restaurants'][i]['restaurant']['name'])
			print(data['restaurants'][i]['restaurant']['location']['address'])
			print(data['restaurants'][i]['restaurant']['user_rating']['aggregate_rating'])	
			#print restaurant['address']
		#pprint(data)
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
	
client = Wit(access_token = wit_access_token, actions=actions)

#context={}
client.interactive()
#wit_response("6657","Hi",context)
#wit_response("6657","i want mexican",context)
#wit_response("6657","tell me fine dining restaurants near surat",context)
