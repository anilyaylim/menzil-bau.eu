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
  glassDoor: new THREE.MeshStandardMaterial({ color: 0xc9d6dc, transparent: true, opacity: 0.55, roughness: 0.3, metalness: 0.1 }),
  mirror: std(0xc9d4da, { r: 0.12, m: 0.35 }), leaf: std(0x4f7a3e, { r: 0.85 }), pot: std(0xd9d3c9, { r: 0.7 }),
  glow: new THREE.MeshStandardMaterial({ color: 0xfff1d6, emissive: 0xffe2b0, emissiveIntensity: 2.2 }),
  screen: std(0x0d0e10, { r: 0.15, m: 0.2 }), art: std(0xffffff, { map: artTex(), r: 0.9 }),
  tileWall: std(0xffffff, { map: tileTex('#d9d6d1', '#c9c5bf', 4, 5, 9), r: 0.35 }),
  tileFloor: std(0xffffff, { map: tileTex('#6b6862', '#55524d', 3, 8, 21), r: 0.5 }),
  hallTile: std(0xffffff, { map: tileTex('#cbc6be', '#b3ada4', 2, 6, 31), r: 0.4 }),
  anthDoor: std(0x33373d, { r: 0.5, m: 0.3 }), red: std(0xb3000a, { r: 0.6 }), kidsWall: std(0xa9bfcb, { r: 0.95 }),
  kidsDuvet: std(0xffffff, { map: fabricTex('#e2ad4b'), r: 0.95 }), rugKids: std(0xffffff, { map: fabricTex('#d6cfc3'), r: 1 }),
};
[M.wall, M.ceil, M.accent, M.kidsWall].forEach(m => { m.shadowSide = THREE.DoubleSide; });

/* ───────────── geometry helpers ───────────── */
function mesh(geo, mat, x, y, z, { cast = true, receive = true, ry = 0 } = {}) {
  const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.rotation.y = ry; m.castShadow = cast; m.receiveShadow = receive; return m;
}
// box with its BOTTOM at y
const box = (g, w, h, d, mat, x, y, z, o) => g.add(mesh(new THREE.BoxGeometry(w, h, d), mat, x, y + h / 2, z, o));
const rbox = (g, w, h, d, r, mat, x, y, z, o) => g.add(mesh(new RoundedBoxGeometry(w, h, d, 4, Math.min(r, w / 2, h / 2, d / 2)), mat, x, y + h / 2, z, o));
const cyl = (g, rt, rb, h, mat, x, y, z, seg = 28, o) => g.add(mesh(new THREE.CylinderGeometry(rt, rb, h, seg), mat, x, y + h / 2, z, o));

