from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
from app.models.camera import CameraSettings
from app.models.lighting import LightingSetup

@dataclass
class Scene:
    """
    Representa una escena completa con todos los parámetros para generación.
    
    Combina prompt, cámara, iluminación y configuraciones técnicas
    en un único objeto serializable.
    """
    
    # ============ PROMPT ============
    prompt: str
    """
    Descripción textual de la escena (requerido).
    Ejemplo: "A cyberpunk street at night with neon lights and rain"
    """
    
    negative_prompt: str = ""
    """
    Elementos a evitar en la generación.
    Ejemplo: "blurry, low quality, distorted, ugly"
    """
    
    # ============ CONFIGURACIONES CINEMATOGRÁFICAS ============
    camera: CameraSettings = field(default_factory=CameraSettings)
    """
    Configuración de cámara (ángulos, encuadre, lente, etc).
    """
    
    lighting: LightingSetup = field(default_factory=LightingSetup)
    """
    Configuración de iluminación (luces, ambiente, color grading, etc).
    """
    
    # ============ PARÁMETROS DE GENERACIÓN ============
    width: int = 1024
    """
    Ancho de la imagen en píxeles.
    Valores comunes: 512, 768, 1024, 1280, 1920
    """
    
    height: int = 576
    """
    Alto de la imagen en píxeles.
    Valores comunes: 512, 576, 720, 1080
    """
    
    steps: int = 30
    """
    Número de pasos de difusión.
    Rango típico: 20-50
        - 20-25: Rápido, menos detalle
        - 30-35: Balance (recomendado)
        - 40-50: Más detalle, más lento
    """
    
    guidance_scale: float = 7.5
    """
    Qué tan estrictamente seguir el prompt.
    Rango típico: 5.0-15.0
        - 5.0-7.0: Más creativo, menos preciso
        - 7.5-9.0: Balance (recomendado)
        - 10.0-15.0: Muy preciso al prompt
    """
    
    seed: Optional[int] = None
    """
    Semilla para reproducibilidad.
    Si es None, se genera aleatoriamente.
    Usar el mismo seed + parámetros = misma imagen.
    """
    
    # ============ ESTILO Y CONTROL ============
    style: str = "cinematic"
    """
    Estilo artístico general.
    Opciones:
        - cinematic: Estilo cinematográfico
        - realistic: Fotorrealista
        - artistic: Artístico/pintado
        - anime: Estilo anime
        - cartoon: Dibujo animado
        - sketch: Boceto
        - oil_painting: Pintura al óleo
        - watercolor: Acuarela
        - comic_book: Cómic
        - concept_art: Arte conceptual
    """
    
    color_palette: Optional[str] = None
    """
    Paleta de colores a usar.
    Opciones:
        - vibrant: Colores vibrantes/saturados
        - muted: Colores apagados/desaturados
        - pastel: Colores pastel
        - monochrome: Monocromático
        - warm: Paleta cálida (rojos, naranjas, amarillos)
        - cool: Paleta fría (azules, verdes, púrpuras)
        - earth_tones: Tonos tierra
        - neon: Colores neón
        - black_white: Blanco y negro
    """
    
    mood: Optional[str] = None
    """
    Estado de ánimo/atmósfera de la escena.
    Opciones:
        - epic: Épico/grandioso
        - intimate: Íntimo/cercano
        - mysterious: Misterioso
        - peaceful: Pacífico/tranquilo
        - tense: Tenso/suspense
        - joyful: Alegre
        - melancholic: Melancólico
        - dramatic: Dramático
        - romantic: Romántico
        - horrific: Terrorífico
    """
    
    # ============ CONTROL AVANZADO ============
    detail_level: float = 1.0
    """
    Nivel de detalle en la imagen.
    Rango: 0.5 (poco detalle) a 2.0 (mucho detalle)
    """
    
    texture_strength: float = 1.0
    """
    Intensidad de texturas.
    Rango: 0.0 (suave) a 2.0 (muy texturizado)
    """
    
    sharpness: float = 1.0
    """
    Nitidez de la imagen.
    Rango: 0.5 (suave) a 1.5 (muy nítido)
    """
    
    # ============ METADATOS ============
    scene_number: Optional[int] = None
    """
    Número de escena en una secuencia (para storyboards).
    """
    
    project_id: Optional[str] = None
    """
    ID del proyecto al que pertenece esta escena.
    """
    
    tags: list = field(default_factory=list)
    """
    Tags/etiquetas para organización.
    Ejemplo: ["exterior", "night", "action"]
    """
    
    notes: str = ""
    """
    Notas adicionales sobre la escena.
    """
    
    def to_fibo_payload(self) -> Dict[str, Any]:
        """
        Genera el payload completo para enviar a FIBO API.
        
        Returns:
            dict: Payload formateado para FIBO
        """
        # Payload base
        payload = {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "width": self.width,
            "height": self.height,
            "steps": self.steps,
            "guidance_scale": self.guidance_scale,
            "style": self.style,
            "detail_level": self.detail_level,
            "texture_strength": self.texture_strength,
            "sharpness": self.sharpness
        }
        
        # Agregar seed si existe
        if self.seed is not None:
            payload["seed"] = self.seed
        
        # Agregar paleta de colores si existe
        if self.color_palette:
            payload["color_palette"] = self.color_palette
        
        # Agregar mood si existe
        if self.mood:
            payload["mood"] = self.mood
        
        # Merge camera settings
        payload.update(self.camera.to_fibo_json())
        
        # Merge lighting settings
        payload.update(self.lighting.to_fibo_json())
        
        # Agregar metadatos
        if self.scene_number is not None:
            payload["scene_number"] = self.scene_number
        
        if self.tags:
            payload["tags"] = self.tags
        
        return payload
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte a diccionario simple para serialización.
        
        Returns:
            dict: Escena como diccionario
        """
        return {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "camera": self.camera.to_dict(),
            "lighting": self.lighting.to_dict(),
            "width": self.width,
            "height": self.height,
            "steps": self.steps,
            "guidance_scale": self.guidance_scale,
            "seed": self.seed,
            "style": self.style,
            "color_palette": self.color_palette,
            "mood": self.mood,
            "detail_level": self.detail_level,
            "texture_strength": self.texture_strength,
            "sharpness": self.sharpness,
            "scene_number": self.scene_number,
            "project_id": self.project_id,
            "tags": self.tags,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Scene':
        """
        Crea una escena desde un diccionario.
        
        Args:
            data: Diccionario con los parámetros
            
        Returns:
            Scene: Instancia configurada
        """
        # Extraer y convertir camera
        camera_data = data.pop('camera', {})
        camera = CameraSettings.from_dict(camera_data) if camera_data else CameraSettings()
        
        # Extraer y convertir lighting
        lighting_data = data.pop('lighting', {})
        lighting = LightingSetup.from_dict(lighting_data) if lighting_data else LightingSetup()
        
        # Crear escena con el resto de datos
        return cls(
            camera=camera,
            lighting=lighting,
            **data
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Valida que todos los parámetros sean correctos.
        
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        # Validar prompt
        if not self.prompt or len(self.prompt.strip()) == 0:
            return False, "El prompt no puede estar vacío"
        
        if len(self.prompt) > 2000:
            return False, "El prompt no puede exceder 2000 caracteres"
        
        # Validar dimensiones
        if not 256 <= self.width <= 2048:
            return False, "Width debe estar entre 256 y 2048"
        
        if not 256 <= self.height <= 2048:
            return False, "Height debe estar entre 256 y 2048"
        
        # Validar steps
        if not 10 <= self.steps <= 100:
            return False, "Steps debe estar entre 10 y 100"
        
        # Validar guidance_scale
        if not 1.0 <= self.guidance_scale <= 20.0:
            return False, "Guidance scale debe estar entre 1.0 y 20.0"
        
        # Validar seed si existe
        if self.seed is not None and self.seed < 0:
            return False, "Seed debe ser un número positivo"
        
        # Validar detail_level
        if not 0.1 <= self.detail_level <= 3.0:
            return False, "Detail level debe estar entre 0.1 y 3.0"
        
        # Validar texture_strength
        if not 0.0 <= self.texture_strength <= 3.0:
            return False, "Texture strength debe estar entre 0.0 y 3.0"
        
        # Validar sharpness
        if not 0.1 <= self.sharpness <= 2.0:
            return False, "Sharpness debe estar entre 0.1 y 2.0"
        
        # Validar cámara
        valid_camera, camera_error = self.camera.validate()
        if not valid_camera:
            return False, f"Error en cámara: {camera_error}"
        
        # Validar iluminación
        valid_lighting, lighting_error = self.lighting.validate()
        if not valid_lighting:
            return False, f"Error en iluminación: {lighting_error}"
        
        return True, None
    
    @classmethod
    def preset_cinematic_wide(cls, prompt: str) -> 'Scene':
        """
        Preset para tomas cinematográficas amplias.
        
        Args:
            prompt: Descripción de la escena
            
        Returns:
            Scene: Escena configurada
        """
        return cls(
            prompt=prompt,
            camera=CameraSettings.preset_cinematic(),
            lighting=LightingSetup.preset_golden_hour(),
            width=1920,
            height=816,  # 2.35:1 cinemascope
            style="cinematic",
            mood="epic"
        )
    
    @classmethod
    def preset_portrait(cls, prompt: str) -> 'Scene':
        """
        Preset para retratos.
        
        Args:
            prompt: Descripción del sujeto
            
        Returns:
            Scene: Escena configurada
        """
        return cls(
            prompt=prompt,
            camera=CameraSettings.preset_portrait(),
            lighting=LightingSetup.preset_soft_portrait(),
            width=768,
            height=1024,  # Vertical
            style="realistic",
            mood="intimate"
        )
    
    @classmethod
    def preset_landscape(cls, prompt: str) -> 'Scene':
        """
        Preset para paisajes.
        
        Args:
            prompt: Descripción del paisaje
            
        Returns:
            Scene: Escena configurada
        """
        return cls(
            prompt=prompt,
            camera=CameraSettings.preset_landscape(),
            lighting=LightingSetup.preset_natural_daylight(),
            width=1920,
            height=1080,
            style="realistic",
            mood="peaceful"
        )
    
    @classmethod
    def preset_noir(cls, prompt: str) -> 'Scene':
        """
        Preset estilo film noir.
        
        Args:
            prompt: Descripción de la escena
            
        Returns:
            Scene: Escena configurada
        """
        return cls(
            prompt=prompt,
            camera=CameraSettings(
                angle="low_angle",
                shot_type="medium_shot",
                focal_length=35.0,
                composition_rule="diagonal"
            ),
            lighting=LightingSetup.preset_dramatic_noir(),
            style="cinematic",
            mood="mysterious",
            color_palette="monochrome"
        )
    
    @classmethod
    def preset_cyberpunk(cls, prompt: str) -> 'Scene':
        """
        Preset estilo cyberpunk.
        
        Args:
            prompt: Descripción de la escena
            
        Returns:
            Scene: Escena configurada
        """
        return cls(
            prompt=prompt,
            camera=CameraSettings(
                angle="low_angle",
                shot_type="wide_shot",
                focal_length=24.0,
                vignette=0.3
            ),
            lighting=LightingSetup.preset_cyberpunk(),
            style="cinematic",
            mood="tense",
            color_palette="neon"
        )
    
    def clone(self, **overrides) -> 'Scene':
        """
        Clona la escena con modificaciones opcionales.
        
        Args:
            **overrides: Campos a sobrescribir
            
        Returns:
            Scene: Nueva escena clonada
        """
        data = self.to_dict()
        data.update(overrides)
        return Scene.from_dict(data)
    
    def get_aspect_ratio(self) -> str:
        """
        Calcula el aspect ratio de la escena.
        
        Returns:
            str: Aspect ratio (ej: "16:9")
        """
        from math import gcd
        divisor = gcd(self.width, self.height)
        return f"{self.width // divisor}:{self.height // divisor}"
    
    def estimate_generation_time(self) -> float:
        """
        Estima el tiempo de generación en segundos.
        
        Returns:
            float: Tiempo estimado en segundos
        """
        # Fórmula básica: base_time + (width * height * steps) / factor
        base_time = 2.0  # segundos base
        pixels = self.width * self.height
        complexity_factor = 1000000  # ajustar según hardware
        
        estimated = base_time + (pixels * self.steps) / complexity_factor
        return round(estimated, 1)