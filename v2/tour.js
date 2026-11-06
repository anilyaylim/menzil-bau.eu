/* MENZIL-BAU v2 · virtual tour (demo)
   A procedural 3D house: exterior view, then an interior walk-through
   (living room, kitchen, bedroom, bathroom). Everything is generated in code –
   textures are drawn on canvases, furniture is built from primitives.
   Look around by dragging; move between rooms via hotspots or the room bar. */
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { makeModel } from './houses.js';

const I = window.TOUR_I18N;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const stage = document.getElementById('tourStage');

/* ───────────── deterministic random ───────────── */
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

/* ───────────── canvas textures ───────────── */
function canvasTex(w, h, draw, repeat = [1, 1]) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...repeat); t.anisotropy = 8;
  return t;
}
const woodTex = () => canvasTex(1024, 1024, (g, w, h) => {
  const r = rng(7), rows = 8, ph = h / rows;
  for (let i = 0; i < rows; i++) {
    let x = -r() * 400;
    while (x < w) {
      const len = 380 + r() * 360, l = 54 + r() * 10, hue = 30 + r() * 6;
      g.fillStyle = `hsl(${hue},38%,${l}%)`; g.fillRect(x, i * ph, len, ph);
      g.globalAlpha = 0.12;
      for (let k = 0; k < 14; k++) {
        g.strokeStyle = r() > 0.5 ? '#5a3b1e' : '#f3d9b0'; g.lineWidth = 0.6 + r() * 1.4; g.beginPath();
        const yy = i * ph + r() * ph; g.moveTo(x, yy);
        for (let s = 0; s <= len; s += 40) g.lineTo(x + s, yy + Math.sin(s / 70 + k) * 2.2);
        g.stroke();
      }
      g.globalAlpha = 1; g.fillStyle = 'rgba(60,40,20,.55)'; g.fillRect(x, i * ph, 2, ph);
      x += len;
    }
    g.fillStyle = 'rgba(60,40,20,.45)'; g.fillRect(0, i * ph, w, 2);
  }
});
const tileTex = (base, grout, n, jitter = 6, seed = 3) => canvasTex(1024, 1024, (g, w, h) => {
  const r = rng(seed), s = w / n;
  g.fillStyle = grout; g.fillRect(0, 0, w, h);
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
    const d = (r() - 0.5) * jitter; g.fillStyle = shade(base, d); g.fillRect(i * s + 2, j * s + 2, s - 4, s - 4);
    g.globalAlpha = 0.06; for (let k = 0; k < 220; k++) { g.fillStyle = r() > 0.5 ? '#000' : '#fff'; g.fillRect(i * s + r() * s, j * s + r() * s, 2, 2); } g.globalAlpha = 1;
  }
});
const marbleTex = () => canvasTex(1024, 512, (g, w, h) => {
  const r = rng(11); g.fillStyle = '#f2f0ec'; g.fillRect(0, 0, w, h);
  g.filter = 'blur(1.4px)';
  for (let k = 0; k < 26; k++) {
    g.strokeStyle = `rgba(120,120,125,${0.08 + r() * 0.22})`; g.lineWidth = 0.8 + r() * 2.5; g.beginPath();
    let x = r() * w, y = r() * h; g.moveTo(x, y);
    for (let s = 0; s < 12; s++) { x += (r() - 0.3) * 120; y += (r() - 0.5) * 90; g.lineTo(x, y); }
    g.stroke();
  }
  g.filter = 'none';
});
const fabricTex = (base) => canvasTex(512, 512, (g, w, h) => {
  const r = rng(5); g.fillStyle = base; g.fillRect(0, 0, w, h);
  g.globalAlpha = 0.08; for (let k = 0; k < 9000; k++) { g.fillStyle = r() > 0.5 ? '#000' : '#fff'; g.fillRect(r() * w, r() * h, 1.5, 1.5); }
  g.globalAlpha = 0.05; for (let y = 0; y < h; y += 3) { g.fillStyle = '#000'; g.fillRect(0, y, w, 1); }
}, [3, 3]);
const landscapeTex = (seed) => canvasTex(2048, 1024, (g, w, h) => {
  const r = rng(seed);
  const sky = g.createLinearGradient(0, 0, 0, h * 0.62); sky.addColorStop(0, '#a9c9e6'); sky.addColorStop(1, '#eef3f6');
  g.fillStyle = sky; g.fillRect(0, 0, w, h);
  g.globalAlpha = 0.6; for (let k = 0; k < 9; k++) { g.fillStyle = '#fff'; g.beginPath(); g.ellipse(r() * w, 80 + r() * 220, 140 + r() * 200, 24 + r() * 30, 0, 0, Math.PI * 2); g.fill(); } g.globalAlpha = 1;
  const hills = (y, col, amp) => { g.fillStyle = col; g.beginPath(); g.moveTo(0, h); for (let x = 0; x <= w; x += 32) g.lineTo(x, y + Math.sin(x / 260 + r() * 0.2) * amp + Math.sin(x / 90) * amp * 0.25); g.lineTo(w, h); g.fill(); };
  hills(h * 0.55, '#9db3a4', 26); hills(h * 0.6, '#7f9b78', 20);
  for (let k = 0; k < 60; k++) { const x = r() * w, y = h * 0.6 + r() * 30, s = 18 + r() * 40; g.fillStyle = r() > 0.5 ? '#557a46' : '#4a6b3d'; g.beginPath(); g.ellipse(x, y - s * 0.6, s * 0.6, s, 0, 0, Math.PI * 2); g.fill(); }
  g.fillStyle = '#86a862'; g.fillRect(0, h * 0.66, w, h);
  g.fillStyle = '#d8d3ca'; g.fillRect(0, h * 0.8, w, 40);   // terrace edge
});
const artTex = () => canvasTex(512, 640, (g, w, h) => {
  g.fillStyle = '#efe9df'; g.fillRect(0, 0, w, h);
  g.fillStyle = '#b3000a'; g.beginPath(); g.arc(w * 0.38, h * 0.42, 120, 0, Math.PI * 2); g.fill();
  g.fillStyle = '#1c1f24'; g.fillRect(w * 0.5, h * 0.3, 150, 260);
  g.fillStyle = '#b08d57'; g.fillRect(w * 0.18, h * 0.7, 300, 26);
});
function shade(hex, d) { const n = parseInt(hex.slice(1), 16); const f = c => Math.max(0, Math.min(255, c + d)); return `rgb(${f(n >> 16)},${f(n >> 8 & 255)},${f(n & 255)})`; }

