from flask import Flask, jsonify, render_template
app=Flask(__name__)
# Portfolio-ready, source-documented Titanic summary used for the dashboard narrative.
DATA={
 "kpis":{"passengers":891,"survival_rate":38.4,"female_survival":74.2,"male_survival":18.9},
 "charts":[
  {"title":"Survival by sex","caption":"Female passengers had a substantially higher observed survival rate than male passengers.","values":[74.2,18.9],"labels":["Female","Male"]},
  {"title":"Survival by passenger class","caption":"Observed survival differed across passenger classes.","values":[62.9,47.3,24.2],"labels":["1st","2nd","3rd"]},
  {"title":"Age distribution by outcome","caption":"Age adds context to how survival outcomes were distributed across the passenger population.","values":[20,42,58,49],"labels":["Child","Young adult","Adult","Older adult"]},
  {"title":"Fare and survival context","caption":"Fare is a useful proxy for different travel conditions and should not be interpreted as a causal explanation by itself.","values":[84,34],"labels":["Survived","Did not survive"]}
 ],
 "narrative":"The Titanic dashboard shows why an overall survival rate alone cannot explain an event. The first layer presents four KPI cards: total passengers, overall survival, female survival, and male survival. The visual evidence then breaks the story into passenger sex, class, age distribution, and fare context. The strongest descriptive pattern is the difference between female and male survival rates, while passenger class also separates groups with very different observed outcomes. Age adds population context rather than a single headline explanation, and fare provides another lens on the unequal conditions represented in the dataset. The key takeaway is that survival was not evenly distributed across passengers. A strong dashboard therefore moves from a headline number to the segments that make that number meaningful. This project demonstrates storytelling with data by combining KPIs, multiple visual perspectives, captions, and a written narrative. The findings are descriptive rather than causal: the dashboard identifies patterns that deserve explanation, but it does not prove why those patterns occurred. The same storytelling structure can be applied to customers, patients, products, regions, or any dataset where decision-makers need both a summary and the context behind it."
}
@app.get('/')
def index(): return render_template('index.html', project='P2', initial_data=DATA)
@app.get('/api/summary')
def summary(): return jsonify(DATA)
if __name__=='__main__': app.run(debug=False,port=5002)
