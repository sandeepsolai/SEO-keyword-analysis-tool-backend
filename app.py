from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from collections import Counter
import requests
import re

app = Flask(__name__)

STOPWORDS = set([
    "the", "and", "to", "of", "a", "in", "is", "it", "on", "for", "with", 
    "as", "at", "by", "this", "that", "an", "be", "are"
])

def get_lines_with_word(text, word, position='prefix', limit=2):
    lines = text.lower().splitlines()
    matched = []
    for line in lines:
        if position == 'prefix' and line.strip().startswith(word):
            matched.append(line.strip())
        elif position == 'suffix' and line.strip().endswith(word):
            matched.append(line.strip())
        if len(matched) == limit:
            break
    return matched if matched else ["-----------"]

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        url = request.json.get("url")
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')

        for tag in soup(["script", "style"]):
            tag.extract()

        text = soup.get_text(separator=" ").lower()
        lines = soup.get_text(separator="\n")

        words = re.findall(r'\b[a-z]{2,}\b', text)
        words = [w for w in words if w not in STOPWORDS]
        freq_counter = Counter(words)
        top_words = freq_counter.most_common(5)

        result = []

        for word, count in top_words:
            prefix_examples = get_lines_with_word(lines, word, 'prefix')
            suffix_examples = get_lines_with_word(lines, word, 'suffix')

            result.append({
                "word": word,
                "count": count,
                "prefix": prefix_examples,
                "suffix": suffix_examples
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "✅ Word Analyzer API Running"

if __name__ == "__main__":
    app.run()
