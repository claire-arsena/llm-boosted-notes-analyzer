let API_URL = '';

const textarea    = document.getElementById('noteInput');
const btn         = document.getElementById('analyzeBtn');
const btnLabel    = document.getElementById('btnLabel');
const summaryEl   = document.getElementById('summaryText');
const sentimentEl = document.getElementById('sentimentText');
const tagsEl      = document.getElementById('tagsContainer');
const cards       = document.querySelectorAll('.result-card');

async function loadConfig() {
  try {
    const res = await fetch('/api/config');
    const config = await res.json();
    API_URL = `${config.apiBaseUrl}/api/analyze-note`;
  } catch {
    API_URL = '/api/analyze-note';
  }
}

btn.addEventListener('click', async () => {
  const content = textarea.value.trim();
  if (!content) {
    textarea.focus();
    return;
  }

  btn.disabled = true;
  btnLabel.textContent = '';
  const spinner = document.createElement('div');
  spinner.className = 'spinner';
  btn.insertBefore(spinner, btnLabel);
  btnLabel.textContent = 'Analyse en cours…';

  cards.forEach(c => c.classList.remove('visible'));

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content }),
    });

    if (!res.ok) throw new Error(`Erreur HTTP ${res.status}`);

    const data = await res.json();

    summaryEl.textContent   = data.summary   || '—';
    sentimentEl.textContent = data.sentiment  || '—';

    tagsEl.innerHTML = '';
    (data.tags || []).forEach(tag => {
      const pill = document.createElement('span');
      pill.className = 'tag-pill';
      pill.textContent = tag;
      tagsEl.appendChild(pill);
    });

    requestAnimationFrame(() => {
      cards.forEach(c => c.classList.add('visible'));
    });

  } catch (err) {
    summaryEl.textContent   = `Erreur : ${err.message}`;
    sentimentEl.textContent = '—';
    tagsEl.innerHTML        = '<span class="text-error">Impossible de contacter le serveur</span>';
    cards.forEach(c => c.classList.add('visible'));
  } finally {
    spinner.remove();
    btnLabel.textContent = 'Analyser la note';
    btn.disabled = false;
  }
});

loadConfig();
