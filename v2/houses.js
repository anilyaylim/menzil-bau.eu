/* MENZIL-BAU v2 · procedural 3D house models (Three.js)
   - makeModel(type): 'efh' | 'dh' | 'mfh'  → { group, setProgress(p) }
   - every part is registered with an order; setProgress(0..1) assembles the building
     (foundation → walls → slabs → roof → windows), a blueprint wireframe fades out. */
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const C = {
  wall: 0xF3F0EA, wall2: 0xDCD6CC, ochre: 0xD99A2B, plaster: 0xE9E4DA,
  roofRed: 0xA3241C, roofDark: 0x2E3238, glass: 0x23384A, frame: 0xFFFFFF,
  slab: 0x9EA3A8, ground: 0xD9D3C8, wood: 0x8A6A45, rail: 0x1C1F24, green: 0x7D9A62, gold: 0xB08D57,
};
const mat = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: o.r ?? 0.85, metalness: o.m ?? 0, ...(o.extra || {}) });
const ease = t => 1 - Math.pow(1 - Math.min(Math.max(t, 0), 1), 3);
const back = t => { t = Math.min(Math.max(t, 0), 1); const s = 1.4; return 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2); };

function Builder() {
  const group = new THREE.Group();
  const ghost = new THREE.Group();       // blueprint wireframe
  const parts = [];
  let maxOrder = 0;
  const ghostMat = new THREE.LineBasicMaterial({ color: C.gold, transparent: true, opacity: 0.9 });
  const edgeMat = new THREE.LineBasicMaterial({ color: 0x1C1F24, transparent: true, opacity: 0.18 });

  // add a mesh whose pivot sits at its bottom centre; mode: 'grow' (scale y), 'drop' (fall in), 'pop' (scale all)
  function add(geo, material, pos, order, mode = 'grow', opts = {}) {
    const mesh = new THREE.Mesh(geo, material);
    mesh.castShadow = opts.shadow !== false; mesh.receiveShadow = true;
    geo.computeBoundingBox();
    const bb = geo.boundingBox; mesh.position.y = -bb.min.y;
    const pivot = new THREE.Group(); pivot.add(mesh);
    pivot.position.set(pos[0], pos[1], pos[2]);
    if (opts.rot) pivot.rotation.y = opts.rot;
    if (opts.edges !== false) {
      const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), edgeMat); e.position.copy(mesh.position); pivot.add(e);
      const g = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), ghostMat); g.position.copy(mesh.position);
      const gp = new THREE.Group(); gp.position.copy(pivot.position); gp.rotation.copy(pivot.rotation); gp.add(g); ghost.add(gp);
    }
    group.add(pivot);
    parts.push({ pivot, order, mode, baseY: pos[1] });
    maxOrder = Math.max(maxOrder, order);
    return pivot;
  }
  function box(w, h, d) { return new THREE.BoxGeometry(w, h, d); }
  function gable(w, h, d) { // triangular prism, ridge along z
    const s = new THREE.Shape(); s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(0, h); s.lineTo(-w / 2, 0);
    const g = new THREE.ExtrudeGeometry(s, { depth: d, bevelEnabled: false }); g.translate(0, 0, -d / 2); return g;
  }
  function hip(w, h, d, ridge) { // hipped roof: every face wound outward, flat normals
    const x = w / 2, z = d / 2, r = ridge / 2;
    const P = [[-x, 0, -z], [x, 0, -z], [x, 0, z], [-x, 0, z], [-r, h, 0], [r, h, 0]];
    const tris = [[0, 1, 5], [0, 5, 4], [2, 3, 4], [2, 4, 5], [1, 2, 5], [3, 0, 4], [0, 2, 1], [0, 3, 2]];
    const c = new THREE.Vector3(0, h * 0.35, 0), pos = [];
    const A = new THREE.Vector3(), Bv = new THREE.Vector3(), Cv = new THREE.Vector3(), n = new THREE.Vector3(), m = new THREE.Vector3();
    for (const t of tris) {
      A.fromArray(P[t[0]]); Bv.fromArray(P[t[1]]); Cv.fromArray(P[t[2]]);
      n.subVectors(Bv, A).cross(m.subVectors(Cv, A));
      m.copy(A).add(Bv).add(Cv).divideScalar(3).sub(c);           // centroid direction from inside
      const tri = n.dot(m) < 0 ? [A, Cv, Bv] : [A, Bv, Cv];        // flip if it points inward
      for (const v of tri) pos.push(v.x, v.y, v.z);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals(); return g;
  }
  function setProgress(p) {
    const n = maxOrder + 1;
    for (const part of parts) {
      const t = p * (n + 0.6) - part.order;
      const k = ease(t);
      if (part.mode === 'grow') { part.pivot.scale.set(1, Math.max(k, 0.0001), 1); part.pivot.visible = t > 0; }
      else if (part.mode === 'drop') { part.pivot.position.y = part.baseY + (1 - ease(t)) * 6; part.pivot.visible = t > 0; part.pivot.scale.setScalar(1); }
      else { const b = back(t); part.pivot.scale.setScalar(Math.max(b, 0.0001)); part.pivot.visible = t > 0; }
    }
    ghostMat.opacity = Math.max(0, 0.9 - p * 1.6);
    ghost.visible = ghostMat.opacity > 0.01;
  }
  return { group, ghost, add, box, gable, hip, setProgress };
}

