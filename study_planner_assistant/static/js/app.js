const $=s=>document.querySelector(s);

$('#plan-form').addEventListener('submit', async e => {
  e.preventDefault();
  const body = {goal: $('#goal').value, topics: $('#topics').value, days: $('#days').value, hours: $('#hours').value};
  const d = await (await fetch('/api/plan', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)})).json();
  $('#plan-meta').innerHTML = `<div class="metric-label">Plan status</div><div class="metric-value" style="font-size:21px">${d.days} days</div><div class="metric-change">${d.hours} hours total · ${Math.round(d.hours/d.days*60)} min/day · source: ${d.source||'offline_fallback_scheduler'}</div>`;
  $('#tasks').innerHTML = d.tasks.map(task=>`<div class="list-item"><div><span class="tag">Day ${task.day}</span><h3 style="margin-top:8px">${task.task}</h3><p>${task.date} · ${task.topic} · ${task.minutes} minutes</p></div><input type="checkbox" aria-label="Complete day ${task.day}" style="width:20px;height:20px;accent-color:#64b5ff"></div>`).join('');
});

// --- new: render the documented prompt template on load ---
fetch('/api/prompt-template').then(r=>r.json()).then(t=>{
  const rows=[['Role',t.role,t.why_role_exists],['Context',t.context,t.why_context_exists],['Format',t.format,t.why_format_exists],['Constraints',t.constraints.join(' '),t.why_constraints_exist]];
  $('#prompt-template').innerHTML=rows.map(([label,text,why])=>`<div class="list-item"><div><h3>${label}</h3><p>${text}</p><p class="small muted">Why: ${why}</p></div></div>`).join('');
});

// --- new: render the 5 full sample interactions on load ---
fetch('/api/sample-interactions').then(r=>r.json()).then(samples=>{
  $('#sample-interactions').innerHTML=samples.map((s,i)=>{
    const days=s.output.map(day=>`<div><strong>${day.date}</strong>: ${day.blocks.length? day.blocks.map(b=>`${b.topic} (${b.minutes}m) - ${b.task}`).join('; ') : 'no free time'} <span class="small muted">— ${day.rationale}</span></div>`).join('');
    return `<div class="list-item"><div><h3>Sample ${i+1}: ${s.input.syllabus}</h3><p class="small muted">Time blocks: ${s.input.time_blocks}</p>${days}</div></div>`;
  }).join('');
});
