def distribute_audio(total_duration, scene_durations):
    total = sum(scene_durations)
    if total <= 0:
        raise ValueError("scene durations must be positive")
    scale = total_duration / total
    return [round(x * scale, 3) for x in scene_durations]