import csv
import io
from collections import Counter, defaultdict
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
SAMPLE = [
 {'medicine':'CardioSafe','region':'North','stock':72,'demand':91,'sales':182,'quality':'Pass'},
 {'medicine':'CardioSafe','region':'South','stock':48,'demand':77,'sales':151,'quality':'Pass'},
 {'medicine':'GlucoRelief','region':'North','stock':34,'demand':88,'sales':169,'quality':'Pass'},
 {'medicine':'GlucoRelief','region':'East','stock':19,'demand':94,'sales':201,'quality':'Review'},
 {'medicine':'RespiraClear','region':'East','stock':64,'demand':53,'sales':98,'quality':'Pass'},
 {'medicine':'RespiraClear','region':'South','stock':27,'demand':67,'sales':127,'quality':'Pass'},
]

def analyze(rows):
    valid=[]
    for row in rows:
        try:
            valid.append({'medicine':str(row.get('medicine','')).strip(),'region':str(row.get('region','')).strip(),'stock':float(row.get('stock',0)),'demand':float(row.get('demand',0)),'sales':float(row.get('sales',0)),'quality':str(row.get('quality','Unknown')).strip()})
        except (TypeError, ValueError):
            continue
    medicine=defaultdict(lambda:{'stock':0,'demand':0,'sales':0,'count':0})
    for row in valid:
        item=medicine[row['medicine']]; item['stock']+=row['stock']; item['demand']+=row['demand']; item['sales']+=row['sales']; item['count']+=1
    products=[]
    for name, values in sorted(medicine.items()):
        risk=round(max(0, values['demand']-values['stock']),1)
        products.append({'medicine':name,'stock':round(values['stock'],1),'demand':round(values['demand'],1),'sales':round(values['sales'],1),'risk':risk,'coverage':round(values['stock']/values['demand']*100,1) if values['demand'] else 0})
    risk_items=sorted(products,key=lambda item:item['risk'],reverse=True)
    return {'rows':valid,'products':products,'summary':{'rows':len(valid),'medicines':len(products),'sales':round(sum(r['sales'] for r in valid),1),'at_risk':sum(1 for item in products if item['risk']>0),'quality_reviews':sum(1 for r in valid if r['quality'].lower()!='pass')},'insights':[f"{risk_items[0]['medicine']} has the largest projected supply gap ({risk_items[0]['risk']:.0f} units)." if risk_items and risk_items[0]['risk']>0 else 'No immediate supply gap detected.', f"{max(products,key=lambda item:item['sales'])['medicine']} leads the sample by sales." if products else 'Add a dataset to generate insights.', 'Review flagged quality records before using the dashboard for operational decisions.']}

@app.get('/')
def index(): return render_template('index.html', project='P1', initial_data=analyze(SAMPLE))

@app.get('/api/analysis')
def analysis(): return jsonify(analyze(SAMPLE))
@app.post('/api/analysis')
def upload_analysis():
    payload=request.get_json(silent=True) or {}; return jsonify(analyze(payload.get('rows') or SAMPLE))
@app.get('/api/risk-checklist')
def risk_checklist():
    return jsonify({'risks':[{'risk':'Data quality','mitigation':'Validate required columns and review skipped rows.'},{'risk':'Operational overreach','mitigation':'Treat supply gaps as review signals, not automatic actions.'},{'risk':'Domain misuse','mitigation':'Require qualified pharmaceutical and supply-chain review.'}]})

@app.get('/api/report')
def report_export():
    result=analyze(SAMPLE); result['report_title']='PharmaInsight AI operational review'; result['generated_for']='Educational capstone demonstration'; return jsonify(result)

@app.post('/api/analysis/csv')
def csv_analysis():
    uploaded=request.files.get('file')
    if not uploaded: return jsonify(error='Attach a CSV with medicine, region, stock, demand, sales, quality columns.'),400
    rows=list(csv.DictReader(io.StringIO(uploaded.read().decode('utf-8')))); return jsonify(analyze(rows))

if __name__ == '__main__': app.run(debug=False, port=5011)
