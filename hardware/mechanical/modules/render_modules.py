# SPDX-FileCopyrightText: 2026 Plone Mraz
# SPDX-License-Identifier: Apache-2.0
"""Scene, GLB, stills and turntable frames of the joint modules, in Blender 5.3 (plan ID-9).

    python3 generate_modules.py --mesh MESHDIR
    blender -b --factory-startup -P render_modules.py -- MESHDIR OUTDIR glb|still|turn [frames]

Writes gems-module-layout.glb, still_*.png or f_*.png with a transparent film.
The captions and the WEBM and WebP of media/ are made from these frames.
"""
import bpy, bmesh, sys, json, math, pathlib
from mathutils import Vector, Matrix
A = sys.argv[sys.argv.index("--") + 1:]; MD, OUT, MODE = pathlib.Path(A[0]), pathlib.Path(A[1]), A[2]; N = int(A[3]) if len(A) > 3 else 180
OUT.mkdir(parents=True, exist_ok=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
L = json.load(open(MD / "layout.json")); MM = .001
def mat(name, col, metal, rough, alpha=1.0):
    m = bpy.data.materials.new(name); b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough; b.inputs["Alpha"].default_value = alpha
    if alpha < 1: m.surface_render_method = "BLENDED"; m.use_backface_culling = True
    m.diffuse_color = (*col, alpha); return m
M = {"body": mat("anodised", (.13, .145, .17), .65, .40), "cap": mat("cover", (.05, .055, .06), .1, .5), "output": mat("output", (.80, .81, .83), 1.0, .28),
     "x12": mat("myactuator", (.06, .06, .066), .5, .45), "se": mat("semotor", (.20, .26, .34), .6, .45), "seg": mat("segment envelope", (.10, .30, .55), 0, .6)}
def stl(p, name):
    bpy.ops.wm.stl_import(filepath=str(p)); o = bpy.context.selected_objects[0]; me = o.data; bpy.data.objects.remove(o); me.name = name
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-3); bm.to_mesh(me); bm.free()
    me.transform(Matrix.Scale(MM, 4)); me.shade_smooth(); me.set_sharp_from_angle(angle=math.radians(28)); return me
meshes = {}
for p in sorted(MD.glob("*__*.stl")):
    n, part = p.stem.split("__"); me = stl(p, n + " " + part); me.materials.clear()
    me.materials.append(M["output"] if part == "output" else M["x12"] if n.startswith("RMD") else M["se"] if n.startswith("SEAF") else M[part]); meshes.setdefault(n, {})[part] = me
turn = Matrix.Rotation(math.radians(-90), 4, "Z"); sc = bpy.context.scene
root = bpy.data.objects.new("GEMs", None); sc.collection.objects.link(root)
def col(n): c = bpy.data.collections.new(n); sc.collection.children.link(c); return c
cm, cs = col("modules"), col("segments"); em = bpy.data.objects.new("modules", None); es = bpy.data.objects.new("segments", None)
for e in (em, es): sc.collection.objects.link(e); e.parent = root
for m in L["modules"]:
    q = Vector((0, 0, 1)).rotation_difference(Vector(m["out"])).to_matrix().to_4x4(); W = turn @ Matrix.Translation(Vector(m["centre"]) * MM) @ q
    e = bpy.data.objects.new(m["name"], None); cm.objects.link(e); e.parent = em; e.matrix_world = W; e["module"] = m["module"]; e["housing_link"] = m["link"]
    for part, me in meshes[m["module"]].items():
        o = bpy.data.objects.new(m["name"] + " " + part, me); cm.objects.link(o); o.parent = e
def wire(name, polys, r=.0011):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 1; cu.resolution_u = 1
    for pts, cyc in polys:
        sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1); sp.use_cyclic_u = cyc
        for q, v in zip(sp.points, pts): q.co = (*v, 1)
    o = bpy.data.objects.new(name, cu); cs.objects.link(o); dg = bpy.context.evaluated_depsgraph_get(); me = bpy.data.meshes.new_from_object(o.evaluated_get(dg)); bpy.data.objects.remove(o); return me
