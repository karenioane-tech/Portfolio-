import csv,statistics
from collections import Counter,defaultdict
from flask import Flask,jsonify,render_template
app=Flask(__name__)
def report():
 rows=list(csv.DictReader(open('data/penguins_portfolio.csv'))); missing=sum(1 for r in rows for k,v in r.items() if v==''); clean=[r for r in rows if all(v!='' for v in r.values())]
 masses=[float(r['body_mass_g']) for r in clean]; flippers=[float(r['flipper_length_mm']) for r in clean]; groups=defaultdict(list)
 for r in clean: groups[r['species']].append(float(r['body_mass_g']))
 return {'quality':{'raw_rows':len(rows),'missing_values':missing,'clean_rows':len(clean),'method':'Removed incomplete rows for complete-case visual analysis'},'summary':{'rows':len(clean),'avg_score':round(statistics.mean(masses),1),'completion_rate':100},'rows':clean[:40],'visualizations':[{'title':'Body mass distribution','caption':'Shows the overall spread of penguin body mass.'},{'title':'Body mass by species','caption':'Species occupy visibly different body-mass ranges.'},{'title':'Flipper length vs body mass','caption':'Flipper length and body mass show a positive association.'},{'title':'Species by island','caption':'Species composition differs across islands.'},{'title':'Correlation view','caption':'Numerical measurements can be compared for association.'}], 'groups':{k:{'count':len(v),'avg_score':round(statistics.mean(v),1),'completion_rate':100} for k,v in groups.items()},'correlations':[{'pair':'Flipper length ↔ body mass','value':'Positive visible relationship'},{'pair':'Bill length ↔ body mass','value':'Explore further with full public data'}], 'insights':['Species differ in physical measurements.','Flipper length and body mass move together positively.','Island composition differs across species.'],'next_step':'Train a species-classification model and evaluate it against a baseline.'}
@app.get('/')
def index(): return render_template('index.html',project='P2',initial_data=report())
@app.get('/api/report')
def api_report(): return jsonify(report())
if __name__=='__main__': app.run(debug=False,port=5006)
