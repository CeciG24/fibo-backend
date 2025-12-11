from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any

@dataclass
class CameraSettings:
    """
    Configuración de cámara estilo cinematográfico.
    
    Simula controles profesionales de cámara para generación de imágenes.
    Todos los parámetros están inspirados en cinematografía real.
    """
    
    # ============ ÁNGULOS DE CÁMARA ============
    angle: str = "eye_level"
    """
    Ángulo vertical de la cámara.
    Opciones:
        - eye_level: A la altura de los ojos (neutro)
        - high_angle: Ángulo alto (mirando hacia abajo, hace al sujeto pequeño)
        - low_angle: Ángulo bajo (mirando hacia arriba, hace al sujeto poderoso)
        - birds_eye: Vista aérea desde arriba (90 grados)
        - dutch_angle: Ángulo holandés (cámara inclinada, tensión)
        - worms_eye: Vista desde el suelo mirando hacia arriba
    """
    
    # ============ TIPOS DE ENCUADRE ============
    shot_type: str = "medium_shot"
    """
    Distancia y encuadre del sujeto.
    Opciones:
        - extreme_close_up: Primer plano extremo (ojos, detalles)
        - close_up: Primer plano (cabeza y hombros)
        - medium_close_up: Plano medio corto (pecho para arriba)
        - medium_shot: Plano medio (cintura para arriba)
        - medium_full_shot: Plano americano (rodillas para arriba)
        - full_shot: Plano completo (cuerpo entero)
        - wide_shot: Plano general (sujeto + entorno)
        - extreme_wide_shot: Gran plano general (paisaje amplio)
    """
    
    # ============ MOVIMIENTO DE CÁMARA ============
    movement: Optional[str] = None
    """
    Tipo de movimiento de cámara (para secuencias).
    Opciones:
        - static: Sin movimiento
        - pan_left: Paneo hacia la izquierda
        - pan_right: Paneo hacia la derecha
        - tilt_up: Inclinación hacia arriba
        - tilt_down: Inclinación hacia abajo
        - dolly_in: Acercamiento (travelling in)
        - dolly_out: Alejamiento (travelling out)
        - zoom_in: Zoom acercamiento
        - zoom_out: Zoom alejamiento
        - tracking: Seguimiento lateral
        - crane_up: Grúa ascendente
        - crane_down: Grúa descendente
    """
    
    # ============ PARÁMETROS TÉCNICOS ============
    fov: float = 50.0
    """
    Field of View (Campo de visión) en grados.
    Rango típico: 15-120
        - 15-35: Telefoto (comprime espacio, baja distorsión)
        - 40-60: Normal (visión natural humana)
        - 70-120: Gran angular (exagera perspectiva, distorsión)
    """
    
    focal_length: float = 50.0
    """
    Distancia focal en milímetros (equivalente 35mm).
    Valores comunes:
        - 24mm: Gran angular, landscapes
        - 35mm: Cine documental
        - 50mm: Visión humana, versátil
        - 85mm: Retratos, bokeh hermoso
        - 135mm: Telefoto, compresión
    """
    
    aperture: float = 2.8
    """
    Apertura del diafragma (f-stop).
    Rango típico: 1.4-22
        - f/1.4-2.8: Apertura amplia, bokeh fuerte, baja profundidad
        - f/4-5.6: Apertura moderada, balance
        - f/8-16: Apertura cerrada, todo enfocado
    Menor número = más luz + menos profundidad de campo
    """
    
    sensor_size: str = "full_frame"
    """
    Tamaño del sensor de la cámara.
    Opciones:
        - full_frame: 35mm completo (más cinematic)
        - aps_c: Crop sensor (más zoom aparente)
        - medium_format: Sensor más grande (ultra detalle)
    """
    
    # ============ COMPOSICIÓN ============
    composition_rule: str = "rule_of_thirds"
    """
    Regla de composición a seguir.
    Opciones:
        - rule_of_thirds: Regla de tercios (clásica)
        - center: Composición centrada (simétrica)
        - golden_ratio: Proporción áurea
        - diagonal: Líneas diagonales (dinámica)
        - frame_within_frame: Marco dentro del marco
        - leading_lines: Líneas guía hacia el sujeto
        - symmetry: Simetría perfecta
    """
    
    depth_of_field: str = "medium"
    """
    Profundidad de campo (cuánto está enfocado).
    Opciones:
        - shallow: Poca profundidad (bokeh fuerte, sujeto aislado)
        - medium: Profundidad media (balance)
        - deep: Mucha profundidad (todo enfocado, paisajes)
    """
    
    focus_point: str = "center"
    """
    Punto de enfoque en la composición.
    Opciones:
        - center: Centro de la imagen
        - left_third: Tercio izquierdo
        - right_third: Tercio derecho
        - foreground: Primer plano
        - background: Fondo
        - eyes: Ojos del sujeto (retratos)
    """
    
    # ============ EFECTOS ÓPTICOS ============
    lens_distortion: float = 0.0
    """
    Distorsión de lente.
    Rango: -1.0 a 1.0
        - Negativo: Distorsión barril (gran angular)
        - 0: Sin distorsión
        - Positivo: Distorsión almohada (telefoto)
    """
    
    vignette: float = 0.0
    """
    Viñeteado (oscurecimiento de bordes).
    Rango: 0.0 (sin viñeta) a 1.0 (viñeta fuerte)
    """
    
    chromatic_aberration: bool = False
    """
    Aberración cromática (efecto vintage de lentes antiguas).
    """
    
    # ============ ASPECT RATIO ============
    aspect_ratio: str = "16:9"
    """
    Relación de aspecto de la imagen.
    Opciones:
        - 16:9: Widescreen moderno (HD, 4K)
        - 21:9: Cinemascope (ultra wide)
        - 4:3: Formato clásico (TV antigua)
        - 1:1: Cuadrado (Instagram)
        - 9:16: Vertical (TikTok, Stories)
        - 2.39:1: Anamórfico (cine épico)
    """
    
    def to_fibo_json(self) -> Dict[str, Any]:
        """
        Convierte los settings a formato JSON compatible con FIBO API.
        
        Returns:
            dict: Parámetros formateados para FIBO
        """
        return {
            "camera": {
                "angle": self.angle,
                "shot_type": self.shot_type,
                "movement": self.movement,
                "fov": self.fov,
                "focal_length": self.focal_length,
                "aperture": self.aperture,
                "sensor_size": self.sensor_size
            },
            "composition": {
                "rule": self.composition_rule,
                "depth_of_field": self.depth_of_field,
                "focus_point": self.focus_point
            },
            "optical_effects": {
                "lens_distortion": self.lens_distortion,
                "vignette": self.vignette,
                "chromatic_aberration": self.chromatic_aberration
            },
            "format": {
                "aspect_ratio": self.aspect_ratio
            }
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte a diccionario simple.
        
        Returns:
            dict: Todos los campos como diccionario
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CameraSettings':
        """
        Crea una instancia desde un diccionario.
        
        Args:
            data: Diccionario con los parámetros
            
        Returns:
            CameraSettings: Instancia configurada
        """
        # Filtrar solo campos válidos
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)
    
    @classmethod
    def preset_portrait(cls) -> 'CameraSettings':
        """
        Preset optimizado para retratos.
        
        Returns:
            CameraSettings: Configuración para retratos
        """
        return cls(
            angle="eye_level",
            shot_type="close_up",
            focal_length=85.0,
            aperture=1.8,
            depth_of_field="shallow",
            composition_rule="rule_of_thirds",
            focus_point="eyes"
        )
    
    @classmethod
    def preset_landscape(cls) -> 'CameraSettings':
        """
        Preset optimizado para paisajes.
        
        Returns:
            CameraSettings: Configuración para paisajes
        """
        return cls(
            angle="eye_level",
            shot_type="extreme_wide_shot",
            focal_length=24.0,
            aperture=11.0,
            depth_of_field="deep",
            composition_rule="rule_of_thirds"
        )
    
    @classmethod
    def preset_cinematic(cls) -> 'CameraSettings':
        """
        Preset estilo cinematográfico.
        
        Returns:
            CameraSettings: Configuración cinematográfica
        """
        return cls(
            angle="low_angle",
            shot_type="medium_shot",
            focal_length=35.0,
            aperture=2.8,
            depth_of_field="shallow",
            aspect_ratio="21:9",
            vignette=0.3
        )
    
    @classmethod
    def preset_documentary(cls) -> 'CameraSettings':
        """
        Preset estilo documental.
        
        Returns:
            CameraSettings: Configuración documental
        """
        return cls(
            angle="eye_level",
            shot_type="medium_shot",
            focal_length=35.0,
            aperture=4.0,
            depth_of_field="medium",
            composition_rule="center"
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Valida que los parámetros estén en rangos aceptables.
        
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        # Validar FOV
        if not 10 <= self.fov <= 150:
            return False, "FOV debe estar entre 10 y 150 grados"
        
        # Validar focal length
        if not 10 <= self.focal_length <= 500:
            return False, "Focal length debe estar entre 10mm y 500mm"
        
        # Validar aperture
        if not 0.95 <= self.aperture <= 32:
            return False, "Aperture debe estar entre f/0.95 y f/32"
        
        # Validar lens distortion
        if not -1.0 <= self.lens_distortion <= 1.0:
            return False, "Lens distortion debe estar entre -1.0 y 1.0"
        
        # Validar vignette
        if not 0.0 <= self.vignette <= 1.0:
            return False, "Vignette debe estar entre 0.0 y 1.0"
        
        return True, None