/* ───────────── rooms ───────────── */
// point lights are collected per room; a small fixed pool is re-used per stop (no shader recompiles)
const lights = []; let curRoom = null;
function addLight(g, color, intensity, x, y, z) {
  const p = new THREE.PointLight(color, intensity, 0, 2); p.position.set(x, y, z);
  g.updateWorldMatrix(true, false); g.localToWorld(p.position); p.userData.room = curRoom; lights.push(p); return p;
}
function room({ ox, w, d, h = 2.8, floor, wall = M.wall, windows = [], doors = [], wallMat = {}, landscape = 1 }) {
  const g = new THREE.Group(); g.position.x = ox; curRoom = g;
  const fl = floor.clone(); if (fl.map) { fl.map = fl.map.clone(); fl.map.needsUpdate = true; fl.map.repeat.set(w / 2.2, d / 2.2); }
  const f = mesh(new THREE.PlaneGeometry(w, d), fl, 0, 0, 0, { cast: false }); f.rotation.x = -Math.PI / 2; g.add(f);
  const c = mesh(new THREE.PlaneGeometry(w, d), M.ceil, 0, h, 0); c.rotation.x = Math.PI / 2; g.add(c);
  const F = {
    n: { r: 0, o: [0, -d / 2], u: [1, 0], n: [0, 1], L: w, flip: 1 }, s: { r: Math.PI, o: [0, d / 2], u: [-1, 0], n: [0, -1], L: w, flip: -1 },
    e: { r: -Math.PI / 2, o: [w / 2, 0], u: [0, 1], n: [-1, 0], L: d, flip: 1 }, w: { r: Math.PI / 2, o: [-w / 2, 0], u: [0, -1], n: [1, 0], L: d, flip: -1 },
  };
  // place(obj, side, c, y, t): c = room x (n/s) or z (e/w); t > 0 = into the room
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
    part(s, 0, 0, 0.008, L - 0.02, 0.07, 0.016, M.white, false);   // skirting
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
  for (const dr of doors) {   // closed interior doors (visual); glass = frosted glass door
    part(dr.s, dr.c, 0, 0.02, 0.98, 2.12, 0.04, dr.glass ? M.glassDoor : M.white, !dr.glass);
    if (dr.glass) { part(dr.s, dr.c, 0.08, 0.045, 0.9, 0.03, 0.012, M.anth, false); part(dr.s, dr.c, 2.02, 0.045, 0.9, 0.03, 0.012, M.anth, false); part(dr.s, dr.c - 0.44, 0.08, 0.045, 0.03, 1.97, 0.012, M.anth, false); part(dr.s, dr.c + 0.44, 0.08, 0.045, 0.03, 1.97, 0.012, M.anth, false); }
    part(dr.s, dr.c, 2.12, 0.02, 1.1, 0.06, 0.05, M.white); part(dr.s, dr.c - 0.52, 0, 0.02, 0.06, 2.12, 0.05, M.white); part(dr.s, dr.c + 0.52, 0, 0.02, 0.06, 2.12, 0.05, M.white);
    part(dr.s, dr.c + 0.36 * (dr.hand || 1), 1.02, 0.07, 0.14, 0.02, 0.03, M.anth);
  }
  // world position of a door hotspot
  const door = (s, cc, y = 1.3) => { const W = ox; return s === 'n' ? [W + cc, y, -d / 2 + 0.12] : s === 's' ? [W + cc, y, d / 2 - 0.12] : s === 'e' ? [W + w / 2 - 0.12, y, cc] : [W - w / 2 + 0.12, y, cc]; };
  return { g, place, part, door, w, d, h };
}
function pendant(g, x, z, h, drop = 0.9, r = 0.14, light = true) {
  cyl(g, 0.004, 0.004, drop, M.anth, x, h - drop, z, 6, { cast: false });
  cyl(g, r * 0.35, r, r * 0.9, M.anth, x, h - drop - r * 0.9, z);
  cyl(g, r * 0.92, r * 0.92, 0.01, M.glow, x, h - drop - r * 0.9 - 0.005, z, 28, { cast: false });
  if (light) addLight(g, 0xffe0b8, 2.6, x, h - drop - r - 0.08, z);
}
function downlight(g, x, z, h = 2.8, light = false, I0 = 1.6) {
  cyl(g, 0.07, 0.07, 0.008, M.glow, x, h - 0.009, z, 20, { cast: false });
  if (light) addLight(g, 0xfff0dc, I0, x, h - 0.25, z);
}
function plant(g, x, z, s = 1) {
  cyl(g, 0.2 * s, 0.16 * s, 0.42 * s, M.pot, x, 0, z);
  const r = rng(Math.round(x * 100 + z * 10));
  for (let k = 0; k < 14; k++) {
    const leaf = mesh(new THREE.SphereGeometry(0.12 * s, 8, 6), M.leaf, x + (r() - 0.5) * 0.4 * s, 0.55 * s + r() * 0.75 * s, z + (r() - 0.5) * 0.4 * s);
    leaf.scale.set(1.6, 0.35, 0.8); leaf.rotation.set(r() * 1.2, r() * 6, r() * 1.2); g.add(leaf);
  }
}
function art(R, s, c, y, w, hh) { R.part(s, c, y, 0.02, w, hh, 0.03, M.anth); R.part(s, c, y + 0.04, 0.04, w - 0.08, hh - 0.08, 0.01, M.art, false); }

