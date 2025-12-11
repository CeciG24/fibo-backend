from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any

@dataclass
class LightSource:
    """
    Representa una fuente de luz individual en la escena.
    """
    
    type: str = "key"
    """
    Tipo de luz en el esquema de iluminación.
    Opciones:
        - key: Luz principal (la más brillante)
        - fill: Luz de relleno (suaviza sombras)
        - back: Luz trasera/rim (separa sujeto del fondo)
        - rim: Luz de contorno (resalta bordes)
        - ambient: Luz ambiental (iluminación general)
        - accent: Luz de acento (destaca detalles)
    """
    
    intensity: float = 1.0
    """
    Intensidad de la luz.
    Rango: 0.0 (apagada) a 2.0 (muy brillante)
    """
    
    color_temp: int = 5500
    """
    Temperatura de color en Kelvin.
    Valores típicos:
        - 2700K: Cálido (velas, atardecer)
        - 3200K: Tungsteno (luz incandescente)
        - 5500K: Luz día (neutral)
        - 6500K: Nublado (frío)
        - 10000K: Cielo azul (muy frío)
    """
    
    position: str = "front"
    """
    Posición relativa de la luz.
    Opciones:
        - front: Frontal
        - front_left: Frontal izquierda
        - front_right: Frontal derecha
        - back: Trasera
        - back_left: Trasera izquierda
        - back_right: Trasera derecha
        - side_left: Lateral izquierda
        - side_right: Lateral derecha
        - top: Superior
        - bottom: Inferior
    """
    
    softness: float = 0.5
    """
    Suavidad de la luz (dureza de sombras).
    Rango: 0.0 (luz dura, sombras definidas) a 1.0 (luz suave, sombras difusas)
    """
    
    angle: float = 45.0
    """
    Ángulo de incidencia en grados.
    Rango: 0-90
    """
    
    color_tint: Optional[str] = None
    """
    Tinte de color opcional (hex o nombre).
    Ejemplos: "#FF6B6B", "blue", "amber"
    """


