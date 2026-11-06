const { chromium } = require('playwright'); const fs = require('fs');
const OUT = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 800, height: 600 } }); p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('http://localhost:8765/v2/rundgang.html', { waitUntil: 'domcontentloaded' });
  await p.waitForFunction(() => window.__tour && window.__tour.rooms, null, { timeout: 90000 });
  const res = await p.evaluate(async () => {
    const { GLTFExporter } = await import('three/addons/exporters/GLTFExporter.js');
    const T = window.__tour, ex = new GLTFExporter(), out = {};
    for (let i = 0; i < T.rooms.length; i++) {
      const g = T.rooms[i]; g.visible = true; g.updateMatrixWorld(true);
      const buf = await ex.parseAsync(g, { binary: true, onlyVisible: false });
      const u8 = new Uint8Array(buf); let s = ''; for (let k = 0; k < u8.length; k += 0x8000) s += String.fromCharCode.apply(null, u8.subarray(k, k + 0x8000));
      out[T.roomIds[i]] = btoa(s);
    }
    const lights = T.lights.map(l => ({ room: T.roomIds[T.rooms.indexOf(l.userData.room)], pos: l.position.toArray(), color: l.color.toArray(), intensity: l.intensity }));
    return { out, lights, ox: T.rooms.map(r => r.position.x) };
  });
  for (const [k, v] of Object.entries(res.out)) fs.writeFileSync(`${OUT}/${k}.glb`, Buffer.from(v, 'base64'));
  fs.writeFileSync(`${OUT}/lights.json`, JSON.stringify({ lights: res.lights, ox: res.ox }, null, 1));
  console.log('done'); await b.close(); })();