// windows along a facade at explicit positions (xs); rotY = side facade
function windows(B, { xs, y, z, w = 1.2, h = 1.4, order, rotY = 0, frameColor = C.frame, d = 0.12 }) {
  const glass = mat(C.glass, { r: 0.15, m: 0.3 });
  const frame = mat(frameColor, { r: 0.6 });
  for (const x of xs) {
    const pos = rotY ? [z, y, x] : [x, y, z];
    B.add(B.box(w + 0.16, h + 0.16, d * 0.6), frame, pos, order, 'pop', { edges: false, rot: rotY });
    const gpos = rotY ? [z + (z > 0 ? 0.04 : -0.04), y + 0.08, x] : [x, y + 0.08, z + (z > 0 ? 0.04 : -0.04)];
    B.add(B.box(w, h, d), glass, gpos, order, 'pop', { edges: false, rot: rotY, shadow: false });
  }
}
function door(B, x, z, { w = 1.1, h = 2.2, y = 0.35, order = 5, color = 0x2A2F36 } = {}) {
  B.add(B.box(w + 0.18, h + 0.12, 0.08), mat(C.frame), [x, y, z], order, 'pop', { edges: false });
  B.add(B.box(w, h, 0.14), mat(color, { r: 0.5 }), [x, y, z + (z > 0 ? 0.03 : -0.03)], order, 'pop', { edges: false });
}

