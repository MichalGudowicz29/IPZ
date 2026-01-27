# Beach Crowd Analysis System

## Overview
AI-powered beach crowd detection system that analyzes video footage using the Moondream2 vision-language model to determine crowd levels.

## Hardware Requirements
- **GPU**: NVIDIA CUDA-compatible GPU (required)
- **RAM**: Minimum 8GB (16GB+ recommended for model loading)
- **Storage**: ~5GB for model weights

## Software Dependencies
```bash
pip install torch transformers pillow opencv-python numpy
```

## Project Structure
```
IPZ/
├── src/
│   ├── main.py          # Main analysis script
│   └── videos/          # Video files directory
│       └── beach_video.mp4
└── deploy-src.sh        # Deployment script
```

## How to Run

### Local Execution
```bash
cd src
python main.py
```

### Remote Deployment
```bash
./deploy-src.sh
```
Deploys to: `dataengine@31.193.99.96:~/src`

## Usage
1. Place video file in `src/videos/` directory
2. Edit `video_file` variable in [`main.py`](src/main.py:205) to match your filename
3. Run the script
4. Results saved as `analysis_<filename>.json`

## Output Format
```json
{
  "video": "beach_video.mp4",
  "duration_seconds": 30.5,
  "total_frames_analyzed": 30,
  "frames_per_second": 1,
  "frame_analyses": [...],
  "summary": {
    "is_crowded": false,
    "crowd_level": "low",
    "conclusion": "The beach is not crowded..."
  }
}
```

## Configuration
- **Frames per second**: Modify `frames_per_second` parameter (default: 1)
- **Model**: Uses `vikhyatk/moondream2` (revision: 2025-06-21)
- **Crowd thresholds**: 
  - High crowd: ≥70% frames crowded
  - Medium crowd: 40-70% frames crowded
  - Low crowd: <40% frames crowded