/* ───────── entrance hall ───────── */
const H = room({ ox: 100, w: 3.0, d: 4.4, floor: M.hallTile, landscape: 13,
  windows: [{ s: 's', c: 0.62, w: 0.5, h: 2.25, y: 0 }], doors: [{ s: 'n', c: 0.25, glass: true }] });
{
  const g = H.g;
  // front door (anthracite, with glass strip and long handle)
  H.part('s', -0.35, 0, 0.0, 1.16, 2.28, 0.06, M.anth); H.part('s', -0.35, 0, 0.012, 1.04, 2.2, 0.06, M.anthDoor);
  H.part('s', -0.35 + 0.3, 0.35, 0.05, 0.12, 1.6, 0.01, M.frosted, false);
  H.part('s', -0.35 - 0.36, 0.7, 0.09, 0.03, 1.0, 0.03, M.chrome);
  box(g, 1.0, 0.012, 0.6, M.rugDark, -0.35, 0, 1.75, { cast: false });
  // cloakroom cabinet (west, north part) + bench with hooks
  box(g, 0.5, 2.5, 1.7, M.white, -1.5 + 0.25, 0, -1.35);
  for (const z of [-1.92, -1.35, -0.78]) box(g, 0.01, 2.46, 0.006, M.anth, -1.5 + 0.505, 0.02, z + 0.28, { cast: false });
  box(g, 0.02, 0.7, 0.02, M.anth, -0.99, 0.9, -1.1);
  rbox(g, 0.4, 0.42, 1.2, 0.02, M.oak, -1.3, 0, 0.55); rbox(g, 0.38, 0.06, 1.15, 0.03, M.sofaDark, -1.3, 0.42, 0.55);
  H.part('w', -0.55, 1.62, 0.02, 1.2, 0.08, 0.03, M.oak);
  for (const z of [0.1, 0.4, 0.7, 1.0]) box(g, 0.08, 0.02, 0.02, M.anth, -1.44, 1.66, z);
  box(g, 0.28, 0.12, 0.26, M.oakDark, -1.25, 0, 1.45); box(g, 0.28, 0.12, 0.26, M.anth, -1.25, 0, 1.15);   // shoes
  // console + round mirror (east)
  box(g, 0.32, 0.05, 1.1, M.oak, 1.5 - 0.16, 0.85, -0.4);
  const mir = mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.02, 48), M.mirror, 1.5 - 0.02, 1.55, -0.4, { cast: false }); mir.rotation.z = Math.PI / 2; g.add(mir);
  const rim = mesh(new THREE.TorusGeometry(0.42, 0.012, 8, 48), M.oakDark, 1.5 - 0.025, 1.55, -0.4, { cast: false }); rim.rotation.y = Math.PI / 2; g.add(rim);
  cyl(g, 0.07, 0.05, 0.22, M.pot, 1.36, 0.9, -0.7); box(g, 0.18, 0.03, 0.12, M.oakDark, 1.36, 0.9, -0.15);
  plant(g, 1.12, 1.75, 0.9);
  for (const z of [-1.2, 0.4]) downlight(g, 0, z, 2.8, true, 1.8);
  downlight(g, 0, 1.6);
}

/* ───────── hallway / corridor ───────── */
const FL = room({ ox: 140, w: 1.9, d: 8, floor: M.oak, landscape: 17,
  windows: [{ s: 'n', c: 0, w: 0.9, h: 1.7, y: 0.5 }],
  doors: [{ s: 's', c: 0, glass: true }, { s: 'w', c: -2.9 }, { s: 'w', c: -0.6, hand: -1 }, { s: 'e', c: -2.5 }, { s: 'e', c: -0.2, hand: -1 }] });
{
  const g = FL.g;
  box(g, 0.9, 0.012, 6.2, M.rug, 0, 0, -0.2, { cast: false });
  art(FL, 'e', -1.35, 1.15, 0.6, 0.8); art(FL, 'w', -1.75, 1.3, 0.5, 0.5);
  plant(g, 0.55, -3.55, 0.95);
  for (const z of [-3.0, -1.4, 0.2, 1.8, 3.2]) downlight(g, 0, z, 2.8, z === -1.4 || z === 1.8, 1.7);
}

