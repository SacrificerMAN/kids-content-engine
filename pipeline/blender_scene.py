from pathlib import Path
from .schema import Episode

def write_blender_script(ep: Episode, path: Path):
    chars=repr(ep.characters)
    scene_plan=repr([s.__dict__ for s in ep.scenes])
    total_frames=max(1, round(ep.duration * 24))
    output_mp4=str(path.parent / "render.mp4")
    blend_file=str(path.parent / "scene.blend")
    script=f"""import bpy, math
from mathutils import Vector
FPS=24
TOTAL_FRAMES={total_frames}
CHARACTERS={chars}
SCENES={scene_plan}

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

def keyframe_pair(obj, frame, action):
    loc=obj.location.copy()
    rot=obj.rotation_euler.copy()
    obj.keyframe_insert(data_path='location', frame=frame)
    obj.keyframe_insert(data_path='rotation_euler', frame=frame)
    if action == 'jump':
        obj.location.z += 0.9
    elif action == 'dance':
        obj.rotation_euler.y += 0.35
        obj.location.x += 0.35
    elif action == 'wave':
        obj.rotation_euler.x += 0.25
    elif action == 'point':
        obj.rotation_euler.y -= 0.22
    elif action == 'clap':
        obj.location.y -= 0.12
    elif action == 'celebrate':
        obj.location.z += 0.35
        obj.rotation_euler.y += 0.3
    elif action == 'walk':
        obj.location.x += 0.7
    obj.keyframe_insert(data_path='location', frame=frame)
    obj.keyframe_insert(data_path='rotation_euler', frame=frame)
    obj.location=loc
    obj.rotation_euler=rot

sky=mat('Sky',(0.55,0.78,1.0))
primary=mat('Primary',(0.98,0.72,0.25))
accent=mat('Accent',(0.35,0.55,0.95))
ground=mat('Ground',(0.35,0.75,0.42))
cube('ground',(0,0,-0.1),(7,5,0.1),ground)

objects=[]
for i,name in enumerate(CHARACTERS):
    x=(i-len(CHARACTERS)/2)*2.0
    head=sphere(name+'_head',(x,0,2.5),(0.65,0.65,0.65),primary)
    body=cube(name+'_body',(x,0,1.35),(0.55,0.35,0.75),accent)
    objects.append((head,body))

frame=1
for scene_data in SCENES:
    scene_frames=max(1,round(float(scene_data.get('duration',1))*FPS))
    actions=scene_data.get('actions',[]) or ['wave']
    end=min(TOTAL_FRAMES,frame+scene_frames)
    for action_index,action in enumerate(actions):
        f0=min(end,max(frame,frame+round((end-frame)*action_index/max(1,len(actions)))))
        f1=min(end,f0+max(1,round((end-frame)/max(1,len(actions)))))
        for head,body in objects:
            keyframe_pair(head,f0,action)
            keyframe_pair(body,f0,action)
            keyframe_pair(head,f1,action)
            keyframe_pair(body,f1,action)
    frame=end+1

bpy.ops.object.camera_add(location=(0,-16,6))
camera=bpy.context.object
target=Vector((0,0,1.7))
camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
bpy.context.scene.camera=camera

scene=bpy.context.scene
try:
    scene.render.engine='BLENDER_EEVEE_NEXT'
except Exception:
    scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1280
scene.render.resolution_y=720
scene.render.resolution_percentage=50
scene.render.fps=FPS
scene.frame_start=1
scene.frame_end=TOTAL_FRAMES
scene.render.image_settings.file_format='FFMPEG'
scene.render.ffmpeg.format='MPEG4'
scene.render.ffmpeg.codec='H264'
try:
    scene.render.ffmpeg.constant_rate_factor='MEDIUM'
except Exception:
    pass
scene.render.filepath=r'{output_mp4}'
scene.world.color=(0.55,0.78,1.0)
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=r'{blend_file}')
bpy.ops.render.render(animation=True)
"""
    path.write_text(script,encoding="utf-8")
