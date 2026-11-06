import bpy, json, math, sys, os, numpy as np, time
from mathutils import Vector
from PIL import Image
room, size, samples = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
BASE = os.path.dirname(os.path.abspath(__file__))
SUN = {  # sun position (relative to room centre) per room, from STOPS; None = no direct sun
  'hall': (3, 9, 14), 'corridor': None, 'living': (-6, 9, 14), 'kitchen': (-12, 9, -6),
  'kids': (4, 9, -14), 'bedroom': (4, 9, -14), 'bath': (12, 9, 3)}
EXCL = {'glass', 'showerGlass', 'glassDoor', 'frosted', 'glow', 'backdrop', 'mirror'}
LIGHT_W = 22.0      # three.js candela -> Blender watts (tuned by eye)
SUN_S = 4.5
SCALE = 0.5         # stored value = irradiance * SCALE  (decode: lightMapIntensity = 1/SCALE * PI-ish, tuned in viewer)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=f'{BASE}/glb/{room}.glb')
meta = json.load(open(f'{BASE}/glb/lights.json'))
ids = ['hall', 'corridor', 'living', 'kitchen', 'kids', 'bedroom', 'bath']
ox = meta['ox'][ids.index(room)]

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
hidden_names = []
def mats(o): return {s.material.name.split('.')[0] for s in o.material_slots if s.material}
bake_objs = [o for o in meshes if not (mats(o) & EXCL)]
for o in meshes:
    if 'backdrop' in mats(o): o.hide_render = True; hidden_names.append(o.name)
# ceiling glow-ish emission off for the bake (real light comes from lamps)
for m in bpy.data.materials:
    nt = m.node_tree
    if not nt: continue
    for n in nt.nodes:
        if n.type == 'BSDF_PRINCIPLED' and m.name.split('.')[0] == 'ceil':
            n.inputs['Emission Strength'].default_value = 0.0

# join everything bakeable into one object
bpy.ops.object.select_all(action='DESELECT')
for o in bake_objs: o.select_set(True)
bpy.context.view_layer.objects.active = bake_objs[0]
bpy.ops.object.make_single_user(object=True, obdata=True)
bpy.ops.object.join()
J = bpy.context.view_layer.objects.active; J.name = f'{room}_baked'
orig_uv = J.data.uv_layers[0].name if J.data.uv_layers else None
if not J.data.uv_layers: J.data.uv_layers.new(name='UVMap')
lm = J.data.uv_layers.new(name='lightmap'); J.data.uv_layers.active = lm
J.data.uv_layers[0].active_render = True
# triangulate, then xatlas lightmap UVs (face order is preserved)
import xatlas
mod = J.modifiers.new('tri', 'TRIANGULATE'); bpy.ops.object.modifier_apply(modifier='tri')
me = J.data; t = time.time()
V = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
F = np.zeros(len(me.polygons) * 3, np.uint32); me.polygons.foreach_get('vertices', F); F = F.reshape(-1, 3)
atlas = xatlas.Atlas(); atlas.add_mesh(V, F)
co = xatlas.ChartOptions(); co.max_iterations = 2
po = xatlas.PackOptions(); po.resolution = size; po.padding = 4; po.bilinear = True; po.bruteForce = False
atlas.generate(co, po)
vmap, idx, uvs = atlas[0]
assert len(idx) == len(F), (len(idx), len(F))
loop_uv = uvs[idx].reshape(-1, 2)          # per loop, polygons are triangles in order
J.data.uv_layers['lightmap'].data.foreach_set('uv', loop_uv.astype(np.float32).ravel())
print('uv', round(time.time() - t, 1), 's', len(J.data.polygons), 'faces')

img = bpy.data.images.new('lightmap', size, size, float_buffer=True)
for s in J.material_slots:
    m = s.material; nt = m.node_tree
    n = nt.nodes.new('ShaderNodeTexImage'); n.image = img; n.name = 'BAKE'
    for x in nt.nodes: x.select = False
    n.select = True; nt.nodes.active = n