/* ───────────── materials ───────────── */
const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: o.r ?? 0.8, metalness: o.m ?? 0, map: o.map || null, ...(o.x || {}) });
const WOOD = woodTex(), MARBLE = marbleTex();
const M = {
  wall: std(0xf2efea, { r: 0.95 }), ceil: std(0xfbfaf8, { r: 1, x: { emissive: 0x2a2826 } }), accent: std(0x8e9b88, { r: 0.95 }),
  oak: std(0xffffff, { map: WOOD, r: 0.55 }), oakDark: std(0x8a6a48, { r: 0.6 }),
  white: std(0xf4f3f0, { r: 0.45 }), anth: std(0x2b2f35, { r: 0.45, m: 0.4 }), black: std(0x141517, { r: 0.35 }),
  stone: std(0xffffff, { map: MARBLE, r: 0.22 }), chrome: std(0xe6e8ea, { r: 0.12, m: 1 }),
  sofa: std(0xffffff, { map: fabricTex('#8f8b84'), r: 0.95 }), sofaDark: std(0xffffff, { map: fabricTex('#4c4e52'), r: 0.95 }),
  linen: std(0xffffff, { map: fabricTex('#ece8e0'), r: 0.95 }), throw: std(0xffffff, { map: fabricTex('#b39575'), r: 0.95 }),
  rug: std(0xffffff, { map: fabricTex('#d9d2c6'), r: 1 }), rugDark: std(0xffffff, { map: fabricTex('#5d5a55'), r: 1 }),
  glass: new THREE.MeshStandardMaterial({ color: 0xe4eef3, transparent: true, opacity: 0.14, roughness: 0.04, metalness: 0.1, depthWrite: false }),
  frosted: new THREE.MeshStandardMaterial({ color: 0xf5f7f8, transparent: true, opacity: 0.82, roughness: 0.4 }),
  mirror: std(0xc9d4da, { r: 0.12, m: 0.35 }), leaf: std(0x4f7a3e, { r: 0.85 }), pot: std(0xd9d3c9, { r: 0.7 }),
  glow: new THREE.MeshStandardMaterial({ color: 0xfff1d6, emissive: 0xffe2b0, emissiveIntensity: 2.2 }),
  screen: std(0x0d0e10, { r: 0.15, m: 0.2 }), art: std(0xffffff, { map: artTex(), r: 0.9 }),
  tileWall: std(0xffffff, { map: tileTex('#d9d6d1', '#c9c5bf', 4, 5, 9), r: 0.35 }),
  tileFloor: std(0xffffff, { map: tileTex('#6b6862', '#55524d', 3, 8, 21), r: 0.5 }),
};
[M.wall, M.ceil, M.accent].forEach(m => { m.shadowSide = THREE.DoubleSide; });

/* ───────────── geometry helpers ───────────── */
function mesh(geo, mat, x, y, z, { cast = true, receive = true, ry = 0 } = {}) {
  const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.rotation.y = ry; m.castShadow = cast; m.receiveShadow = receive; return m;
}
// box with its BOTTOM at y
const box = (g, w, h, d, mat, x, y, z, o) => g.add(mesh(new THREE.BoxGeometry(w, h, d), mat, x, y + h / 2, z, o));
const rbox = (g, w, h, d, r, mat, x, y, z, o) => g.add(mesh(new RoundedBoxGeometry(w, h, d, 4, Math.min(r, w / 2, h / 2, d / 2)), mat, x, y + h / 2, z, o));
const cyl = (g, rt, rb, h, mat, x, y, z, seg = 28, o) => g.add(mesh(new THREE.CylinderGeometry(rt, rb, h, seg), mat, x, y + h / 2, z, o));