/* ───────── living room ───────── */
const L = room({ ox: 0, w: 5.4, d: 6.5, floor: M.oak, landscape: 2,
  windows: [{ s: 's', c: -0.6, w: 3.2, h: 2.45, y: 0 }, { s: 's', c: 1.95, w: 1.0, h: 2.45, y: 0 }],
  doors: [{ s: 'n', c: 1.8 }] });
{
  const g = new THREE.Group(); g.position.x = 1.8; L.g.add(g);   // furniture laid out for the old open plan, shifted
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
  for (let z = -1.6; z <= 2.0; z += 0.09) box(g, 0.035, 2.8, 0.05, M.oak, -4.47, 0, z, { cast: false });
  rbox(g, 0.44, 0.42, 2.6, 0.02, M.white, -4.24, 0.2, 0.35);
  box(g, 0.03, 0.72, 1.28, M.screen, -4.4, 1.05, 0.35);
  plant(g, -4.05, 2.75, 1.25);
  cyl(g, 0.15, 0.17, 0.03, M.anth, -0.5, 0, 2.55); cyl(g, 0.012, 0.012, 1.45, M.anth, -0.5, 0.03, 2.55, 8);
  cyl(g, 0.17, 0.22, 0.3, M.linen, -0.5, 1.45, 2.55); addLight(g, 0xffd9a8, 1.6, -0.5, 1.5, 2.55);
  pendant(g, -2.55, 0.35, 2.8, 0.25, 0.32, true);
  // reading corner + sideboard (east part)
  const a = L.g;
  rbox(a, 0.8, 0.42, 0.8, 0.08, M.sofaDark, 1.85, 0.05, -1.75, { ry: -0.5 }); rbox(a, 0.8, 0.5, 0.18, 0.06, M.sofaDark, 2.02, 0.42, -2.05, { ry: -0.5 });
  for (const [dx, dz] of [[-0.3, -0.3], [0.3, -0.3], [-0.3, 0.3], [0.3, 0.3]]) cyl(a, 0.02, 0.015, 0.06, M.anth, 1.85 + dx * 0.9, 0, -1.75 + dz * 0.9, 8);
  cyl(a, 0.22, 0.22, 0.03, M.oak, 1.0, 0.5, -2.35, 32); cyl(a, 0.02, 0.02, 0.5, M.anth, 1.0, 0, -2.35, 8);
  art(L, 'e', 0.6, 1.1, 0.9, 1.1);
}

/* ───────── kitchen (own room, with dining) ───────── */
const K = room({ ox: 20, w: 5.6, d: 5.2, floor: M.oak, landscape: 21,
  windows: [{ s: 'n', c: 0.9, w: 1.7, h: 0.95, y: 1.12 }, { s: 'w', c: 1.7, w: 1.6, h: 1.55, y: 0.65 }],
  doors: [{ s: 's', c: 1.8 }] });
{
  const g = K.g, kx0 = -1.0, kx1 = 2.8, kl = kx1 - kx0, kc = (kx0 + kx1) / 2, kz = -2.6 + 0.32;
  box(g, kl, 0.1, 0.56, M.anth, kc, 0, kz - 0.02); box(g, kl, 0.76, 0.62, M.white, kc, 0.1, kz);
  box(g, kl + 0.02, 0.04, 0.65, M.stone, kc, 0.86, kz);
  for (let x = kx0 + 0.6; x < kx1; x += 0.6) box(g, 0.006, 0.74, 0.01, M.anth, x, 0.11, kz + 0.31, { cast: false });
  box(g, 0.5, 0.012, 0.36, M.black, 0.9, 0.893, kz);
  cyl(g, 0.016, 0.02, 0.3, M.chrome, 0.9, 0.9, kz - 0.22, 12); box(g, 0.025, 0.025, 0.2, M.chrome, 0.9, 1.18, kz - 0.14);
  box(g, 1.1, 0.03, 0.26, M.oak, -0.45, 1.55, -2.6 + 0.13); box(g, 0.9, 0.03, 0.26, M.oak, 2.25, 1.55, -2.6 + 0.13);
  for (const x of [-0.75, -0.45]) cyl(g, 0.05, 0.05, 0.14, M.pot, x, 1.58, -2.47); cyl(g, 0.09, 0.09, 0.03, M.oakDark, 2.2, 1.58, -2.47);
  // tall units on the east wall
  box(g, 0.62, 2.4, 1.8, M.white, 2.8 - 0.31, 0, -0.96);
  box(g, 0.01, 0.58, 0.58, M.black, 2.8 - 0.62, 0.9, -1.4); box(g, 0.01, 0.42, 0.58, M.black, 2.8 - 0.62, 1.52, -1.4);
  box(g, 0.006, 2.36, 0.01, M.anth, 2.8 - 0.625, 0.02, -1.1, { cast: false });
  // island
  rbox(g, 1.9, 0.86, 0.95, 0.02, M.oak, 0.35, 0, 0.5); rbox(g, 2.1, 0.045, 1.1, 0.01, M.stone, 0.35, 0.86, 0.5);
  box(g, 0.62, 0.008, 0.48, M.black, 0.1, 0.905, 0.3);
  for (const x of [-0.25, 0.35, 0.95]) {
    cyl(g, 0.2, 0.2, 0.06, M.sofaDark, x, 0.64, 1.27);
    for (const [dx, dz] of [[-0.13, -0.13], [0.13, -0.13], [-0.13, 0.13], [0.13, 0.13]]) cyl(g, 0.01, 0.012, 0.64, M.anth, x + dx, 0, 1.27 + dz, 8);
    cyl(g, 0.15, 0.15, 0.012, M.anth, x, 0.24, 1.27, 20);
  }
  for (const x of [-0.25, 0.35, 0.95]) pendant(g, x, 0.5, 2.8, 0.95, 0.12, x === 0.35);
  // dining by the west window
  const tx = -1.85, tz = 1.6;
  cyl(g, 0.6, 0.6, 0.04, M.oak, tx, 0.72, tz, 48); cyl(g, 0.05, 0.05, 0.72, M.anth, tx, 0, tz, 12); cyl(g, 0.3, 0.3, 0.02, M.anth, tx, 0, tz, 24);
  for (let k = 0; k < 4; k++) {
    const a = k * Math.PI / 2 + Math.PI / 4, x = tx + Math.cos(a) * 0.78, z = tz + Math.sin(a) * 0.78;
    rbox(g, 0.44, 0.06, 0.44, 0.03, M.sofa, x, 0.44, z, { ry: -a });
    const bk = mesh(new RoundedBoxGeometry(0.44, 0.38, 0.05, 3, 0.02), M.sofa, x + Math.cos(a) * 0.2, 0.69, z + Math.sin(a) * 0.2); bk.rotation.y = -a + Math.PI / 2; bk.castShadow = true; g.add(bk);
    for (const [dx, dz] of [[-0.16, -0.16], [0.16, -0.16], [-0.16, 0.16], [0.16, 0.16]]) cyl(g, 0.012, 0.012, 0.44, M.anth, x + dx, 0, z + dz, 8);
  }
  cyl(g, 0.08, 0.06, 0.2, M.pot, tx, 0.76, tz);
  pendant(g, tx, tz, 2.8, 1.05, 0.22, true);
  plant(g, -2.35, -0.6, 1.1);
}

