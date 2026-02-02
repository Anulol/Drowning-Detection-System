# Drowning Detection Web App

A web application for detecting drowning incidents in images and videos using YOLOv8 AI model.

## Features

- Upload images or videos for drowning detection
- Real-time AI analysis using YOLOv8
- Visual results with bounding boxes
- Detection confidence scores
- Alert system for drowning incidents
- **Video analysis with sample frames** (processes every 120th frame, shows 10 representative frames)
- **Final prediction verdict** with confidence level for videos
- Summary reports for video analysis

## Installation

1. Clone or download the repository
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000/`

3. Upload an image or video and click "Analyze"

4. For images: View the detection results with highlighted areas
5. For videos: View sample frame analysis and **final prediction verdict** (DROWNING DETECTED / NO DROWNING DETECTED)

## Supported Formats

- **Images:** JPG, PNG
- **Videos:** MP4, AVI, MOV, MKV, WMV

## Requirements

- Python 3.8+
- YOLOv8 model file (model.pt)
- Web browser

## Model

The application uses a pre-trained YOLOv8 model for drowning detection. Make sure `model.pt` is in the same directory as `app.py`.

## File Structure

```
├── app.py                 # Flask application
├── model.pt              # YOLOv8 model
├── requirements.txt      # Python dependencies
├── templates/
│   ├── index.html        # Upload page
│   ├── result.html       # Image results page
│   └── video_result.html # Video results page
├── uploads/              # Uploaded files
├── results/              # Processed results
└── frames/               # Video frames
```