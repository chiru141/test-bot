from googleplaces import GooglePlaces, types, lang
import json
from pprint import pprint

google_api_key = 'AIzaSyCzoYCtiRMpJKOm1Qi8xWrcds6na1vHv7I'

google_places = GooglePlaces(google_api_key)


query_result=google_places.text_search(query="a fine dine restaurant",location='surat, gujarat')


if query_result.has_attributions:
    print query_result.html_attributions
	
#pprint (query_result.raw_response)
for place in query_result.places:
    print place.place_id
    print place.types
    print place.name
    place.get_details()
    print place.vicinity
    print place.local_phone_number
    print place.rating
	
	
	
#from location	