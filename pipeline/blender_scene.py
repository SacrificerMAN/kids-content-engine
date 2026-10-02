from pathlib import Path
from .schema import Episode

def write_blender_script(ep: Episode, path: Path):
    chars=repr(ep.characters)
    script="""import bpy, math
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
def mat(name, rgba):
    m=bpy.data.materials.new(name); m.diffuse_color=(*rgba,1); return m
def cube(name, loc, scale, material):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material); return o
def sphere(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=loc); o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material); return o
sky=mat('Sky',(0.55,0.78,1.0)); primary=mat('Primary',(0.98,0.72,0.25)); accent=mat('Accent',(0.35,0.55,0.95))
"""
    script += f"characters={chars}\n"
    script += "for i,name in enumerate(characters):\n    x=(i-len(characters)/2)*2.0\n    sphere(name+'_head',(x,0,2.5),(0.65,0.65,0.65),primary)\n    cube(name+'_body',(x,0,1.35),(0.55,0.35,0.75),accent)\n    sphere(name+'_eye',(x-0.22,-0.58,2.62),(0.09,0.05,0.09),sky)\n    sphere(name+'_eye2',(x+0.22,-0.58,2.62),(0.09,0.05,0.09),sky)\n"
    script += "bpy.ops.object.camera_add(location=(0,-12,5), rotation=(math.radians(72),0,0))\nbpy.context.scene.camera=bpy.context.object\nbpy.context.scene.render.engine='BLENDER_EEVEE_NEXT'\nbpy.context.scene.render.resolution_x=1920\nbpy.context.scene.render.resolution_y=1080\nbpy.context.scene.render.resolution_percentage=50\nbpy.context.scene.render.fps=24\n"
    path.write_text(script,encoding='utf-8')
