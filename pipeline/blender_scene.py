from pathlib import Path
from .schema import Episode

def write_blender_script(ep: Episode, path: Path):
    chars=repr(ep.characters)
    total_frames=max(1, round(ep.duration * 24))
    output_mp4=str(path.parent / "render.mp4")
    blend_file=str(path.parent / "scene.blend")
    script=f"""import bpy, math
FPS=24
TOTAL_FRAMES={total_frames}
CHARACTERS={chars}

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def mat(name, rgba):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color=(*rgba,1)
    return m

def cube(name, loc, scale, material):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o=bpy.context.object
    o.name=name
    o.scale=scale
    o.data.materials.append(material)
    return o

def sphere(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=loc)
    o=bpy.context.object
    o.name=name
    o.scale=scale
    o.data.materials.append(material)
    return o

sky=mat('Sky',(0.55,0.78,1.0))
primary=mat('Primary',(0.98,0.72,0.25))
accent=mat('Accent',(0.35,0.55,0.95))
ground=mat('Ground',(0.35,0.75,0.42))
cube('ground',(0,0,-0.1),(7,5,0.1),ground)

for i,name in enumerate(CHARACTERS):
    x=(i-len(CHARACTERS)/2)*2.0
    head=sphere(name+'_head',(x,0,2.5),(0.65,0.65,0.65),primary)
    body=cube(name+'_body',(x,0,1.35),(0.55,0.35,0.75),accent)
    for obj in (head, body):
        obj.keyframe_insert(data_path='location', frame=1)
        obj.location.z += 0.22
        obj.keyframe_insert(data_path='location', frame=max(2,TOTAL_FRAMES//2))
        obj.location.z -= 0.22
        obj.keyframe_insert(data_path='location', frame=TOTAL_FRAMES)
    body.rotation_euler.y=0.15
    body.keyframe_insert(data_path='rotation_euler', frame=1)
    body.rotation_euler.y=-0.15
    body.keyframe_insert(data_path='rotation_euler', frame=max(2,TOTAL_FRAMES//2))
    body.rotation_euler.y=0.15
    body.keyframe_insert(data_path='rotation_euler', frame=TOTAL_FRAMES)

bpy.ops.object.camera_add(location=(0,-14,5.2))
camera=bpy.context.object
camera.rotation_euler=(math.radians(78),0,0)
bpy.context.scene.camera=camera

scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE_NEXT'
scene.render.resolution_x=1280
scene.render.resolution_y=720
scene.render.resolution_percentage=50
scene.render.fps=FPS
scene.frame_start=1
scene.frame_end=TOTAL_FRAMES
scene.render.image_settings.file_format='FFMPEG'
scene.render.ffmpeg.format='MPEG4'
scene.render.ffmpeg.codec='H264'
scene.render.ffmpeg.constant_rate_factor='MEDIUM'
scene.render.filepath=r'{output_mp4}'
scene.world.color=(0.55,0.78,1.0)
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=r'{blend_file}')
bpy.ops.render.render(animation=True)
"""
    path.write_text(script,encoding="utf-8")
