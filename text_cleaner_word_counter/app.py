import re
from collections import Counter

STOPWORDS = {'the','a','an','and','or','but','to','of','in','on','for','is','it','this','that','with','as','at','by','from'}
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html', project='P2')


@app.post('/api/analyze')
def analyze():
    data = request.get_json(silent=True) or {}
    text = str(data.get('text', ''))
    cleaned = text
    if data.get('lowercase', True): cleaned = cleaned.lower()
    if data.get('remove_punctuation', True): cleaned = re.sub(r'[^\w\s]', '', cleaned)
    if data.get('collapse_spaces', True): cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    words = re.findall(r"[\w']+", cleaned)
    filtered_words = [word for word in words if word not in STOPWORDS]
    counts = Counter(filtered_words)
    return jsonify({'cleaned': cleaned, 'characters': len(cleaned), 'words': len(words), 'sentences': len([item for item in re.split(r'[.!?]+', text) if item.strip()]), 'reading_minutes': round(len(words) / 220, 1), 'top_words': counts.most_common(10), 'stopwords_removed': len(words) - len(filtered_words), 'frequency_chart': [{'word': word, 'count': count} for word, count in counts.most_common(10)]})

if __name__ == '__main__':
    app.run(debug=False, port=5004)
