FIBO Director - Professional Cinematic Image Generation API
<img alt="Python" src="https://img.shields.io/badge/Python-3.12-blue.svg">
<img alt="Flask" src="https://img.shields.io/badge/Flask-3.0-green.svg">
<img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-15-blue.svg">
<img alt="Bria FIBO" src="https://img.shields.io/badge/Bria-FIBO API-orange.svg">

Transform 3D scene data into professional cinematic images using JSON-native control

FIBO Director is a production-ready REST API that bridges the gap between 3D visualization tools and AI image generation. By translating real-time 3D camera/lighting data into structured JSON parameters, it enables deterministic, controllable, and professional-grade image generation powered by Bria's FIBO foundation model.

🎯 Overview
The Problem
Traditional text-to-image generation relies on prompt engineering - an unpredictable, inconsistent process that makes professional workflows nearly impossible. Artists waste time tweaking prompts instead of focusing on creative decisions.

Our Solution
FIBO Director leverages FIBO's JSON-native control to provide:

✅ Deterministic generation: Same parameters = same results, every time
✅ Professional camera controls: FOV, focal length, aperture, shot types
✅ Cinematic lighting: Time of day, color grading, atmospheric effects
✅ 3D-to-2D translation: Real-time conversion of 3D scene data
✅ Production workflows: Project management, sequencing, versioning
🏆 Competition Categories Addressed
✨ Best Overall
JSON-native architecture throughout the entire pipeline
Mathematical translation from 3D coordinates to cinematic parameters
Professional-grade controls matching industry tools (Unreal, Cinema 4D)
Full commercial indemnity through FIBO's licensed training data
🎮 Best Controllability
Disentangled parameters: Camera angle, shot type, lighting independently controlled
Real-time preview: Interactive 3D scene manipulation → instant parameter mapping
Preset library: Predefined styles from renowned directors (Wes Anderson, Christopher Nolan)
Validation system: Ensures parameters stay within professional ranges
🤖 Best JSON-Native/Agentic Workflow
Zero prompt engineering: All control via structured JSON
LLM-friendly: Parameters translate seamlessly from natural language
Batch processing: Generate entire storyboards with consistent parameters
Reproducible pipelines: Store and replay entire generation sequences
🛠️ Best Professional Tool
Project-based organization: Manage campaigns, storyboards, sequences
User authentication & plans: Enterprise-ready user management
Generation history: Track, favorite, and reuse successful generations
API-first design: Integrate with any professional pipeline
🏗️ Architecture
🚀 Key Features
1. Mathematical 3D-to-Cinematic Translation
The Translator Service (app/services/translator.py) converts raw 3D data into professional parameters:

Mapping Logic:

Camera Angle: arctan(y/distance) → low_angle | eye_level | high_angle
Shot Type: distance → close_up | medium_shot | wide_shot
Lighting: Light angle relative to camera → rembrandt | butterfly | split
2. Dataclass-Based Scene Composition
Strongly-typed scene definitions prevent errors and enable IDE autocomplete:

3. Professional Presets Library
Director-inspired presets (app/routes/presets.py):

4. Intelligent Prompt Enhancement
FIBO Service (app/services/fibo_service.py) enriches prompts with cinematic context:

5. Project & Sequence Management
Organize generations into projects with multiple scenes:

📦 Installation
Prerequisites
Python 3.12+
PostgreSQL 15+
Bria FIBO API Key (Get one here)
1. Clone & Setup
2. Environment Configuration
Create .env file:

3. Database Setup
4. Run Server
Server runs at http://localhost:5000

🔌 API Reference
Authentication
Health Check
Single Image Generation
Method 1: Direct Parameters
Method 2: 3D Scene Data (Auto-Translated)
Response:

Sequence Generation (Storyboard)
Project Management
Generation History
Presets
🎨 Cinematic Parameters Reference
Camera Settings
Parameter	Type	Options	Description
angle	string	eye_level, low_angle, high_angle, birds_eye, dutch_angle	Vertical camera angle
shot_type	string	extreme_close_up, close_up, medium_shot, wide_shot, extreme_wide_shot	Subject framing
focal_length	float	10-500	Lens focal length (mm)
aperture	float	0.95-32	F-stop (lower = shallower DOF)
depth_of_field	string	shallow, medium, deep	Focus range
composition_rule	string	rule_of_thirds, golden_ratio, center, diagonal	Composition guide
Full schema: camera.py

Lighting Setup
Parameter	Type	Options	Description
preset	string	three_point, natural, dramatic, high_key, low_key, rembrandt	Lighting scheme
time_of_day	string	dawn, morning, golden_hour, day, blue_hour, night	Time-based lighting
color_grading	string	neutral, warm, cool, cinematic, cyberpunk, noir	Color treatment
fog	float	0.0-1.0	Atmospheric fog density
bloom	float	0.0-1.0	Light bloom intensity
god_rays	boolean	-	Volumetric light rays
Full schema: lighting.py

Scene Configuration
Parameter	Type	Range	Description
width	int	256-2048	Image width (px)
height	int	256-2048	Image height (px)
steps	int	10-100	Diffusion steps
guidance_scale	float	5.0-15.0	Prompt adherence
style	string	cinematic, realistic, artistic, anime	Overall style
detail_level	float	0.5-2.0	Detail intensity
Full schema: scene.py

🧪 Testing
Run Tests
Mock Mode (No API Calls)
Set in .env:

Returns placeholder images from https://picsum.photos/ for testing workflows without consuming API credits.

🔧 Development
Project Structure
Adding New Camera Presets
Edit camera.py:

Adding New Lighting Presets
Edit lighting.py:

🌟 Use Cases
1. Marketing Agencies
Generate consistent brand visuals across campaigns:

2. Game Development
Pre-visualize cinematics before rendering:

3. Film Pre-Production
Storyboard generation with director presets:

4. E-Commerce
Automated product photography:

📊 Performance
Generation Time: 2-5 seconds (with FIBO sync mode)
Consistency: 100% (same JSON = same output)
API Rate Limits:
Free: 100 generations/day
Pro: 500 generations/day
Enterprise: Unlimited
🤝 Contributing
We welcome contributions! Areas of focus:

New Translator Functions: Additional 3D coordinate mappings
Preset Library: More director/cinematographer styles
Validation: Enhanced parameter range checking
Documentation: API examples and tutorials
📝 License
MIT License - See LICENSE for details.

🙏 Acknowledgments
Bria.ai for the FIBO foundation model and API
FIBO Hackathon 2025 for inspiring this project
Open-source community for Flask, SQLAlchemy, and dependencies
📧 Contact
Author: [Your Name]
Email: your.email@example.com
Demo: https://fibo-director.demo
Documentation: https://docs.fibo-director.io
🚀 Next Steps
Try the API: Follow installation steps above
Explore Presets: GET /presets/directors
Generate Your First Image: Use the single generation endpoint
Build a Workflow: Create a project and sequence
Integrate with Your Tools: Use the 3D translation API
Made with ❤️ for the FIBO Hackathon 2025