/* ───────── children's room ───────── */
const KR = room({ ox: 60, w: 3.8, d: 3.6, floor: M.oak, landscape: 29,
  windows: [{ s: 'n', c: 0.5, w: 1.4, h: 1.4, y: 0.8 }], doors: [{ s: 's', c: 1.2 }], wallMat: { w: M.kidsWall } });
{
  const g = KR.g, bx = -1.35, bz = 0.45;
  rbox(g, 1.0, 0.28, 2.05, 0.03, M.oak, bx, 0.05, bz); rbox(g, 0.95, 0.18, 1.98, 0.06, M.linen, bx, 0.33, bz);
  rbox(g, 0.97, 0.08, 1.4, 0.03, M.kidsDuvet, bx, 0.48, bz + 0.3); rbox(g, 0.6, 0.12, 0.36, 0.05, M.linen, bx, 0.5, bz - 0.75);
  rbox(g, 1.02, 0.7, 0.06, 0.02, M.oak, bx, 0.05, bz - 1.03);
  for (const [x, z, c] of [[-1.55, 0.95, M.red], [-1.2, 1.15, M.kidsDuvet]]) rbox(g, 0.2, 0.2, 0.08, 0.04, c, x, 0.54, z, { ry: 0.3 });
  // desk under the window
  box(g, 1.2, 0.04, 0.6, M.oak, 0.5, 0.72, -1.48);
  for (const [dx, dz] of [[-0.56, -0.26], [0.56, -0.26], [-0.56, 0.26], [0.56, 0.26]]) box(g, 0.03, 0.72, 0.03, M.anth, 0.5 + dx, 0, -1.48 + dz);
  rbox(g, 0.42, 0.06, 0.42, 0.03, M.red, 0.5, 0.44, -0.95); rbox(g, 0.42, 0.34, 0.05, 0.02, M.red, 0.5, 0.5, -0.75);
  cyl(g, 0.15, 0.15, 0.02, M.anth, 0.5, 0, -0.95, 20); cyl(g, 0.02, 0.02, 0.44, M.anth, 0.5, 0.02, -0.95, 8);
  cyl(g, 0.06, 0.07, 0.02, M.anth, 0.05, 0.76, -1.6); cyl(g, 0.008, 0.008, 0.38, M.anth, 0.05, 0.78, -1.6, 6); cyl(g, 0.05, 0.09, 0.1, M.white, 0.05, 1.12, -1.6);
  box(g, 0.24, 0.03, 0.32, M.white, 0.75, 0.76, -1.5); box(g, 0.2, 0.025, 0.28, M.kidsDuvet, 0.78, 0.79, -1.52);
  // shelf with toy bins (east wall)
  box(g, 0.36, 1.1, 1.5, M.white, 1.9 - 0.18, 0, 0.35);
  const bins = [M.red, M.kidsDuvet, M.kidsWall, M.sofaDark, M.throw, M.kidsWall];
  bins.forEach((m, i) => box(g, 0.3, 0.3, 0.42, m, 1.9 - 0.2, 0.08 + (i % 2) * 0.5, -0.12 + Math.floor(i / 2) * 0.48));
  cyl(g, 0.12, 0.12, 0.25, M.kidsDuvet, 1.72, 1.1, 0.0, 20); rbox(g, 0.2, 0.2, 0.2, 0.03, M.red, 1.72, 1.1, 0.6);
  cyl(g, 0.85, 0.85, 0.012, M.rugKids, 0.15, 0, 0.55, 48, { cast: false });
  rbox(g, 0.22, 0.22, 0.22, 0.03, M.kidsWall, 0.4, 0.012, 0.75, { ry: 0.4 }); rbox(g, 0.16, 0.16, 0.16, 0.03, M.red, 0.62, 0.012, 0.6, { ry: 0.9 });
  art(KR, 'w', 0.45, 1.25, 0.7, 0.55);
  pendant(g, 0, 0.2, 2.8, 0.6, 0.2, true);
}

