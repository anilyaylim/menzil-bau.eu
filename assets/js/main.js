/* MENZIL-BAU · main.js — nav, scroll, reveal, form, filters, lightbox */
(function () {
  'use strict';
  var nav = document.querySelector('.site-nav');
  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');

  /* ── Mobile nav (DKI behaviour) ── */
  function closeMenu() {
    links.classList.remove('open');
    nav.classList.remove('menu-open');
    toggle.setAttribute('aria-expanded', 'false');
  }
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      nav.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeMenu); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && links.classList.contains('open')) closeMenu(); });
    window.addEventListener('resize', function () { if (window.innerWidth > 960) closeMenu(); });
  }

  /* ── Scroll state: nav logo swap + scroll-to-top ── */
  var topBtn = document.getElementById('scroll-top');
  var hero = document.querySelector('.hero');
  function onScroll() {
    var y = window.scrollY;
    nav.classList.toggle('scrolled', y > 60);
    if (topBtn) {
      topBtn.classList.toggle('visible', y > 300);
      if (hero) topBtn.classList.toggle('past-hero', y > hero.offsetHeight - window.innerHeight + 40);
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (topBtn) topBtn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  /* ── Reveal on scroll ── */
  var rev = document.querySelectorAll('.reveal, .metric-card');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    rev.forEach(function (el) { io.observe(el); });
  } else { rev.forEach(function (el) { el.classList.add('in'); }); }

  /* ── Form ── */
  document.querySelectorAll('form.hero-form').forEach(function (form) {
    var wrap = form.closest('.hero-form-wrap');
    var success = wrap.querySelector('.hf-success');
    var btn = form.querySelector('.hf-submit');
    var btnLabel = btn.innerHTML;
    var d = form.dataset;
    var phone = form.querySelector('.hf-phone-num');
    var email = form.querySelector('[name="email"]');
    var err = form.querySelector('.hf-error');

    if (phone) {
      phone.addEventListener('input', function () { this.value = this.value.replace(/[^0-9 ]/g, ''); });
    }
    form.querySelectorAll('[data-letters]').forEach(function (inp) {
      inp.addEventListener('input', function () { this.value = this.value.replace(/[^\p{L}\s\-'.]/gu, ''); });
    });
    if (email && err) {
      email.addEventListener('blur', function () { err.style.display = (this.value && this.value.indexOf('@') === -1) ? 'block' : 'none'; });
      email.addEventListener('input', function () { if (this.value.indexOf('@') !== -1) err.style.display = 'none'; });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (email && email.value.indexOf('@') === -1) { err.style.display = 'block'; email.focus(); return; }
      var f = form.elements;
      var payload = {
        name: f.first_name.value + ' ' + f.last_name.value,
        email: f.email.value,
        phone: f.country.value + ' ' + f.phone.value,
        project_type: f.project_type.value,
        location: f.location.value,
        message: f.message.value,
        language: document.documentElement.lang,
        page: location.pathname,
        _subject: d.subject,
        _template: 'table'
      };
      btn.disabled = true; btn.textContent = d.sending;
      fetch(d.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          btn.disabled = false; btn.innerHTML = btnLabel;
          if (res.success === true || res.success === 'true') {
            form.style.display = 'none'; success.style.display = 'flex'; form.reset();
          } else { alert(d.err); }
        })
        .catch(function () { btn.disabled = false; btn.innerHTML = btnLabel; alert(d.netErr); });
    });
    var again = wrap.querySelector('.hf-close');
    if (again) again.addEventListener('click', function () { success.style.display = 'none'; form.style.display = 'flex'; });
  });

  /* ── Filters (projects + gallery) ── */
  document.querySelectorAll('[data-filter-group]').forEach(function (bar) {
    var target = document.getElementById(bar.dataset.filterGroup);
    bar.querySelectorAll('.filter').forEach(function (b) {
      b.addEventListener('click', function () {
        bar.querySelectorAll('.filter').forEach(function (x) { x.classList.remove('active'); x.setAttribute('aria-pressed', 'false'); });
        b.classList.add('active'); b.setAttribute('aria-pressed', 'true');
        var c = b.dataset.cat;
        target.querySelectorAll('[data-cat]').forEach(function (it) { it.hidden = !(c === 'all' || it.dataset.cat === c); });
      });
    });
  });

  /* ── Lightbox ── */
  var lb = document.getElementById('lightbox');
  if (lb) {
    var img = lb.querySelector('.lb-img'), cap = lb.querySelector('.lb-cap'), cnt = lb.querySelector('.lb-count');
    var list = [], idx = 0, lastFocus = null;
    function show(i) {
      idx = (i + list.length) % list.length;
      var it = list[idx];
      img.src = it.src; img.alt = it.alt || '';
      cap.innerHTML = it.cap || '';
      cnt.textContent = (idx + 1) + ' / ' + list.length;
    }
    function open(items, i) {
      list = items; lastFocus = document.activeElement;
      lb.classList.add('open'); document.body.style.overflow = 'hidden'; show(i);
      lb.querySelector('.lb-close').focus();
    }
    function close() { lb.classList.remove('open'); document.body.style.overflow = ''; img.src = ''; if (lastFocus) lastFocus.focus(); }
    document.addEventListener('click', function (e) {
      var t = e.target.closest('[data-lb]');
      if (!t) return;
      e.preventDefault();
      var group = t.dataset.lbGroup;
      var nodes = group ? Array.prototype.filter.call(document.querySelectorAll('[data-lb][data-lb-group="' + group + '"]'), function (n) { return !n.hidden; }) : [t];
      var items = [];
      var start = 0;
      nodes.forEach(function (n) {
        var srcs = n.dataset.lb.split('|');
        if (n === t) start = items.length;
        srcs.forEach(function (s) { items.push({ src: s, cap: n.dataset.lbCap, alt: n.dataset.lbAlt }); });
      });
      open(items, start);
    });
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function () { show(idx - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
    var sx = null;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (sx === null) return; var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1)); sx = null;
    });
  }
})();
