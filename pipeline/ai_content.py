import json, os
from pathlib import Path
import requests

SYSTEM = """You create original preschool educational content. Never imitate named children's shows, characters, branding, songs, plots, or distinctive visual designs. Keep language simple, positive, age-appropriate, non-scary, and educational. Return JSON only."""

def _fallback(topic, duration):
    topic=topic.strip().lower()
    title=f"{topic.title()} Adventure"
    lines=[
        f"Hello friends! Today we are learning about {topic}.",
        f"Look, listen, and say it with us: {topic}!",
        f"Let's clap, move, and learn together.",
        f"Great job, little learners! See you next time!"
    ]
    return {
        "title":title,
        "learning_goal":f"Introduce the preschool concept of {topic}.",
        "lyrics":f"Hello friends, let's learn {topic},\nClap your hands and move along!\nLook and listen, one, two, three,\nLearning together happily!",
        "narration":lines,
        "scenes":[
            {"location":"colorful_classroom","visual_prompt":f"Original cheerful preschool 3D classroom for learning {topic}, rounded shapes, soft lighting, original child characters","actions":["enter","wave","point","clap"],"voice":lines[0]},
            {"location":"alphabet_garden","visual_prompt":f"Original bright educational garden with playful {topic} learning objects, friendly child characters and a dog","actions":["walk","point","dance","celebrate"],"voice":lines[1]},
            {"location":"sunny_playground","visual_prompt":f"Original sunny preschool playground celebrating {topic}, colorful props, joyful child characters","actions":["jump","wave","clap","celebrate"],"voice":lines[2]}
        ]
    }

def generate_ai_content(topic, duration=30):
    key=os.getenv("OPENAI_API_KEY")
    endpoint=os.getenv("CONTENT_LLM_ENDPOINT","https://api.openai.com/v1/chat/completions")
    model=os.getenv("CONTENT_LLM_MODEL","gpt-4o-mini")
    if not key:
        return _fallback(topic,duration)
    payload={
        "model":model,
        "temperature":0.7,
        "response_format":{"type":"json_object"},
        "messages":[
            {"role":"system","content":SYSTEM},
            {"role":"user","content":json.dumps({"topic":topic,"duration":duration,"required_scenes":3,"output":"title,learning_goal,lyrics,narration,scenes with location,visual_prompt,actions,voice"})}
        ]
    }
    r=requests.post(endpoint,json=payload,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},timeout=90)
    r.raise_for_status()
    data=r.json()
    return json.loads(data["choices"][0]["message"]["content"])

def save_content(data,path):
    Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
    return str(path)
