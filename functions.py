from wit import Wit
import requests
import json
from pprint import pprint

wit_access_token = "GPOOEJ2VHEGD5BA5C5EFZ3GZ4YYFTBZ2"
zomato_api_key="bdb3b7c195a74c2b0deefe4534c6a410"

URL_zomatoApi_param = "?apikey=bdb3b7c195a74c2b0deefe4534c6a410"

BasicURL = "https://developers.zomato.com/api/v2.1/"

def first_entity_value(entities, entity):
	if entity not in entities:
		return None
		
	val = entities[entity][0]["value"]
	if not val:
		return None
	return val["value"] if isinstance(val, dict) else val 

def send(request, response):
    print(response['text'])
	
def availableCuisines(request):
	context=request['context']
	URL_availCuisines = BasicURL + "cuisines" + URL_zomatoApi_param + "&city_id="+context['location_id']
	response = requests.get(URL_availCuisines)
	data=response.json()
	length=len(data['cuisines'])
	for i in range(0,length):
		print data['cuisines'][i]['cuisine']['cuisine_name']
		
	return context
		
		
def availableCategories(request):
	context=request['context']
	URL_availCategories = BasicURL + "categories" + URL_zomatoApi_param 
	response = requests.get(URL_availCategories)
	data=response.json()
	length=len(data['categories'])
	for i in range(0,length):
		print data['categories'][i]['categories']['name']
	
	return context
	
	
def setCuisine(request):
	print('entity : ',request['entities'])
	context=request['context']
	entities=request['entities']
	
	cuisine = first_entity_value(entities, "cuisine")
	URL_availCuisines = BasicURL + "cuisines" + URL_zomatoApi_param
	
	if 'location_id' in context:
		URL_availCuisines=URL_availCuisines	+ "&city_id="+context['location_id']
	else:
		print "Enter location:"
		setLocation(request)
	#try:
	#	URL_availCuisines=URL_availCuisines	+ "&city_id="+context['location_id']
	#except:
	#	print "Enter location"
	#	setLocation(request)
	#	pass
	
	response = requests.get(URL_availCuisines)
	data=response.json()
	length=len(data['cuisines'])
	
	flag=0
	for i in range(0,length):
		if data['cuisines'][i]['cuisine']['cuisine_name'].lower() == cuisine.lower():
			context['cuisine_name']=cuisine
			context['cuisine_id']=data['cuisines'][i]['cuisine']['cuisine_id']
			flag = 1
			break
	
	if flag != 1:
		print "cuisine doesn't exist in the location"
		
	return context
	
def setCategory(request):
	print('entity : ',request['entities'])
	context=request['context']
	entities=request['entities']
	
	category = first_entity_value(entities, "category")
	URL_availCategories = BasicURL + "categories" + URL_zomatoApi_param 
	response = requests.get(URL_availCategories)
	data=response.json()
	length=len(data['categories'])
	
	flag=0
	for i in range(0,length):
		if data['categories'][i]['categories']['name'].lower() == cuisine.lower():
			context['category_name']=category
			context['category_id']=data['categories'][i]['categories']['id']
			flag = 1
			break
	
	if flag != 1:
		print "category doesn't exist in the location"
		
	return context	
	
def availableEstablishments(request):
	context=request['context']
	URL_availEstablishments = BasicURL + "establishments" + URL_zomatoApi_param + "&city_id="+context['location_id']
	response = requests.get(URL_availEstablishments)
	data=response.json()
	length=len(data['establishments'])
	for i in range(0,length):
		print data['establishments'][i]['establishment']['name']
		
def setEstablishment(request):
	print('entity : ',request['entities'])
	context=request['context']
	entities=request['entities']
	
	establishment = first_entity_value(entities, "establishment")
	URL_availEstablishments = BasicURL + "establishments" + URL_zomatoApi_param + "&city_id="+context['location_id'] 
	response = requests.get(URL_availEstablishments)
	data=response.json()
	length=len(data['establishments'])
	
	flag=0
	for i in range(0,length):
		if data['establishments'][i]['establishment']['name'].lower() == cuisine.lower():
			context['establishment_name']=establishment
			context['establishment_id']=data['establishments'][i]['establishment']['id']
			flag = 1
			break
	
	if flag != 1:
		print "establishment doesn't exist in the location"
		
	return context	
		
