''' Executing this function initiates the application of sentiment
    analysis to be executed over the Flask channel and deployed on
    localhost:5000.
'''
from flask import Flask, render_template, request
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

app = Flask("Sentiment Analyzer")

@app.route("/sentimentAnalyzer")
def sent_analyzer():
    ''' This code receives the text from the HTML interface and 
        runs sentiment analysis over it using sentiment_analysis()
        function. The output returned shows the label and its confidence 
        score for the provided text.
    '''
    text_to_analyze = request.args.get('textToAnalyze')
    
    # Handle the special case for blank input
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid input: The text field cannot be blank."

    response = sentiment_analyzer(text_to_analyze)

    # Handle cases where the analyzer failed (e.g., invalid text, API error)
    if response is None or response.get('label') is None:
        return "Invalid text! Please try again with valid English text."

    label = response['label']
    score = response['score']

    try:
        sentiment = label.split('_')[1]
    except (IndexError, AttributeError):
        return f"Error: Could not parse the sentiment label '{label}'."

    return f"The given text has been identified as {sentiment} with a score of {score}."


@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    # This function executes the flask app and deploys it on localhost:5000.
    # The debug=True parameter enables the interactive debugger and reloader,
    # which is very useful during development.
    app.run(host="0.0.0.0", port=5000, debug=True)
