from flask import Blueprint, jsonify

bp = Blueprint('presets', __name__)

DIRECTOR_PRESETS = {
    "wes_anderson": {
        "name": "Wes Anderson",
        "camera": {
            "angle": "eye_level",
            "shot_type": "medium_shot",
            "composition_rule": "center"
        },
        "lighting": {
            "preset": "high_key",
            "color_grading": "warm"
        },
        "style": "cinematic"
    },
    "christopher_nolan": {
        "name": "Christopher Nolan",
        "camera": {
            "angle": "low_angle",
            "shot_type": "wide_shot",
            "fov": 35.0
        },
        "lighting": {
            "preset": "dramatic",
            "color_grading": "cool"
        },
        "style": "realistic"
    },
    "roger_deakins": {
        "name": "Roger Deakins (Cinematographer)",
        "camera": {
            "shot_type": "full_shot",
            "depth_of_field": "shallow"
        },
        "lighting": {
            "preset": "natural",
            "time_of_day": "golden_hour",
            "color_grading": "cinematic"
        }
    }
}

@bp.route('/list', methods=['GET'])
def list_presets():
    """Lista todos los presets de directores"""
    return jsonify(DIRECTOR_PRESETS)

@bp.route('/<preset_name>', methods=['GET'])
def get_preset(preset_name):
    """Obtiene un preset específico"""
    preset = DIRECTOR_PRESETS.get(preset_name)
    if not preset:
        return jsonify({"error": "Preset not found"}), 404
    return jsonify(preset)