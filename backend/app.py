from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Common English stopwords to ignore (you can add more as needed)
STOPWORDS = {
    'the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'on', 'with', 'as', 'by',
    'at', 'an', 'be', 'this', 'that', 'from', 'or', 'are', 'it', 'was', 'but',
    'not', 'have', 'has', 'they', 'you', 'we', 'he', 'she', 'his', 'her', 'them',
    'their', 'which', 'will', 'can', 'all', 'do', 'if', 'so', 'about', 'what',
    'when', 'where', 'who', 'how', 'why', 'may', 'also', 'than', 'these', 'such',
    'there', 'some', 'no', 'into', 'more', 'up', 'out', 'would', 'should', 'could',
    'each', 'other', 'only', 'any', 'like', 'over', 'after', 'before', 'most',
    'just', 'get', 'because', 'then', 'now', 'very'
}

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

    # Filter out stopwords
    filtered_words = [w for w in words if w not in STOPWORDS and len(w) > 2]

    count = Counter(filtered_words)
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
