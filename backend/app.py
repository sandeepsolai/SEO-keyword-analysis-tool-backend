from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        return ""

def extract_prefix_suffix(word, sentences):
    prefixes = []
    suffixes = []
    for sentence in sentences:
        if word in sentence:
            words = sentence.split()
            for i, w in enumerate(words):
                if w == word:
                    if i > 0:
                        prefixes.append(words[i-1] + " " + word)
                    if i < len(words) - 1:
                        suffixes.append(word + " " + words[i+1])
    return prefixes, suffixes

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url')
    top_n = data.get('top_n', 5)

    text = fetch_text_from_url(url)
    sentences = re.split(r'[.!?]', text)
    words = re.findall(r'\b\w+\b', text.lower())
    count = Counter(words)
    most_common = count.most_common(top_n)

    result = []
    for word, freq in most_common:
        prefixes, suffixes = extract_prefix_suffix(word, sentences)
        result.append({
            'word': word,
            'count': freq,
            'prefix': prefixes[:3],
            'suffix': suffixes[:3]
        })

    return jsonify(result)

@app.route('/', methods=['GET'])
def home():
    return 'SEO Keyword Analyzer Backend Running', 200
