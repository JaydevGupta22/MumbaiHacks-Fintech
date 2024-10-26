pip install requests

import requests

API_KEY = '73f7695eb3d341b8bea8b495aaef7deb'  # Replace with your NewsAPI key
url = f"https://newsapi.org/v2/everything?q=stock+market&sortBy=publishedAt&apiKey={API_KEY}"

response = requests.get(url)
news_data = response.json()

# Extract titles and descriptions of news articles
articles = [{'title': article['title'], 'description': article['description']} for article in news_data['articles']]

import spacy

# Load English tokenizer, tagger, parser, and NER
nlp = spacy.load("en_core_web_sm")

# Function to preprocess text (tokenization, removing stopwords, etc.)
def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

# Preprocess titles and descriptions
for article in articles:
    article['preprocessed_title'] = preprocess_text(article['title'])
    article['preprocessed_description'] = preprocess_text(article['description'] or "")


!pip install vaderSentiment

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to get sentiment scores
def analyze_sentiment(text):
    sentiment = analyzer.polarity_scores(text)
    return sentiment

# Apply sentiment analysis on titles and descriptions
for article in articles:
    title_sentiment = analyze_sentiment(article['preprocessed_title'])
    description_sentiment = analyze_sentiment(article['preprocessed_description'])

    # Store sentiment scores in the article data
    article['title_sentiment'] = title_sentiment
    article['description_sentiment'] = description_sentiment

# Function to extract named entities
def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Extract entities from titles and descriptions
for article in articles:
    article['title_entities'] = extract_entities(article['preprocessed_title'])
    article['description_entities'] = extract_entities(article['preprocessed_description'])


pip install transformers

from transformers import pipeline

# Load summarization model
summarizer = pipeline("summarization")

# Function to summarize text
def summarize_text(text):
    if len(text) > 50:
        return summarizer(text, max_length=50, min_length=25, do_sample=False)[0]['summary_text']
    return text

# Summarize descriptions
for article in articles:
    article['summary'] = summarize_text(article['preprocessed_description'])

for article in articles:
    print(f"Title: {article['title']}")
    print(f"Sentiment: {article['title_sentiment']}")
    print(f"Entities: {article['title_entities']}")
    print(f"Summary: {article.get('summary', article['description'])}")
    print("\n")