// ── Einfamilienhaus: 2 floors, gable roof, garage, terrace
function efh(B, ox = 0, opt = {}) {
  const wallC = opt.wall ?? C.wall, roofC = opt.roof ?? C.roofRed, mirror = opt.mirror ? -1 : 1;
  const W = 8.4, D = 7.2;
  B.add(B.box(W + 0.6, 0.35, D + 0.6), mat(C.slab), [ox, 0, 0], 0);
  B.add(B.box(W, 2.9, D), mat(wallC), [ox, 0.35, 0], 1);
  B.add(B.box(W + 0.2, 0.25, D + 0.2), mat(C.slab), [ox, 3.25, 0], 2);
  B.add(B.box(W, 2.6, D), mat(wallC), [ox, 3.5, 0], 3);
  B.add(B.gable(W + 0.9, 2.9, D + 0.9), mat(roofC, { r: 0.7 }), [ox, 6.1, 0], 4, 'drop');
  B.add(B.box(0.7, 1.8, 0.7), mat(C.wall2), [ox + 2.0 * mirror, 7.0, -1.2], 5, 'pop');
  // garage
  if (!opt.noGarage) {
    B.add(B.box(3.6, 0.3, 6.2), mat(C.slab), [ox + (W / 2 + 1.9) * mirror, 0, -0.4], 1);
    B.add(B.box(3.4, 2.6, 6), mat(C.wall2), [ox + (W / 2 + 1.9) * mirror, 0.3, -0.4], 2);
    B.add(B.box(3.7, 0.22, 6.3), mat(C.roofDark), [ox + (W / 2 + 1.9) * mirror, 2.9, -0.4], 3, 'drop');
    B.add(B.box(2.6, 2.0, 0.08), mat(0x9AA0A6, { r: 0.5, m: 0.2 }), [ox + (W / 2 + 1.9) * mirror, 0.3, 2.62], 5, 'pop', { edges: false });
  }
  // terrace + railing
  B.add(B.box(W - 1, 0.18, 2.6), mat(C.wood), [ox, 0.2, D / 2 + 1.3], 2);
  // facade: door on the outer side, two windows next to it; three windows upstairs – all windows 1.2 × 1.4
  door(B, ox - 2.7 * mirror, D / 2 + 0.01);
  windows(B, { xs: [ox - 0.2 * mirror, ox + 2.6 * mirror], y: 1.15, z: D / 2 + 0.01, order: 6 });
  windows(B, { xs: [ox - 2.7, ox, ox + 2.7], y: 4.25, z: D / 2 + 0.01, order: 6 });
  windows(B, { xs: [ox - 2.7, ox, ox + 2.7], y: 4.25, z: -D / 2 - 0.01, order: 6 });
  windows(B, { xs: [ox - 2.7, ox + 2.7], y: 1.15, z: -D / 2 - 0.01, order: 6 });
}

// ── Mehrfamilienhaus: 3 floors, light plaster with anthracite base, balconies with balcony doors, hipped roof
function mfh(B) {
  const W = 17, D = 10, FH = 3, F = 3, base = 0x5C6168, upper = 0xE8E2D8;
  const zf = D / 2 + 0.01, zb = -D / 2 - 0.01;
  B.add(B.box(W + 0.8, 0.4, D + 0.8), mat(C.slab), [0, 0, 0], 0);
  for (let f = 0; f < F; f++) {
    const y0 = 0.4 + f * FH;
    B.add(B.box(W, FH - 0.2, D), mat(f === 0 ? base : upper), [0, y0, 0], 1 + f);
    B.add(B.box(W + 0.2, 0.2, D + 0.2), mat(C.slab), [0, y0 + FH - 0.2, 0], 1 + f);
    if (f === 0) {
      door(B, 0, zf, { w: 1.8, h: 2.3, y: 0.4, order: 5, color: 0x1C1F24 });
      B.add(B.box(3.2, 0.14, 1.4), mat(C.slab), [0, 0.4 + 2.55, D / 2 + 0.7], 5, 'pop');      // entrance canopy
      windows(B, { xs: [-7, -4.6, -2.3, 2.3, 4.6, 7], y: y0 + 0.9, z: zf, order: 6 });
    } else {
      windows(B, { xs: [-7, -2.3, 2.3, 7], y: y0 + 0.9, z: zf, order: 6 });
      for (const x of [-4.6, 0, 4.6]) {
        windows(B, { xs: [x], y: y0 + 0.15, z: zf, w: 1.2, h: 2.2, order: 6 });            // balcony door
        B.add(B.box(3.2, 0.18, 1.4), mat(C.slab), [x, y0 - 0.05, D / 2 + 0.7], 4, 'pop');
        B.add(B.box(3.2, 0.95, 0.04), mat(0xBFD3DE, { r: 0.1, m: 0.1, extra: { transparent: true, opacity: 0.45 } }), [x, y0 + 0.13, D / 2 + 1.38], 6, 'pop', { edges: false, shadow: false });
        B.add(B.box(3.24, 0.06, 0.08), mat(C.rail, { r: 0.4, m: 0.5 }), [x, y0 + 1.08, D / 2 + 1.38], 6, 'pop', { edges: false });
      }
    }
    windows(B, { xs: [-7, -4.6, -2.3, 0, 2.3, 4.6, 7], y: y0 + 0.9, z: zb, order: 6 });
  }
  B.add(B.hip(W + 1, 3.4, D + 1, W - 7), mat(C.roofRed, { r: 0.75 }), [0, 0.4 + F * FH + 0.03, 0], 4, 'drop');  // +3 cm: no z-fighting with the top slab
}

