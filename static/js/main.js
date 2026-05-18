document.addEventListener('DOMContentLoaded', () => {
  const alg = document.getElementById('algorithm');
  const inputs = Array.from(document.querySelectorAll('.alg-input'));
  function updateAlg() {
    const val = alg.value;
    inputs.forEach(el => {
      el.classList.toggle('d-none', el.dataset.alg !== val);
    });
  }
  if (alg) alg.addEventListener('change', updateAlg);
  updateAlg();

  const themeToggle = document.getElementById('theme-toggle');
  themeToggle?.addEventListener('click', () => {
    document.body.classList.toggle('dark');
  });

  // small step reveal animation
  const steps = document.getElementById('steps');
  if (steps) {
    Array.from(steps.querySelectorAll('li')).forEach((li, i) => {
      li.style.opacity = 0;
      setTimeout(() => { li.style.opacity = 1; }, i * 80);
    });
  }

  // Hill matrix client-side check: determinant, mod26, invertibility
  const hillTextarea = document.querySelector('textarea[name="key_matrix"]');
  const hillCheck = document.getElementById('hill-check');
  const processBtn = document.getElementById('process-btn');
  const modeRadios = Array.from(document.querySelectorAll('input[name="mode"]'));

  function gcd(a, b) {
    a = Math.abs(a); b = Math.abs(b);
    while (b) { const t = b; b = a % b; a = t; }
    return a;
  }

  function parseMatrix(text) {
    const rows = text.split('\n').map(r => r.trim()).filter(r => r.length);
    if (rows.length === 0) return {ok:false, msg:'Matrix is empty'};
    const mat = [];
    for (const r of rows) {
      const cols = r.split(',').map(c => c.trim()).filter(c=>c.length);
      const nums = cols.map(c => {
        const v = Number(c);
        return Number.isFinite(v) ? Math.floor(v) : NaN;
      });
      if (nums.some(n => Number.isNaN(n))) return {ok:false, msg:'Matrix contains non-number'};
      mat.push(nums);
    }
    const n = mat.length;
    if (!mat.every(row => row.length === n)) return {ok:false, msg:'Matrix must be square (n x n)'};
    if (n < 2 || n > 3) return {ok:false, msg:'Only 2x2 or 3x3 matrices supported in client check'};
    return {ok:true, mat};
  }

  function det2(m) {
    return m[0][0]*m[1][1] - m[0][1]*m[1][0];
  }

  function det3(m) {
    return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
         - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
         + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]);
  }

  function checkHill() {
    if (!hillTextarea || !hillCheck) return;
    const parsed = parseMatrix(hillTextarea.value);
    if (!parsed.ok) {
      hillCheck.textContent = parsed.msg;
      hillCheck.classList.remove('text-success');
      hillCheck.classList.add('text-danger');
      // disable submit only when hill is selected and decrypt mode
      toggleProcessEnabled();
      return;
    }
    const m = parsed.mat;
    const n = m.length;
    let d = n===2 ? det2(m) : det3(m);
    const dmod = ((d % 26) + 26) % 26;
    const inv = gcd(dmod, 26) === 1;
    hillCheck.classList.remove('text-danger');
    hillCheck.classList.add('text-success');
    hillCheck.innerHTML = `determinant = ${d} (mod26 = ${dmod}) — invertible: <strong>${inv? 'Yes':'No'}</strong>`;
    toggleProcessEnabled();
  }

  function getSelectedMode() {
    const sel = document.querySelector('input[name="mode"]:checked');
    return sel ? sel.value : null;
  }

  function toggleProcessEnabled() {
    // disable process button when algorithm is hill AND mode is decrypt AND matrix not invertible
    const algVal = document.getElementById('algorithm')?.value;
    if (algVal !== 'hill') { processBtn.disabled = false; return; }
    const parsed = parseMatrix(hillTextarea.value);
    if (!parsed.ok) { processBtn.disabled = true; return; }
    const m = parsed.mat; const n = m.length;
    let d = n===2 ? det2(m) : det3(m);
    const dmod = ((d % 26) + 26) % 26;
    const inv = gcd(dmod, 26) === 1;
    const mode = getSelectedMode();
    if (mode === 'decrypt' && !inv) {
      processBtn.disabled = true;
    } else {
      processBtn.disabled = false;
    }
  }

  hillTextarea?.addEventListener('input', checkHill);
  document.getElementById('algorithm')?.addEventListener('change', toggleProcessEnabled);
  modeRadios.forEach(r => r.addEventListener('change', toggleProcessEnabled));
  // initial run
  checkHill();
});
