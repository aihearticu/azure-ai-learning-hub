# 🧪 Complete Hands-On Labs Guide for Azure AI Engineers

## Overview
This guide contains 50+ hands-on labs organized by service, with step-by-step instructions, code samples, and real-world scenarios.

---

## 📋 Lab Index

### Computer Vision Labs (10 Labs)
- [Lab CV-01: Image Analysis Pipeline](#lab-cv-01-image-analysis-pipeline)
- [Lab CV-02: Custom Object Detection](#lab-cv-02-custom-object-detection)
- [Lab CV-03: Face Recognition System](#lab-cv-03-face-recognition-system)
- [Lab CV-04: OCR Document Processor](#lab-cv-04-ocr-document-processor)
- [Lab CV-05: Brand Detection](#lab-cv-05-brand-detection)
- [Lab CV-06: Video Content Analysis](#lab-cv-06-video-content-analysis)
- [Lab CV-07: Spatial Analysis](#lab-cv-07-spatial-analysis)
- [Lab CV-08: Image Moderation](#lab-cv-08-image-moderation)
- [Lab CV-09: Product Visual Search](#lab-cv-09-product-visual-search)
- [Lab CV-10: Medical Image Analysis](#lab-cv-10-medical-image-analysis)

### Natural Language Labs (10 Labs)
- [Lab NLP-01: Sentiment Analysis Dashboard](#lab-nlp-01-sentiment-analysis-dashboard)
- [Lab NLP-02: Custom Entity Extractor](#lab-nlp-02-custom-entity-extractor)
- [Lab NLP-03: Multi-language Translator](#lab-nlp-03-multi-language-translator)
- [Lab NLP-04: Speech Transcription Service](#lab-nlp-04-speech-transcription-service)
- [Lab NLP-05: Conversational Language Model](#lab-nlp-05-conversational-language-model)
- [Lab NLP-06: Text Summarization](#lab-nlp-06-text-summarization)
- [Lab NLP-07: PII Detection & Redaction](#lab-nlp-07-pii-detection-redaction)
- [Lab NLP-08: Voice Assistant](#lab-nlp-08-voice-assistant)
- [Lab NLP-09: Meeting Transcriber](#lab-nlp-09-meeting-transcriber)
- [Lab NLP-10: Language Detection API](#lab-nlp-10-language-detection-api)

### Document Intelligence Labs (5 Labs)
- [Lab DOC-01: Invoice Processing](#lab-doc-01-invoice-processing)
- [Lab DOC-02: Receipt Analyzer](#lab-doc-02-receipt-analyzer)
- [Lab DOC-03: Custom Form Extractor](#lab-doc-03-custom-form-extractor)
- [Lab DOC-04: ID Document Verification](#lab-doc-04-id-document-verification)
- [Lab DOC-05: Contract Analysis](#lab-doc-05-contract-analysis)

### Knowledge Mining Labs (5 Labs)
- [Lab KM-01: Enterprise Search](#lab-km-01-enterprise-search)
- [Lab KM-02: Custom Skills Pipeline](#lab-km-02-custom-skills-pipeline)
- [Lab KM-03: Vector Search Implementation](#lab-km-03-vector-search-implementation)
- [Lab KM-04: Knowledge Graph Builder](#lab-km-04-knowledge-graph-builder)
- [Lab KM-05: FAQ Chatbot](#lab-km-05-faq-chatbot)

### OpenAI & Generative AI Labs (10 Labs)
- [Lab GEN-01: Prompt Engineering Workshop](#lab-gen-01-prompt-engineering-workshop)
- [Lab GEN-02: RAG Implementation](#lab-gen-02-rag-implementation)
- [Lab GEN-03: Function Calling](#lab-gen-03-function-calling)
- [Lab GEN-04: Fine-tuning GPT](#lab-gen-04-fine-tuning-gpt)
- [Lab GEN-05: Image Generation with DALL-E](#lab-gen-05-image-generation-dalle)
- [Lab GEN-06: Code Generation Assistant](#lab-gen-06-code-generation-assistant)
- [Lab GEN-07: Content Generation Pipeline](#lab-gen-07-content-generation-pipeline)
- [Lab GEN-08: Semantic Kernel Agent](#lab-gen-08-semantic-kernel-agent)
- [Lab GEN-09: Multi-modal AI App](#lab-gen-09-multi-modal-ai-app)
- [Lab GEN-10: AI Safety Implementation](#lab-gen-10-ai-safety-implementation)

### Integration Labs (5 Labs)
- [Lab INT-01: Power Platform Integration](#lab-int-01-power-platform-integration)
- [Lab INT-02: Logic Apps Workflow](#lab-int-02-logic-apps-workflow)
- [Lab INT-03: Event-Driven Architecture](#lab-int-03-event-driven-architecture)
- [Lab INT-04: API Management](#lab-int-04-api-management)
- [Lab INT-05: Hybrid Cloud AI](#lab-int-05-hybrid-cloud-ai)

### Production & MLOps Labs (5 Labs)
- [Lab MLO-01: CI/CD Pipeline](#lab-mlo-01-cicd-pipeline)
- [Lab MLO-02: Model Monitoring](#lab-mlo-02-model-monitoring)
- [Lab MLO-03: A/B Testing](#lab-mlo-03-ab-testing)
- [Lab MLO-04: Auto-scaling](#lab-mlo-04-auto-scaling)
- [Lab MLO-05: Disaster Recovery](#lab-mlo-05-disaster-recovery)

---

## Computer Vision Labs

### Lab CV-01: Image Analysis Pipeline
**Duration**: 2 hours  
**Difficulty**: ⭐⭐  
**Services**: Azure Computer Vision

#### Objectives
- Set up Computer Vision resource
- Analyze images for multiple features
- Build automated processing pipeline
- Implement batch processing

#### Prerequisites
```bash
# Create resources
az group create --name rg-cv-lab --location eastus
az cognitiveservices account create \
  --name cv-lab-$RANDOM \
  --resource-group rg-cv-lab \
  --kind ComputerVision \
  --sku F0 \
  --location eastus
```

#### Step 1: Environment Setup
```python
# requirements.txt
azure-ai-vision-imageanalysis==1.0.0
azure-storage-blob==12.19.0
python-dotenv==1.0.0
Pillow==10.0.0
matplotlib==3.7.0
```

#### Step 2: Image Analysis Client
```python
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

load_dotenv()

class ImageAnalyzer:
    def __init__(self):
        self.client = ImageAnalysisClient(
            endpoint=os.getenv("VISION_ENDPOINT"),
            credential=AzureKeyCredential(os.getenv("VISION_KEY"))
        )
    
    def analyze_image(self, image_path):
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        result = self.client.analyze(
            image_data=image_data,
            visual_features=[
                VisualFeatures.CAPTION,
                VisualFeatures.DENSE_CAPTIONS,
                VisualFeatures.TAGS,
                VisualFeatures.OBJECTS,
                VisualFeatures.PEOPLE,
                VisualFeatures.SMART_CROPS,
                VisualFeatures.READ
            ],
            smart_crops_aspect_ratios=[0.9, 1.33],
            gender_neutral_caption=True,
            language="en"
        )
        
        return self._format_results(result)
    
    def _format_results(self, result):
        analysis = {
            "caption": None,
            "tags": [],
            "objects": [],
            "people_count": 0,
            "text": []
        }
        
        if result.caption:
            analysis["caption"] = {
                "text": result.caption.text,
                "confidence": result.caption.confidence
            }
        
        if result.tags:
            analysis["tags"] = [
                {"name": tag.name, "confidence": tag.confidence}
                for tag in result.tags.list
            ]
        
        if result.objects:
            analysis["objects"] = [
                {
                    "name": obj.tags[0].name,
                    "confidence": obj.tags[0].confidence,
                    "bbox": {
                        "x": obj.bounding_box.x,
                        "y": obj.bounding_box.y,
                        "w": obj.bounding_box.width,
                        "h": obj.bounding_box.height
                    }
                }
                for obj in result.objects.list
            ]
        
        if result.people:
            analysis["people_count"] = len(result.people.list)
        
        if result.read:
            for block in result.read.blocks:
                for line in block.lines:
                    analysis["text"].append(line.text)
        
        return analysis
```

#### Step 3: Batch Processing Pipeline
```python
from azure.storage.blob import BlobServiceClient
import json
from concurrent.futures import ThreadPoolExecutor
import logging

class BatchImageProcessor:
    def __init__(self, storage_connection_string):
        self.analyzer = ImageAnalyzer()
        self.blob_client = BlobServiceClient.from_connection_string(
            storage_connection_string
        )
        self.logger = logging.getLogger(__name__)
    
    def process_container(self, container_name, output_container):
        container = self.blob_client.get_container_client(container_name)
        output = self.blob_client.get_container_client(output_container)
        
        # List all blobs
        blobs = container.list_blobs()
        
        # Process in parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for blob in blobs:
                if blob.name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    future = executor.submit(
                        self._process_blob, 
                        container_name, 
                        blob.name, 
                        output_container
                    )
                    futures.append(future)
            
            # Wait for completion
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"Processing failed: {e}")
    
    def _process_blob(self, container_name, blob_name, output_container):
        # Download image
        blob = self.blob_client.get_blob_client(
            container=container_name,
            blob=blob_name
        )
        image_data = blob.download_blob().readall()
        
        # Save temporarily
        temp_path = f"/tmp/{blob_name}"
        with open(temp_path, "wb") as f:
            f.write(image_data)
        
        # Analyze
        try:
            results = self.analyzer.analyze_image(temp_path)
            
            # Save results
            output_blob = self.blob_client.get_blob_client(
                container=output_container,
                blob=f"{blob_name}.json"
            )
            output_blob.upload_blob(
                json.dumps(results, indent=2),
                overwrite=True
            )
            
            self.logger.info(f"Processed {blob_name}")
        finally:
            # Cleanup
            os.remove(temp_path)

# Usage
processor = BatchImageProcessor(storage_connection_string)
processor.process_container("input-images", "analysis-results")
```

#### Step 4: Visualization Dashboard
```python
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class VisionResultVisualizer:
    def __init__(self):
        self.colors = plt.cm.Set3(np.linspace(0, 1, 12))
    
    def visualize_analysis(self, image_path, analysis_results):
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Original image with objects
        img = Image.open(image_path)
        self._draw_objects(axes[0, 0], img, analysis_results['objects'])
        axes[0, 0].set_title('Detected Objects')
        
        # Caption and tags
        self._show_text_info(axes[0, 1], analysis_results)
        
        # Tag cloud
        self._create_tag_cloud(axes[1, 0], analysis_results['tags'])
        
        # Statistics
        self._show_statistics(axes[1, 1], analysis_results)
        
        plt.tight_layout()
        return fig
    
    def _draw_objects(self, ax, img, objects):
        draw = ImageDraw.Draw(img)
        
        for i, obj in enumerate(objects):
            color = tuple(int(c * 255) for c in self.colors[i % 12][:3])
            bbox = obj['bbox']
            
            # Draw bounding box
            draw.rectangle(
                [(bbox['x'], bbox['y']), 
                 (bbox['x'] + bbox['w'], bbox['y'] + bbox['h'])],
                outline=color,
                width=3
            )
            
            # Add label
            draw.text(
                (bbox['x'], bbox['y'] - 20),
                f"{obj['name']} ({obj['confidence']:.2f})",
                fill=color
            )
        
        ax.imshow(img)
        ax.axis('off')
    
    def _show_text_info(self, ax, results):
        ax.axis('off')
        text = f"Caption: {results['caption']['text']}\n"
        text += f"Confidence: {results['caption']['confidence']:.2f}\n\n"
        text += f"People Count: {results['people_count']}\n\n"
        
        if results['text']:
            text += "Detected Text:\n"
            text += "\n".join(results['text'][:5])
        
        ax.text(0.1, 0.9, text, transform=ax.transAxes,
                fontsize=12, verticalalignment='top')
    
    def _create_tag_cloud(self, ax, tags):
        # Simple tag visualization
        tags_sorted = sorted(tags, key=lambda x: x['confidence'], reverse=True)
        y_pos = np.arange(len(tags_sorted[:10]))
        confidences = [tag['confidence'] for tag in tags_sorted[:10]]
        names = [tag['name'] for tag in tags_sorted[:10]]
        
        ax.barh(y_pos, confidences)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(names)
        ax.set_xlabel('Confidence')
        ax.set_title('Top 10 Tags')
    
    def _show_statistics(self, ax, results):
        stats = {
            'Total Objects': len(results['objects']),
            'Total Tags': len(results['tags']),
            'People Detected': results['people_count'],
            'Text Blocks': len(results['text']),
            'Avg Tag Confidence': np.mean([t['confidence'] for t in results['tags']])
        }
        
        ax.axis('off')
        text = "Analysis Statistics:\n\n"
        for key, value in stats.items():
            if isinstance(value, float):
                text += f"{key}: {value:.2f}\n"
            else:
                text += f"{key}: {value}\n"
        
        ax.text(0.1, 0.9, text, transform=ax.transAxes,
                fontsize=14, verticalalignment='top')
```

#### Challenge Extensions
1. Add real-time streaming analysis from webcam
2. Implement custom vision model integration
3. Add anomaly detection for unusual objects
4. Create mobile app with image upload
5. Build API endpoint for analysis service

---

### Lab CV-02: Custom Object Detection
**Duration**: 3 hours  
**Difficulty**: ⭐⭐⭐  
**Services**: Azure Custom Vision

#### Objectives
- Train custom object detection model
- Prepare and label training data
- Evaluate model performance
- Deploy to edge devices

#### Step 1: Data Preparation
```python
import json
import uuid
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateBatch,
    ImageFileCreateEntry,
    Region
)

class CustomVisionTrainer:
    def __init__(self, training_key, endpoint):
        self.trainer = CustomVisionTrainingClient(
            training_key, 
            endpoint=endpoint
        )
        self.project = None
        self.tags = {}
    
    def create_project(self, name, domain="General"):
        # Get domain ID
        domains = self.trainer.get_domains()
        domain_id = next(d.id for d in domains if d.name == domain)
        
        # Create project
        self.project = self.trainer.create_project(
            name,
            domain_id=domain_id,
            classification_type="Multiclass",
            target_export_platforms=["CoreML", "TensorFlow", "ONNX"]
        )
        
        return self.project.id
    
    def create_tags(self, tag_names):
        for name in tag_names:
            tag = self.trainer.create_tag(self.project.id, name)
            self.tags[name] = tag.id
    
    def upload_training_images(self, image_data):
        """
        image_data = [
            {
                'path': 'image1.jpg',
                'regions': [
                    {'tag': 'cat', 'x': 0.1, 'y': 0.2, 'w': 0.3, 'h': 0.4}
                ]
            }
        ]
        """
        batch_size = 64
        for i in range(0, len(image_data), batch_size):
            batch = image_data[i:i + batch_size]
            
            images = []
            for item in batch:
                with open(item['path'], 'rb') as f:
                    regions = [
                        Region(
                            tag_id=self.tags[r['tag']],
                            left=r['x'],
                            top=r['y'],
                            width=r['w'],
                            height=r['h']
                        )
                        for r in item['regions']
                    ]
                    
                    images.append(
                        ImageFileCreateEntry(
                            name=item['path'],
                            contents=f.read(),
                            regions=regions
                        )
                    )
            
            batch_create = ImageFileCreateBatch(images=images)
            self.trainer.create_images_from_files(
                self.project.id,
                batch_create
            )
    
    def train_model(self, training_type="Quick"):
        iteration = self.trainer.train_project(
            self.project.id,
            training_type=training_type
        )
        
        # Wait for training to complete
        while iteration.status != "Completed":
            iteration = self.trainer.get_iteration(
                self.project.id, 
                iteration.id
            )
            time.sleep(5)
        
        return iteration
    
    def evaluate_model(self, iteration_id):
        performance = self.trainer.get_iteration_performance(
            self.project.id,
            iteration_id
        )
        
        metrics = {
            'precision': performance.precision,
            'recall': performance.recall,
            'mAP': performance.average_precision,
            'per_tag_performance': {}
        }
        
        for tag_perf in performance.per_tag_performance:
            metrics['per_tag_performance'][tag_perf.name] = {
                'precision': tag_perf.precision,
                'recall': tag_perf.recall,
                'ap': tag_perf.average_precision
            }
        
        return metrics
```

#### Step 2: Model Deployment
```python
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import cv2
import numpy as np

class ObjectDetector:
    def __init__(self, prediction_key, endpoint, project_id, iteration_name):
        self.predictor = CustomVisionPredictionClient(
            prediction_key,
            endpoint=endpoint
        )
        self.project_id = project_id
        self.iteration_name = iteration_name
    
    def detect_objects(self, image_path, threshold=0.5):
        with open(image_path, 'rb') as f:
            results = self.predictor.detect_image(
                self.project_id,
                self.iteration_name,
                f
            )
        
        detections = []
        for prediction in results.predictions:
            if prediction.probability > threshold:
                detections.append({
                    'tag': prediction.tag_name,
                    'probability': prediction.probability,
                    'bbox': {
                        'left': prediction.bounding_box.left,
                        'top': prediction.bounding_box.top,
                        'width': prediction.bounding_box.width,
                        'height': prediction.bounding_box.height
                    }
                })
        
        return detections
    
    def detect_objects_video(self, video_path, output_path):
        cap = cv2.VideoCapture(video_path)
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process every 5th frame for efficiency
            if frame_count % 5 == 0:
                # Save frame temporarily
                temp_path = f'/tmp/frame_{frame_count}.jpg'
                cv2.imwrite(temp_path, frame)
                
                # Detect objects
                detections = self.detect_objects(temp_path)
                
                # Draw bounding boxes
                for det in detections:
                    bbox = det['bbox']
                    x = int(bbox['left'] * width)
                    y = int(bbox['top'] * height)
                    w = int(bbox['width'] * width)
                    h = int(bbox['height'] * height)
                    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    label = f"{det['tag']}: {det['probability']:.2f}"
                    cv2.putText(frame, label, (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                os.remove(temp_path)
            
            out.write(frame)
            frame_count += 1
        
        cap.release()
        out.release()
```

#### Step 3: Edge Deployment
```python
# Export model for edge
def export_model(trainer, project_id, iteration_id, platform="ONNX"):
    # Request export
    export = trainer.export_iteration(
        project_id,
        iteration_id,
        platform
    )
    
    # Wait for export to complete
    while export.status == "Exporting":
        time.sleep(5)
        exports = trainer.get_exports(project_id, iteration_id)
        export = next(e for e in exports if e.platform == platform)
    
    # Download model
    if export.status == "Done":
        model_url = export.download_uri
        response = requests.get(model_url)
        
        with open(f"model.{platform.lower()}", "wb") as f:
            f.write(response.content)
        
        return f"model.{platform.lower()}"
    
    return None

# ONNX Runtime inference
import onnxruntime as ort

class ONNXObjectDetector:
    def __init__(self, model_path):
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [o.name for o in self.session.get_outputs()]
    
    def preprocess_image(self, image_path, target_size=(416, 416)):
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, target_size)
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        return img
    
    def detect(self, image_path):
        input_data = self.preprocess_image(image_path)
        outputs = self.session.run(
            self.output_names,
            {self.input_name: input_data}
        )
        
        # Parse outputs (format depends on model architecture)
        detections = self._parse_outputs(outputs)
        return detections
    
    def _parse_outputs(self, outputs):
        # Implementation depends on model architecture
        # This is a simplified example
        boxes = outputs[0]
        scores = outputs[1]
        classes = outputs[2]
        
        detections = []
        for i in range(len(scores)):
            if scores[i] > 0.5:
                detections.append({
                    'class': classes[i],
                    'score': scores[i],
                    'bbox': boxes[i]
                })
        
        return detections
```

---

### Lab CV-03: Face Recognition System
**Duration**: 2.5 hours  
**Difficulty**: ⭐⭐⭐  
**Services**: Azure Face API

#### Objectives
- Implement face detection and recognition
- Build face verification system
- Create emotion analysis
- Handle privacy and security

#### Implementation
```python
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import io
from PIL import Image
import numpy as np

class FaceRecognitionSystem:
    def __init__(self, key, endpoint):
        self.client = FaceClient(endpoint, CognitiveServicesCredentials(key))
        self.person_group_id = "employees"
    
    def create_person_group(self, name="Employee Group"):
        try:
            self.client.person_group.create(
                person_group_id=self.person_group_id,
                name=name,
                recognition_model="recognition_04"
            )
        except Exception as e:
            print(f"Person group may already exist: {e}")
    
    def add_person(self, name, image_paths):
        # Create person
        person = self.client.person_group_person.create(
            person_group_id=self.person_group_id,
            name=name
        )
        
        # Add faces
        for path in image_paths:
            with open(path, 'rb') as image:
                self.client.person_group_person.add_face_from_stream(
                    person_group_id=self.person_group_id,
                    person_id=person.person_id,
                    image=image,
                    detection_model="detection_03"
                )
        
        return person.person_id
    
    def train_model(self):
        self.client.person_group.train(self.person_group_id)
        
        # Wait for training to complete
        while True:
            training_status = self.client.person_group.get_training_status(
                self.person_group_id
            )
            if training_status.status == 'succeeded':
                break
            elif training_status.status == 'failed':
                raise Exception('Training failed')
            time.sleep(1)
    
    def identify_faces(self, image_path):
        with open(image_path, 'rb') as image:
            faces = self.client.face.detect_with_stream(
                image,
                detection_model="detection_03",
                recognition_model="recognition_04",
                return_face_attributes=['emotion', 'age', 'gender', 'glasses'],
                return_face_id=True
            )
        
        if not faces:
            return []
        
        # Identify faces
        face_ids = [face.face_id for face in faces]
        results = self.client.face.identify(
            face_ids,
            person_group_id=self.person_group_id,
            max_num_of_candidates_returned=1,
            confidence_threshold=0.5
        )
        
        identified_faces = []
        for face, result in zip(faces, results):
            face_info = {
                'face_id': face.face_id,
                'rectangle': {
                    'left': face.face_rectangle.left,
                    'top': face.face_rectangle.top,
                    'width': face.face_rectangle.width,
                    'height': face.face_rectangle.height
                },
                'attributes': {
                    'age': face.face_attributes.age,
                    'gender': face.face_attributes.gender,
                    'emotion': max(
                        face.face_attributes.emotion.as_dict().items(),
                        key=lambda x: x[1]
                    )[0],
                    'glasses': face.face_attributes.glasses
                }
            }
            
            if result.candidates:
                person = self.client.person_group_person.get(
                    person_group_id=self.person_group_id,
                    person_id=result.candidates[0].person_id
                )
                face_info['person_name'] = person.name
                face_info['confidence'] = result.candidates[0].confidence
            else:
                face_info['person_name'] = "Unknown"
                face_info['confidence'] = 0
            
            identified_faces.append(face_info)
        
        return identified_faces
    
    def verify_face(self, face_id1, face_id2):
        result = self.client.face.verify_face_to_face(face_id1, face_id2)
        return {
            'is_identical': result.is_identical,
            'confidence': result.confidence
        }
    
    def analyze_emotions(self, image_path):
        with open(image_path, 'rb') as image:
            faces = self.client.face.detect_with_stream(
                image,
                return_face_attributes=['emotion'],
                detection_model="detection_03"
            )
        
        emotions = []
        for face in faces:
            emotion_scores = face.face_attributes.emotion.as_dict()
            emotions.append({
                'face_location': {
                    'left': face.face_rectangle.left,
                    'top': face.face_rectangle.top,
                    'width': face.face_rectangle.width,
                    'height': face.face_rectangle.height
                },
                'emotions': emotion_scores,
                'dominant_emotion': max(emotion_scores.items(), key=lambda x: x[1])
            })
        
        return emotions

# Privacy-compliant face blurring
class PrivacyProtector:
    def __init__(self, face_client):
        self.face_client = face_client
    
    def blur_faces(self, image_path, output_path, blur_strength=15):
        # Detect faces
        with open(image_path, 'rb') as f:
            faces = self.face_client.face.detect_with_stream(
                f,
                detection_model="detection_03"
            )
        
        # Load image
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Blur each face
        for face in faces:
            rect = face.face_rectangle
            x, y = rect.left, rect.top
            w, h = rect.width, rect.height
            
            # Extract face region
            face_region = img_array[y:y+h, x:x+w]
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(face_region, (blur_strength, blur_strength), 0)
            
            # Replace original region
            img_array[y:y+h, x:x+w] = blurred
        
        # Save result
        result_img = Image.fromarray(img_array)
        result_img.save(output_path)
        
        return len(faces)
```

---

### Lab NLP-01: Sentiment Analysis Dashboard
**Duration**: 2 hours  
**Difficulty**: ⭐⭐  
**Services**: Azure Language Service

#### Objectives
- Analyze sentiment from multiple sources
- Build real-time dashboard
- Implement aspect-based sentiment
- Create alerting system

#### Implementation
```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
import asyncio

class SentimentAnalyzer:
    def __init__(self, key, endpoint):
        self.client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )
    
    def analyze_sentiment(self, texts, language="en"):
        results = self.client.analyze_sentiment(
            documents=texts,
            language=language,
            show_opinion_mining=True
        )
        
        analyzed = []
        for doc in results:
            if not doc.is_error:
                sentiment_data = {
                    'id': doc.id,
                    'sentiment': doc.sentiment,
                    'confidence': {
                        'positive': doc.confidence_scores.positive,
                        'neutral': doc.confidence_scores.neutral,
                        'negative': doc.confidence_scores.negative
                    },
                    'sentences': []
                }
                
                # Extract sentence-level sentiment
                for sentence in doc.sentences:
                    sent_info = {
                        'text': sentence.text,
                        'sentiment': sentence.sentiment,
                        'confidence': {
                            'positive': sentence.confidence_scores.positive,
                            'neutral': sentence.confidence_scores.neutral,
                            'negative': sentence.confidence_scores.negative
                        },
                        'opinions': []
                    }
                    
                    # Extract opinions (aspect-based sentiment)
                    for opinion in sentence.mined_opinions:
                        sent_info['opinions'].append({
                            'target': opinion.target.text,
                            'sentiment': opinion.target.sentiment,
                            'assessments': [
                                {
                                    'text': assessment.text,
                                    'sentiment': assessment.sentiment
                                }
                                for assessment in opinion.assessments
                            ]
                        })
                    
                    sentiment_data['sentences'].append(sent_info)
                
                analyzed.append(sentiment_data)
        
        return analyzed
    
    def analyze_streaming(self, text_stream):
        """Analyze sentiment from streaming data"""
        buffer = []
        results = []
        
        for text in text_stream:
            buffer.append(text)
            
            # Process in batches of 10
            if len(buffer) >= 10:
                batch_results = self.analyze_sentiment(buffer)
                results.extend(batch_results)
                buffer = []
        
        # Process remaining
        if buffer:
            batch_results = self.analyze_sentiment(buffer)
            results.extend(batch_results)
        
        return results

class SentimentDashboard:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.data = []
    
    def create_dashboard(self):
        st.title("🎭 Real-Time Sentiment Analysis Dashboard")
        
        # Sidebar configuration
        st.sidebar.header("Configuration")
        data_source = st.sidebar.selectbox(
            "Data Source",
            ["Manual Input", "CSV Upload", "API Stream", "Social Media"]
        )
        
        # Main dashboard layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Analyzed", len(self.data))
        with col2:
            positive_pct = self._calculate_sentiment_percentage("positive")
            st.metric("Positive %", f"{positive_pct:.1f}%")
        with col3:
            negative_pct = self._calculate_sentiment_percentage("negative")
            st.metric("Negative %", f"{negative_pct:.1f}%")
        
        # Input section
        if data_source == "Manual Input":
            text_input = st.text_area("Enter text to analyze")
            if st.button("Analyze"):
                if text_input:
                    result = self.analyzer.analyze_sentiment([{"id": "1", "text": text_input}])
                    self.data.append(result[0])
                    st.success("Analysis complete!")
        
        # Visualization section
        if self.data:
            # Sentiment over time
            fig_timeline = self._create_timeline_chart()
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Sentiment distribution
            fig_dist = self._create_distribution_chart()
            st.plotly_chart(fig_dist, use_container_width=True)
            
            # Aspect-based sentiment
            fig_aspects = self._create_aspect_chart()
            st.plotly_chart(fig_aspects, use_container_width=True)
            
            # Recent analyses table
            st.subheader("Recent Analyses")
            df = self._create_dataframe()
            st.dataframe(df)
    
    def _calculate_sentiment_percentage(self, sentiment):
        if not self.data:
            return 0
        count = sum(1 for d in self.data if d['sentiment'] == sentiment)
        return (count / len(self.data)) * 100
    
    def _create_timeline_chart(self):
        # Simulate timestamps for demo
        timestamps = pd.date_range(
            start=datetime.now() - timedelta(hours=len(self.data)),
            periods=len(self.data),
            freq='H'
        )
        
        sentiments = [d['sentiment'] for d in self.data]
        
        fig = go.Figure()
        
        for sentiment in ['positive', 'neutral', 'negative']:
            y_values = [1 if s == sentiment else 0 for s in sentiments]
            fig.add_trace(go.Scatter(
                x=timestamps,
                y=y_values,
                mode='lines',
                name=sentiment.capitalize(),
                stackgroup='one'
            ))
        
        fig.update_layout(
            title="Sentiment Over Time",
            xaxis_title="Time",
            yaxis_title="Sentiment Distribution",
            hovermode='x unified'
        )
        
        return fig
    
    def _create_distribution_chart(self):
        sentiment_counts = pd.Series([d['sentiment'] for d in self.data]).value_counts()
        
        fig = go.Figure(data=[
            go.Bar(
                x=sentiment_counts.index,
                y=sentiment_counts.values,
                marker_color=['green', 'gray', 'red']
            )
        ])
        
        fig.update_layout(
            title="Sentiment Distribution",
            xaxis_title="Sentiment",
            yaxis_title="Count"
        )
        
        return fig
    
    def _create_aspect_chart(self):
        aspects = {}
        for item in self.data:
            for sentence in item.get('sentences', []):
                for opinion in sentence.get('opinions', []):
                    target = opinion['target']
                    sentiment = opinion['sentiment']
                    if target not in aspects:
                        aspects[target] = {'positive': 0, 'neutral': 0, 'negative': 0}
                    aspects[target][sentiment] += 1
        
        if not aspects:
            return go.Figure()
        
        fig = go.Figure()
        
        for sentiment in ['positive', 'neutral', 'negative']:
            fig.add_trace(go.Bar(
                name=sentiment.capitalize(),
                x=list(aspects.keys()),
                y=[aspects[a][sentiment] for a in aspects.keys()]
            ))
        
        fig.update_layout(
            title="Aspect-Based Sentiment",
            xaxis_title="Aspect",
            yaxis_title="Count",
            barmode='group'
        )
        
        return fig
    
    def _create_dataframe(self):
        data = []
        for item in self.data[-10:]:  # Last 10 items
            data.append({
                'ID': item['id'],
                'Sentiment': item['sentiment'],
                'Positive': f"{item['confidence']['positive']:.2f}",
                'Neutral': f"{item['confidence']['neutral']:.2f}",
                'Negative': f"{item['confidence']['negative']:.2f}"
            })
        
        return pd.DataFrame(data)

# Alert system
class SentimentAlertSystem:
    def __init__(self, analyzer, threshold=0.8):
        self.analyzer = analyzer
        self.threshold = threshold
        self.alerts = []
    
    def monitor_sentiment(self, text_stream):
        for text in text_stream:
            result = self.analyzer.analyze_sentiment([{"id": str(uuid.uuid4()), "text": text}])
            
            if result:
                sentiment_data = result[0]
                
                # Check for strong negative sentiment
                if (sentiment_data['sentiment'] == 'negative' and 
                    sentiment_data['confidence']['negative'] > self.threshold):
                    
                    alert = {
                        'timestamp': datetime.now(),
                        'text': text,
                        'sentiment': sentiment_data['sentiment'],
                        'confidence': sentiment_data['confidence']['negative'],
                        'alert_type': 'HIGH_NEGATIVE_SENTIMENT'
                    }
                    
                    self.alerts.append(alert)
                    self._send_alert(alert)
    
    def _send_alert(self, alert):
        # Implement notification logic (email, SMS, webhook, etc.)
        print(f"ALERT: {alert['alert_type']} - Confidence: {alert['confidence']:.2f}")
        
        # Example: Send to webhook
        # requests.post(webhook_url, json=alert)

# Run dashboard
if __name__ == "__main__":
    analyzer = SentimentAnalyzer(key="YOUR_KEY", endpoint="YOUR_ENDPOINT")
    dashboard = SentimentDashboard(analyzer)
    dashboard.create_dashboard()
```

---

### Lab GEN-02: RAG Implementation
**Duration**: 3 hours  
**Difficulty**: ⭐⭐⭐⭐  
**Services**: Azure OpenAI, Cognitive Search

#### Objectives
- Build end-to-end RAG system
- Implement document chunking
- Create vector embeddings
- Optimize retrieval accuracy

#### Complete Implementation
```python
import openai
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    SemanticSearch,
    SearchField,
    VectorSearchAlgorithmKind,
    HnswParameters
)
from azure.core.credentials import AzureKeyCredential
import tiktoken
import numpy as np
from typing import List, Dict
import hashlib

class RAGSystem:
    def __init__(self, search_endpoint, search_key, openai_endpoint, openai_key):
        # Initialize clients
        self.search_credential = AzureKeyCredential(search_key)
        self.index_client = SearchIndexClient(
            endpoint=search_endpoint,
            credential=self.search_credential
        )
        
        openai.api_type = "azure"
        openai.api_base = openai_endpoint
        openai.api_key = openai_key
        openai.api_version = "2024-02-01"
        
        self.embedding_model = "text-embedding-ada-002"
        self.chat_model = "gpt-4"
        self.index_name = "rag-index"
        
        # Initialize tokenizer
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")
    
    def create_search_index(self):
        """Create Azure Cognitive Search index with vector search"""
        
        # Define vector search configuration
        vector_search = VectorSearch(
            profiles=[
                VectorSearchProfile(
                    name="vector-profile",
                    algorithm_configuration_name="hnsw-config"
                )
            ],
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="hnsw-config",
                    kind=VectorSearchAlgorithmKind.HNSW,
                    parameters=HnswParameters(
                        m=4,
                        ef_construction=400,
                        ef_search=500,
                        metric="cosine"
                    )
                )
            ]
        )
        
        # Define semantic search configuration
        semantic_search = SemanticSearch(
            configurations=[
                SemanticConfiguration(
                    name="semantic-config",
                    prioritized_fields=SemanticPrioritizedFields(
                        title_field=SemanticField(field_name="title"),
                        content_fields=[SemanticField(field_name="content")],
                        keywords_fields=[SemanticField(field_name="keywords")]
                    )
                )
            ]
        )
        
        # Define index fields
        fields = [
            SimpleField(name="id", type="Edm.String", key=True),
            SearchableField(name="title", type="Edm.String", 
                          searchable=True, retrievable=True),
            SearchableField(name="content", type="Edm.String", 
                          searchable=True, retrievable=True),
            SearchableField(name="keywords", type="Edm.String", 
                          searchable=True, retrievable=True),
            SimpleField(name="source", type="Edm.String", 
                       filterable=True, retrievable=True),
            SimpleField(name="page", type="Edm.Int32", 
                       filterable=True, retrievable=True),
            SearchField(
                name="content_vector",
                type="Collection(Edm.Single)",
                searchable=True,
                retrievable=True,
                vector_search_dimensions=1536,
                vector_search_profile_name="vector-profile"
            ),
            SimpleField(name="chunk_id", type="Edm.String", retrievable=True),
            SimpleField(name="metadata", type="Edm.String", retrievable=True)
        ]
        
        # Create index
        index = SearchIndex(
            name=self.index_name,
            fields=fields,
            vector_search=vector_search,
            semantic_search=semantic_search
        )
        
        self.index_client.create_or_update_index(index)
        
        # Create search client
        self.search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=self.index_name,
            credential=self.search_credential
        )
    
    def chunk_document(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Chunk document with token-aware splitting"""
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), chunk_size - overlap):
            chunk_tokens = tokens[i:i + chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
        
        return chunks
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings using Azure OpenAI"""
        response = openai.Embedding.create(
            input=text,
            engine=self.embedding_model
        )
        return response['data'][0]['embedding']
    
    def index_documents(self, documents: List[Dict]):
        """
        Index documents with embeddings
        documents = [
            {
                'title': 'Document Title',
                'content': 'Full document content',
                'source': 'source_file.pdf',
                'metadata': {...}
            }
        ]
        """
        indexed_chunks = []
        
        for doc in documents:
            # Chunk the document
            chunks = self.chunk_document(doc['content'])
            
            for i, chunk in enumerate(chunks):
                # Generate unique ID
                chunk_id = hashlib.md5(
                    f"{doc['source']}_{i}_{chunk[:50]}".encode()
                ).hexdigest()
                
                # Generate embedding
                embedding = self.generate_embedding(chunk)
                
                # Create document for indexing
                index_doc = {
                    'id': chunk_id,
                    'title': doc['title'],
                    'content': chunk,
                    'keywords': self._extract_keywords(chunk),
                    'source': doc['source'],
                    'page': i,
                    'content_vector': embedding,
                    'chunk_id': f"{doc['source']}_chunk_{i}",
                    'metadata': str(doc.get('metadata', {}))
                }
                
                indexed_chunks.append(index_doc)
        
        # Upload to search index
        self.search_client.upload_documents(documents=indexed_chunks)
        
        return len(indexed_chunks)
    
    def _extract_keywords(self, text: str, max_keywords: int = 10) -> str:
        """Extract keywords using Azure Language Service or simple heuristics"""
        # For simplicity, using word frequency
        # In production, use Azure Language Service key phrase extraction
        words = text.lower().split()
        word_freq = {}
        
        stop_words = {'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'as', 'are', 'was', 'were', 'to', 'of', 'for', 'with', 'in'}
        
        for word in words:
            if word not in stop_words and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top keywords
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:max_keywords]
        return ' '.join([k[0] for k in keywords])
    
    def hybrid_search(self, query: str, top_k: int = 5, use_semantic: bool = True) -> List[Dict]:
        """Perform hybrid search (keyword + vector + semantic)"""
        
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        
        # Perform search
        results = self.search_client.search(
            search_text=query,
            vector_queries=[
                {
                    "vector": query_embedding,
                    "k_nearest_neighbors": top_k,
                    "fields": "content_vector"
                }
            ],
            select=["id", "title", "content", "source", "page"],
            query_type="semantic" if use_semantic else "simple",
            semantic_configuration_name="semantic-config" if use_semantic else None,
            top=top_k
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                'id': result['id'],
                'title': result['title'],
                'content': result['content'],
                'source': result['source'],
                'page': result['page'],
                'score': result['@search.score'],
                'reranker_score': result.get('@search.reranker_score', 0)
            })
        
        return formatted_results
    
    def generate_answer(self, query: str, context_docs: List[Dict], 
                       system_prompt: str = None) -> Dict:
        """Generate answer using retrieved context"""
        
        # Prepare context
        context = "\n\n".join([
            f"Source: {doc['source']} (Page {doc['page']})\n{doc['content']}"
            for doc in context_docs
        ])
        
        # Default system prompt
        if not system_prompt:
            system_prompt = """You are a helpful AI assistant that answers questions based on the provided context.
            Always cite your sources when providing information.
            If the context doesn't contain relevant information, say so."""
        
        # Prepare messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""Context:\n{context}\n\nQuestion: {query}
            
            Please provide a comprehensive answer based on the context above. 
            Include citations to the sources."""}
        ]
        
        # Generate response
        response = openai.ChatCompletion.create(
            engine=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        
        # Extract citations
        citations = []
        for doc in context_docs:
            if doc['content'][:50] in answer or doc['source'] in answer:
                citations.append({
                    'source': doc['source'],
                    'page': doc['page']
                })
        
        return {
            'answer': answer,
            'citations': citations,
            'context_used': len(context_docs),
            'tokens_used': response.usage.total_tokens
        }
    
    def rag_pipeline(self, query: str, top_k: int = 5) -> Dict:
        """Complete RAG pipeline"""
        
        # 1. Retrieve relevant documents
        search_results = self.hybrid_search(query, top_k=top_k)
        
        # 2. Generate answer
        if search_results:
            answer_data = self.generate_answer(query, search_results)
            
            return {
                'query': query,
                'answer': answer_data['answer'],
                'sources': search_results,
                'citations': answer_data['citations'],
                'tokens_used': answer_data['tokens_used']
            }
        else:
            return {
                'query': query,
                'answer': "I couldn't find relevant information to answer your question.",
                'sources': [],
                'citations': [],
                'tokens_used': 0
            }

# Advanced RAG with reranking and filtering
class AdvancedRAG(RAGSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reranker_model = "gpt-4"  # Can use specialized reranking model
    
    def rerank_results(self, query: str, results: List[Dict], top_k: int = 3) -> List[Dict]:
        """Rerank search results using LLM"""
        
        # Prepare reranking prompt
        rerank_prompt = f"""Given the query: '{query}'
        
        Rank the following passages by relevance (1 = most relevant):
        
        """
        
        for i, result in enumerate(results):
            rerank_prompt += f"\nPassage {i+1}:\n{result['content'][:200]}...\n"
        
        rerank_prompt += "\nProvide rankings as a comma-separated list of passage numbers (e.g., '3,1,2'):"
        
        # Get rankings from LLM
        response = openai.ChatCompletion.create(
            engine=self.reranker_model,
            messages=[
                {"role": "system", "content": "You are a search result reranking assistant."},
                {"role": "user", "content": rerank_prompt}
            ],
            temperature=0,
            max_tokens=50
        )
        
        # Parse rankings
        try:
            rankings = [int(x.strip()) - 1 for x in response.choices[0].message.content.split(',')]
            reranked = [results[i] for i in rankings[:top_k]]
        except:
            # Fallback to original order
            reranked = results[:top_k]
        
        return reranked
    
    def filter_by_recency(self, results: List[Dict], days: int = 30) -> List[Dict]:
        """Filter results by recency"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        filtered = []
        for result in results:
            # Assume metadata contains timestamp
            try:
                metadata = eval(result.get('metadata', '{}'))
                if 'timestamp' in metadata:
                    doc_date = datetime.fromisoformat(metadata['timestamp'])
                    if doc_date >= cutoff_date:
                        filtered.append(result)
                else:
                    filtered.append(result)  # Include if no timestamp
            except:
                filtered.append(result)
        
        return filtered
    
    def advanced_rag_pipeline(self, query: str, top_k: int = 5, 
                             use_reranking: bool = True,
                             filter_days: int = None) -> Dict:
        """Enhanced RAG pipeline with reranking and filtering"""
        
        # 1. Initial retrieval
        search_results = self.hybrid_search(query, top_k=top_k * 2)  # Get more for reranking
        
        # 2. Filter by recency if specified
        if filter_days:
            search_results = self.filter_by_recency(search_results, filter_days)
        
        # 3. Rerank results
        if use_reranking and search_results:
            search_results = self.rerank_results(query, search_results, top_k=top_k)
        else:
            search_results = search_results[:top_k]
        
        # 4. Generate answer
        if search_results:
            answer_data = self.generate_answer(query, search_results)
            
            return {
                'query': query,
                'answer': answer_data['answer'],
                'sources': search_results,
                'citations': answer_data['citations'],
                'tokens_used': answer_data['tokens_used'],
                'reranking_applied': use_reranking,
                'filtering_applied': filter_days is not None
            }
        else:
            return {
                'query': query,
                'answer': "I couldn't find relevant information to answer your question.",
                'sources': [],
                'citations': [],
                'tokens_used': 0,
                'reranking_applied': False,
                'filtering_applied': filter_days is not None
            }

# Usage example
if __name__ == "__main__":
    # Initialize RAG system
    rag = AdvancedRAG(
        search_endpoint="https://your-search.search.windows.net",
        search_key="your-search-key",
        openai_endpoint="https://your-openai.openai.azure.com/",
        openai_key="your-openai-key"
    )
    
    # Create index
    rag.create_search_index()
    
    # Index documents
    documents = [
        {
            'title': 'Azure AI Services Guide',
            'content': 'Your document content here...',
            'source': 'azure_guide.pdf',
            'metadata': {'timestamp': '2024-01-15', 'author': 'Microsoft'}
        }
    ]
    rag.index_documents(documents)
    
    # Query the system
    result = rag.advanced_rag_pipeline(
        query="What are the best practices for implementing RAG systems?",
        top_k=5,
        use_reranking=True,
        filter_days=30
    )
    
    print(f"Question: {result['query']}")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {len(result['sources'])} documents used")
    print(f"Tokens: {result['tokens_used']}")
```

---

## Additional Resources

### Lab Templates
Each lab includes:
- Pre-configured environment setup
- Step-by-step instructions
- Working code samples
- Challenge extensions
- Troubleshooting guide
- Cost optimization tips

### Assessment Criteria
- Code functionality (40%)
- Best practices implementation (20%)
- Error handling (15%)
- Documentation (15%)
- Performance optimization (10%)

### Support Resources
- Lab discussion forums
- Office hours schedule
- Video walkthroughs
- Solution repositories
- Peer review system

---

*Total Labs: 50+*  
*Estimated Completion Time: 200+ hours*  
*Skill Level: Beginner to Advanced*

**Remember**: Practice makes perfect. Complete all labs to master Azure AI Engineering!