const $=s=>document.querySelector(s); const d=window.INITIAL_DATA||{};

$('#responses').textContent=d.responses;
$('#satisfaction').textContent=d.avg_satisfaction;
$('#nps').textContent=d.nps;

$('#themes').innerHTML=d.themes.map(([theme,count],i)=>`<div class="list-item"><div><h3>${theme}</h3><p>${count} response${count===1?'':'s'} mention this theme</p></div><span class="tag ${i===0?'good':''}">${Math.round(count/d.responses*100)}%</span></div>`).join('');

$('#teams').innerHTML=Object.entries(d.teams).map(([team,score])=>`<div><div class="list-item"><div><h3>${team}</h3><p>Average satisfaction</p></div><strong>${score}/5</strong></div><div class="progress" style="margin-top:7px"><span style="width:${score/5*100}%"></span></div></div>`).join('');

$('#table').innerHTML=`<table><thead><tr><th>Team</th><th>Satisfaction</th><th>Recommend</th><th>Theme</th></tr></thead><tbody>${d.rows.map(r=>`<tr><td>${r.team}</td><td>${r.satisfaction}/5</td><td>${r.recommend}/10</td><td>${r.theme}</td></tr>`).join('')}</tbody></table>`;

// --- new: the 5-question statistics table (mean/median/variance/std dev) ---
$('#question-stats').innerHTML=`<table><thead><tr><th>Question</th><th>Mean</th><th>Median</th><th>Variance</th><th>Std dev</th></tr></thead><tbody>${
  d.questions.map(q=>{const s=d.question_statistics[q];return `<tr><td>${q}</td><td>${s.mean}</td><td>${s.median}</td><td>${s.variance}</td><td>${s.std_dev}</td></tr>`;}).join('')
}</tbody></table>`;

// --- new: correlation list, strongest first ---
$('#correlations').innerHTML=d.correlations.map((c,i)=>`<div class="list-item"><div><h3>${c.variables}</h3><p>${i===0?'Strongest relationship in this sample':'Pearson correlation'}</p></div><span class="tag ${i===0?'good':''}">r = ${c.r}</span></div>`).join('');

// --- new: recommendations tied to the numbers above ---
$('#recommendations').innerHTML=d.recommendations.map(rec=>`<div class="insight"><div class="insight-icon">→</div><div><p>${rec}</p></div></div>`).join('');