/* ───────── master bedroom ───────── */
const B = room({ ox: 40, w: 4.8, d: 4.4, floor: M.oak, landscape: 5,
  windows: [{ s: 'n', c: 0.7, w: 1.8, h: 1.6, y: 0.65 }], doors: [{ s: 's', c: -0.2 }, { s: 'e', c: 1.55, hand: -1 }], wallMat: { w: M.accent } });
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
  addLight(g, 0xffd8a6, 1.2, bx + 0.3, 0.95, -1.4);
  box(g, 0.64, 2.5, 2.6, M.white, 2.4 - 0.32, 0, -0.55);
  for (const z of [-1.2, -0.55, 0.1]) box(g, 0.006, 2.46, 0.01, M.anth, 2.4 - 0.645, 0.02, z + 0.32, { cast: false });
  for (const z of [-1.0, -0.12]) box(g, 0.02, 0.5, 0.02, M.anth, 2.4 - 0.65, 0.95, z);
  plant(g, -0.45, -1.8, 1.0);
  B.part('w', 0, 1.55, 0.02, 1.5, 0.6, 0.03, M.anth); B.part('w', 0, 1.58, 0.035, 1.42, 0.54, 0.01, M.art, false);
  cyl(g, 0.3, 0.3, 0.04, M.glow, 0, 2.76, 0, 32, { cast: false });
  addLight(g, 0xffe6c4, 1.5, 0, 2.5, 0);
}

