import requests
from typing import Optional, Dict, Any
from app.config import Config

class FIBOService:
    """Servicio para interactuar con FIBO API"""
    
    def __init__(self):
        self.api_url = Config.FIBO_API_URL
        self.api_key = Config.FIBO_API_KEY
        
    def generate_image(self, scene_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Genera una imagen usando FIBO"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json=scene_payload,
                headers=headers,
                timeout=300  # 5 minutos timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def generate_sequence(self, scenes: list) -> list:
        """Genera una secuencia de frames"""
        results = []
        for i, scene in enumerate(scenes):
            print(f"Generando frame {i+1}/{len(scenes)}")
            result = self.generate_image(scene)
            results.append(result)
        return results
    
    def get_generation_status(self, generation_id: str) -> Dict[str, Any]:
        """Obtiene el estado de una generación asíncrona"""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            response = requests.get(
                f"{self.api_url}/status/{generation_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}      