import math
from typing import Dict, Any

class SceneTranslator:
    """
    Traduce los datos de cámara 3D provenientes del frontend (Three.js)
    al formato que FIBO/Bria necesita para componer una imagen.
    """

    # ---------------------------------------------------------
    # 1️⃣ CONVERTIR ROTACIÓN RADIANES → DEGRADOS
    # ---------------------------------------------------------
    @staticmethod
    def radians_to_degrees(radians: float) -> float:
        return radians * 180.0 / math.pi

    # ---------------------------------------------------------
    # 2️⃣ DETERMINAR ÁNGULO DE CÁMARA
    # ---------------------------------------------------------
    @staticmethod
    def get_camera_angle(rot_x_deg: float) -> str:
        """
        Determina el ángulo según la rotación vertical.
        """
        if rot_x_deg > 25:
            return "high_angle"
        elif rot_x_deg < -25:
            return "low_angle"
        return "eye_level"

    # ---------------------------------------------------------
    # 3️⃣ DETERMINAR TIPO DE TOMA (DEPENDE LA DISTANCIA)
    # ---------------------------------------------------------
    @staticmethod
    def get_shot_type(position: list) -> str:
        """
        Determina si es close_up, medium_shot o wide_shot
        según la distancia de la cámara al punto de interés.
        """
        x, y, z = position
        dist = math.sqrt(x*x + y*y + z*z)

        if dist > 6:
            return "wide_shot"
        elif dist > 2.5:
            return "medium_shot"
        else:
            return "close_up"

    # ---------------------------------------------------------
    # 4️⃣ CALCULAR LONGITUD FOCAL (conversión aproximada FOV → focal)
    # ---------------------------------------------------------
    @staticmethod
    def get_focal_length(fov: float) -> float:
        """
        Conversión aproximada de FOV → focal_length para Bria/FIBO.
        """
        base_focal = 50  # focal "default"
        return round(base_focal * (60 / max(fov, 1)), 2)

    # ---------------------------------------------------------
    # 5️⃣ ARMAR EL BLOQUE "camera" QUE BRIA NECESITA
    # ---------------------------------------------------------
    @staticmethod
    def translate_camera(camera_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convierte los datos 3D en parámetros cinematográficos para FIBO.
        """
        position = camera_data.get("position", [0, 0, 5])
        rotation = camera_data.get("rotation", [0, 0, 0])
        fov = camera_data.get("fov", 60)

        # Convertir rotación
        rot_x_deg = SceneTranslator.radians_to_degrees(rotation[0])
        rot_y_deg = SceneTranslator.radians_to_degrees(rotation[1])
        rot_z_deg = SceneTranslator.radians_to_degrees(rotation[2])

        return {
            "position": position,
            "rotation_degrees": [rot_x_deg, rot_y_deg, rot_z_deg],
            "angle": SceneTranslator.get_camera_angle(rot_x_deg),
            "shot_type": SceneTranslator.get_shot_type(position),
            "fov": fov,
            "focal_length": SceneTranslator.get_focal_length(fov),
            "depth_of_field": "medium"
        }

    # ---------------------------------------------------------
    # 6️⃣ FUNCIÓN PRINCIPAL
    # ---------------------------------------------------------
    @staticmethod
    def translate(scene_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traduce TODA la escena del frontend al formato interno que usa FIBOService.
        """

        camera_block = SceneTranslator.translate_camera(
            scene_payload.get("camera", {})
        )

        result = {
            "prompt": scene_payload.get("prompt", ""),
            "camera": camera_block,
            "lighting": scene_payload.get("lighting", {
                "time_of_day": "daylight",
                "color_grading": "neutral"
            }),
            "style": scene_payload.get("style", "realistic"),
            "width": scene_payload.get("width", 1024),
            "height": scene_payload.get("height", 576),
            "seed": scene_payload.get("seed"),
            "steps": scene_payload.get("steps", 30)
        }

        return result
