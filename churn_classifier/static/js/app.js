const $=s=>document.querySelector(s);

function renderEvaluation(evaluation){
  $('#eval-accuracy').textContent=`${Math.round(evaluation.accuracy*100)}%`;
  $('#eval-precision').textContent=`${Math.round(evaluation.precision*100)}%`;
  $('#eval-recall').textContent=`${Math.round(evaluation.recall*100)}%`;
  const cm=evaluation.confusion_matrix;
  $('#eval-confusion').innerHTML=`<table><thead><tr><th></th><th>Predicted: No churn</th><th>Predicted: Churn</th></tr></thead><tbody><tr><th>Actual: No churn</th><td>${cm[0][0]}</td><td>${cm[0][1]}</td></tr><tr><th>Actual: Churn</th><td>${cm[1][0]}</td><td>${cm[1][1]}</td></tr></tbody></table><p class="small muted">Evaluated on ${evaluation.test_rows} held-out test rows (trained on ${evaluation.train_rows}).</p>`;
  $('#eval-features').innerHTML=evaluation.top_features.map(f=>`<div class="list-item"><div><h3>${f.feature}</h3><p>Coefficient: ${f.coefficient}</p></div><span class="tag">${f.importance}</span></div>`).join('');
}

// Load real evaluation metrics on page load, independent of any prediction.
fetch('/api/evaluation').then(r=>r.json()).then(renderEvaluation);

$('#churn-form').addEventListener('submit', async e => {
  e.preventDefault();
  const body = {
    months: $('#months').value, usage: $('#usage').value,
    support: $('#support').value, late_payments: $('#late').value,
    plan: $('#plan').value,
  };
  const d = await (await fetch('/api/predict', {
    method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body),
  })).json();
  $('#band').textContent = `${d.band} risk`;
  $('#score').textContent = `${d.score}/100`;
  $('#score-bar').style.width = `${d.score}%`;
  $('#action').textContent = d.action;
  $('#reasons').innerHTML = d.reasons.map(reason =>
    `<div class="insight"><div class="insight-icon">!</div><div><h3>Signal</h3><p>${reason}</p></div></div>`
  ).join('');
  renderEvaluation(d.evaluation);
});
