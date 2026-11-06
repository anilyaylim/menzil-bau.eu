# Baked lighting for the 3D tour

The tour rooms are built procedurally in `v2/tour.js`. For a realistic look the
lighting is computed offline in Blender (Cycles: sun through the windows, sky
light, lamps, bounced light, contact shadows) and stored as one lightmap per
room. The site then loads `v2/tour/<room>.glb` + `v2/tour/<room>-lm.jpg`;
rooms without these files fall back to real-time lights.

## Steps

1. Serve the repo (`python3 -m http.server 8765`) and export the procedural
   rooms with exact dimensions:

       node tools/bake/export.js <workdir>/glb

   (writes `<room>.glb` for hall, corridor, living, kitchen, kids, bedroom,
   bath and `lights.json`).

2. Bake each room (Blender as a Python module: `pip install bpy xatlas pillow
   opencv-python-headless`, put `bake.py` next to the `glb/` folder):

       python bake.py <room> <lightmap size> <samples>     # e.g. living 2048 160

   Lightmap UVs come from xatlas, the bake is Cycles DIFFUSE
   (direct + indirect, no colour), denoised, stored sRGB-encoded at x0.5.

3. Copy `out/<room>.glb` to `v2/tour/` and save `out/<room>-lm.png` as
   `v2/tour/<room>-lm.jpg`, then run `python3 tools/build_v2.py` (it lists the
   baked rooms in `window.TOUR_BAKED`).

Re-run 1–3 whenever room geometry, furniture or materials change in `tour.js`.

## Furniture and textures (dress.py)

Before baking, `dress.py` replaces placeholders with scanned CC0 models from
Poly Haven and gives the main surfaces real PBR textures:

- `plant_<scale>` groups → `potted_plant_01` / `potted_plant_02`
- `armchair` group → `modern_arm_chair_01`
- floors → `wood_floor`, furniture oak → `kitchen_wood`, walls/ceilings →
  `painted_plaster_wall` (tinted to the wall colour), bath floor →
  `granite_tile`, entrance floor → `floor_tiles_08`

Download them into `assets/` (models: glTF 1k, textures: diffuse, nor_gl,
rough jpg) from polyhaven.com; textures get metric cube-projected UVs.