/* ───────────── rooms ───────────── */
const lights = [];
function room({ ox, w, d, h = 2.8, floor, wall = M.wall, windows = [], doors = [], wallMat = {}, landscape = 1 }) {
  const g = new THREE.Group(); g.position.x = ox;
  const fl = floor.clone(); if (fl.map) { fl.map = fl.map.clone(); fl.map.needsUpdate = true; fl.map.repeat.set(w / 2.2, d / 2.2); }
  const f = mesh(new THREE.PlaneGeometry(w, d), fl, 0, 0, 0, { cast: false }); f.rotation.x = -Math.PI / 2; g.add(f);
  const c = mesh(new THREE.PlaneGeometry(w, d), M.ceil, 0, h, 0); c.rotation.x = Math.PI / 2; g.add(c);
  const F = {
    n: { r: 0, o: [0, -d / 2], u: [1, 0], n: [0, 1], L: w, flip: 1 }, s: { r: Math.PI, o: [0, d / 2], u: [-1, 0], n: [0, -1], L: w, flip: -1 },
    e: { r: -Math.PI / 2, o: [w / 2, 0], u: [0, 1], n: [-1, 0], L: d, flip: 1 }, w: { r: Math.PI / 2, o: [-w / 2, 0], u: [0, -1], n: [1, 0], L: d, flip: -1 },
  };
  // place(obj, side, c, y, t): c = world x (n/s) or z (e/w); t > 0 = into the room
  const place = (obj, s, cc, y, t) => { const fr = F[s], u = cc * fr.flip; obj.position.set(fr.o[0] + u * fr.u[0] + t * fr.n[0], y, fr.o[1] + u * fr.u[1] + t * fr.n[1]); obj.rotation.y = fr.r; g.add(obj); return obj; };
  const part = (s, cc, y, t, gw, gh, gd, mat, cast = true) => place(mesh(new THREE.BoxGeometry(gw, gh, gd), mat, 0, 0, 0, { cast }), s, cc, y + gh / 2, t);
  const backdrops = {};
  for (const s of ['n', 's', 'e', 'w']) {
    const fr = F[s], L = fr.L, shape = new THREE.Shape();
    shape.moveTo(-L / 2, 0); shape.lineTo(L / 2, 0); shape.lineTo(L / 2, h); shape.lineTo(-L / 2, h); shape.lineTo(-L / 2, 0);
    for (const win of windows.filter(o => o.s === s)) {
      const u = win.c * fr.flip, hole = new THREE.Path();
      hole.moveTo(u - win.w / 2, win.y); hole.lineTo(u + win.w / 2, win.y); hole.lineTo(u + win.w / 2, win.y + win.h); hole.lineTo(u - win.w / 2, win.y + win.h); hole.lineTo(u - win.w / 2, win.y);
      shape.holes.push(hole);
    }
    place(mesh(new THREE.ShapeGeometry(shape), wallMat[s] || wall, 0, 0, 0), s, 0, 0, 0);
    // skirting
    part(s, 0, 0, 0.008, L - 0.02, 0.07, 0.016, M.white, false);
  }
  for (const win of windows) {
    const T = 0.28, s = win.s, glass = win.frosted ? M.frosted : M.glass;
    part(s, win.c, win.y + win.h, -T / 2, win.w, 0.02, T, M.wall); if (win.y > 0.02) part(s, win.c, win.y - 0.02, -T / 2, win.w, 0.02, T, M.wall);
    part(s, win.c - win.w / 2, win.y, -T / 2, 0.02, win.h, T, M.wall); part(s, win.c + win.w / 2, win.y, -T / 2, 0.02, win.h, T, M.wall);
    const ft = 0.055, fd = 0.07, tz = -0.14;
    part(s, win.c, win.y + win.h - ft, tz, win.w, ft, fd, M.anth); part(s, win.c, win.y, tz, win.w, ft, fd, M.anth);
    part(s, win.c - win.w / 2 + ft / 2, win.y, tz, ft, win.h, fd, M.anth); part(s, win.c + win.w / 2 - ft / 2, win.y, tz, ft, win.h, fd, M.anth);
    if (win.w > 1.6) part(s, win.c, win.y, tz, ft, win.h, fd, M.anth);
    part(s, win.c, win.y, tz, win.w, win.h, 0.012, glass, false);
    if (win.y > 0.2) part(s, win.c, win.y - 0.03, 0.08, win.w + 0.12, 0.03, 0.2, M.stone);
    if (!win.frosted && !backdrops[s]) {
      backdrops[s] = true;
      const bd = new THREE.Mesh(new THREE.PlaneGeometry(F[s].L + 24, 14), new THREE.MeshBasicMaterial({ map: landscapeTex(landscape + s.charCodeAt(0)), toneMapped: false }));
      place(bd, s, 0, 3.4, -7.5);
    }
  }
  for (const dr of doors) {   // closed interior doors (visual)
    part(dr.s, dr.c, 0, 0.02, 0.98, 2.12, 0.04, M.white);
    part(dr.s, dr.c, 2.12, 0.02, 1.1, 0.06, 0.05, M.white); part(dr.s, dr.c - 0.52, 0, 0.02, 0.06, 2.12, 0.05, M.white); part(dr.s, dr.c + 0.52, 0, 0.02, 0.06, 2.12, 0.05, M.white);
    part(dr.s, dr.c + 0.36 * (dr.hand || 1), 1.02, 0.07, 0.14, 0.02, 0.03, M.anth);
  }
  return { g, place, part, w, d, h };
}
function pendant(g, x, z, h, drop = 0.9, r = 0.14, light = true) {
  cyl(g, 0.004, 0.004, drop, M.anth, x, h - drop, z, 6, { cast: false });
  cyl(g, r * 0.35, r, r * 0.9, M.anth, x, h - drop - r * 0.9, z);
  cyl(g, r * 0.92, r * 0.92, 0.01, M.glow, x, h - drop - r * 0.9 - 0.005, z, 28, { cast: false });
  if (light) { const p = new THREE.PointLight(0xffe0b8, 2.6, 0, 2); p.position.set(g.position.x + x, h - drop - r - 0.08, z); lights.push(p); }
}
function plant(g, x, z, s = 1) {
  cyl(g, 0.2 * s, 0.16 * s, 0.42 * s, M.pot, x, 0, z);
  const r = rng(Math.round(x * 100 + z * 10));
  for (let k = 0; k < 14; k++) {
    const leaf = mesh(new THREE.SphereGeometry(0.12 * s, 8, 6), M.leaf, x + (r() - 0.5) * 0.4 * s, 0.55 * s + r() * 0.75 * s, z + (r() - 0.5) * 0.4 * s);
    leaf.scale.set(1.6, 0.35, 0.8); leaf.rotation.set(r() * 1.2, r() * 6, r() * 1.2); g.add(leaf);
  }
}

