"""Swap placeholder furniture for scanned Poly Haven models and give the main
surfaces real PBR textures (metric UVs). Imported by bake.py before the join."""
import bpy, math, os, random, numpy as np
from mathutils import Vector, Matrix
from PIL import Image
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
TINT_DIR = os.path.join(A, 'tinted'); os.makedirs(TINT_DIR, exist_ok=True)

def _children(o):
    out = []
    for c in o.children: out += [c] + _children(c)
    return out

def import_model(name):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=f'{A}/models/{name}/{name}.gltf')
    new = [o for o in bpy.data.objects if o not in before]
    roots = [o for o in new if o.parent is None]
    # bake everything into one root empty
    root = bpy.data.objects.new(name + '_root', None); bpy.context.collection.objects.link(root)
    for r in roots: r.parent = root
    meshes = [o for o in new if o.type == 'MESH']
    return root, meshes

def bbox(meshes):
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi

def replace(placeholder, model, target_h=None, max_w=None, rot_z=0.0):
    loc = placeholder.matrix_world.translation.copy()
    for c in _children(placeholder): bpy.data.objects.remove(c)
    root, meshes = import_model(model)
    bpy.context.view_layer.update()
    lo, hi = bbox(meshes); h = hi.z - lo.z; w = max(hi.x - lo.x, hi.y - lo.y)
    s = 1.0
    if target_h: s = target_h / h
    if max_w and w * s > max_w: s = max_w / w
    root.scale = (s, s, s); root.rotation_euler = (0, 0, rot_z)
    bpy.context.view_layer.update()
    lo, hi = bbox(meshes)
    root.location = (loc.x - (lo.x + hi.x) / 2 + root.location.x, loc.y - (lo.y + hi.y) / 2 + root.location.y, loc.z - lo.z + root.location.z)
    bpy.data.objects.remove(placeholder)
    return meshes

def swap_models():
    out = []
    rnd = random.Random(7)
    for o in [o for o in bpy.data.objects if o.name.startswith('plant_')]:
        s = float(o.name.split('_')[1][:4])
        model = 'potted_plant_02' if rnd.random() < 0.6 else 'potted_plant_01'
        out += replace(o, model, target_h=1.05 * s, max_w=0.75 * s, rot_z=rnd.random() * 6.283)
    for o in [o for o in bpy.data.objects if o.name.startswith('armchair')]:
        out += replace(o, 'modern_arm_chair_01', rot_z=-math.pi / 2)
    return out

# ── materials ───────────────────────────────────────────────
def tinted(tex, rgb, strength=1.0):
    """copy of a diffuse map re-coloured so its mean equals rgb (sRGB 0-255)"""
    key = f"{tex}_{''.join('%02x' % c for c in rgb)}_{strength}.jpg"; path = os.path.join(TINT_DIR, key)
    if not os.path.exists(path):
        im = np.asarray(Image.open(f'{A}/tex/{tex}_diff.jpg').convert('RGB')).astype(np.float32)
        lum = im.mean(axis=2, keepdims=True); lum = lum / lum.mean()
        lum = 1 + (lum - 1) * strength
        out = np.clip(lum * np.array(rgb, np.float32)[None, None, :], 0, 255).astype(np.uint8)
        Image.fromarray(out).save(path, quality=90)
    return path

def pbr(mat, diff_path, tex, size, nor_strength=0.6, rough_mul=None):
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); bs = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(bs.outputs[0], out.inputs[0])
    uv = nt.nodes.new('ShaderNodeUVMap'); uv.uv_map = 'UVMap'
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / size, 1 / size, 1)
    nt.links.new(uv.outputs[0], mp.inputs[0])
    def img(path, non_color=False):
        n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(path, check_existing=True)
        if non_color: n.image.colorspace_settings.name = 'Non-Color'
        nt.links.new(mp.outputs[0], n.inputs[0]); return n
    d = img(diff_path); nt.links.new(d.outputs[0], bs.inputs['Base Color'])
    r = img(f'{A}/tex/{tex}_rough.jpg', True); nt.links.new(r.outputs[0], bs.inputs['Roughness'])
    n = img(f'{A}/tex/{tex}_nor.jpg', True); nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = nor_strength
    nt.links.new(n.outputs[0], nm.inputs['Color']); nt.links.new(nm.outputs[0], bs.inputs['Normal'])

# material base name -> (texture, real size in m, tint or None, tint strength, normal strength)
MAP = {
    'floor_oak':  ('wood_floor', 1.7, (222, 196, 160), 1.0, 0.5),
    'oak':        ('kitchen_wood', 0.6, (205, 170, 125), 1.0, 0.4),
    'wall':       ('painted_plaster_wall', 2.0, (242, 239, 234), 0.25, 0.25),
    'ceil':       ('painted_plaster_wall', 2.0, (250, 249, 247), 0.15, 0.15),
    'accent':     ('painted_plaster_wall', 2.0, (142, 155, 136), 0.3, 0.25),
    'kidsWall':   ('painted_plaster_wall', 2.0, (169, 191, 203), 0.3, 0.25),
    'floor_tileFloor': ('granite_tile', 2.3, None, 1.0, 0.6),
    'floor_hallTile':  ('floor_tiles_08', 1.5, (214, 206, 194), 0.8, 0.6),
}
def base(n): return n.split('.')[0]

def retexture(J):
    """J: the joined room mesh. Metric cube-projected UVs for the remapped materials."""
    targets = {i for i, s in enumerate(J.material_slots) if s.material and base(s.material.name) in MAP}
    done = set()
    for i in targets:
        m = J.material_slots[i].material
        if m.name in done: continue
        tex, size, tint, ts, ns = MAP[base(m.name)]
        diff = tinted(tex, tint, ts) if tint else f'{A}/tex/{tex}_diff.jpg'
        pbr(m, diff, tex, size, ns); done.add(m.name)
    me = J.data; me.uv_layers.active_index = 0
    bpy.context.scene.tool_settings.use_uv_select_sync = True
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    for p in me.polygons: p.select = p.material_index in targets
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.cube_project(cube_size=1.0, correct_aspect=False, clip_to_bounds=False, scale_to_bounds=False)
    bpy.ops.object.mode_set(mode='OBJECT')
