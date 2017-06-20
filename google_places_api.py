from googleplaces import GooglePlaces, types, lang
import json
import pprint

google_api_key = 'AIzaSyCzoYCtiRMpJKOm1Qi8xWrcds6na1vHv7I'

google_places = GooglePlaces(google_api_key)


query_result=google_places.text_search(query="chinese restaurant in surat")


if query_result.has_attributions:
    print query_result.html_attributions
	
for place in query_result.places:
    # Returned places from a query are place summaries.
    print place.name
    #print place.geo_location
    #print place.place_id

    # The following method has to make a further API call.
    place.get_details()
    #json.loads(place)
    # Referencing any of the attributes below, prior to making a call to
    # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    print place.details # A dict matching the JSON response from Google.
    #print place.local_phone_number
    #print place.international_phone_number
    #print place.website
    #print place.url