/* ───────── en-suite bathroom ───────── */
const C = room({ ox: 80, w: 3.4, d: 3.0, floor: M.tileFloor, wall: M.tileWall, landscape: 9,
  windows: [{ s: 'e', c: 0.4, w: 0.9, h: 0.8, y: 1.45, frosted: true }], doors: [{ s: 's', c: 0.9 }] });
{
  const g = C.g;
  box(g, 0.012, 2.0, 1.0, M.glass, -0.55, 0.0, -1.0, { cast: false });
  box(g, 0.02, 0.02, 1.0, M.chrome, -0.55, 2.0, -1.0);
  box(g, 0.05, 0.02, 0.4, M.chrome, -1.55, 2.2, -1.1); cyl(g, 0.16, 0.16, 0.015, M.chrome, -1.32, 2.18, -1.1, 32);
  box(g, 0.7, 0.006, 0.05, M.chrome, -1.1, 0.003, -0.6, { cast: false });
  C.part('n', -1.3, 1.2, 0.04, 0.6, 0.3, 0.08, M.tileWall);
  rbox(g, 1.2, 0.42, 0.5, 0.02, M.oak, 0.85, 0.45, -1.25);
  box(g, 1.22, 0.03, 0.52, M.stone, 0.85, 0.87, -1.25);
  cyl(g, 0.21, 0.18, 0.13, M.white, 0.85, 0.9, -1.22, 40);
  cyl(g, 0.014, 0.014, 0.3, M.chrome, 0.85, 0.9, -1.45, 12); box(g, 0.02, 0.02, 0.16, M.chrome, 0.85, 1.19, -1.38);
  C.part('n', 0.85, 1.25, 0.012, 0.95, 0.8, 0.02, M.mirror, false);
  C.part('n', 0.85, 2.1, 0.03, 0.8, 0.03, 0.04, M.glow, false);
  C.part('w', 0.65, 0.3, 0.04, 0.5, 0.9, 0.12, M.tileWall);
  rbox(g, 0.55, 0.36, 0.37, 0.12, M.white, -1.7 + 0.38, 0.4, 0.65);
  C.part('w', 0.65, 1.0, 0.105, 0.2, 0.14, 0.01, M.chrome, false);
  for (let k = 0; k < 9; k++) C.part('s', -0.6, 0.35 + k * 0.13, 0.06, 0.55, 0.025, 0.03, M.anth);
  C.part('s', -0.6 - 0.27, 0.33, 0.06, 0.03, 1.2, 0.03, M.anth); C.part('s', -0.6 + 0.27, 0.33, 0.06, 0.03, 1.2, 0.03, M.anth);
  rbox(g, 0.5, 0.012, 0.75, 0.005, M.rugDark, 0.85, 0, -0.6, { cast: false });
  plant(g, 1.4, 1.15, 0.7);
  cyl(g, 0.22, 0.22, 0.03, M.glow, 0, 2.77, 0, 32, { cast: false });
  addLight(g, 0xfff0dc, 1.8, 0, 2.45, 0);
}
const ROOMS = [H.g, FL.g, L.g, K.g, KR.g, B.g, C.g];

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
scene.add(...ROOMS);
// fixed pool of point lights, filled per room on each stop
const POOL = Math.max(...ROOMS.map(r => lights.filter(l => l.userData.room === r).length));
const pool = Array.from({ length: POOL }, () => { const p = new THREE.PointLight(0xffffff, 0, 0, 2); scene.add(p); return p; });
function useLights(r) {
  const ls = lights.filter(l => l.userData.room === r);
  pool.forEach((p, i) => { const l = ls[i]; if (l) { p.position.copy(l.position); p.color.copy(l.color); p.intensity = l.intensity; } else p.intensity = 0; });
}

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
  ext:     { room: ext, pos: [-120 + 23, 12, 27], look: [-120, 3.3, 0], orbit: true, sun: [-120 + 18, 26, 16] },
  hall:    { room: H.g, pos: [100 + 0.75, 1.6, 1.95], look: [100 - 0.15, 1.15, -1.9], sun: [100 + 3, 9, 14] },
  corridor: { room: FL.g, pos: [140, 1.6, 2.4], look: [140, 1.25, -3.8], sun: [140 + 2, 9, -14], sunI: 0 },
  living:  { room: L.g, pos: [2.25, 1.6, 1.35], look: [-2.3, 1.0, -0.1], sun: [-6, 9, 14] },
  kitchen: { room: K.g, pos: [20 + 1.9, 1.6, 2.15], look: [20 - 0.6, 1.0, -1.7], sun: [20 - 12, 9, -6] },
  kids:    { room: KR.g, pos: [60 + 1.05, 1.5, 1.25], look: [60 - 1.3, 0.8, -0.7], sun: [60 + 4, 9, -14] },
  bedroom: { room: B.g, pos: [40 + 1.0, 1.55, 1.6], look: [40 - 1.9, 0.75, -0.3], sun: [40 + 4, 9, -14] },
  bath:    { room: C.g, pos: [80 + 1.05, 1.6, 1.05], look: [80 - 0.8, 1.15, -1.0], sun: [80 + 12, 9, 3] },
};
const ORDER = ['ext', 'hall', 'corridor', 'living', 'kitchen', 'kids', 'bedroom', 'bath'];
// where the back button leads from each room
const PARENT = { hall: 'ext', corridor: 'hall', living: 'corridor', kitchen: 'corridor', kids: 'corridor', bedroom: 'corridor', bath: 'bedroom' };
// info hotspots (world positions) + door hotspots that move to another room
const SPOTS = {
  hall: [['info', 'frontdoor', [100 - 0.35, 1.5, 2.1]], ['info', 'cloak', [100 - 1.0, 1.7, -1.35]], ['info', 'hallfloor', [100 + 0.3, 0.03, 0.2]],
    ['go', 'corridor', H.door('n', 0.25)], ['go', 'ext', H.door('s', -0.35, 1.1)]],
  corridor: [['info', 'doors', [140 - 0.85, 1.9, -0.6]], ['info', 'spots', [140, 2.74, -1.4]],
    ['go', 'living', FL.door('w', -2.9, 1.75)], ['go', 'kitchen', FL.door('w', -0.6, 1.0)], ['go', 'kids', FL.door('e', -2.5, 1.75)], ['go', 'bedroom', FL.door('e', -0.2, 1.0)], ['go', 'hall', FL.door('s', 0)]],
  living: [['info', 'floor', [-0.2, 0.03, 1.9]], ['info', 'glazing', [-0.6, 1.5, 3.2]], ['info', 'slats', [-2.6, 2.1, -0.9]], ['go', 'corridor', L.door('n', 1.8)]],
  kitchen: [['info', 'island', [20 + 0.35, 1.05, 0.5]], ['info', 'worktop', [20 + 2.0, 0.95, -2.35]], ['info', 'heating', [20 + 0.9, 0.03, 1.95]], ['go', 'corridor', K.door('s', 1.8)]],
  kids: [['info', 'paint', [60 - 1.85, 2.0, -0.7]], ['info', 'desk', [60 + 0.5, 0.85, -1.5]], ['go', 'corridor', KR.door('s', 1.2)]],
  bedroom: [['info', 'accent', [40 - 2.38, 1.9, 1.3]], ['info', 'wardrobe', [40 + 1.75, 1.6, -0.6]], ['info', 'window', [40 + 0.7, 1.5, -2.2]], ['go', 'bath', B.door('e', 1.55)], ['go', 'corridor', B.door('s', -0.2)]],
  bath:  [['info', 'shower', [80 - 1.1, 1.5, -1.0]], ['info', 'tiles', [80 + 1.68, 0.9, -0.6]], ['info', 'vanity', [80 + 0.85, 1.0, -1.1]], ['go', 'bedroom', C.door('s', 0.9)]],
};

