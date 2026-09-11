const $=s=>document.querySelector(s); let latest='';$('#content-form').addEventListener('submit',async e=>{e.preventDefault();const body={topic:$('#topic').value,audience:$('#audience').value,tone:$('#tone').value,channel:$('#channel').value};const d=await(await fetch('/api/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})).json();latest=`${d.hook}

${d.body}

${d.cta}

${d.hashtags.join(' ')}`;$('#output-channel').textContent=`${d.channel} draft · ${d.tone}`;$('#draft').innerHTML=`<div class="insight"><div class="insight-icon">H</div><div><h3>Hook</h3><p>${d.hook}</p></div></div><div class="insight"><div class="insight-icon">B</div><div><h3>Body</h3><p>${d.body}</p></div></div><div class="insight"><div class="insight-icon">→</div><div><h3>Call to action</h3><p>${d.cta}</p></div></div><div class="code-box">${d.hashtags.join('  ')}</div>`;});$('#copy').addEventListener('click',async()=>{if(latest){await navigator.clipboard?.writeText(latest);$('#copy').textContent='Copied';setTimeout(()=>$('#copy').textContent='Copy draft',1600);}});

function getBatchInputs(){return $('#batch-input').value.split('\n').map(line=>line.trim()).filter(Boolean).slice(0,5);}

$('#batch-generate').addEventListener('click', async () => {
  const inputs = getBatchInputs();
  if (!inputs.length) return;
  const d = await (await fetch('/api/batch-generate', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({inputs})})).json();
  $('#batch-outputs').innerHTML = d.outputs.map((o,i)=>`<div class="list-item"><div><h3>Article ${i+1} (${o.source})</h3><p><strong>Summary:</strong> ${o.summary}</p><p><strong>Posts:</strong> ${o.social_posts.join(' · ')}</p></div></div>`).join('');
  $('#batch-risk').innerHTML = `<strong>Bias/hallucination review:</strong><ul>${d.risk_review.map(r=>`<li>${r}</li>`).join('')}</ul>`;
});

$('#batch-export').addEventListener('click', async () => {
  const inputs = getBatchInputs();
  if (!inputs.length) return;
  const res = await fetch('/api/export-csv', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({inputs})});
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'content_generator_output.csv';
  document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(url);
});
