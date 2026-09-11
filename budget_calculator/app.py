from flask import Flask, jsonify, render_template, request
from collections import defaultdict
app=Flask(__name__)
EXPENSES=[]
@app.get('/')
def index(): return render_template('index.html', project='P1')
@app.get('/api/expenses')
def expenses():
    totals=defaultdict(float)
    for e in EXPENSES: totals[e['category']]+=e['amount']
    threshold=float(request.args.get('threshold',5000))
    warnings=[f"{c} exceeded the KSh {threshold:,.0f} threshold: KSh {v:,.0f}" for c,v in totals.items() if v>threshold]
    return jsonify({'expenses':EXPENSES,'totals':dict(totals),'grand_total':round(sum(totals.values()),2),'warnings':warnings})
@app.post('/api/expenses')
def add_expense():
    d=request.get_json(silent=True) or {}; amount=max(float(d.get('amount',0)),0); category=str(d.get('category','Other')).strip() or 'Other'; dt=str(d.get('date',''))
    if amount<=0 or not dt: return jsonify({'error':'Enter a positive amount and date.'}),400
    EXPENSES.append({'id':len(EXPENSES)+1,'amount':round(amount,2),'category':category,'date':dt})
    return jsonify({'ok':True})
@app.post('/api/reset')
def reset():
    EXPENSES.clear(); return jsonify({'ok':True})
if __name__=='__main__': app.run(debug=False,port=5003)
