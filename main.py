from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

origins = [
    "http://localhost",
     "http://127.0.0.1:5500",
    "/Users/admin/Desktop/AI:ML/Potato_Disease_CNN/Potato-Disease-Classifier/Potato_Disease_CNN/index.html",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("/Users/admin/Desktop/AI:ML/Potato_Disease_CNN/cauliflower__model_v1.h5")  # Replace with path of the model needed

# CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]   # Potato model
# CLASS_NAMES = ['Anthracnose', 'Bacterial Canker', 'Cutting Weevil', 'Die Back', 'Gall Midge', 'Healthy', 'ODD(Cifar10_Subset)', 'Powdery Mildew', 'Sooty Mould']  # Mango model
# CLASS_NAMES = ['ODD(Cifar10_Subset)', 'bacterial_leaf_blight', 'brown_spot', 'healthy', 'leaf_blast', 'leaf_scald', 'narrow_brown_spot']  # Rice Model
# CLASS_NAMES = ['Anthracnose', 'ODD(Cifar10_Subset)', 'bird eye spot', 'brown blight', 'healthy']   # Tea Model
CLASS_NAMES = ['Bacterial spot rot', 'Black Rot', 'Downy Mildew', 'Healthy', 'ODD(Cifar10_Subset)']  # Cauliflower Model

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

def format_prediction(predicted_class, confidence):
    # Check if confidence is less than 60%
    if confidence < 60:
        confidence_message = f"{confidence}% - Confidence very low"
    else:
        confidence_message = f"{confidence}%"
    
    return {
        'class': predicted_class,
        'confidence': confidence_message
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = round(np.max(predictions[0]) * 100, 2)

    # Call the format_prediction function and return the result
    result = format_prediction(predicted_class, confidence)
    
    return result

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