/* ───────── living + kitchen (open plan) ───────── */
const L = room({ ox: 0, w: 9, d: 6.5, floor: M.oak, landscape: 2,
  windows: [{ s: 's', c: -2.4, w: 3.2, h: 2.45, y: 0 }, { s: 's', c: 1.9, w: 2.2, h: 2.45, y: 0 }, { s: 'n', c: 2.75, w: 1.7, h: 0.95, y: 1.12 }],
  doors: [{ s: 'e', c: 2.6 }, { s: 'n', c: -3.6, hand: -1 }] });
{
  const g = L.g;
  // living
  box(g, 3.4, 0.012, 2.5, M.rug, -2.55, 0, 0.35, { cast: false });
  rbox(g, 0.98, 0.4, 2.7, 0.05, M.sofa, -1.05, 0.03, 0.35);
  rbox(g, 0.24, 0.42, 2.7, 0.06, M.sofa, -0.6, 0.42, 0.35);
  rbox(g, 0.98, 0.62, 0.22, 0.06, M.sofa, -1.05, 0, -1.04); rbox(g, 0.98, 0.62, 0.22, 0.06, M.sofa, -1.05, 0, 1.74);
  for (const z of [-0.5, 0.35, 1.2]) rbox(g, 0.76, 0.15, 0.82, 0.07, M.sofa, -1.13, 0.43, z);
  for (const z of [-0.45, 0.35, 1.15]) rbox(g, 0.2, 0.44, 0.78, 0.08, M.sofa, -0.79, 0.56, z);
  rbox(g, 0.13, 0.38, 0.38, 0.06, M.sofaDark, -0.92, 0.62, -0.72, { ry: 0.25 }); rbox(g, 0.13, 0.38, 0.38, 0.06, M.throw, -0.92, 0.62, 1.42, { ry: -0.2 });
  for (const [x, z] of [[-1.05, -1.0], [-1.05, 1.7], [-0.55, -1.0], [-0.55, 1.7]]) cyl(g, 0.025, 0.02, 0.05, M.anth, x, -0.02, z, 10);
  rbox(g, 1.15, 0.05, 0.62, 0.02, M.oak, -2.55, 0.36, 0.35);
  for (const [dx, dz] of [[-0.5, -0.25], [0.5, -0.25], [-0.5, 0.25], [0.5, 0.25]]) cyl(g, 0.018, 0.018, 0.36, M.anth, -2.55 + dx, 0, 0.35 + dz, 10);
  box(g, 0.3, 0.04, 0.22, M.oakDark, -2.4, 0.41, 0.25); cyl(g, 0.06, 0.05, 0.16, M.pot, -2.8, 0.41, 0.42);
  // TV wall with oak slats
  for (let z = -1.6; z <= 2.0; z += 0.09) box(g, 0.035, 2.8, 0.05, M.oak, -4.47, 0, z, { cast: false });
  rbox(g, 0.44, 0.42, 2.6, 0.02, M.white, -4.24, 0.2, 0.35);
  box(g, 0.03, 0.72, 1.28, M.screen, -4.4, 1.05, 0.35);
  plant(g, -4.05, 2.75, 1.25);
  // floor lamp
  cyl(g, 0.15, 0.17, 0.03, M.anth, -0.5, 0, 2.55); cyl(g, 0.012, 0.012, 1.45, M.anth, -0.5, 0.03, 2.55, 8);
  cyl(g, 0.17, 0.22, 0.3, M.linen, -0.5, 1.45, 2.55); const fl = new THREE.PointLight(0xffd9a8, 1.6, 0, 2); fl.position.set(-0.5, 1.5, 2.55); lights.push(fl);
  // art on north wall
  L.part('n', -1.4, 1.2, 0.02, 0.86, 1.06, 0.03, M.anth); L.part('n', -1.4, 1.24, 0.04, 0.78, 0.98, 0.01, M.art, false);
  // kitchen run along north wall
  const kx0 = 1.0, kx1 = 4.45, kl = kx1 - kx0, kc = (kx0 + kx1) / 2, kz = -3.25 + 0.32;
  box(g, kl, 0.1, 0.56, M.anth, kc, 0, kz - 0.02); box(g, kl, 0.76, 0.62, M.white, kc, 0.1, kz);
  box(g, kl + 0.02, 0.04, 0.65, M.stone, kc, 0.86, kz);
  for (let x = kx0 + 0.6; x < kx1; x += 0.6) box(g, 0.006, 0.74, 0.01, M.anth, x, 0.11, kz + 0.31, { cast: false });
  box(g, 0.5, 0.012, 0.36, M.black, 2.75, 0.893, kz);   // sink
  cyl(g, 0.016, 0.02, 0.3, M.chrome, 2.75, 0.9, kz - 0.22, 12); box(g, 0.025, 0.025, 0.2, M.chrome, 2.75, 1.18, kz - 0.14);
  box(g, 1.2, 0.03, 0.26, M.oak, 1.6, 1.55, -3.25 + 0.13); box(g, 1.2, 0.03, 0.26, M.oak, 3.95, 1.55, -3.25 + 0.13);
  // tall units on east wall
  box(g, 0.62, 2.4, 1.8, M.white, 4.45 - 0.31, 0, -1.25);
  box(g, 0.01, 0.58, 0.58, M.black, 4.45 - 0.62, 0.9, -1.75); box(g, 0.01, 0.42, 0.58, M.black, 4.45 - 0.62, 1.52, -1.75);
  box(g, 0.006, 2.36, 0.01, M.anth, 4.45 - 0.625, 0.02, -1.45, { cast: false });
  // island
  rbox(g, 2.3, 0.86, 0.95, 0.02, M.oak, 2.55, 0, -0.35); rbox(g, 2.5, 0.045, 1.1, 0.01, M.stone, 2.55, 0.86, -0.35);
  box(g, 0.62, 0.008, 0.48, M.black, 2.2, 0.905, -0.55);
  for (const x of [1.8, 2.55, 3.3]) {
    cyl(g, 0.2, 0.2, 0.06, M.sofaDark, x, 0.64, 0.42);
    for (const [dx, dz] of [[-0.13, -0.13], [0.13, -0.13], [-0.13, 0.13], [0.13, 0.13]]) cyl(g, 0.01, 0.012, 0.64, M.anth, x + dx, 0, 0.42 + dz, 8);
    cyl(g, 0.15, 0.15, 0.012, M.anth, x, 0.24, 0.42, 20);
  }
  for (const x of [1.75, 2.55, 3.35]) pendant(g, x, -0.35, 2.8, 0.95, 0.12, x === 2.55);
  // dining
  cyl(g, 0.62, 0.62, 0.04, M.oak, 2.5, 0.72, 2.1, 48); cyl(g, 0.05, 0.05, 0.72, M.anth, 2.5, 0, 2.1, 12); cyl(g, 0.3, 0.3, 0.02, M.anth, 2.5, 0, 2.1, 24);
  for (let k = 0; k < 4; k++) {
    const a = k * Math.PI / 2 + Math.PI / 4, x = 2.5 + Math.cos(a) * 0.82, z = 2.1 + Math.sin(a) * 0.82;
    rbox(g, 0.46, 0.06, 0.46, 0.03, M.sofa, x, 0.44, z, { ry: -a });
    const bk = mesh(new RoundedBoxGeometry(0.46, 0.38, 0.05, 3, 0.02), M.sofa, x + Math.cos(a) * 0.21, 0.69, z + Math.sin(a) * 0.21); bk.rotation.y = -a + Math.PI / 2; bk.castShadow = true; g.add(bk);
    for (const [dx, dz] of [[-0.17, -0.17], [0.17, -0.17], [-0.17, 0.17], [0.17, 0.17]]) cyl(g, 0.012, 0.012, 0.44, M.anth, x + dx, 0, z + dz, 8);
  }
  pendant(g, 2.5, 2.1, 2.8, 1.05, 0.22, true);
  pendant(g, -2.55, 0.35, 2.8, 0.25, 0.32, true);
}