/* ───────────── UI ───────────── */
const ui = {
  title: document.getElementById('tourRoom'), text: document.getElementById('tourText'), step: document.getElementById('tourStep'),
  back: stage.querySelector('.tour-back'), backLabel: stage.querySelector('.tour-back span'),
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
  sun.position.set(...st.sun); sun.intensity = st.sunI ?? 3.2; sun.target.position.set(st.room.position.x, 0, 0);
  ext.visible = st.room === ext; ROOMS.forEach(r => { r.visible = r === st.room; }); useLights(st.room);
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
  const par = PARENT[id]; ui.back.hidden = !par; if (par) ui.backLabel.textContent = I.rooms[par].name;
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
ui.start.addEventListener('click', () => go('hall'));
ui.back.addEventListener('click', () => PARENT[current] && go(PARENT[current]));
stage.querySelector('.tour-full').addEventListener('click', () => {
  const el = stage.closest('.tour'); if (!document.fullscreenElement) el.requestFullscreen?.(); else document.exitFullscreen?.();
});
document.addEventListener('keydown', e => {
  if (!current || e.target.closest('input, textarea')) return;
  const i = ORDER.indexOf(current);
  if (e.key === 'ArrowRight' && document.activeElement.closest?.('.tour')) go(ORDER[Math.min(i + 1, ORDER.length - 1)]);
  if (e.key === 'ArrowLeft' && document.activeElement.closest?.('.tour')) go(ORDER[Math.max(i - 1, 0)]);
  if ((e.key === 'Escape' || e.key === 'Backspace') && PARENT[current] && document.activeElement.closest?.('.tour') && !document.fullscreenElement) go(PARENT[current]);
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
