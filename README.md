# Automated Drowning Detection

This repository presents a comprehensive solution for automated drowning detection leveraging deep learning models and advanced methodologies. Our work focuses on revolutionizing drowning incident response systems by swiftly identifying distress situations in aquatic environments.

## Methodology Highlights

Our approach involved rigorous model refinement to achieve accurate drowning detection:
- **Initial Model Training:** We initially trained the YOLO v8 architecture on a [dataset](https://universe.roboflow.com/object-detection-model/drowning-detection-wqiom) but encountered suboptimal detection results.
- **Dataset Analysis:** Recognizing the limitations, we integrated a secondary dataset, [Team Burraq via Roboflow Universe](https://universe.roboflow.com/team-burraq/drowning-detection-main), to augment our model's understanding of varied drowning scenarios.
- **Fine-Tuning for Enhanced Precision:** To address the limitations observed in initial detection, we subjected the previously trained model to a further 20 epochs of fine-tuning on the new dataset. This refined training significantly improved detection accuracy and sensitivity, evident in the detection images included.

## Key Features
- **Dataset Collection and Cleaning:** Curated diverse datasets from reputable sources, ensuring comprehensive coverage of drowning scenarios.
- **Model Selection and Fine-Tuning:** Employed YOLO v8 architecture, fine-tuning it exclusively for drowning instances to enhance accuracy and sensitivity.
- **Integration and Refinement:** Integrated secondary datasets to further refine the model's understanding of varied drowning scenarios.
- **Code Implementation:** Utilized Ultralytics library for seamless model loading and image analysis, facilitating efficient drowning instance detection.
- **Coordinate Calculation Methodology:** Incorporated coordinate calculation to precisely determine spatial coordinates of detected objects, enhancing object localization.
- **Integration with Real-Life Pool Cameras and Depth Estimation Sensors:** Worked towards integrating the detection system with pool cameras and depth estimation sensors for real-time spatial analysis.
- **Conclusion and Future Recommendations:** Summarized findings, highlighting accuracy improvements and proposed future enhancements for real-time drowning detection systems.

## Dataset Used
- **First Dataset:** [Roboflow Universe](https://universe.roboflow.com/object-detection-model/drowning-detection-wqiom)
- **Second Dataset:** [Team Burraq via Roboflow Universe](https://universe.roboflow.com/team-burraq/drowning-detection-main)

## Sample Detection Images
![WhatsApp Image 2023-12-10 at 12 38 25 PM (1)](https://github.com/Hasibwajid/Automated-Drowning-Detection-YOLOV8/assets/72168225/1796c6c3-e36c-4866-8a0e-97053717981e)
![WhatsApp Image 2023-12-10 at 12 37 08 PM](https://github.com/Hasibwajid/Automated-Drowning-Detection-YOLOV8/assets/72168225/2c4c93ac-497e-497d-bbec-58fda3de8b8c)

### Additional Detection Results
Here are some sample detection results from our YOLOv8 model:

**Detection Result 1:**
![Detection Result 1](results/result_02173e7ac58a42baab209aba7f7c7846.jpg)

**Detection Result 2:**
![Detection Result 2](results/result_0392cb0c388648ce93a96d2e7f4e5395.jpg)

**Detection Result 3:**
![Detection Result 3](results/result_046cf6879c7b45c9a13afa3e8c96fafe.jpg)

**Detection Result 4:**
![Detection Result 4](results/result_048ad909e4b84c649ae07ceab4daa2ea.jpg)

## Web Application Screenshots

### Homepage Interface
![Web App Homepage](https://via.placeholder.com/800x600/4facfe/ffffff?text=Drowning+Detection+Web+App)
*Modern web interface with gradient background, drag-and-drop upload functionality, and intuitive navigation.*

### Detection Results Page
![Results Interface](https://via.placeholder.com/800x600/43e97b/ffffff?text=AI+Detection+Results)
*Results page showing original image, processed image with bounding boxes, confidence scores, and detailed analysis.*

### Video Analysis Interface
![Video Analysis](https://via.placeholder.com/800x600/f093fb/ffffff?text=Video+Drowning+Analysis)
*Video analysis interface displaying sample frames, final prediction verdict (DROWNING DETECTED/NOT DETECTED), and comprehensive report.*

## Usage
Detailed instructions and code implementation for automated drowning detection are provided in this repo.