/* ───────── bedroom ───────── */
const B = room({ ox: 40, w: 4.8, d: 4.4, floor: M.oak, landscape: 5,
  windows: [{ s: 'n', c: 0.7, w: 1.8, h: 1.6, y: 0.65 }], doors: [{ s: 's', c: 1.5 }], wallMat: { w: M.accent } });
{
  const g = B.g, bx = -2.4;
  box(g, 2.6, 0.012, 2.6, M.rug, -1.2, 0, 0, { cast: false });
  rbox(g, 0.1, 1.15, 2.1, 0.04, M.sofaDark, bx + 0.06, 0, 0);
  rbox(g, 2.1, 0.3, 1.95, 0.04, M.sofaDark, bx + 1.15, 0.04, 0);
  rbox(g, 2.0, 0.22, 1.82, 0.08, M.linen, bx + 1.15, 0.33, 0);
  rbox(g, 1.45, 0.07, 1.88, 0.03, M.linen, bx + 1.45, 0.53, 0);
  rbox(g, 0.5, 0.05, 1.92, 0.02, M.throw, bx + 1.8, 0.59, 0);
  for (const z of [-0.45, 0.45]) rbox(g, 0.42, 0.15, 0.68, 0.06, M.linen, bx + 0.42, 0.55, z, { ry: 0.05 });
  for (const z of [-1.4, 1.4]) {
    rbox(g, 0.45, 0.42, 0.45, 0.02, M.oak, bx + 0.3, 0.12, z);
    cyl(g, 0.06, 0.08, 0.04, M.anth, bx + 0.3, 0.54, z); cyl(g, 0.01, 0.01, 0.3, M.anth, bx + 0.3, 0.58, z, 8); cyl(g, 0.12, 0.15, 0.2, M.linen, bx + 0.3, 0.82, z);
  }
  const bl = new THREE.PointLight(0xffd8a6, 1.2, 0, 2); bl.position.set(40 + bx + 0.3, 0.95, -1.4); lights.push(bl);
  // wardrobe
  box(g, 0.64, 2.5, 2.6, M.white, 2.4 - 0.32, 0, -0.55);
  for (const z of [-1.2, -0.55, 0.1]) box(g, 0.006, 2.46, 0.01, M.anth, 2.4 - 0.645, 0.02, z + 0.32, { cast: false });
  for (const z of [-1.0, -0.12]) box(g, 0.02, 0.5, 0.02, M.anth, 2.4 - 0.65, 0.95, z);
  plant(g, 1.85, 1.75, 1.1);
  B.part('w', 0, 1.55, 0.02, 1.5, 0.6, 0.03, M.anth); B.part('w', 0, 1.58, 0.035, 1.42, 0.54, 0.01, M.art, false);
  cyl(g, 0.3, 0.3, 0.04, M.glow, 0, 2.76, 0, 32, { cast: false });
  const bc = new THREE.PointLight(0xffe6c4, 1.5, 0, 2); bc.position.set(40, 2.5, 0); lights.push(bc);
}

