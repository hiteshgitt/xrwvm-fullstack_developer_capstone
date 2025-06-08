# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# Mock data for testing
MOCK_DEALERS = [
    {
        "id": 1,
        "full_name": "Best Cars",
        "city": "New York",
        "address": "123 Main St",
        "zip": "10001",
        "state": "NY"
    },
    {
        "id": 2,
        "full_name": "Auto World",
        "city": "Los Angeles",
        "address": "456 Oak Ave",
        "zip": "90001",
        "state": "CA"
    },
    {
        "id": 3,
        "full_name": "Car City",
        "city": "Chicago",
        "address": "789 Pine St",
        "zip": "60601",
        "state": "IL"
    }
]

def get_request(endpoint, **kwargs):
    # For testing, return mock data
    if "fetchDealers" in endpoint:
        return MOCK_DEALERS
    
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        # If any error occurs
        print("Network exception occurred")
        return []

def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"sentiment": "neutral"}

def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")
        return {"status": "error"}