@dataclass
class LightingSetup:
    """
    Configuración completa de iluminación para la escena.
    
    Simula setup profesional de iluminación cinematográfica.
    """
    
    # ============ PRESETS DE ILUMINACIÓN ============
    preset: str = "three_point"
    """
    Esquema de iluminación predefinido.
    Opciones:
        - three_point: Iluminación de tres puntos (clásica)
        - natural: Luz natural/realista
        - dramatic: Iluminación dramática (alto contraste)
        - high_key: Clave alta (brillante, pocas sombras)
        - low_key: Clave baja (oscuro, sombras marcadas)
        - rembrandt: Iluminación Rembrandt (triángulo en mejilla)
        - butterfly: Iluminación mariposa (sombra bajo nariz)
        - split: Iluminación dividida (mitad luz/mitad sombra)
        - loop: Iluminación loop (sombra nariz forma loop)
        - broad: Iluminación amplia
        - short: Iluminación corta
        - rim: Solo luz de contorno
        - silhouette: Silueta (contraluz)
    """
    
    # ============ MOMENTO DEL DÍA ============
    time_of_day: str = "golden_hour"
    """
    Momento del día que determina calidad de luz.
    Opciones:
        - dawn: Amanecer (5-7am, luz suave azulada)
        - golden_hour: Hora dorada (7-9am, 5-7pm, cálida)
        - morning: Mañana (9am-12pm, luz clara)
        - noon: Mediodía (12-2pm, luz dura cenital)
        - afternoon: Tarde (2-5pm)
        - blue_hour: Hora azul (antes amanecer/después atardecer)
        - dusk: Anochecer (luz cálida desapareciendo)
        - night: Noche (artificial o lunar)
        - overcast: Nublado (luz difusa todo el día)
    """
    
    # ============ FUENTES DE LUZ PERSONALIZADAS ============
    lights: Optional[List[LightSource]] = None
    """
    Lista de fuentes de luz individuales.
    Si es None, usa el preset. Si se define, tiene prioridad sobre preset.
    """
    
    # ============ AMBIENTE ============
    ambient_intensity: float = 0.3
    """
    Intensidad de luz ambiental general.
    Rango: 0.0 (oscuridad total) a 1.0 (muy brillante)
    """
    
    ambient_color: str = "neutral"
    """
    Color de la luz ambiental.
    Opciones:
        - neutral: Sin tinte
        - warm: Cálido (naranja/amarillo)
        - cool: Frío (azul)
        - custom: Usar ambient_color_hex
    """
    
    ambient_color_hex: Optional[str] = None
    """
    Color personalizado de ambiente en hex.
    Ejemplo: "#FFE5B4"
    """
    
    # ============ COLOR GRADING ============
    color_grading: str = "neutral"
    """
    Gradación de color cinematográfica.
    Opciones:
        - neutral: Sin gradación
        - warm: Tonos cálidos (naranja/amarillo)
        - cool: Tonos fríos (azul/cyan)
        - cinematic: Look cinematográfico (teal & orange)
        - vintage: Look vintage/retro
        - bleach_bypass: Proceso de blanqueado
        - cross_process: Proceso cruzado
        - sepia: Tono sepia (marrón antiguo)
        - black_white: Blanco y negro
        - noir: Film noir (alto contraste B&N)
        - cyberpunk: Neones saturados (magenta/cyan)
        - matrix: Verde matrix
        - blade_runner: Naranja/azul Blade Runner
    """
    
    # ============ CONTRASTE Y EXPOSICIÓN ============
    contrast: float = 1.0
    """
    Nivel de contraste.
    Rango: 0.5 (bajo contraste) a 2.0 (alto contraste)
    """
    
    exposure: float = 0.0
    """
    Compensación de exposición (brightness).
    Rango: -2.0 (subexpuesto) a +2.0 (sobreexpuesto)
    """
    
    highlights: float = 0.0
    """
    Control de altas luces.
    Rango: -1.0 (recuperar highlights) a +1.0 (potenciar)
    """
    
    shadows: float = 0.0
    """
    Control de sombras.
    Rango: -1.0 (oscurecer) a +1.0 (aclarar/recuperar detalle)
    """
    
    # ============ EFECTOS ATMOSFÉRICOS ============
    fog: float = 0.0
    """
    Densidad de niebla/neblina.
    Rango: 0.0 (sin niebla) a 1.0 (niebla densa)
    """
    
    haze: float = 0.0
    """
    Bruma atmosférica (god rays).
    Rango: 0.0 (sin bruma) a 1.0 (bruma intensa)
    """
    
    god_rays: bool = False
    """
    Rayos de luz volumétricos (god rays/crepuscular rays).
    """
    
    # ============ SOMBRAS ============
    shadow_intensity: float = 1.0
    """
    Intensidad de las sombras.
    Rango: 0.0 (sin sombras) a 2.0 (sombras muy marcadas)
    """
    
    shadow_softness: float = 0.5
    """
    Suavidad de las sombras.
    Rango: 0.0 (sombras duras) a 1.0 (sombras muy suaves)
    """
    
    # ============ EFECTOS ESPECIALES ============
    lens_flare: bool = False
    """
    Efecto de lens flare (destello de lente).
    """
    
    bloom: float = 0.0
    """
    Efecto de bloom (resplandor en luces brillantes).
    Rango: 0.0 (sin bloom) a 1.0 (bloom intenso)
    """
    
    def to_fibo_json(self) -> Dict[str, Any]:
        """
        Convierte los settings a formato JSON compatible con FIBO API.
        
        Returns:
            dict: Parámetros formateados para FIBO
        """
        result = {
            "lighting": {
                "preset": self.preset,
                "time_of_day": self.time_of_day,
                "ambient_intensity": self.ambient_intensity,
                "ambient_color": self.ambient_color,
                "color_grading": self.color_grading
            },
            "exposure": {
                "contrast": self.contrast,
                "exposure": self.exposure,
                "highlights": self.highlights,
                "shadows": self.shadows
            },
            "atmosphere": {
                "fog": self.fog,
                "haze": self.haze,
                "god_rays": self.god_rays
            },
            "shadows": {
                "intensity": self.shadow_intensity,
                "softness": self.shadow_softness
            },
            "effects": {
                "lens_flare": self.lens_flare,
                "bloom": self.bloom
            }
        }
        
        # Si hay luces personalizadas, incluirlas
        if self.lights:
            result["custom_lights"] = [
                {
                    "type": light.type,
                    "intensity": light.intensity,
                    "color_temp": light.color_temp,
                    "position": light.position,
                    "softness": light.softness,
                    "angle": light.angle,
                    "color_tint": light.color_tint
                }
                for light in self.lights
            ]
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte a diccionario simple.
        
        Returns:
            dict: Todos los campos como diccionario
        """
        data = asdict(self)
        # Convertir lista de LightSource a dicts
        if self.lights:
            data['lights'] = [asdict(light) for light in self.lights]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LightingSetup':
        """
        Crea una instancia desde un diccionario.
        
        Args:
            data: Diccionario con los parámetros
            
        Returns:
            LightingSetup: Instancia configurada
        """
        # Convertir lights si existen
        if 'lights' in data and data['lights']:
            data['lights'] = [LightSource(**light) for light in data['lights']]
        
        # Filtrar solo campos válidos
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)
    
    @classmethod
    def preset_natural_daylight(cls) -> 'LightingSetup':
        """
        Preset de luz natural diurna.
        
        Returns:
            LightingSetup: Configuración de luz natural
        """
        return cls(
            preset="natural",
            time_of_day="morning",
            ambient_intensity=0.7,
            color_grading="neutral",
            shadows=0.2,
            contrast=0.9
        )
    
    @classmethod
    def preset_golden_hour(cls) -> 'LightingSetup':
        """
        Preset de hora dorada (mágica).
        
        Returns:
            LightingSetup: Configuración hora dorada
        """
        return cls(
            preset="natural",
            time_of_day="golden_hour",
            ambient_intensity=0.6,
            color_grading="warm",
            exposure=0.3,
            haze=0.3,
            god_rays=True,
            bloom=0.4
        )
    
    @classmethod
    def preset_dramatic_noir(cls) -> 'LightingSetup':
        """
        Preset estilo film noir dramático.
        
        Returns:
            LightingSetup: Configuración noir
        """
        return cls(
            preset="low_key",
            time_of_day="night",
            ambient_intensity=0.1,
            color_grading="noir",
            contrast=1.8,
            shadows=-0.5,
            shadow_intensity=1.5,
            shadow_softness=0.2
        )
    
    @classmethod
    def preset_soft_portrait(cls) -> 'LightingSetup':
        """
        Preset para retratos suaves.
        
        Returns:
            LightingSetup: Configuración retrato suave
        """
        return cls(
            preset="rembrandt",
            time_of_day="overcast",
            ambient_intensity=0.5,
            color_grading="warm",
            shadow_softness=0.8,
            contrast=0.8,
            bloom=0.2
        )
    
    @classmethod
    def preset_cyberpunk(cls) -> 'LightingSetup':
        """
        Preset estilo cyberpunk con neones.
        
        Returns:
            LightingSetup: Configuración cyberpunk
        """
        return cls(
            preset="dramatic",
            time_of_day="night",
            ambient_intensity=0.2,
            color_grading="cyberpunk",
            contrast=1.4,
            fog=0.3,
            bloom=0.8,
            lens_flare=True
        )
    
    @classmethod
    def preset_blade_runner(cls) -> 'LightingSetup':
        """
        Preset estilo Blade Runner.
        
        Returns:
            LightingSetup: Configuración Blade Runner
        """
        return cls(
            preset="low_key",
            time_of_day="night",
            ambient_intensity=0.15,
            color_grading="blade_runner",
            contrast=1.3,
            fog=0.4,
            haze=0.5,
            god_rays=True,
            bloom=0.6
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Valida que los parámetros estén en rangos aceptables.
        
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        # Validar ambient_intensity
        if not 0.0 <= self.ambient_intensity <= 1.0:
            return False, "Ambient intensity debe estar entre 0.0 y 1.0"
        
        # Validar contrast
        if not 0.1 <= self.contrast <= 3.0:
            return False, "Contrast debe estar entre 0.1 y 3.0"
        
        # Validar exposure
        if not -3.0 <= self.exposure <= 3.0:
            return False, "Exposure debe estar entre -3.0 y 3.0"
        
        # Validar highlights y shadows
        if not -1.0 <= self.highlights <= 1.0:
            return False, "Highlights debe estar entre -1.0 y 1.0"
        if not -1.0 <= self.shadows <= 1.0:
            return False, "Shadows debe estar entre -1.0 y 1.0"
        
        # Validar fog y haze
        if not 0.0 <= self.fog <= 1.0:
            return False, "Fog debe estar entre 0.0 y 1.0"
        if not 0.0 <= self.haze <= 1.0:
            return False, "Haze debe estar entre 0.0 y 1.0"
        
        # Validar shadow_intensity
        if not 0.0 <= self.shadow_intensity <= 2.0:
            return False, "Shadow intensity debe estar entre 0.0 y 2.0"
        
        # Validar bloom
        if not 0.0 <= self.bloom <= 1.0:
            return False, "Bloom debe estar entre 0.0 y 1.0"
        
        # Validar luces personalizadas
        if self.lights:
            for i, light in enumerate(self.lights):
                if not 0.0 <= light.intensity <= 2.0:
                    return False, f"Light {i}: intensity debe estar entre 0.0 y 2.0"
                if not 1000 <= light.color_temp <= 12000:
                    return False, f"Light {i}: color_temp debe estar entre 1000K y 12000K"
                if not 0.0 <= light.softness <= 1.0:
                    return False, f"Light {i}: softness debe estar entre 0.0 y 1.0"
        
        return True, None