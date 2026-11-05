/* MENZIL-BAU v2 · motion (GSAP + ScrollTrigger + Lenis) */
(function () {
  'use strict';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const gsap = window.gsap, ST = window.ScrollTrigger;
  gsap.registerPlugin(ST);

  /* smooth scroll */
  let lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new window.Lenis({ lerp: 0.09, smoothWheel: true });
    lenis.on('scroll', ST.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  window.__lenis = lenis;
  document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href'); if (id.length < 2) return;
    const el = document.querySelector(id); if (!el) return;
    e.preventDefault(); nav.classList.remove('open');
    lenis ? lenis.scrollTo(el, { offset: -20 }) : el.scrollIntoView({ behavior: 'smooth' });
  }));

  /* nav: hide on scroll down, show on scroll up; burger */
  const nav = document.querySelector('.nav');
  let lastY = 0;
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    nav.classList.toggle('hide', y > 300 && y > lastY && !nav.classList.contains('open'));
    lastY = y;
  }, { passive: true });
  document.querySelector('.nav-burger').addEventListener('click', () => nav.classList.toggle('open'));

  /* hero slideshow (Ken Burns crossfade) */
  const slides = [...document.querySelectorAll('.hero-media img')];
  let cur = 0;
  function show(i) {
    slides.forEach((s, k) => s.classList.toggle('on', k === i));
    if (reduce) return;
    gsap.set(slides[i], { opacity: 0, scale: 1.14, zIndex: 2 });
    gsap.to(slides[i], { opacity: 1, duration: 1.4, ease: 'power2.out' });
    gsap.to(slides[i], { scale: 1, duration: 7.5, ease: 'none' });
  }
  show(0);
  if (!reduce && slides.length > 1) setInterval(() => {
    const prev = slides[cur]; cur = (cur + 1) % slides.length;
    gsap.set(prev, { zIndex: 1 }); gsap.to(prev, { opacity: 0, duration: 1.6, delay: 0.4 });
    show(cur);
  }, 6000);

  if (reduce) { document.documentElement.classList.add('reduced'); return; }

  /* split lines reveal */
  const intro = gsap.timeline({ defaults: { ease: 'expo.out' } });
  intro.from('.hero .line > span', { yPercent: 115, duration: 1.3, stagger: 0.1 }, 0.15)
       .from('.hero-eyebrow, .hero-sub, .hero-ctas', { y: 24, opacity: 0, duration: 1, stagger: 0.08 }, 0.55)
       .from('.hero-badge, .hero-scroll', { y: 20, opacity: 0, duration: 0.8 }, 0.9)
       .from('.nav', { yPercent: -160, duration: 1 }, 0.2);
  // hero card shrinks slightly while scrolling away
  gsap.to('.hero-card', { scale: 0.94, borderRadius: 40, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });

  gsap.utils.toArray('[data-split]').forEach(el => {
    gsap.from(el.querySelectorAll('.line > span'), { yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: 0.08,
      scrollTrigger: { trigger: el, start: 'top 85%' } });
  });
  gsap.utils.toArray('[data-rise]').forEach(el => {
    gsap.from(el.children, { y: 50, opacity: 0, duration: 1, ease: 'power3.out', stagger: 0.1, scrollTrigger: { trigger: el, start: 'top 85%' } });
  });

  /* statement 3D object parallax */
  gsap.fromTo('.statement .float3d', { y: 80, rotate: -6 }, { y: -80, rotate: 6, ease: 'none', scrollTrigger: { trigger: '.statement', start: 'top bottom', end: 'bottom top', scrub: true } });

  /* stat counters */
  gsap.utils.toArray('[data-count]').forEach(el => {
    const end = +el.dataset.count, o = { v: 0 };
    gsap.to(o, { v: end, duration: 1.8, ease: 'power2.out', scrollTrigger: { trigger: el, start: 'top 85%' }, onUpdate: () => { el.firstChild.nodeValue = Math.round(o.v); } });
  });
  gsap.from('.stat-card', { y: 90, rotate: (i) => [-4, 2, 5][i % 3], opacity: 0, duration: 1.1, ease: 'power3.out', stagger: 0.12, scrollTrigger: { trigger: '.stat-cards', start: 'top 85%' } });

  /* sticky build: steps follow progress (3D handled in module) */
  const steps = gsap.utils.toArray('.step');
  ST.create({ trigger: '.build', start: 'top top', end: 'bottom bottom', scrub: true,
    onUpdate: self => {
      const p = self.progress;
      window.__buildProgress && window.__buildProgress(p);
      steps.forEach((s, i) => s.classList.toggle('on', p >= i / steps.length - 0.02));
      document.querySelector('.build-bar i').style.transform = `scaleX(${p})`;
      document.querySelector('.build-pct').textContent = Math.round(p * 100) + '%';
      document.querySelector('.build-done').classList.toggle('on', p > 0.97);
    } });

  /* carousel: buttons + drag */
  const car = document.querySelector('.carousel');
  const step = () => car.querySelector('.svc').offsetWidth + 16;
  document.querySelector('[data-car="prev"]').addEventListener('click', () => car.scrollBy({ left: -step(), behavior: 'smooth' }));
  document.querySelector('[data-car="next"]').addEventListener('click', () => car.scrollBy({ left: step(), behavior: 'smooth' }));
  let down = false, sx = 0, sl = 0;
  car.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; sx = e.clientX; sl = car.scrollLeft; car.style.scrollSnapType = 'none'; });
  window.addEventListener('pointerup', () => { if (!down) return; down = false; car.style.scrollSnapType = ''; });
  car.addEventListener('pointermove', e => { if (down) car.scrollLeft = sl - (e.clientX - sx); });
  gsap.from('.svc', { x: 120, opacity: 0, duration: 1, ease: 'power3.out', stagger: 0.08, scrollTrigger: { trigger: '.carousel', start: 'top 85%' } });

  /* scattered words + photos (pinned section, desktop only) */
  const mm = gsap.matchMedia();
  mm.add('(min-width: 761px)', () => {
    const tl = gsap.timeline({ scrollTrigger: { trigger: '.scatter', start: 'top top', end: 'bottom bottom', scrub: 1 } });
    tl.from('.sw[data-from="l"]', { xPercent: -60, opacity: 0, ease: 'none' }, 0)
      .from('.sw[data-from="r"]', { xPercent: 60, opacity: 0, ease: 'none' }, 0)
      .from('.sp', { y: (i) => [300, -260, 340, -300][i % 4], rotate: (i) => [-12, 10, -8, 14][i % 4], scale: 0.7, ease: 'none', stagger: 0.02 }, 0)
      .fromTo('.scatter .float3d', { scale: 0.5, rotate: -20 }, { scale: 1.1, rotate: 15, ease: 'none' }, 0);
  });

  /* stacked cards: slight scale-down of covered cards */
  gsap.utils.toArray('.scard').forEach((c, i, all) => {
    if (i === all.length - 1) return;
    gsap.to(c, { scale: 0.94, opacity: 0.7, ease: 'none', scrollTrigger: { trigger: all[i + 1], start: 'top 85%', end: 'top 25%', scrub: true } });
  });

  /* footer word letters */
  gsap.from('.foot-word span', { yPercent: 100, opacity: 0, duration: 1, ease: 'expo.out', stagger: 0.04, scrollTrigger: { trigger: '.foot', start: 'top 80%' } });
})();