# lights
for i, L in enumerate(l for l in meta['lights'] if l['room'] == room):
    d = bpy.data.lights.new(f'L{i}', 'POINT'); d.energy = L['intensity'] * LIGHT_W; d.color = L['color'][:3]; d.shadow_soft_size = 0.06
    ob = bpy.data.objects.new(f'L{i}', d); bpy.context.collection.objects.link(ob)
    x, y, z = L['pos']; ob.location = (x, -z, y)            # glTF Y-up -> Blender Z-up
if SUN[room]:
    sx, sy, sz = SUN[room]
    d = bpy.data.lights.new('sun', 'SUN'); d.energy = SUN_S; d.angle = math.radians(1.5)
    ob = bpy.data.objects.new('sun', d); bpy.context.collection.objects.link(ob)
    v = Vector((sx, -sz, sy)).normalized(); ob.rotation_euler = v.to_track_quat('Z', 'Y').to_euler()
w = bpy.data.worlds.new('w'); bpy.context.scene.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.55, 0.7, 0.9, 1); bg.inputs[1].default_value = 1.6

sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = samples
sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 4; sc.cycles.transparent_max_bounces = 8
sc.render.bake.margin = 6; sc.render.bake.use_pass_direct = True; sc.render.bake.use_pass_indirect = True; sc.render.bake.use_pass_color = False
if os.environ.get('PREVIEW'):
    cam = bpy.data.cameras.new('c'); cam.lens_unit = 'FOV'; cam.angle = math.radians(80)
    co = bpy.data.objects.new('c', cam); bpy.context.collection.objects.link(co); sc.camera = co
    px_, py_, pz_, lx, ly, lz = map(float, os.environ['PREVIEW'].split(','))
    co.location = (px_, -pz_, py_); co.rotation_euler = (Vector((lx, -lz, ly)) - co.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.resolution_x, sc.render.resolution_y = 960, 600; sc.cycles.samples = 32; sc.cycles.use_denoising = False
    sc.render.filepath = f'{BASE}/out/{room}-preview.png'; bpy.ops.render.render(write_still=True); print('preview done')
bpy.ops.object.select_all(action='DESELECT'); J.select_set(True); bpy.context.view_layer.objects.active = J
t = time.time()
bpy.ops.object.bake(type='DIFFUSE', pass_filter={'DIRECT', 'INDIRECT'}, margin=6, use_clear=True)
print('bake', round(time.time() - t, 1), 's')

px = np.array(img.pixels[:], dtype=np.float32).reshape(size, size, 4)[::-1, :, :3] * SCALE
srgb = np.where(px <= 0.0031308, px * 12.92, 1.055 * np.power(np.clip(px, 0, None), 1 / 2.4) - 0.055)
u8 = (np.clip(srgb, 0, 1) * 255 + 0.5).astype(np.uint8)
import cv2
den = cv2.fastNlMeansDenoisingColored(np.ascontiguousarray(u8), None, h=11, hColor=10, templateWindowSize=7, searchWindowSize=21)
Image.fromarray(den).save(f'{BASE}/out/{room}-lm.png')
print('max', float(px.max()), 'mean', float(px.mean()))

# clean bake nodes, export
for s in J.material_slots:
    nt = s.material.node_tree; nt.nodes.remove(nt.nodes['BAKE'])
for nm in hidden_names: bpy.data.objects[nm].hide_render = False
for o in [o for o in bpy.data.objects if o.type == 'LIGHT']: bpy.data.objects.remove(o)
bpy.ops.export_scene.gltf(filepath=f'{BASE}/out/{room}.glb', export_format='GLB', export_image_format='JPEG', export_jpeg_quality=85,
                          export_texcoords=True, export_normals=True, export_lights=False, export_apply=False, export_yup=True)
print('exported')