def setLocation(request):
	print("received location from user ",request['entities'])
	context=request['context']
	entities=request['entities']
	location = first_entity_value(entities, "location")
	
	if location == "near me":
		getLocation()       # get user's location (Anna's module)
	
	URL_location = BasicURL + "locations?apikey=" + zomato_api_key 
	if 'location_id' in context:
		URL_location = URL_location + "&query=" + location
	response = requests.get(URL_location)
	data=response.json()
	
	context['city_id']= data['location_suggestions'][0]['city_id']
	context['location_lat']=data['location_suggestions'][0]['latitude']
	context['location_long']=data['location_suggestions'][0]['longitude']
	
	return context

def trending(request):
	context=request['context']
	city_id=context['city_id']
	
	URL_collection = BasicURL + "collections/" + URL_zomatoApi_param + "&city_id=" + city_id
	
	if 'location_lat' in context:
		location_lat = context['location_lat']
		URL_collection = URL_collection + "&lat=" + location_lat
	if 'location_long' in context:
		location_long = context['location_long']
		URL_collection = URL_collection + "&lon=" + location_long
	if 'count' in context:
		count = context['count']
		URL_collection = URL_collection + "&count=" + count
	
	response = requests.get(URL_collection)
	data=response.json()
	print data['collections'][0]['collection']['share_url']
	
	return context
	
def popularNearby(request):
	context=request['context']
	location_lat = context['location_lat']
	location_long = context['location_long']
	
	URL_geocode = BasicURL + "geocode/" + URL_zomatoApi_param + "&lat=" + location_lat + "&lon=" + location_long
	
	response = requests.get(URL_geocode)
	data=response.json()
	length = len(data['nearby_restaurants'])
	for i in range(0,length):
		print data['nearby_restaurants'][i]['restaurant']['name']
		print data['nearby_restaurants'][i]['restaurant']['location']['address']
	
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
		#print request['context']['cuisine']
		URL_findRestaurant = BasicURL + "search" + "?apikey=" + zomato_api_key + "&sort=rating&order=desc"
		context=request['context']
		
		
		if 'start' in context:
			URL_findRestaurant = URL_findRestaurant + "&start=" + context['start']
		if 'count' in context:
			URL_findRestaurant = URL_findRestaurant + "&count=" + context['count']
		if 'cuisine_id' in context:
			URL_findRestaurant = URL_findRestaurant + "&cuisines=" + context['cuisine_id']
		if 'city_id' in context:
			URL_findRestaurant = URL_findRestaurant + "&entity_id=" + context['city_id']
		if 'location_lat' in context:
			URL_findRestaurant = URL_findRestaurant + "&lat=" + context['location_lat']
		else:
			setLocation(request)
			URL_findRestaurant = URL_findRestaurant + "&lat=" + context['location_lat']
		if 'location_long' in context:
			URL_findRestaurant = URL_findRestaurant + "&lon=" + context['location_long']
		if 'establishment_id' in context:
			URL_findRestaurant = URL_findRestaurant + "&establishment_type=" + context['establishment_id']
		if 'category_id' in context:
			URL_findRestaurant = URL_findRestaurant + "&category=" + context['category_id']

		response = requests.get(URL_findRestaurant)
		#print response
		data=response.json()
		number = len(data['restaurants'])
		#print number
		for i in range(0,number):
			print(data['restaurants'][i]['restaurant']['name'].encode('utf-8'))
			print(data['restaurants'][i]['restaurant']['location']['address'].encod('utf-8'))
			print(data['restaurants'][i]['restaurant']['user_rating']['aggregate_rating'].encode('utf-8'))	



		
actions = {
    'send': send,
	'availableCuisines':availableCuisines,
	'setCuisine':setCuisine,
	'availableCategories':availableCategories,
	'setCategory':setCategory,
	'availableEstablishments':availableEstablishments,
	'setEstablishment':setEstablishment,
	'trending':trending,
	'popularNearby':popularNearby,
	'setLocation':setLocation,
	'fetchReview':fetchReview,
	'findRestaurant':findRestaurant
}
	
client = Wit(access_token = wit_access_token, actions=actions)
client.interactive()