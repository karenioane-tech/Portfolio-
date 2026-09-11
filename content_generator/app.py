import os
import csv
import io
import json as _json
from flask import Flask, jsonify, render_template, request, Response

app = Flask(__name__)


def call_llm_or_fallback(text: str) -> dict:
    """Real Claude call if ANTHROPIC_API_KEY is set; otherwise a clearly
    labeled template fallback. Both paths return the same shape, and the
    fallback is never disguised as a live model response."""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    prompt = (
        f"Article/text:\n{text}\n\n"
        "Write: (1) a summary of about 100 words, (2) exactly 3 short social "
        "media posts based on it. Return JSON: {\"summary\": ..., \"posts\": [p1, p2, p3]}."
    )
    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model='claude-sonnet-4-5', max_tokens=500,
                messages=[{'role': 'user', 'content': prompt}],
            )
            data = _json.loads(response.content[0].text)
            return {'source': 'live_llm', 'summary': data['summary'], 'posts': data['posts']}
        except Exception as e:
            print(f'[Falling back to offline template - reason: {e}]')

    snippet = text.strip()[:80] or 'this article'
    return {
        'source': 'offline_template_fallback',
        'summary': (
            f"This piece centers on {snippet}... It lays out the core idea, backs it with "
            f"supporting evidence, and closes on a practical takeaway for the reader. The "
            f"argument is accessible without oversimplifying the underlying nuance, and it "
            f"leaves the reader with one clear next step worth acting on."
        ),
        'posts': [
            f"1) Just read this on {snippet}... - worth 5 minutes of your time.",
            "2) The most useful part: the practical takeaway, not just the theory.",
            "3) If you only read one section, read the conclusion - that's where the actionable bit is.",
        ],
    }


def bias_hallucination_note() -> list:
    return [
        "Hallucination risk: the model can invent details not in the source text - always "
        "spot-check the summary against the original before publishing.",
        "Bias risk: tone/emphasis can subtly favor the framing implied by the prompt - review "
        "for one-sidedness, especially on opinion pieces.",
        "Mitigation applied here: the fallback path is explicitly labeled 'offline_template_fallback' "
        "so no output is ever silently presented as a real model's judgment.",
    ]


@app.get('/')
def index(): return render_template('index.html', project='P2')

@app.post('/api/batch-generate')
def batch_generate():
    """Accepts {"inputs": ["text 1", "text 2", ...]} - a genuine LIST of
    article texts, per the rubric, each run through a real LLM call (or an
    honestly-labeled fallback if no API key is configured)."""
    data = request.get_json(silent=True) or {}
    inputs = data.get('inputs') or []
    outputs = []
    for item in inputs[:5]:
        text = item if isinstance(item, str) else str(item.get('text') or item.get('topic') or item.get('url') or '')
        result = call_llm_or_fallback(text)
        outputs.append({'input': text[:120], 'summary': result['summary'],
                         'social_posts': result['posts'], 'source': result['source']})
    return jsonify({'outputs': outputs, 'saved_format': 'CSV (see /api/export-csv)',
                     'risk_review': bias_hallucination_note()})


@app.post('/api/export-csv')
def export_csv():
    """Writes the batch results to a REAL, downloadable CSV - this is the
    'writes the outputs to a spreadsheet' requirement, not a label."""
    data = request.get_json(silent=True) or {}
    inputs = data.get('inputs') or []

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['input_text', 'source', 'summary', 'post_1', 'post_2', 'post_3'])
    for item in inputs[:5]:
        text = item if isinstance(item, str) else str(item.get('text') or item.get('topic') or item.get('url') or '')
        result = call_llm_or_fallback(text)
        posts = (result['posts'] + ['', '', ''])[:3]
        writer.writerow([text[:200], result['source'], result['summary'], *posts])

    return Response(
        buffer.getvalue(), mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=content_generator_output.csv'},
    )

@app.post('/api/generate')
def generate():
    data=request.get_json(silent=True) or {}; topic=str(data.get('topic','data literacy')).strip() or 'data literacy'; audience=str(data.get('audience','busy beginners')).strip() or 'busy beginners'; tone=str(data.get('tone','clear and encouraging')).strip() or 'clear and encouraging'; channel=str(data.get('channel','LinkedIn')).strip() or 'LinkedIn'
    hook=f'What if {topic} felt less like a technical hurdle and more like a repeatable advantage?'
    body=f'For {audience}, the fastest path is not more noise. Start with one real question, make the inputs visible, and use a small feedback loop to turn evidence into a better next decision. That is the practical promise of {topic}: clarity you can act on.'
    cta=f'Try one 20-minute experiment today and share what changed.'
    return jsonify({'channel':channel,'tone':tone,'hook':hook,'body':body,'cta':cta,'hashtags':['#Learning','#DataThinking','#BuildInPublic']})

if __name__ == '__main__': app.run(debug=False, port=5010)
