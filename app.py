from flask import Flask, request, render_template, send_from_directory
import os
import shutil
from ultralytics import YOLO
import cv2
import uuid

app = Flask(__name__)

# Load the model
model_path = 'model.pt'
model = YOLO(model_path)

# Create directories
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
FRAMES_FOLDER = 'frames'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)

def remove_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

def detect_drowning(imgpath, confidence=0.4):
    print(f"Processing: {imgpath}")

    # Remove previous prediction
    remove_directory('runs/detect/predict')

    if not os.path.exists(imgpath):
        return None, "Image file not found"

    # Check file size
    if os.path.getsize(imgpath) == 0:
        return None, "Image file is empty"

    # Load the image first to validate
    image = cv2.imread(imgpath)
    if image is None or image.size == 0:
        return None, "Could not load image"

    # Run YOLO detection
    try:
        results = model.predict(source=imgpath, conf=confidence, save=True, save_txt=True)
    except Exception as e:
        print(f"Error during model prediction: {e}")
        return None, f"Model prediction failed: {str(e)}"

    result = results[0]
    print(f"Detection complete. Boxes found: {len(result.boxes)}")

    detections = []
    drowning_detected = False

    # Draw bounding boxes on the image
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls = int(box.cls[0])

        print(f"Detected - Class: {cls}, Confidence: {conf:.2f}")

        if cls == 0:  # Drowning class
            drowning_detected = True
            color = (255, 0, 0)  # Blue
            label = f'Drowning: {conf:.2f}'
            detections.append({"class": "Drowning", "confidence": conf})
        else:
            color = (0, 255, 0)  # Green
            label = f'Not Drowning: {conf:.2f}'
            detections.append({"class": "Not Drowning", "confidence": conf})

        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # Save the result image
    result_filename = f"result_{uuid.uuid4().hex}.jpg"
    result_path = os.path.join(RESULTS_FOLDER, result_filename)
    cv2.imwrite(result_path, image)

    return result_filename, detections

def process_video(video_path, confidence=0.4, frame_interval=120):  # Process every 120th frame for fewer samples
    """Process video by analyzing frames at specified intervals"""
    print(f"Processing video: {video_path}")

    # Create a unique folder for this video's frames
    video_id = uuid.uuid4().hex
    video_frames_dir = os.path.join(FRAMES_FOLDER, video_id)
    os.makedirs(video_frames_dir, exist_ok=True)

    # Open video
    vidcap = cv2.VideoCapture(video_path)
    if not vidcap.isOpened():
        return None, "Could not open video file"

    success, image = vidcap.read()
    count = 0
    processed_frames = []
    max_frames = 50  # Limit processing to prevent long videos from taking too much time
    max_display_frames = 10  # Show 10 representative frames in results
    display_interval = max(1, (max_frames * frame_interval) // max_display_frames)  # Distribute display frames

    while success and count < max_frames * frame_interval:
        if count % frame_interval == 0:
            # Validate frame before processing
            if image is not None and image.size > 0 and image.shape[0] > 0 and image.shape[1] > 0:
                # Save frame
                frame_filename = f"frame_{count:06d}.jpg"
                frame_path = os.path.join(video_frames_dir, frame_filename)
                cv2.imwrite(frame_path, image)

                # Verify the frame was saved correctly
                if os.path.exists(frame_path) and os.path.getsize(frame_path) > 0:
                    # Process frame
                    result_filename, detections = detect_drowning(frame_path, confidence)
                    if result_filename:
                        frame_data = {
                            'frame_number': count,
                            'original_frame': frame_filename,
                            'result_frame': result_filename,
                            'detections': detections
                        }
                        processed_frames.append(frame_data)

                        # For display, only keep frames at regular intervals
                        if len(processed_frames) <= max_display_frames:
                            pass  # Keep all until we reach the limit
                        elif len(processed_frames) > max_display_frames:
                            # Replace with more evenly distributed frames
                            if count % display_interval == 0:
                                processed_frames[max_display_frames-1] = frame_data
                    else:
                        print(f"Warning: Failed to process frame {count}")
                else:
                    print(f"Warning: Failed to save frame {count}")
            else:
                print(f"Warning: Invalid or empty frame at {count}")

        success, image = vidcap.read()
        count += 1

    # Trim to max display frames
    if len(processed_frames) > max_display_frames:
        # Select evenly distributed frames
        step = max(1, len(processed_frames) // max_display_frames)
        processed_frames = processed_frames[::step][:max_display_frames]

    vidcap.release()

    # Calculate summary
    total_frames_analyzed = len(processed_frames)
    drowning_frames = sum(1 for frame in processed_frames if any(d['class'] == 'Drowning' for d in frame['detections']))

    # Final prediction based on drowning detection
    if total_frames_analyzed > 0:
        if drowning_frames > 0:
            final_prediction = "DROWNING DETECTED"
            confidence_level = min(95, (drowning_frames / total_frames_analyzed) * 100)  # Estimate confidence
        else:
            final_prediction = "NO DROWNING DETECTED"
            confidence_level = 90  # High confidence when no drowning detected
    else:
        final_prediction = "NO DROWNING DETECTED"
        confidence_level = 0  # No frames analyzed

    summary = {
        'total_frames_analyzed': total_frames_analyzed,
        'drowning_frames': drowning_frames,
        'video_id': video_id,
        'final_prediction': final_prediction,
        'confidence_level': confidence_level,
        'frame_limit_reached': count >= max_frames * frame_interval
    }

    return processed_frames, summary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error='No file uploaded')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file selected')

    if file:
        # Determine file type
        filename = file.filename.lower()
        is_video = filename.endswith(('.mp4', '.avi', '.mov', '.mkv', '.wmv'))

        # Save uploaded file
        file_extension = os.path.splitext(filename)[1]
        unique_filename = f"upload_{uuid.uuid4().hex}{file_extension}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)

        if is_video:
            # Process video
            try:
                processed_frames, summary = process_video(filepath)
                if processed_frames is None:
                    return render_template('index.html', error=summary)
            except Exception as e:
                print(f"Error processing video: {e}")
                return render_template('index.html', error=f"Video processing failed: {str(e)}")

            # Ensure summary has all required keys
            required_keys = ['total_frames_analyzed', 'drowning_frames', 'video_id', 'final_prediction', 'confidence_level', 'frame_limit_reached']
            for key in required_keys:
                if key not in summary:
                    summary[key] = 0 if key in ['total_frames_analyzed', 'drowning_frames', 'confidence_level'] else ('NO DROWNING DETECTED' if key == 'final_prediction' else False)

            return render_template('video_result.html',
                                 video_filename=unique_filename,
                                 processed_frames=processed_frames,
                                 summary=summary)
        else:
            # Process image
            try:
                result_image, detections = detect_drowning(filepath)
                if result_image is None:
                    return render_template('index.html', error=detections)
            except Exception as e:
                print(f"Error processing image: {e}")
                return render_template('index.html', error=f"Image processing failed: {str(e)}")

            return render_template('result.html',
                                 original_image=unique_filename,
                                 result_image=result_image,
                                 detections=detections)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(RESULTS_FOLDER, filename)

@app.route('/frames/<video_id>/<filename>')
def frame_file(video_id, filename):
    return send_from_directory(os.path.join(FRAMES_FOLDER, video_id), filename)

if __name__ == '__main__':
    app.run(debug=True)