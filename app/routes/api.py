from flask import Blueprint, jsonify, request
from app.services.fibo_service import FiboService

api_bp = Blueprint('api', __name__)

@api_bp.route('/generate', methods=['POST'])
def generate():
    data = request.json
    # Call the FiboService to handle the generation logic
    result = FiboService.generate(data)
    return jsonify(result), 200

@api_bp.route('/presets', methods=['GET'])
def get_presets():
    presets = FiboService.get_presets()
    return jsonify(presets), 200

@api_bp.route('/projects', methods=['GET'])
def get_projects():
    projects = FiboService.get_projects()
    return jsonify(projects), 200

@api_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = FiboService.get_project(project_id)
    return jsonify(project), 200

@api_bp.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    project = FiboService.create_project(data)
    return jsonify(project), 201

@api_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.json
    project = FiboService.update_project(project_id, data)
    return jsonify(project), 200

@api_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    FiboService.delete_project(project_id)
    return jsonify({'message': 'Project deleted'}), 204