for s in L["segments"]:
    if s["kind"] == "box":
        a, b, c = (v * MM / 2 for v in s["size"]); P = []
        for z in (-c, c): P.append(([(-a, -b, z), (a, -b, z), (a, b, z), (-a, b, z)], True))
        for x, y in ((-a, -b), (a, -b), (a, b), (-a, b)): P.append(([(x, y, -c), (x, y, c)], False))
    else:
        rr, h = s["r"] * MM, s["h"] * MM / 2; ring = [(rr * math.cos(2 * math.pi * k / 48), rr * math.sin(2 * math.pi * k / 48)) for k in range(48)]
        P = [([(x, y, z) for x, y in ring], True) for z in (-h, h)] + [([(*ring[k], -h), (*ring[k], h)], False) for k in (0, 12, 24, 36)]
    me = wire(s["link"], P); me.materials.append(M["seg"]); o = bpy.data.objects.new("segment " + s["link"], me); cs.objects.link(o); o.parent = es; o.matrix_world = turn @ Matrix.Translation(Vector(s["centre"]) * MM)
bpy.context.view_layer.update()
print("OBJ", len(bpy.data.objects), "unique tris", sum(len(me.loop_triangles) if me.calc_loop_triangles() is None else 0 for d in meshes.values() for me in d.values()))
if MODE == "glb":
    bpy.ops.export_scene.gltf(filepath=str(OUT / "gems-module-layout.glb"), export_format="GLB", export_yup=True, export_extras=True, export_apply=False, export_cameras=False, export_lights=False, export_animations=False)
    print("GLB", (OUT / "gems-module-layout.glb").stat().st_size); sys.exit()
# stage
lo = -1.016
w = bpy.data.worlds.new("w"); sc.world = w; bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND"); bg.inputs[0].default_value = (.86, .89, .92, 1); bg.inputs[1].default_value = .62
def area(loc, size, power, tgt=(0, 0, -.2)):
    l = bpy.data.lights.new("a", "AREA"); l.size = size; l.energy = power; o = bpy.data.objects.new("a", l); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
area((2.6, -3.0, 2.4), 2.0, 130); area((-3.2, -1.6, 1.2), 2.4, 60); area((0.6, 3.2, 2.2), 1.6, 110)
cd = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam; cd.lens = 70
def look(az, el, dist, tgt, lens=70):
    cd.lens = lens; t = Vector(tgt); a, e = math.radians(az), math.radians(el); cam.location = t + Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))) * dist; cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
r = sc.render; r.engine = "BLENDER_EEVEE"; sc.eevee.taa_render_samples = 48 if MODE != "turn" else 24; sc.eevee.use_raytracing = True
r.film_transparent = True; r.image_settings.color_mode = "RGBA"; sc.view_settings.view_transform = "Khronos PBR Neutral"; r.image_settings.file_format = "PNG"
V = dict(whole=(28, 6, 3.95, (0, 0, -.175), 70), hip=(38, 12, 1.5, (0, 0, -.14), 70), leg=(52, 6, 2.1, (0, 0, -.62), 70), shoulder=(30, 14, 1.7, (0, 0, .33), 70))
def shot(n, name, res): r.resolution_x, r.resolution_y = res; look(*V[n]); r.filepath = str(OUT / name); bpy.ops.render.render(write_still=True)
if MODE == "still":
    for n in V: shot(n, "still_%s.png" % n, (1000, 1500) if n == "whole" else (1400, 1050))
if MODE == "turn":
    r.resolution_x, r.resolution_y = 800, 1200; r.use_persistent_data = True
    for k in range(N): look(28 + 360 * k / N, 6, 3.95, (0, 0, -.175)); r.filepath = str(OUT / ("f_%04d.png" % k)); bpy.ops.render.render(write_still=True)
