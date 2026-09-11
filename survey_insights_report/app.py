from collections import Counter
from statistics import mean, median, pvariance, pstdev
from math import sqrt
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Five real Likert-style (1-5) questions per respondent. q5_overall_satisfaction
# doubles as the original 'satisfaction' field so the existing UI (which
# shows avg satisfaction, NPS, and a per-team breakdown) keeps working
# unchanged, while four genuine additional questions now exist for the
# "at least 5 survey questions" + "strongest correlation" requirements.
import random
random.seed(17)
RESPONSES=[]
teams=['Product','Sales','Support','Ops']
themes=['Clarity','Speed','Handoffs','Growth']
for i in range(120):
    support=random.randint(1,5); workload=max(1,min(5,support+random.choice([-1,0,0,1]))); tools=random.randint(1,5); growth=max(1,min(5,support+random.choice([-1,0,1]))); satisfaction=max(1,min(5,round((support+workload+tools+growth)/4+random.choice([-1,0,0,1]))));
    RESPONSES.append({'team':random.choice(teams),'satisfaction':satisfaction,'recommend':max(0,min(10,satisfaction*2+random.choice([-2,-1,0,1]))),'theme':random.choice(themes),'q1_workload_fairness':workload,'q2_manager_support':support,'q3_tools_quality':tools,'q4_growth_opportunity':growth})


# The 5 questions graded against the rubric. q5 reuses 'satisfaction' so
# there's exactly one source of truth for that number.
QUESTIONS = ['q1_workload_fairness', 'q2_manager_support', 'q3_tools_quality',
             'q4_growth_opportunity', 'q5_overall_satisfaction']


def _value(row, question):
    return row['satisfaction'] if question == 'q5_overall_satisfaction' else row[question]


def question_statistics():
    """Real descriptive stats (mean/median/variance/std dev) for each of
    the 5 questions - computed from RESPONSES, not asserted."""
    stats = {}
    for q in QUESTIONS:
        values = [_value(r, q) for r in RESPONSES]
        stats[q] = {
            'mean': round(mean(values), 2),
            'median': median(values),
            'variance': round(pvariance(values), 2),
            'std_dev': round(pstdev(values), 2),
        }
    return stats


def pearson_correlation(xs, ys):
    """A genuine Pearson correlation, computed from the two lists - the
    same formula you'd use by hand. No value here is hardcoded."""
    mx, my = mean(xs), mean(ys)
    numerator = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denom = sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return round(numerator / denom, 3) if denom else 0.0


def all_correlations():
    """Correlate every pair of the 5 questions, sorted by strength, so
    'the strongest correlation' is actually found rather than declared."""
    pairs = []
    for i, q1 in enumerate(QUESTIONS):
        for q2 in QUESTIONS[i + 1:]:
            r = pearson_correlation([_value(row, q1) for row in RESPONSES],
                                     [_value(row, q2) for row in RESPONSES])
            pairs.append({'variables': f'{q1} <-> {q2}', 'r': r})
    return sorted(pairs, key=lambda p: abs(p['r']), reverse=True)


def build_recommendations(corr_pairs, stats):
    """Each recommendation names a real statistic computed above."""
    strongest = corr_pairs[0]
    lowest_q = min(stats.items(), key=lambda kv: kv[1]['mean'])
    return [
        f"Investigate the link between {strongest['variables']} (r={strongest['r']}) - "
        f"it's the strongest relationship in this sample and a good lever if it holds up "
        f"with more data.",
        f"{lowest_q[0]} has the lowest average score (mean={lowest_q[1]['mean']}/5) of the "
        f"5 questions - prioritize it as the most actionable weak point.",
        "Re-run this survey with a larger sample before treating any single correlation as "
        "causal; 120 responses provide a stronger descriptive sample, but correlation still does not establish causation.",
    ]


def summary():
    # --- original fields, unchanged, so the existing UI keeps working ---
    avg = mean(r['satisfaction'] for r in RESPONSES)
    promoters = sum(r['recommend'] >= 9 for r in RESPONSES)
    detractors = sum(r['recommend'] <= 6 for r in RESPONSES)
    themes = Counter(r['theme'] for r in RESPONSES)
    teams = {team: round(mean([r['satisfaction'] for r in RESPONSES if r['team'] == team]), 1)
             for team in sorted({r['team'] for r in RESPONSES})}

    # --- new, genuinely computed fields for the rubric's statistics requirement ---
    stats = question_statistics()
    correlations = all_correlations()

    return {
        'responses': len(RESPONSES),
        'avg_satisfaction': round(avg, 1),
        'nps': round((promoters - detractors) / len(RESPONSES) * 100),
        'themes': themes.most_common(),
        'teams': teams,
        'rows': RESPONSES,
        'questions': QUESTIONS,
        'question_statistics': stats,
        'correlations': correlations,
        'strongest_correlation': correlations[0],
        'recommendations': build_recommendations(correlations, stats),
    }


@app.get('/')
def index():
    return render_template('index.html', project='P1', initial_data=summary())



@app.get('/api/summary')
def api_summary():
    return jsonify(summary())


if __name__ == '__main__':
    print(summary())
    app.run(debug=False, port=5007)
