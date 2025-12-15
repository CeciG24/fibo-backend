# FIBO Director - Professional Cinematic Image Generation API

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Bria FIBO](https://img.shields.io/badge/Bria-FIBO%20API-orange.svg)](https://bria.ai/)

> **Transform 3D scene data into professional cinematic images using JSON-native control**

FIBO Director is a production-ready REST API that bridges the gap between 3D visualization tools and AI image generation. By translating real-time 3D camera/lighting data into structured JSON parameters, it enables **deterministic, controllable, and professional-grade image generation** powered by Bria's FIBO foundation model.

---

## 🎯 Overview

### The Problem

Traditional text-to-image generation relies on prompt engineering - an unpredictable, inconsistent process that makes professional workflows nearly impossible. Artists waste time tweaking prompts instead of focusing on creative decisions.

### Our Solution

**FIBO Director** leverages FIBO's JSON-native control to provide:

- ✅ **Deterministic generation**: Same parameters = same results, every time
- ✅ **Professional camera controls**: FOV, focal length, aperture, shot types
- ✅ **Cinematic lighting**: Time of day, color grading, atmospheric effects
- ✅ **3D-to-2D translation**: Real-time conversion of 3D scene data
- ✅ **Production workflows**: Project management, sequencing, versioning

---

## 🏆 Competition Categories Addressed

### ✨ Best Overall

- **JSON-native architecture** throughout the entire pipeline
- **Mathematical translation** from 3D coordinates to cinematic parameters
- **Professional-grade controls** matching industry tools (Unreal, Cinema 4D)
- Full **commercial indemnity** through FIBO's licensed training data

### 🎮 Best Controllability

- **Disentangled parameters**: Camera angle, shot type, lighting independently controlled
- **Real-time preview**: Interactive 3D scene manipulation → instant parameter mapping
- **Preset library**: Predefined styles from renowned directors (Wes Anderson, Christopher Nolan)
- **Validation system**: Ensures parameters stay within professional ranges

### 🤖 Best JSON-Native/Agentic Workflow

- **Zero prompt engineering**: All control via structured JSON
- **LLM-friendly**: Parameters translate seamlessly from natural language
- **Batch processing**: Generate entire storyboards with consistent parameters
- **Reproducible pipelines**: Store and replay entire generation sequences

### 🛠️ Best Professional Tool

- **Project-based organization**: Manage campaigns, storyboards, sequences
- **User authentication & plans**: Enterprise-ready user management
- **Generation history**: Track, favorite, and reuse successful generations
- **API-first design**: Integrate with any professional pipeline

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend 3D   │  (Three.js, React Three Fiber)
│   Scene Editor  │
└────────┬────────┘
         │ Camera: {position, rotation, fov}
         │ Light: {position, intensity, color}
         ▼
┌─────────────────────────────────────────┐
│       FIBO Director API (Flask)         │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   Translator Service            │   │
│  │  (3D → Cinematic Parameters)    │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│             ▼                           │
│  ┌─────────────────────────────────┐   │
│  │   Scene Builder                 │   │
│  │  - Camera Settings              │   │
│  │  - Lighting Setup               │   │
│  │  - Composition Rules            │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│             ▼                           │
│  ┌─────────────────────────────────┐   │
│  │   FIBO Service                  │   │
│  │  (Bria.ai Integration)          │   │
│  └──────────┬──────────────────────┘   │
└─────────────┼───────────────────────────┘
              │ Enhanced JSON Payload
              ▼
    ┌──────────────────┐
    │   Bria FIBO API  │
    │  (Text-to-Image) │
    └──────────┬───────┘
               │
               ▼
         Generated Image
```

---

## 🚀 Key Features

### 1. Mathematical 3D-to-Cinematic Translation

The **Translator Service** (`app/services/translator.py`) converts raw 3D data into professional parameters:

```python
# Input: 3D camera position [x, y, z]
camera_position = [0, 2, 5]  # Eye-level, medium distance

# Output: Cinematic parameters
{
    "angle": "eye_level",        # Calculated from Y position
    "shot_type": "medium_shot",  # Calculated from distance
    "fov": 50,                   # Direct mapping
    "lighting": "three_point"    # Derived from light position
}
```

**Mapping Logic:**

- **Camera Angle**: `arctan(y/distance)` → `low_angle` | `eye_level` | `high_angle`
- **Shot Type**: `distance` → `close_up` | `medium_shot` | `wide_shot`
- **Lighting**: Light angle relative to camera → `rembrandt` | `butterfly` | `split`

### 2. Dataclass-Based Scene Composition

Strongly-typed scene definitions prevent errors and enable IDE autocomplete:

```python
from app.models.scene import Scene
from app.models.camera import CameraSettings
from app.models.lighting import LightingSetup

scene = Scene(
    prompt="A cyberpunk street at night",
    camera=CameraSettings(
        angle="low_angle",
        shot_type="wide_shot",
        focal_length=24.0,      # mm
        aperture=2.8,           # f-stop
        depth_of_field="shallow"
    ),
    lighting=LightingSetup(
        preset="dramatic",
        time_of_day="night",
        color_grading="cyberpunk",
        fog=0.3,
        bloom=0.8
    ),
    width=1920,
    height=1080
)
```

### 3. Professional Presets Library

Director-inspired presets (`app/routes/presets.py`):

```python
# Wes Anderson Style
{
    "camera": {"angle": "eye_level", "composition_rule": "center"},
    "lighting": {"preset": "high_key", "color_grading": "warm"},
    "style": "cinematic"
}

# Roger Deakins (Blade Runner)
{
    "camera": {"angle": "low_angle", "focal_length": 35},
    "lighting": {"preset": "low_key", "fog": 0.4, "god_rays": True},
    "style": "cinematic"
}
```

### 4. Intelligent Prompt Enhancement

FIBO Service (`app/services/fibo_service.py`) enriches prompts with cinematic context:

```python
# Base prompt
"A detective in a dark alley"

# Enhanced with camera/lighting data
"A detective in a dark alley, low angle view, wide shot,
night scene, dramatic noir lighting, cyberpunk neon colors,
cinematic color grading"
```

### 5. Project & Sequence Management

Organize generations into projects with multiple scenes:

```python
POST /projects/
{
    "title": "Cyberpunk Campaign",
    "description": "Marketing materials for new game",
    "aspect_ratio": "16:9"
}

POST /generation/sequence
{
    "project_id": 1,
    "scenes": [
        {"prompt": "Hero closeup", "camera": {...}, "lighting": {...}},
        {"prompt": "City panorama", "camera": {...}, "lighting": {...}},
        {"prompt": "Action sequence", "camera": {...}, "lighting": {...}}
    ]
}
```

---

## 📦 Installation

### Prerequisites

- Python 3.12+
- PostgreSQL 15+
- Bria FIBO API Key ([Get one here](https://bria.ai/))

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/fibo-director.git
cd fibo-director

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create `.env` file:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/fibodb

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# FIBO API
FIBO_API_URL=https://engine.prod.bria-api.com/v2
FIBO_API_KEY=your-bria-api-key-here

# Development
FIBO_MOCK_MODE=false  # Set to true for testing without API calls
FLASK_ENV=development
```

### 3. Database Setup

```bash
# Initialize migrations
flask db init

# Run migrations
flask db upgrade
```

### 4. Run Server

```bash
# Development
python run.py

# Production (with gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

Server runs at `http://localhost:5000`

---

## 🔌 API Reference

### Authentication

```bash
# Register
POST /auth/register
{
    "username": "director",
    "email": "director@studio.com",
    "password": "secure123"
}

# Login
POST /auth/login
{
    "username": "director",
    "password": "secure123"
}
# Returns: {"access_token": "eyJ..."}
```

### Health Check

```bash
GET /generation/health
# Returns FIBO API connection status
```

### Single Image Generation

#### Method 1: Direct Parameters

```bash
POST /generation/single
Headers: Authorization: Bearer <token>

{
    "prompt": "A futuristic city at sunset",
    "camera": {
        "angle": "high_angle",
        "shot_type": "extreme_wide_shot",
        "focal_length": 24.0,
        "aperture": 11.0,
        "depth_of_field": "deep"
    },
    "lighting": {
        "preset": "natural",
        "time_of_day": "golden_hour",
        "color_grading": "warm",
        "bloom": 0.4
    },
    "width": 1920,
    "height": 1080,
    "style": "cinematic"
}
```

#### Method 2: 3D Scene Data (Auto-Translated)

```bash
POST /generation/single
Headers: Authorization: Bearer <token>

{
    "prompt": "A detective in a dark alley",
    "raw_camera": {
        "position": [0, 1.5, 8],
        "rotation": [0, 0, 0],
        "fov": 45
    },
    "raw_light": {
        "position": [5, 3, 2]
    },
    "width": 1024,
    "height": 576
}
```

**Response:**

```json
{
    "success": true,
    "generation": {
        "id": 42,
        "image_url": "https://cdn.bria.ai/...",
        "seed": 123456,
        "status": "completed",
        "generation_time": 2.3,
        "parameters": {...}
    },
    "remaining_today": 450
}
```

### Sequence Generation (Storyboard)

```bash
POST /generation/sequence
Headers: Authorization: Bearer <token>

{
    "project_id": 1,
    "scenes": [
        {
            "prompt": "Opening shot: city skyline at dawn",
            "camera": {"angle": "low_angle", "shot_type": "extreme_wide_shot"},
            "lighting": {"time_of_day": "dawn", "color_grading": "cool"}
        },
        {
            "prompt": "Hero enters frame",
            "camera": {"angle": "eye_level", "shot_type": "medium_shot"},
            "lighting": {"preset": "three_point", "color_grading": "cinematic"}
        },
        {
            "prompt": "Closeup on hero's face",
            "camera": {"angle": "eye_level", "shot_type": "close_up"},
            "lighting": {"preset": "rembrandt", "color_grading": "warm"}
        }
    ]
}
```

### Project Management

```bash
# Create project
POST /projects/
{
    "title": "Spring Campaign 2025",
    "description": "Product launch visuals",
    "aspect_ratio": "16:9"
}

# List projects
GET /projects/

# Get project with all generations
GET /projects/:id

# Update project
PUT /projects/:id
{
    "title": "Updated Title",
    "is_public": true
}

# Get project statistics
GET /projects/:id/stats
```

### Generation History

```bash
# Get user's generation history
GET /generation/history?page=1&per_page=20

# Filter by project
GET /generation/history?project_id=1

# Filter by status
GET /generation/history?status=completed

# Get specific generation
GET /generation/:id

# Toggle favorite
POST /generation/:id/favorite

# Delete generation
DELETE /generation/:id
```

### Presets

```bash
# Get all director presets
GET /presets/directors

# Get camera presets
GET /presets/camera

# Get lighting presets
GET /presets/lighting
```

---

## 🎨 Cinematic Parameters Reference

### Camera Settings

| Parameter          | Type   | Options                                                                         | Description                    |
| ------------------ | ------ | ------------------------------------------------------------------------------- | ------------------------------ |
| `angle`            | string | `eye_level`, `low_angle`, `high_angle`, `birds_eye`, `dutch_angle`              | Vertical camera angle          |
| `shot_type`        | string | `extreme_close_up`, `close_up`, `medium_shot`, `wide_shot`, `extreme_wide_shot` | Subject framing                |
| `focal_length`     | float  | 10-500                                                                          | Lens focal length (mm)         |
| `aperture`         | float  | 0.95-32                                                                         | F-stop (lower = shallower DOF) |
| `depth_of_field`   | string | `shallow`, `medium`, `deep`                                                     | Focus range                    |
| `composition_rule` | string | `rule_of_thirds`, `golden_ratio`, `center`, `diagonal`                          | Composition guide              |

**Full schema:** `app/models/camera.py`

### Lighting Setup

| Parameter       | Type    | Options                                                                  | Description             |
| --------------- | ------- | ------------------------------------------------------------------------ | ----------------------- |
| `preset`        | string  | `three_point`, `natural`, `dramatic`, `high_key`, `low_key`, `rembrandt` | Lighting scheme         |
| `time_of_day`   | string  | `dawn`, `morning`, `golden_hour`, `day`, `blue_hour`, `night`            | Time-based lighting     |
| `color_grading` | string  | `neutral`, `warm`, `cool`, `cinematic`, `cyberpunk`, `noir`              | Color treatment         |
| `fog`           | float   | 0.0-1.0                                                                  | Atmospheric fog density |
| `bloom`         | float   | 0.0-1.0                                                                  | Light bloom intensity   |
| `god_rays`      | boolean | -                                                                        | Volumetric light rays   |

**Full schema:** `app/models/lighting.py`

### Scene Configuration

| Parameter        | Type   | Range                                         | Description       |
| ---------------- | ------ | --------------------------------------------- | ----------------- |
| `width`          | int    | 256-2048                                      | Image width (px)  |
| `height`         | int    | 256-2048                                      | Image height (px) |
| `steps`          | int    | 10-100                                        | Diffusion steps   |
| `guidance_scale` | float  | 5.0-15.0                                      | Prompt adherence  |
| `style`          | string | `cinematic`, `realistic`, `artistic`, `anime` | Overall style     |
| `detail_level`   | float  | 0.5-2.0                                       | Detail intensity  |

**Full schema:** `app/models/scene.py`

---

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_services.py

# With coverage
pytest --cov=app tests/
```

### Mock Mode (No API Calls)

Set in `.env`:

```env
FIBO_MOCK_MODE=true
```

Returns placeholder images from `https://picsum.photos/` for testing workflows without consuming API credits.

---

## 🔧 Development

### Project Structure

```
fibo-director/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration
│   ├── models/                  # Data models
│   │   ├── user.py              # User & auth
│   │   ├── project.py           # Projects & generations
│   │   ├── camera.py            # Camera settings dataclass
│   │   ├── lighting.py          # Lighting setup dataclass
│   │   └── scene.py             # Scene composition
│   ├── routes/                  # API endpoints
│   │   ├── auth.py              # Authentication
│   │   ├── projects.py          # Project CRUD
│   │   ├── generation.py        # Image generation
│   │   ├── users.py             # User profiles
│   │   └── presets.py           # Preset library
│   ├── services/                # Business logic
│   │   ├── fibo_service.py      # Bria API integration
│   │   ├── translator.py        # 3D → Cinematic conversion
│   │   └── scene_builder.py     # Scene construction helpers
│   ├── middleware/              # Custom middleware
│   │   └── auth_middleware.py   # JWT & permissions
│   └── schemas/                 # Pydantic validation
│       └── validation.py
├── migrations/                  # Database migrations
├── tests/                       # Test suite
├── requirements.txt
└── run.py                       # App entry point
```

### Adding New Camera Presets

Edit `app/models/camera.py`:

```python
@classmethod
def preset_action_hero(cls) -> 'CameraSettings':
    """Dynamic action sequence preset"""
    return cls(
        angle="low_angle",
        shot_type="medium_full_shot",
        focal_length=28.0,
        aperture=4.0,
        depth_of_field="medium",
        composition_rule="diagonal"
    )
```

### Adding New Lighting Presets

Edit `app/models/lighting.py`:

```python
@classmethod
def preset_horror(cls) -> 'LightingSetup':
    """Horror film lighting"""
    return cls(
        preset="low_key",
        time_of_day="night",
        ambient_intensity=0.1,
        color_grading="noir",
        contrast=1.8,
        fog=0.5,
        shadow_intensity=1.5
    )
```

---

## 🌟 Use Cases

### 1. Marketing Agencies

Generate consistent brand visuals across campaigns:

```python
# Brand guidelines as JSON
brand_params = {
    "camera": {"composition_rule": "rule_of_thirds"},
    "lighting": {"color_grading": "warm"},
    "color_palette": "earth_tones"
}

# Apply to all product shots
for product in products:
    generate(prompt=product.description, **brand_params)
```

### 2. Game Development

Pre-visualize cinematics before rendering:

```python
# Export Unity camera data → FIBO parameters
unity_camera = {"position": [0, 2, 5], "fov": 60}
translated = translate_camera_data(unity_camera)
preview = generate(prompt="Battlefield scene", **translated)
```

### 3. Film Pre-Production

Storyboard generation with director presets:

```python
# Apply Roger Deakins style to entire sequence
scenes = [
    "Opening: City at night",
    "Hero enters bar",
    "Confrontation"
]

for scene in scenes:
    generate(scene, preset="roger_deakins")
```

### 4. E-Commerce

Automated product photography:

```python
# Consistent product shots
product_preset = {
    "camera": {"angle": "eye_level", "shot_type": "close_up"},
    "lighting": {"preset": "high_key", "time_of_day": "overcast"},
    "style": "realistic"
}

generate(f"Product on white background: {product.name}", **product_preset)
```

---

## 📊 Performance

- **Generation Time**: 2-5 seconds (with FIBO sync mode)
- **Consistency**: 100% (same JSON = same output)
- **API Rate Limits**:
  - Free: 100 generations/day
  - Pro: 500 generations/day
  - Enterprise: Unlimited

---

## 🤝 Contributing

We welcome contributions! Areas of focus:

1. **New Translator Functions**: Additional 3D coordinate mappings
2. **Preset Library**: More director/cinematographer styles
3. **Validation**: Enhanced parameter range checking
4. **Documentation**: API examples and tutorials

```bash
# Fork the repo
git checkout -b feature/amazing-preset

# Make changes
git commit -m "Add Tarantino preset"

# Submit PR
git push origin feature/amazing-preset
```

---

## 📝 License

MIT License - See LICENSE for details.

---

## 🙏 Acknowledgments

- **Bria.ai** for the FIBO foundation model and API
- **FIBO Hackathon 2025** for inspiring this project
- Open-source community for Flask, SQLAlchemy, and dependencies

---

## 📧 Contact

- **Author**: [Your Name]
- **Email**: your.email@example.com
- **Demo**: [https://fibo-director.demo](https://fibo-director.demo)
- **Documentation**: [https://docs.fibo-director.io](https://docs.fibo-director.io)

---

## 🚀 Next Steps

1. **Try the API**: Follow installation steps above
2. **Explore Presets**: `GET /presets/directors`
3. **Generate Your First Image**: Use the single generation endpoint
4. **Build a Workflow**: Create a project and sequence
5. **Integrate with Your Tools**: Use the 3D translation API

---

**Made with ❤️ for the FIBO Hackathon 2025**
