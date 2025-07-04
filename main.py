import os
import json
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from twilio.twiml.messaging_response import MessagingResponse
import azure.functions as func

# Azure Text Analytics setup
endpoint = os.getenv("https://prasarana-ws-incidentreport.cognitiveservices.azure.com/")
api_key = os.getenv("7FZAuhl9fzlWuLs17ct8P0MGYc9f6ag79zx5mW2g64etZSRHGbm7JQQJ99BFAC4f1cMXJ3w3AAAaACOG8Vd8")
client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

def analyze_sentiment(message):
    # Analyzing sentiment using Azure Text Analytics
    response = client.analyze_sentiment([message])
    sentiment = response[0].sentiment  # Sentiment can be 'positive', 'neutral', or 'negative'
    return sentiment

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Get the incoming message text from Twilio
    req_body = req.get_json()
    incoming_message = req_body.get('Body', '')

    # Process the message with Azure Text Analytics
    sentiment = analyze_sentiment(incoming_message)

    # Generate a response based on the sentiment
    if sentiment == 'positive':
        ai_response = "I'm glad you're happy with our service! How can I assist you further?"
    elif sentiment == 'negative':
        ai_response = "I'm sorry to hear you're unhappy. How can we improve?"
    else:
        ai_response = "Thank you for your message! How can I assist you?"

    # Create the Twilio response
    twilio_response = MessagingResponse()
    twilio_response.message(ai_response)

    return func.HttpResponse(str(twilio_response), mimetype="application/xml")
