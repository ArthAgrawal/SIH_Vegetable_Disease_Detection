from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import json
import logging

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define model paths and class names for each plant type
MODELS = {
    "Potato": "/Users/admin/Desktop/AI/Potato_Disease_CNN/potato_model_v1.h5",
    "Mango": "/Users/admin/Desktop/AI/Potato_Disease_CNN/mango_model_v1.h5",
    "Rice": "/Users/admin/Desktop/AI/Potato_Disease_CNN/rice_model_v1.h5",
    "Tea": "/Users/admin/Desktop/AI/Potato_Disease_CNN/tea_model_v1.h5",
    "Cauliflower": '/Users/admin/Desktop/AI/Potato_Disease_CNN/cauliflower_model_v1.h5',
    "Wheat": '/Users/admin/Desktop/AI/Potato_Disease_CNN/wheat_model_v1.h5',
    "Brinjal": '/Users/admin/Desktop/AI/Potato_Disease_CNN/brinjal_model_v1.h5',
    "PepperBell": '/Users/admin/Desktop/AI/Potato_Disease_CNN/pepperbell_model_v1.h5',
    "Tomato": '/Users/admin/Desktop/AI/Potato_Disease_CNN/tomato_model_v1.h5',
    "Apple": '/Users/admin/Desktop/AI/Potato_Disease_CNN/apple_model_v1.h5',
    "Corn": '/Users/admin/Desktop/AI/Potato_Disease_CNN/corn_model_v1.h5',
    "Grape": '/Users/admin/Desktop/AI/Potato_Disease_CNN/grape_model_v1.h5',
    "Cherry": '/Users/admin/Desktop/AI/Potato_Disease_CNN/cherry_model_v1.h5',
    "Peach": '/Users/admin/Desktop/AI/Potato_Disease_CNN/peach_model_v1.h5'
}

class_names = {
    "Potato": ["Early Blight", "Late Blight", "Healthy"],
    "Mango": ['Anthracnose', 'Bacterial Canker', 'Cutting Weevil', 'Die Back', 'Gall Midge', 'Healthy', 'ODD(Cifar10_Subset)', 'Powdery Mildew', 'Sooty Mould'],
    "Rice": ['ODD(Cifar10_Subset)', 'bacterial_leaf_blight', 'brown_spot', 'healthy', 'leaf_blast', 'leaf_scald', 'narrow_brown_spot'],
    "Tea": ['Anthracnose', 'ODD(Cifar10_Subset)', 'bird eye spot', 'brown blight', 'healthy'],
    "Cauliflower": ['Bacterial spot rot', 'Black Rot', 'Downy Mildew', 'Healthy', 'ODD(Cifar10_Subset)'],
    "Wheat": ['Healthy', 'ODD(Cifar10_Subset)', 'septoria', 'stripe_rust'],
    "Brinjal": ['Diseased Brinjal Leaf', 'Fresh Brinjal Leaf', 'ODD(Cifar10_Subset)'],
    "PepperBell": ['ODD(Cifar10_Subset)', 'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy'],
    "Tomato": ['ODD(Cifar10_Subset)', 'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot', 'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy'],
    "Apple": ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'ODD(Cifar10_Subset)'],
    "Corn": ['Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'ODD(Cifar10_Subset)'],
    "Grape": ['Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'ODD(Cifar10_Subset)'],
    "Cherry": ['Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'ODD(Cifar10_Subset)'],
    "Peach": ['ODD(Cifar10_Subset)', 'Peach___Bacterial_spot', 'Peach___healthy']
}

# Load remedies from JSON file
with open('remedies.json') as f:
    remedies = json.load(f)

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

def format_prediction(predicted_class, confidence):
    if confidence < 60:
        confidence_message = f"{confidence}% - Confidence very low"
    else:
        confidence_message = f"{confidence}%"
    
    return {
        'class': predicted_class,
        'confidence': confidence_message
    }

logging.basicConfig(level=logging.INFO)

@app.post("/predict")
async def predict(file: UploadFile = File(...), plant_type: str = Form(...)):
    try:
        if plant_type not in MODELS:
            return {"error": "Invalid plant type selected."}

        model_path = MODELS[plant_type]
        logging.info(f"Loading model for {plant_type} from {model_path}")
        model = tf.keras.models.load_model(model_path)

        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, 0)

        logging.info("Image loaded and preprocessed")

        predictions = model.predict(img_batch)
        predicted_class = class_names[plant_type][np.argmax(predictions[0])]
        confidence = round(np.max(predictions[0]) * 100, 2)

        logging.info(f"Prediction made: {predicted_class} with confidence {confidence}%")

        result = format_prediction(predicted_class, confidence)

        # Get remedy for predicted class
        remedy_data = remedies.get(predicted_class)

        if remedy_data:
            result['remedy'] = {
                "crop_name": remedy_data['crop_name'],
                "crop_disease": remedy_data['crop_disease'],
                "remedies": remedy_data['remedies'],
                "home_remedies": remedy_data['home_remedies']
            }
        else:
            result['remedy'] = {
                "crop_name": "Unknown",
                "crop_disease": predicted_class,
                "remedies": ["No remedy found for this disease."],
                "home_remedies": []
            }
        return result

    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