export function makeModel(type, { floating = false } = {}) {
  const B = Builder();
  if (type === 'efh') efh(B, -1.6);
  else if (type === 'dh') { efh(B, -4.25, { roof: C.roofDark, noGarage: true }); efh(B, 4.25, { roof: C.roofDark, wall: C.plaster, noGarage: true, mirror: true }); }
  else mfh(B);
  // ground + greenery
  // floating objects: shadow-only ground, no trees (transparent canvas next to headlines)
  const ground = new THREE.Mesh(new THREE.CircleGeometry(floating ? 16 : 30, 64),
    floating ? new THREE.ShadowMaterial({ opacity: 0.22 }) : mat(C.ground, { r: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true;
  const root = new THREE.Group(); root.add(ground, B.group, B.ghost);
  if (floating) return { group: root, setProgress: B.setProgress };
  const treeMat = mat(C.green, { r: 0.95 });
  for (const [x, z, s] of [[-14, -6, 1.2], [13, -7, 1], [-13, 7, 0.9], [15, 5, 1.1]]) {
    const t = new THREE.Mesh(new THREE.IcosahedronGeometry(1.6 * s, 0), treeMat); t.position.set(x, 2.6 * s, z); t.castShadow = true;
    const st = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.2, 1.4 * s), mat(C.wood)); st.position.set(x, 0.7 * s, z);
    root.add(t, st);
  }
  return { group: root, setProgress: B.setProgress };
}

// ── Viewer: renderer + lights + camera, renders only while visible
export function createViewer(container, { interactive = false, autoRotate = 0.6, camPos = [22, 15, 26], target = [0, 3.5, 0], fov = 32 } = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  container.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(fov, 1, 0.1, 400);
  camera.position.set(...camPos);
  scene.add(new THREE.HemisphereLight(0xffffff, 0xB9AE9C, 1.15));
  const sun = new THREE.DirectionalLight(0xFFF1DC, 2.1);
  sun.position.set(18, 30, 14); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -30, right: 30, top: 30, bottom: -30, near: 1, far: 90 }); sun.shadow.bias = -0.0004; sun.shadow.radius = 4;
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0xDDE6F0, 0.5); fill.position.set(-20, 10, -10); scene.add(fill);
  let controls = null;
  if (interactive) {
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; controls.enableZoom = false; controls.enablePan = false;
    controls.minPolarAngle = 0.5; controls.maxPolarAngle = 1.35; controls.autoRotate = autoRotate > 0; controls.autoRotateSpeed = autoRotate;
    controls.target.set(...target);
  } else camera.lookAt(...target);
  let model = null, spin = interactive ? 0 : autoRotate, visible = false, raf = 0;
  const pivot = new THREE.Group(); scene.add(pivot);
  function setModel(m) { if (model) pivot.remove(model.group); model = m; pivot.add(m.group); }
  function resize() { const w = container.clientWidth, h = container.clientHeight; renderer.setSize(w, h, false); camera.aspect = w / Math.max(h, 1); camera.updateProjectionMatrix(); }
  const ro = new ResizeObserver(resize); ro.observe(container); resize();
  function loop() { raf = requestAnimationFrame(loop); if (spin) pivot.rotation.y += spin * 0.004; if (controls) controls.update(); renderer.render(scene, camera); }
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible && !raf) loop(); if (!visible && raf) { cancelAnimationFrame(raf); raf = 0; } }).observe(container);
  return { scene, camera, controls, pivot, setModel, render: () => renderer.render(scene, camera), setSpin: s => { spin = s; } };
}
