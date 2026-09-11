import csv
from collections import defaultdict
from datetime import datetime
from flask import Flask,jsonify,render_template
app=Flask(__name__)
def analyze():
 rows=list(csv.DictReader(open('data/raw_sales.csv'))); missing=sum(1 for r in rows if not r['region']); monthly=defaultdict(float); product=defaultdict(float); region=defaultdict(float); cleaned=[]
 for r in rows:
  reg=r['region'] or 'Unknown'; month=r['date'][:7]; revenue=float(r['quantity'])*float(r['unit_price']); cleaned.append({**r,'region':reg,'month':month,'revenue':round(revenue,2)}); monthly[month]+=revenue; product[r['product']]+=revenue; region[reg]+=revenue
 return {'rows':cleaned,'quality':{'raw_rows':len(rows),'missing_found':missing,'rows_fixed':missing,'final_rows':len(cleaned)},'kpis':{'revenue':round(sum(monthly.values()),2),'transactions':len(cleaned),'units':sum(int(r['quantity']) for r in cleaned)},'monthly':sorted(monthly.items()),'top5':sorted(product.items(),key=lambda x:x[1],reverse=True)[:5],'regional':sorted(region.items(),key=lambda x:x[1],reverse=True)}
@app.get('/')
def index(): return render_template('index.html',project='P1',initial_data=analyze())
@app.get('/api/summary')
def summary(): return jsonify(analyze())
if __name__=='__main__': app.run(debug=False,port=5005)
