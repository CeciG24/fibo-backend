# translator.py
# ======================================================
# Traductor matemático que convierte datos 3D del frontend
# en parámetros cinematográficos para FIBO.
# Cumple API Backlog Dev:
#  - T1 map_camera_angle
#  - T2 map_shot_size
#  - T3 map_lighting
# ======================================================

import math


# ======================
# T1: Camera angle
# ======================
def map_camera_angle(position, target=[0, 0, 0]):
    """
    Determina el ángulo de cámara en base a la relación
    de altura entre la cámara y el objetivo.
    
    position: [x, y, z]
    target:   [x, y, z]

    Returns:
        "low_angle", "eye_level", "high_angle", "birds_eye"
    """

    cam_y = position[1]
    target_y = target[1]

    diff = cam_y - target_y

    # Reglas simples basadas en la cinematografía clásica
    if diff > 3.0:
        return "birds_eye"        # Muy arriba
    elif diff > 1.0:
        return "high_angle"       # Arriba
    elif diff < -1.0:
        return "low_angle"        # Abajo
    else:
        return "eye_level"        # A nivel del sujeto


# ======================
# T2: Shot size
# ======================
def map_shot_size(position, target=[0, 0, 0]):
    """
    Determina el tamaño del plano según la distancia
    entre la cámara y el objeto.

    Valores retornados:
        close_up
        medium_shot
        long_shot
    """
    dx = position[0] - target[0]
    dy = position[1] - target[1]
    dz = position[2] - target[2]

    dist = math.sqrt(dx*dx + dy*dy + dz*dz)

    if dist < 4:
        return "close_up"
    elif dist < 8:
        return "medium_shot"
    else:
        return "long_shot"


# ======================
# T3: Lighting
# ======================
def map_lighting(light_position):
    """
    Determina el tipo de iluminación según el ángulo vertical
    de la luz virtual.

    light_position: [x, y, z]

    Reglas:
        35°–55° → studio_lighting
        <20°   → flat_lighting
        >60°   → dramatic_lighting
        else   → neutral
    """

    x, y, z = light_position

    # Ángulo vertical de la luz sobre el horizonte
    angle = math.degrees(math.atan2(y, math.sqrt(x*x + z*z)))

    if 35 <= angle <= 55:
        return "studio_lighting"
    elif angle < 20:
        return "flat_lighting"
    elif angle > 60:
        return "dramatic_lighting"

    return "neutral"


# ======================
# Wrapper principal
# ======================
def translate_camera_data(camera_state, light_position=[0, 3, 3]):
    """
    Convierte el estado de cámara del frontend a parámetros
    cinematográficos para FIBOService.

    camera_state:
    {
       "position": [x,y,z],
       "rotation": [rx,ry,rz],
       "fov": 50
    }
    """

    position = camera_state.get("position", [0, 2, 5])

    return {
        "angle": map_camera_angle(position),
        "shot_type": map_shot_size(position),
        "lighting": map_lighting(light_position),
        "fov": camera_state.get("fov", 50)
    }

