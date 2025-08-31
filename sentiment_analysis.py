import requests
import json

def sentiment_analyzer(text_to_analyse):
    """
    Analyzes sentiment and handles various success and error cases.
    """
    # Handle blank input to avoid an unnecessary API call
    if not text_to_analyse:
        return {'label': None, 'score': None}

    url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'
    myobj = { "raw_document": { "text": text_to_analyse } }
    header = {"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}
    
    try:
        response = requests.post(url, json=myobj, headers=header, timeout=10)
        
        # Handle different status codes from the API
        if response.status_code == 200:
            formatted_response = response.json()
            label = formatted_response['documentSentiment']['label']
            score = formatted_response['documentSentiment']['score']
            return {'label': label, 'score': score}
        else:
            # For any other error status (like 400, 404, 500), return None
            return {'label': None, 'score': None}
    except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError):
        # Handle network errors or cases where the response is not valid JSON
        return {'label': None, 'score': None}