/* ───────── bathroom ───────── */
const C = room({ ox: 80, w: 3.4, d: 3.0, floor: M.tileFloor, wall: M.tileWall, landscape: 9,
  windows: [{ s: 'e', c: 0.4, w: 0.9, h: 0.8, y: 1.45, frosted: true }], doors: [{ s: 's', c: 0.9 }] });
{
  const g = C.g;
  // walk-in shower (north-west)
  box(g, 0.012, 2.0, 1.0, M.glass, -0.55, 0.0, -1.0, { cast: false });
  box(g, 0.02, 0.02, 1.0, M.chrome, -0.55, 2.0, -1.0);
  box(g, 0.05, 0.02, 0.4, M.chrome, -1.55, 2.2, -1.1); cyl(g, 0.16, 0.16, 0.015, M.chrome, -1.32, 2.18, -1.1, 32);
  box(g, 0.7, 0.006, 0.05, M.chrome, -1.1, 0.003, -0.6, { cast: false });
  C.part('n', -1.3, 1.2, 0.04, 0.6, 0.3, 0.08, M.tileWall);
  // floating vanity (north wall, right)
  rbox(g, 1.2, 0.42, 0.5, 0.02, M.oak, 0.85, 0.45, -1.25);
  box(g, 1.22, 0.03, 0.52, M.stone, 0.85, 0.87, -1.25);
  cyl(g, 0.21, 0.18, 0.13, M.white, 0.85, 0.9, -1.22, 40);
  cyl(g, 0.014, 0.014, 0.3, M.chrome, 0.85, 0.9, -1.45, 12); box(g, 0.02, 0.02, 0.16, M.chrome, 0.85, 1.19, -1.38);
  C.part('n', 0.85, 1.25, 0.012, 0.95, 0.8, 0.02, M.mirror, false);
  C.part('n', 0.85, 2.1, 0.03, 0.8, 0.03, 0.04, M.glow, false);
  // wall-hung WC (west wall)
  C.part('w', 0.65, 0.3, 0.04, 0.5, 0.9, 0.12, M.tileWall);
  rbox(g, 0.55, 0.36, 0.37, 0.12, M.white, -1.7 + 0.38, 0.4, 0.65);
  C.part('w', 0.65, 1.0, 0.105, 0.2, 0.14, 0.01, M.chrome, false);
  // towel radiator (south wall)
  for (let k = 0; k < 9; k++) C.part('s', -0.6, 0.35 + k * 0.13, 0.06, 0.55, 0.025, 0.03, M.anth);
  C.part('s', -0.6 - 0.27, 0.33, 0.06, 0.03, 1.2, 0.03, M.anth); C.part('s', -0.6 + 0.27, 0.33, 0.06, 0.03, 1.2, 0.03, M.anth);
  rbox(g, 0.5, 0.012, 0.75, 0.005, M.rugDark, 0.85, 0, -0.6, { cast: false });
  plant(g, 1.4, 1.15, 0.7);
  cyl(g, 0.22, 0.22, 0.03, M.glow, 0, 2.77, 0, 32, { cast: false });
  const cl = new THREE.PointLight(0xfff0dc, 1.8, 0, 2); cl.position.set(80, 2.45, 0); lights.push(cl);
}

