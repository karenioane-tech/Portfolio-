import csv,statistics
from flask import Flask,jsonify,render_template,Response
app=Flask(__name__)
def data():
 rows=list(csv.DictReader(open('data/personal_diary.csv'))); cols=['sleep_hours','screen_hours','mood','steps','study_hours','water_litres']; missing=sum(1 for r in rows for c in cols if r[c]=='')
 avg={c:round(statistics.mean(float(r[c]) for r in rows),2) for c in cols}
 best=max(rows,key=lambda r:float(r['study_hours'])); low=min(rows,key=lambda r:float(r['mood']))
 return {'rows':rows,'quality':{'days_recorded':len(rows),'metrics':len(cols),'missing_values':missing,'status':'CLEAN'},'averages':avg,'insights':[f"Average sleep was {avg['sleep_hours']} hours per night.",f"The highest study time was {best['study_hours']} hours on {best['day']}.",f"The lowest mood score was {low['mood']}/10 on {low['day']}; this is descriptive and does not establish causation."]}
@app.get('/')
def index(): return render_template('index.html',project='P1',initial_data=data())
@app.get('/api/data')
def api_data(): return jsonify(data())
@app.get('/download')
def download():
 return Response(open('data/personal_diary.csv').read(),mimetype='text/csv',headers={'Content-Disposition':'attachment; filename=personal_diary_clean.csv'})
if __name__=='__main__': app.run(debug=False,port=5001)
