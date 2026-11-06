/* MENZIL-BAU v2 · motion (GSAP + ScrollTrigger + Lenis) — shared by all v2 pages */
(function () {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const gsap = window.gsap, ST = window.ScrollTrigger;
  if (gsap && ST) gsap.registerPlugin(ST);

  /* ── smooth scroll ── */
  let lenis = null;
  if (!reduce && window.Lenis && gsap) {
    lenis = new window.Lenis({ lerp: 0.09, smoothWheel: true });
    lenis.on('scroll', ST.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  window.__lenis = lenis;
  /* programmatic scroll: duration grows with distance, eased in and out, input locked meanwhile */
  let autoScrolling = false;
  const easeInOut = t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const NAV_OFFSET = -96;
  function scrollToEl(el, off = NAV_OFFSET) {
    const y = typeof el === 'number' ? el : el.getBoundingClientRect().top + window.scrollY + off;
    if (!lenis) { window.scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' }); return; }
    const dist = Math.abs(y - window.scrollY);
    const duration = Math.min(2.4, Math.max(0.7, dist / 3200));
    autoScrolling = window.__autoScrolling = true;
    lenis.scrollTo(y, { duration, easing: easeInOut, lock: true, force: true, onComplete: () => { autoScrolling = window.__autoScrolling = false; } });
  }

  /* ── nav ── */
  const nav = $('.nav'), navWrap = $('.nav-wrap'), burger = $('.nav-burger');
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href'); if (id.length < 2) return;
    const el = $(id); if (!el) return;
    e.preventDefault(); nav && nav.classList.remove('open');
    scrollToEl(el);
  }));
  let lastY = 0;
  const topBtn = $('.to-top');
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (navWrap) {
      if (autoScrolling) navWrap.classList.remove('hide');
      else {
        navWrap.classList.toggle('hide', y > 300 && y > lastY + 2 && !nav.classList.contains('open'));
        if (y < lastY - 2 || y < 300) navWrap.classList.remove('hide');
      }
    }
    if (topBtn) topBtn.classList.toggle('on', y > window.innerHeight * 0.8);
    lastY = y;
  }, { passive: true });
  if (burger) burger.addEventListener('click', () => { const o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', o); });
  if (topBtn) topBtn.addEventListener('click', () => scrollToEl(0));
  /* arriving with a hash (e.g. index.html#leistungen from another page) */
  if (location.hash.length > 1) {
    const target = document.getElementById(location.hash.slice(1));
    if (target) window.addEventListener('load', () => setTimeout(() => {
      const y = target.getBoundingClientRect().top + window.scrollY + NAV_OFFSET;
      lenis ? lenis.scrollTo(y, { immediate: true, force: true }) : window.scrollTo(0, y);
      window.ScrollTrigger && window.ScrollTrigger.refresh();
    }, 60));
  }

  /* ── cookie notice (no tracking cookies are set; the choice is remembered) ── */
  const cookie = $('.cookie');
  if (cookie) {
    let choice = null;
    try { choice = localStorage.getItem('menzil-cookie'); } catch (e) { /* storage blocked */ }
    if (!choice) setTimeout(() => cookie.classList.add('on'), 1200);
    $$('[data-cookie]', cookie).forEach(b => b.addEventListener('click', () => {
      try { localStorage.setItem('menzil-cookie', b.dataset.cookie); } catch (e) { /* ignore */ }
      cookie.classList.remove('on');
    }));
  }

  /* ── modals (legal notice, certificates) ── */
  let lastFocus = null;
  function openModal(m) {
    lastFocus = document.activeElement; m.hidden = false; document.documentElement.classList.add('modal-open');
    lenis && lenis.stop();
    requestAnimationFrame(() => m.classList.add('open'));
    const c = $('.v-modal-close', m); c && c.focus();
  }
  function closeModal(m) {
    m.classList.remove('open'); document.documentElement.classList.remove('modal-open'); lenis && lenis.start();
    setTimeout(() => { m.hidden = true; }, 250); lastFocus && lastFocus.focus();
  }
  $$('[data-modal]').forEach(t => t.addEventListener('click', e => { const m = document.getElementById(t.dataset.modal); if (!m) return; e.preventDefault(); openModal(m); }));
  $$('.v-modal').forEach(m => {
    $('.v-modal-close', m).addEventListener('click', () => closeModal(m));
    m.addEventListener('click', e => { if (e.target === m) closeModal(m); });
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { $$('.v-modal.open').forEach(closeModal); nav && nav.classList.remove('open'); } });

  /* ── contact form ── */
  $$('form.v-form').forEach(form => {
    const d = form.dataset, btn = $('button[type=submit]', form), label = btn.innerHTML, ok = $('.v-form-ok', form.parentNode), err = $('.v-form-err', form);
    $$('[data-letters]', form).forEach(i => i.addEventListener('input', () => { i.value = i.value.replace(/[^\p{L}\s\-'.]/gu, ''); }));
    const tel = $('[name=phone]', form); tel && tel.addEventListener('input', () => { tel.value = tel.value.replace(/[^0-9 ]/g, ''); });
    form.addEventListener('submit', e => {
      e.preventDefault();
      const f = form.elements;
      if (f.email.value.indexOf('@') === -1) { err.hidden = false; f.email.focus(); return; }
      err.hidden = true; btn.disabled = true; btn.textContent = d.sending;
      fetch(d.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ name: f.first_name.value + ' ' + f.last_name.value, email: f.email.value, phone: f.country.value + ' ' + f.phone.value,
          project_type: f.project_type.value, location: f.location.value, message: f.message.value, language: document.documentElement.lang,
          page: location.pathname, _subject: d.subject, _template: 'table' }) })
        .then(r => r.json()).then(r => {
          btn.disabled = false; btn.innerHTML = label;
          if (r.success === true || r.success === 'true') { form.hidden = true; ok.hidden = false; form.reset(); } else alert(d.err);
        }).catch(() => { btn.disabled = false; btn.innerHTML = label; alert(d.netErr); });
    });
    const again = ok && $('button', ok); again && again.addEventListener('click', () => { ok.hidden = true; form.hidden = false; });
  });

  /* ── hero slideshow (Ken Burns crossfade) ── */
  const slides = $$('.hero-media img');
  let cur = 0;
  function show(i) {
    slides.forEach((s, k) => s.classList.toggle('on', k === i));
    if (reduce || !gsap) return;
    gsap.set(slides[i], { opacity: 0, scale: 1.14, zIndex: 2 });
    gsap.to(slides[i], { opacity: 1, duration: 1.4, ease: 'power2.out' });
    gsap.to(slides[i], { scale: 1, duration: 7.5, ease: 'none' });
  }
  if (slides.length) {
    show(0);
    if (!reduce && slides.length > 1) setInterval(() => {
      const prev = slides[cur]; cur = (cur + 1) % slides.length;
      gsap.set(prev, { zIndex: 1 }); gsap.to(prev, { opacity: 0, duration: 1.6, delay: 0.4 });
      show(cur);
    }, 6000);
  }

  /* ── carousel: buttons + drag (works without motion too) ── */
  const car = $('.carousel');
  if (car) {
    const step = () => car.querySelector('.svc').offsetWidth + 16;
    $('[data-car="prev"]').addEventListener('click', () => car.scrollBy({ left: -step(), behavior: 'smooth' }));
    $('[data-car="next"]').addEventListener('click', () => car.scrollBy({ left: step(), behavior: 'smooth' }));
    let down = false, sx = 0, sl = 0;
    car.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; sx = e.clientX; sl = car.scrollLeft; car.style.scrollSnapType = 'none'; });
    window.addEventListener('pointerup', () => { if (!down) return; down = false; car.style.scrollSnapType = ''; });
    car.addEventListener('pointermove', e => { if (down) car.scrollLeft = sl - (e.clientX - sx); });
  }

  /* ── projects page: tabs ── */
  const vtabs = $$('.vtab');
  vtabs.forEach((tb, i) => {
    const sel = (t, focus) => {
      vtabs.forEach(x => { const on = x === t; x.classList.toggle('on', on); x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; document.getElementById(x.getAttribute('aria-controls')).hidden = !on; });
      if (focus) t.focus();
      window.ScrollTrigger && window.ScrollTrigger.refresh();
    };
    tb.addEventListener('click', () => sel(tb));
    tb.addEventListener('keydown', e => { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); sel(vtabs[(i + (e.key === 'ArrowRight' ? 1 : -1) + vtabs.length) % vtabs.length], true); } });
  });
  if (location.hash === '#plaene' && vtabs[1]) vtabs[1].click();
  /* ── filters ── */
  $$('[data-filter-group]').forEach(bar => {
    const target = document.getElementById(bar.dataset.filterGroup);
    $$('.vfilter', bar).forEach(b => b.addEventListener('click', () => {
      $$('.vfilter', bar).forEach(x => { x.classList.remove('on'); x.setAttribute('aria-pressed', 'false'); });
      b.classList.add('on'); b.setAttribute('aria-pressed', 'true');
      $$('[data-cat]', target).forEach(it => { it.hidden = !(b.dataset.cat === 'all' || it.dataset.cat === b.dataset.cat); });
    }));
  });
  /* ── lightbox ── */
  const lb = $('#vlb');
  if (lb) {
    const img = $('img', lb), cap = $('figcaption', lb), cnt = $('.vlb-count', lb);
    let list = [], idx = 0, back = null;
    const show = i => { idx = (i + list.length) % list.length; img.src = list[idx].src; cap.textContent = list[idx].cap; cnt.textContent = (idx + 1) + ' / ' + list.length; };
    const close = () => { lb.classList.remove('open'); document.documentElement.classList.remove('modal-open'); lenis && lenis.start(); setTimeout(() => { lb.hidden = true; img.src = ''; }, 200); back && back.focus(); };
    document.addEventListener('click', e => {
      const t = e.target.closest('[data-lb]'); if (!t) return;
      const nodes = $$('[data-lb][data-lb-group="' + t.dataset.lbGroup + '"]').filter(n => !n.hidden);
      list = []; let start = 0;
      nodes.forEach(n => { if (n === t) start = list.length; n.dataset.lb.split('|').forEach(src => list.push({ src, cap: n.dataset.lbCap })); });
      back = t; lb.hidden = false; document.documentElement.classList.add('modal-open'); lenis && lenis.stop();
      requestAnimationFrame(() => lb.classList.add('open')); show(start); $('.vlb-x', lb).focus();
    });
    $('.vlb-x', lb).addEventListener('click', close);
    $('.vlb-prev', lb).addEventListener('click', () => show(idx - 1));
    $('.vlb-next', lb).addEventListener('click', () => show(idx + 1));
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    document.addEventListener('keydown', e => { if (lb.hidden) return; if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') show(idx - 1); if (e.key === 'ArrowRight') show(idx + 1); });
    let sx = null;
    lb.addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', e => { if (sx === null) return; const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1)); sx = null; });
  }

  /* ── sticky 3D build: progress → model + steps ── */
  const build = $('.build');
  function setBuild(p) {
    window.__buildProgress && window.__buildProgress(p);
    $$('.step').forEach((s, i, all) => s.classList.toggle('on', p >= i / all.length - 0.02));
    $('.build-bar i').style.transform = `scaleX(${p})`;
    $('.build-pct').textContent = Math.round(p * 100) + '%';
    $('.build-done').classList.toggle('on', p > 0.97);
  }
  if (build && (reduce || !gsap)) setBuild(1);

  if (reduce || !gsap) { document.documentElement.classList.add('reduced'); return; }

  /* ── reveals ── */
  if ($('.hero')) {
    const intro = gsap.timeline({ defaults: { ease: 'expo.out' } });
    intro.from('.hero .line > span', { yPercent: 115, duration: 1.3, stagger: 0.1 }, 0.15)
         .from('.hero-eyebrow, .hero-sub, .hero-ctas', { y: 24, opacity: 0, duration: 1, stagger: 0.08 }, 0.55)
         .from('.hero-badge, .hero-scroll', { y: 20, opacity: 0, duration: 0.8 }, 0.9);
    gsap.to('.hero-card', { scale: 0.94, borderRadius: 40, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  }
  if ($('.sub-hero')) gsap.from('.sub-hero .line > span, .sub-hero .sub-hero-p, .sub-hero .crumbs', { yPercent: 40, opacity: 0, duration: 1.1, ease: 'expo.out', stagger: 0.08, delay: 0.15 });
  $$('[data-split]').forEach(el => gsap.from($$('.line > span', el), { yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: 0.08, scrollTrigger: { trigger: el, start: 'top 85%' } }));
  $$('[data-rise]').forEach(el => gsap.from(el.children, { y: 50, opacity: 0, duration: 1, ease: 'power3.out', stagger: 0.1, scrollTrigger: { trigger: el, start: 'top 85%' } }));
  if ($('.statement .float3d')) gsap.fromTo('.statement .float3d', { y: 80, rotate: -6 }, { y: -80, rotate: 6, ease: 'none', scrollTrigger: { trigger: '.statement', start: 'top bottom', end: 'bottom top', scrub: true } });

  /* counters */
  $$('[data-count]').forEach(el => {
    const end = +el.dataset.count, o = { v: 0 };
    gsap.to(o, { v: end, duration: 1.8, ease: 'power2.out', scrollTrigger: { trigger: el, start: 'top 88%' }, onUpdate: () => { el.firstChild.nodeValue = Math.round(o.v); } });
  });
  if ($('.stat-card')) gsap.from('.stat-card', { y: 90, rotate: i => [-4, 2, 5][i % 3], opacity: 0, duration: 1.1, ease: 'power3.out', stagger: 0.12, scrollTrigger: { trigger: '.stat-cards', start: 'top 85%' } });
  if ($('.region-col')) gsap.from('.region-col li', { x: -20, opacity: 0, duration: 0.6, ease: 'power2.out', stagger: 0.03, scrollTrigger: { trigger: '.regions', start: 'top 80%' } });

  if (build) ST.create({ trigger: build, start: 'top top', end: 'bottom bottom', scrub: true, onUpdate: self => setBuild(self.progress) });
  if (car) gsap.from('.svc', { x: 120, opacity: 0, duration: 1, ease: 'power3.out', stagger: 0.08, scrollTrigger: { trigger: car, start: 'top 85%' } });

  /* scattered words (left) + photos (right), desktop only */
  if ($('.scatter')) gsap.matchMedia().add('(min-width: 761px)', () => {
    const tl = gsap.timeline({ scrollTrigger: { trigger: '.scatter', start: 'top 95%', end: 'top 15%', scrub: 0.6 } });
    tl.from('.sw', { xPercent: -40, opacity: 0, ease: 'none', stagger: 0.08 }, 0)
      .from('.sp', { x: i => [260, 320, 280, 340][i % 4], y: i => [160, -120, 140, -160][i % 4], rotate: i => [-10, 8, -6, 12][i % 4], scale: 0.75, opacity: 0, ease: 'none', stagger: 0.05 }, 0);
  });

  /* stacked cards */
  $$('.scard').forEach((c, i, all) => {
    if (i === all.length - 1) return;
    gsap.to(c, { scale: 0.94, opacity: 0.7, ease: 'none', scrollTrigger: { trigger: all[i + 1], start: 'top 85%', end: 'top 25%', scrub: true } });
  });
  if ($('.foot-word')) gsap.from('.foot-word span', { yPercent: 100, opacity: 0, duration: 1, ease: 'expo.out', stagger: 0.04, scrollTrigger: { trigger: '.foot', start: 'top 80%' } });
})();
