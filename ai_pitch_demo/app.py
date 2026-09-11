from flask import Flask,jsonify,render_template,request
app=Flask(__name__)
SLIDES=[{'number':1,'title':'Problem','subtitle':'Students and health-data teams face fragmented information and limited time.','type':'Problem'},{'number':2,'title':'Users','subtitle':'University learners and operational reviewers who need clearer prioritization.','type':'Users'},{'number':3,'title':'Solution','subtitle':'Structured AI-ready workflows with transparent human control.','type':'Solution'},{'number':4,'title':'Prototype Demo','subtitle':'Show input → processing → insight → human review.','type':'Demo'},{'number':5,'title':'Risks & Responsible AI','subtitle':'Address privacy, hallucination, bias, transparency and oversight.','type':'Risks'}]
@app.get('/')
def index(): return render_template('index.html',project='P2',initial_data=SLIDES)
@app.post('/api/rehearse')
def rehearse():
 a=(request.get_json(silent=True)or{}).get('audience','review panel'); return jsonify({'opening':f'Hello {a}. This project shows how a real problem can move from data to an actionable, reviewable insight.','close':'The prototype is designed to support human judgment, not replace it; privacy, transparency and responsible use remain part of the solution.'})
if __name__=='__main__': app.run(debug=False,port=5012)
