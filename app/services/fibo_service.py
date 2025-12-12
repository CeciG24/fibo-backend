import requests
import os
import time
from typing import Optional, Dict, Any
from app.config import Config

class FIBOService:
    """Servicio para interactuar con FIBO API de Bria.ai"""
    
    def __init__(self):
        self.api_url = Config.FIBO_API_URL
        self.api_key = Config.FIBO_API_KEY
        self.mock_mode = os.getenv('FIBO_MOCK_MODE', 'false').lower() == 'true'
        
    def generate_image(self, scene_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera una imagen usando FIBO.
        En modo mock, simula la respuesta sin llamar a la API real.
        """
        # Si no hay API key o está en modo mock, usar mock
        if self.mock_mode or not self.api_key or self.api_key == 'tu-api-key-aqui-copia-la-de-production':
            return self._mock_generate(scene_payload)
        
        # Llamada real a FIBO API de Bria.ai
        return self._real_generate_bria(scene_payload)
    
    def _real_generate_bria(self, scene_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Llamada real a FIBO API de Bria.ai"""
        
        # Transformar el payload al formato de Bria.ai
        bria_payload = self._transform_to_bria_format(scene_payload)
        
        headers = {
            "Content-Type": "application/json",
            "api_token": self.api_key  # Bria usa "api_token" en header
        }
        
        try:
            # Endpoint de text-to-image de Bria
            url = f"{self.api_url}/image/generate/lite"
            
            print(f"🚀 Llamando a Bria.ai: {url}")
            print(f"📦 Payload: {bria_payload}")
            
            response = requests.post(
                url,
                json=bria_payload,
                headers=headers,
                timeout=300  # 5 minutos timeout
            )
            
            print(f"📡 Response status: {response.status_code}")
            
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Response: {result}")
            
            # Transformar respuesta de Bria al formato interno
            return self._transform_bria_response(result, bria_payload)
            
        except requests.exceptions.ConnectionError as e:
            return {
                "error": f"No se pudo conectar a Bria.ai: {str(e)}",
                "suggestion": "Verifica tu conexión a internet y la URL de la API"
            }
        except requests.exceptions.Timeout:
            return {
                "error": "La generación tardó demasiado tiempo",
                "suggestion": "Intenta con menos steps o menor resolución"
            }
        except requests.exceptions.HTTPError as e:
            error_detail = ""
            try:
                error_detail = e.response.json()
            except:
                error_detail = e.response.text
            
            return {
                "error": f"Error HTTP {e.response.status_code}",
                "detail": error_detail,
                "suggestion": "Verifica tu API key de Bria.ai"
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Error al generar imagen: {str(e)}"
            }
    
    def _transform_to_bria_format(self, scene_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforma nuestro payload interno al formato de Bria.ai FIBO.
        
        Según la documentación de Bria, el formato es:
        {
            "prompt": "...",
            "num_results": 1,
            "width": 1024,
            "height": 1024,
            "seed": 123456 (opcional)
        }
        """
        bria_payload = {
            "prompt": scene_payload.get("prompt", ""),
            "num_results": 1,  # Generar 1 imagen
            "width": scene_payload.get("width", 1024),
            "height": scene_payload.get("height", 1024)
        }
        
        # Agregar negative prompt si existe
        if scene_payload.get("negative_prompt"):
            bria_payload["negative_prompt"] = scene_payload["negative_prompt"]
        
        # Agregar seed si existe
        if scene_payload.get("seed"):
            bria_payload["seed"] = scene_payload["seed"]
        
        # Bria.ai también puede aceptar parámetros de estilo
        # Agregar los parámetros de cámara e iluminación al prompt
        enhanced_prompt = self._enhance_prompt_with_cinematics(
            bria_payload["prompt"],
            scene_payload
        )
        bria_payload["prompt"] = enhanced_prompt
        
        return bria_payload
    
    def _enhance_prompt_with_cinematics(self, base_prompt: str, scene_payload: Dict[str, Any]) -> str:
        """
        Mejora el prompt agregando descripciones cinematográficas.
        Como Bria no tiene parámetros específicos de cámara/luz,
        los agregamos al prompt de texto.
        """
        enhancements = []
        
        # Extraer info de cámara
        camera = scene_payload.get("camera", {})
        if camera:
            shot_type = camera.get("shot_type", "")
            angle = camera.get("angle", "")
            
            if shot_type:
                shot_descriptions = {
                    "close_up": "close-up shot",
                    "medium_shot": "medium shot",
                    "wide_shot": "wide shot",
                    "extreme_wide_shot": "extreme wide angle shot",
                    "full_shot": "full body shot"
                }
                if shot_type in shot_descriptions:
                    enhancements.append(shot_descriptions[shot_type])
            
            if angle and angle != "eye_level":
                angle_descriptions = {
                    "low_angle": "low angle view",
                    "high_angle": "high angle view",
                    "birds_eye": "aerial bird's eye view"
                }
                if angle in angle_descriptions:
                    enhancements.append(angle_descriptions[angle])
        
        # Extraer info de iluminación
        lighting = scene_payload.get("lighting", {})
        if lighting:
            time_of_day = lighting.get("time_of_day", "")
            color_grading = lighting.get("color_grading", "")
            
            if time_of_day:
                time_descriptions = {
                    "golden_hour": "golden hour lighting",
                    "blue_hour": "blue hour lighting",
                    "night": "night scene",
                    "dawn": "dawn lighting"
                }
                if time_of_day in time_descriptions:
                    enhancements.append(time_descriptions[time_of_day])
            
            if color_grading and color_grading != "neutral":
                grading_descriptions = {
                    "cinematic": "cinematic color grading",
                    "warm": "warm tones",
                    "cool": "cool tones",
                    "cyberpunk": "cyberpunk neon colors"
                }
                if color_grading in grading_descriptions:
                    enhancements.append(grading_descriptions[color_grading])
        
        # Agregar estilo si existe
        style = scene_payload.get("style", "")
        if style and style != "realistic":
            enhancements.append(f"{style} style")
        
        # Construir prompt mejorado
        if enhancements:
            enhanced = f"{base_prompt}, {', '.join(enhancements)}"
        else:
            enhanced = base_prompt
        
        return enhanced
    
    def _transform_bria_response(self, bria_result: Dict[str, Any], original_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforma la respuesta de Bria.ai a nuestro formato interno.
        
        Bria devuelve algo como:
        {
            "result": [
                {
                    "image_url": "https://...",
                    "seed": 123456
                }
            ]
        }
        """
        try:
            # Extraer primera imagen del resultado
            result = bria_result.get("result", [{}])[0]
            
            return {
                "success": True,
                "id": str(result.get("seed", "unknown")),
                "image_url": result.get("image_url", ""),
                "seed": result.get("seed"),
                "status": "completed",
                "mock": False,
                "provider": "bria.ai",
                "parameters": {
                    "prompt": original_payload.get("prompt"),
                    "width": original_payload.get("width"),
                    "height": original_payload.get("height")
                }
            }
        except Exception as e:
            return {
                "error": f"Error al procesar respuesta de Bria: {str(e)}",
                "raw_response": bria_result
            }
    
    def _mock_generate(self, scene_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modo MOCK para desarrollo sin API real.
        """
        import random
        import hashlib
        
        # Simular tiempo de generación
        time.sleep(1)
        
        # Generar ID único
        prompt = scene_payload.get('prompt', 'test')
        generation_id = hashlib.md5(prompt.encode()).hexdigest()[:12]
        
        # Generar seed
        seed = scene_payload.get('seed', random.randint(1, 999999))
        
        # Dimensiones
        width = scene_payload.get('width', 1024)
        height = scene_payload.get('height', 576)
        
        # URLs de ejemplo
        image_url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
        
        return {
            "success": True,
            "id": generation_id,
            "image_url": image_url,
            "seed": seed,
            "status": "completed",
            "mock": True,
            "provider": "mock",
            "message": "Imagen generada en modo MOCK (para desarrollo)",
            "parameters": {
                "prompt": scene_payload.get('prompt'),
                "width": width,
                "height": height
            }
        }
    
    def generate_sequence(self, scenes: list) -> list:
        """Genera una secuencia de frames"""
        results = []
        for i, scene in enumerate(scenes):
            print(f"Generando frame {i+1}/{len(scenes)}")
            result = self.generate_image(scene)
            results.append(result)
        return results
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica si la API de FIBO está disponible"""
        
        if self.mock_mode:
            return {
                "status": "healthy",
                "mode": "mock",
                "message": "Modo desarrollo (MOCK) activado"
            }
        
        if not self.api_key or self.api_key == 'tu-api-key-aqui-copia-la-de-production':
            return {
                "status": "not_configured",
                "mode": "real",
                "message": "API key no configurada. Agrega FIBO_API_KEY en .env"
            }
        
        try:
            # Probar conexión con endpoint simple
            response = requests.get(
                f"{self.api_url.replace('/v1', '')}/health",
                timeout=10
            )
            return {
                "status": "healthy" if response.status_code == 200 else "degraded",
                "mode": "real",
                "provider": "bria.ai",
                "api_url": self.api_url
            }
        except:
            return {
                "status": "unreachable",
                "mode": "real",
                "provider": "bria.ai",
                "api_url": self.api_url,
                "message": "No se pudo conectar a Bria.ai"
            }