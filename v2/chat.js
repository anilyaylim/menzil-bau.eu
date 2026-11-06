/* MENZIL-BAU v2 · site assistant
   Rule-based: matches the question against keywords (DE/EN/TR) and answers only with
   texts taken from the website. No server, no AI service, nothing is stored or sent. */
(function () {
  'use strict';
  const D = window.MENZIL_CHAT; if (!D) return;
  const $ = (s, r = document) => r.querySelector(s);
  const root = $('.chat'); if (!root) return;
  const panel = $('.chat-panel', root), log = $('.chat-log', root), form = $('.chat-form', root), input = $('.chat-in', root), fab = $('.chat-fab', root);

  const norm = s => (' ' + s.toLowerCase().replace(/ı/g, 'i').replace(/ß/g, 'ss').normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9@.+\- ]+/g, ' ').replace(/\s+/g, ' ') + ' ');
  const intents = D.intents.map(it => ({ ...it, kw: it.kw.map(k => ' ' + norm(k).trim()) }));

  function match(q) {
    const t = norm(q); let best = null, score = 0;
    for (const it of intents) {
      let s = 0; for (const k of it.kw) if (t.indexOf(k) !== -1) s += k.length > 4 ? 2 : 1;
      if (s > score) { score = s; best = it; }
    }
    return best;
  }
  function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
  function add(who, html) {
    const m = document.createElement('div'); m.className = 'msg ' + who; m.innerHTML = html; log.appendChild(m);
    log.scrollTop = log.scrollHeight; return m;
  }
  function links(ls) {
    if (!ls || !ls.length) return '';
    return '<div class="msg-links">' + ls.map(l => `<a href="${l.h}"${/^https?:/.test(l.h) ? ' target="_blank" rel="noopener"' : ''}>${esc(l.l)} →</a>`).join('') + '</div>';
  }
  function chips() {
    return '<div class="chat-chips">' + D.ui.chips.map((c, i) => `<button type="button" data-i="${D.chipIntents[i]}">${esc(c)}</button>`).join('') + '</div>';
  }
  function answer(it) {
    const typing = add('bot typing', '<span></span><span></span><span></span>');
    setTimeout(() => {
      typing.remove();
      if (it) add('bot', esc(it.a) + links(it.links));
      else add('bot', esc(D.ui.fallback) + links(D.fallbackLinks) + chips());
    }, 450);
  }
  function ask(q) {
    q = q.trim(); if (!q) return;
    add('me', esc(q)); answer(match(q));
  }
  let greeted = false;
  function open(o) {
    root.classList.toggle('open', o); fab.setAttribute('aria-expanded', o);
    fab.setAttribute('aria-label', o ? D.ui.close : D.ui.open);
    if (o && !greeted) { greeted = true; add('bot', esc(D.ui.hello) + chips()); }
    if (o) setTimeout(() => input.focus(), 250);
  }
  fab.addEventListener('click', () => open(!root.classList.contains('open')));
  $('.chat-x', root).addEventListener('click', () => open(false));
  form.addEventListener('submit', e => { e.preventDefault(); ask(input.value); input.value = ''; });
  log.addEventListener('click', e => {
    const b = e.target.closest('.chat-chips button'); if (!b) return;
    const it = intents.find(x => x.id === b.dataset.i); add('me', esc(b.textContent)); answer(it);
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && root.classList.contains('open')) open(false); });
  // keep wheel / touch scrolling inside the log (smooth-scroll library would otherwise take it)
  panel.setAttribute('data-lenis-prevent', '');
})();