/* ───────────── renderer / scene ───────────── */
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
stage.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xdfe7ee);
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.55;
const hemi = new THREE.HemisphereLight(0xffffff, 0xc8bfae, 0.6); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff1dc, 3.2); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -9, right: 9, top: 9, bottom: -9, near: 0.5, far: 60 }); sun.shadow.bias = -0.0003; sun.shadow.normalBias = 0.02;
scene.add(sun, sun.target);
scene.add(L.g, B.g, C.g); lights.forEach(l => scene.add(l));

// exterior
const ext = new THREE.Group(); ext.position.set(-120, 0, 0);
const house = makeModel('efh'); house.setProgress(1); ext.add(house.group);
const lawn = new THREE.Mesh(new THREE.CircleGeometry(120, 64), std(0x8aa86a, { r: 1 })); lawn.rotation.x = -Math.PI / 2; lawn.position.y = -0.02; lawn.receiveShadow = true; ext.add(lawn);
scene.add(ext);

const camera = new THREE.PerspectiveCamera(62, 1, 0.05, 400);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enablePan = false; controls.enableDamping = true; controls.dampingFactor = 0.08;

/* ───────────── stops ───────────── */
const STOPS = {
  ext:   { room: ext, pos: [-120 + 23, 12, 27], look: [-120, 3.3, 0], orbit: true, sun: [-120 + 18, 26, 16] },
  living: { room: L.g, pos: [2.1, 1.55, 2.6], look: [-3.4, 1.0, -0.4], sun: [-6, 9, 14] },
  kitchen: { room: L.g, pos: [-0.9, 1.6, 2.2], look: [3.6, 1.0, -1.9], sun: [-6, 9, 14] },
  bedroom: { room: B.g, pos: [40 + 1.5, 1.55, 1.55], look: [40 - 1.9, 0.75, -0.3], sun: [40 + 4, 9, -14] },
  bath:  { room: C.g, pos: [80 + 1.05, 1.6, 1.05], look: [80 - 0.8, 1.15, -1.0], sun: [80 + 12, 9, 3] },
};
const ORDER = ['ext', 'living', 'kitchen', 'bedroom', 'bath'];
// info hotspots (world positions) + door hotspots that move to another room
const SPOTS = {
  living: [['info', 'floor', [-2.0, 0.03, 1.9]], ['info', 'glazing', [-2.4, 1.5, 3.2]], ['info', 'slats', [-4.4, 2.1, -0.9]], ['go', 'kitchen', [2.55, 1.3, -0.35]], ['go', 'bedroom', [4.4, 1.2, 2.6]]],
  kitchen: [['info', 'island', [2.55, 1.05, -0.35]], ['info', 'worktop', [3.6, 0.95, -2.9]], ['info', 'heating', [0.2, 0.03, 0.8]], ['go', 'living', [-2.5, 1.0, 0.4]], ['go', 'bedroom', [4.4, 1.2, 2.6]]],
  bedroom: [['info', 'accent', [40 - 2.38, 1.9, 1.3]], ['info', 'wardrobe', [40 + 1.75, 1.6, -0.6]], ['info', 'window', [40 + 0.7, 1.5, -2.2]], ['go', 'bath', [40 + 1.5, 1.1, 2.18]], ['go', 'living', [40 - 1.0, 1.1, 2.18]]],
  bath:  [['info', 'shower', [80 - 1.1, 1.5, -1.0]], ['info', 'tiles', [80 + 1.68, 0.9, -0.6]], ['info', 'vanity', [80 + 0.85, 1.0, -1.1]], ['go', 'bedroom', [80 + 0.9, 1.1, 1.48]]],
};

/* ───────────── UI ───────────── */
const ui = {
  title: document.getElementById('tourRoom'), text: document.getElementById('tourText'), step: document.getElementById('tourStep'),
  fade: stage.querySelector('.tour-fade'), start: stage.querySelector('.tour-start'), spots: stage.querySelector('.tour-spots'),
  card: stage.querySelector('.tour-card'), bar: [...document.querySelectorAll('.tour-bar button')], hint: stage.querySelector('.tour-hint'),
};
let current = null, spotEls = [];
function buildSpots(id) {
  ui.spots.innerHTML = ''; spotEls = [];
  for (const [kind, key, p] of SPOTS[id] || []) {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'tspot ' + kind;
    b.innerHTML = kind === 'go' ? `<span>${I.rooms[key].name}</span>` : '<i>+</i>';
    b.setAttribute('aria-label', kind === 'go' ? I.go + ': ' + I.rooms[key].name : I.info[key][0]);
    b.addEventListener('click', e => { e.stopPropagation(); kind === 'go' ? go(key) : showCard(key, b); });
    ui.spots.appendChild(b); spotEls.push({ el: b, v: new THREE.Vector3(...p) });
  }
}
function showCard(key, anchor) {
  const [t, d] = I.info[key]; ui.card.innerHTML = `<b>${t}</b><p>${d}</p>`; ui.card.hidden = false;
  const r = anchor.getBoundingClientRect(), s = stage.getBoundingClientRect();
  ui.card.style.left = Math.min(Math.max(r.left - s.left - 20, 12), s.width - 292) + 'px';
  ui.card.style.top = Math.min(r.bottom - s.top + 8, s.height - 160) + 'px';
}
stage.addEventListener('pointerdown', e => { if (!e.target.closest('.tour-card, .tspot')) ui.card.hidden = true; });

