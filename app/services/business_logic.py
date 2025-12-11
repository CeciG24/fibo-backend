# filepath: fibo-director/app/services/business_logic.py

from app.models.database_models import User
from app.models.database_models import Project
from app.models.database_models import Scene
from app.models.database_models import CameraSettings
from app.models.database_models import LightingSetup

class BusinessLogic:
    def __init__(self):
        self.users = []
        self.projects = []
        self.scenes = []

    def create_user(self, username, email, password):
        new_user = User(username=username, email=email, password=password)
        self.users.append(new_user)
        return new_user

    def create_project(self, user_id, project_name):
        new_project = Project(user_id=user_id, name=project_name)
        self.projects.append(new_project)
        return new_project

    def create_scene(self, project_id, scene_name, camera_settings, lighting_setup):
        new_scene = Scene(project_id=project_id, name=scene_name, camera=camera_settings, lighting=lighting_setup)
        self.scenes.append(new_scene)
        return new_scene

    def get_user_projects(self, user_id):
        return [project for project in self.projects if project.user_id == user_id]

    def get_project_scenes(self, project_id):
        return [scene for scene in self.scenes if scene.project_id == project_id]