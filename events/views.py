from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slackclient import SlackClient

# Retreive token saved in slack/settings.py
SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings,'SLACK_BOT_USER_TOKEN', None)

# Create a SlackClient instance to post bot response to Slack
Client = SlackClient(SLACK_BOT_USER_TOKEN)

# Create an API endpoint for Slack to send event messages 
# Define an APIView with Django Rest Framework to handle POST request
class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        # To validate if incomming request was from Slack
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        # if url verification: respond OK with challenge value
        if slack_message.get('type') == 'url_verification':        
            return Response(data=slack_message, status=status.HTTP_200_OK)

        # GoUnix Bot
        if 'event' in slack_message:
            event_message = slack_message.get('event')

            # respond OK if it's bot's own message (ignore)
            if event_message.get('subtype') == 'bot_message':
                return Response(status=status.HTTP_200_OK)

            # process user's message
            user = event_message.get('user')
            text = event_message.get('text')
            channel = event_message.get('channel')
            bot_text = 'Hi <@{}> :wave: I am the GoUnix :robot_face: who is here to help you fall in :heart: with UNIX. Are you ready for a Unix challenge or do you have any question about Unix :grinning:?'.format(user) 
            if 'unix' in text.lower():
                # Bot post message to the channel
                Client.api_call(method='chat.postMessage', channel=channel,
                text=bot_text)
                return Response(status=status.HTTP_200_OK)

        
        return Response(status=status.HTTP_200_OK)