function applyStop(id) {
  const st = STOPS[id]; current = id;
  sun.position.set(...st.sun); sun.target.position.set(st.room.position.x, 0, 0);
  if (st.orbit) {
    const k = Math.min(1.8, Math.max(1, 1.1 / camera.aspect));
    camera.fov = 34; controls.target.set(...st.look);
    camera.position.set(...st.pos).sub(controls.target).multiplyScalar(k).add(controls.target);
    controls.minDistance = 22 * k; controls.maxDistance = 46 * k; controls.minPolarAngle = 0.6; controls.maxPolarAngle = 1.42;
    controls.enableZoom = true; controls.rotateSpeed = 0.6; controls.autoRotate = !reduce; controls.autoRotateSpeed = 0.5;
  } else {
    camera.fov = camera.aspect < 0.8 ? 84 : 66; camera.position.set(...st.pos);
    const dir = new THREE.Vector3(...st.look).sub(camera.position).normalize();
    controls.target.copy(camera.position).addScaledVector(dir, 0.12);
    controls.minDistance = controls.maxDistance = 0.12; controls.minPolarAngle = 0.55; controls.maxPolarAngle = 2.3;
    controls.enableZoom = false; controls.rotateSpeed = -0.32; controls.autoRotate = false;
  }
  camera.updateProjectionMatrix(); controls.update();
  const r = I.rooms[id]; ui.title.textContent = r.name; ui.text.textContent = r.text; ui.step.textContent = `${ORDER.indexOf(id) + 1} / ${ORDER.length}`;
  ui.bar.forEach(b => b.classList.toggle('on', b.dataset.stop === id));
  ui.start.hidden = id !== 'ext'; stage.classList.toggle('inside', id !== 'ext');
  ui.card.hidden = true; buildSpots(id);
}
let busy = false;
function go(id) {
  if (busy || id === current) return;
  if (reduce) { applyStop(id); return; }
  busy = true; ui.fade.classList.add('on');
  setTimeout(() => { applyStop(id); setTimeout(() => { ui.fade.classList.remove('on'); busy = false; }, 80); }, 380);
}
ui.bar.forEach(b => b.addEventListener('click', () => go(b.dataset.stop)));
ui.start.addEventListener('click', () => go('living'));
stage.querySelector('.tour-full').addEventListener('click', () => {
  const el = stage.closest('.tour'); if (!document.fullscreenElement) el.requestFullscreen?.(); else document.exitFullscreen?.();
});
document.addEventListener('keydown', e => {
  if (!current || e.target.closest('input, textarea')) return;
  const i = ORDER.indexOf(current);
  if (e.key === 'ArrowRight' && document.activeElement.closest?.('.tour')) go(ORDER[Math.min(i + 1, ORDER.length - 1)]);
  if (e.key === 'ArrowLeft' && document.activeElement.closest?.('.tour')) go(ORDER[Math.max(i - 1, 0)]);
});
controls.addEventListener('start', () => { ui.hint.classList.add('gone'); });

/* ───────────── loop ───────────── */
const v = new THREE.Vector3();
let lastA = 0;
function resize() {
  const w = stage.clientWidth, h = stage.clientHeight; renderer.setSize(w, h, false); camera.aspect = w / Math.max(h, 1);
  if (current && (camera.aspect < 0.8) !== (lastA < 0.8)) { const id = current; current = null; applyStop(id); }
  lastA = camera.aspect; camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(stage); resize();
let visible = true;
new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(stage);
function loop() {
  requestAnimationFrame(loop);
  if (!visible || window.__autoScrolling) return;
  controls.update(); renderer.render(scene, camera);
  const w = stage.clientWidth, h = stage.clientHeight;
  for (const s of spotEls) {
    v.copy(s.v).project(camera);
    const on = v.z < 1 && Math.abs(v.x) < 1.05 && Math.abs(v.y) < 1.05;
    s.el.style.opacity = on ? 1 : 0; s.el.style.pointerEvents = on ? 'auto' : 'none';
    s.el.style.transform = `translate(${(v.x * 0.5 + 0.5) * w}px, ${(-v.y * 0.5 + 0.5) * h}px)`;
  }
}
applyStop('ext');
stage.classList.add('ready');
loop();
window.__tour = { go, stops: ORDER };
