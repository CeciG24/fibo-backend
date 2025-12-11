from pydantic import BaseModel, constr, conint
from typing import List, Optional

class UserSchema(BaseModel):
    id: int
    username: constr(min_length=3, max_length=50)
    email: constr(regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    full_name: Optional[constr(max_length=100)] = None

class ProjectSchema(BaseModel):
    id: int
    title: constr(min_length=1, max_length=100)
    description: Optional[constr(max_length=500)] = None
    user_id: int

class SceneSchema(BaseModel):
    id: int
    project_id: int
    name: constr(min_length=1, max_length=100)
    parameters: dict

class CameraSettingsSchema(BaseModel):
    id: int
    scene_id: int
    resolution: str
    frame_rate: conint(gt=0)

class LightingSetupSchema(BaseModel):
    id: int
    scene_id: int
    intensity: conint(ge=0)
    color: str

class AuthSchema(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6)

class FiboSchema(BaseModel):
    input_data: dict
    output_data: dict
    status: str

class ValidationErrorSchema(BaseModel):
    detail: List[str]