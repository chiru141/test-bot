import os, sys
from flask import Flask, request
from pymessenger import Bot
from utils import *

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAADEBIVRjEIBAEfiwMcJXG2AHFyoHlNaCAwQbI9lBp8zZAVJ4npAeL4bQIYVmaJQK0H8Ogq8RccKqe3z9OwHCdrv8AiLbuXKcCeOYUIqOD65zZBvbmM7eZB06jwg2n9EZBGBgGZAOjKvCcFCI8q1UtpJk6YmO0hO9sY1xA0vp0AZDZD'
bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
		# Webhook verification
		if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
			if not request.args.get("hub.verify_token") == "hello":
				return "Verification token mismatch", 403
			return request.args["hub.challenge"], 200
		return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)
	
	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:
				
				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']
				
				if messaging_event.get('message'):
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'
					
					response = None
					entity,value = wit_response(messaging_text)
					
					if entity == "cuisine":
						response = "Oh i love {} too".format(str(value)) 
					elif entity == "establishments":
						response = "okay, let's find a {} for you".format(str(value))
						
					if response == None:
						response = "Sorry"
						
					# echo	
					#response = messaging_text
					
					
					bot.send_text_message(sender_id, response)
	
	
	return "ok", 200  
	
def log(message):
	print(message)
	sys.stdout.flush()
	
	
if __name__ == "_main_":
	app.run(debug = True, port = 5000)