// render.js – loads resume.json and populates pages
async function loadResume() {
  const resp = await fetch('data/resume.json');
  if (!resp.ok) throw new Error('Failed to load resume data');
  const data = await resp.json();
  window.resumeData = data; // expose globally
  return data;
}

function setActiveNav(page) {
  document.querySelectorAll('nav a').forEach(a=>{
    a.classList.toggle('active', a.getAttribute('href')===page);
  });
}

// Index page rendering
function renderIndex() {
  const d = window.resumeData;
  document.getElementById('name').textContent = d.name;
  document.getElementById('title').textContent = d.title;
  const summary = document.getElementById('summary');
  d.summary.forEach(item=>{
    const li = document.createElement('li'); li.textContent = item; summary.appendChild(li);
  });
  document.getElementById('years').textContent = d.experience_years + ' years';
}

// Telemetry page rendering
function renderTelemetry(){
  const skills = window.resumeData.skills.telemetry;
  const container = document.getElementById('telemetry');
  for (const [cat, items] of Object.entries(skills)) {
    const sec = document.createElement('section');
    const h = document.createElement('h3'); h.textContent = cat.charAt(0).toUpperCase()+cat.slice(1);
    sec.appendChild(h);
    const ul = document.createElement('ul');
    items.forEach(it=>{ const li=document.createElement('li'); li.textContent=it; ul.appendChild(li);});
    sec.appendChild(ul); container.appendChild(sec);
  }
}

// Automation page rendering
function renderAutomation(){
  const list = window.resumeData.automation;
  const container = document.getElementById('automation');
  const ul = document.createElement('ul');
  list.forEach(item=>{ const li=document.createElement('li'); li.textContent=item; ul.appendChild(li);});
  container.appendChild(ul);
}

// Incidents (experience) page rendering
function renderIncidents(){
  const exp = window.resumeData.experience;
  const container = document.getElementById('timeline');
  exp.forEach(job=>{
    const card = document.createElement('div'); card.className='card';
    const hdr = document.createElement('h3'); hdr.textContent = `${job.company} – ${job.role}`;
    const period = document.createElement('p'); period.textContent = job.period; period.style.fontStyle='italic';
    const ul = document.createElement('ul');
    job.highlights.forEach(h=>{ const li=document.createElement('li'); li.textContent=h; ul.appendChild(li);});
    card.appendChild(hdr); card.appendChild(period); card.appendChild(ul);
    container.appendChild(card);
  });
}

// Intelligence page (static text)
function renderIntelligence(){
  const container = document.getElementById('intelligence');
  container.innerHTML = `
    <p>Observability provides the data foundation for intelligent automation. AI can surface patterns, suggest remediations, and reduce mean‑time‑to‑resolution, but human expertise is essential to validate actions and avoid false positives.</p>
    <ul>
      <li><strong>Where AI helps:</strong> anomaly detection, root‑cause suggestion, capacity forecasting.</li>
      <li><strong>Where automation should stop:</strong> decisions that require business context or risk assessment.</li>
      <li><strong>Why false positives matter:</strong> noisy alerts increase toil and erode trust in the system.</li>
      <li><strong>Human‑in‑the‑loop:</strong> verification, policy definition, and exception handling.</li>
    </ul>`;
}

// Lab page (placeholder)
function renderLab(){
  const container = document.getElementById('lab');
  container.innerHTML = `<p>Personal experiments: API‑driven Dynatrace dashboards, custom log parsers, automated cost‑optimisation scripts. All built with a focus on safe AI usage and reproducibility.</p>`;
}

// Entry point – called from each HTML page
async function init(page) {
  await loadResume();
  setActiveNav(page+'.html');
  switch(page){
    case 'index': renderIndex(); break;
    case 'telemetry': renderTelemetry(); break;
    case 'automation': renderAutomation(); break;
    case 'incidents': renderIncidents(); break;
    case 'intelligence': renderIntelligence(); break;
    case 'lab': renderLab(); break;
  }
}
