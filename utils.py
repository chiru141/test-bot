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
	
	
client = Wit(access_token = wit_access_token, actions=actions)