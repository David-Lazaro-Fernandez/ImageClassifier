from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from getpass import getpass
import os
from dotenv import load_dotenv
import shutil
import tensorflow as tf
from PIL import Image
import numpy as np
import openai
import sys

load_dotenv()

model = tf.keras.models.load_model('doc_classificator.h5')
api_key = os.getenv("OPENAI_API_KEY", None)

# Función para preprocesar la imagen
def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((256, 256))  # Ajusta el tamaño según las necesidades de tu modelo
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    classes = {
        0:'factura',
        1:'invoice',
        2:'other',
        3:'ticket'
    }
    try:
        temp_file = f"temp/{file.filename}"
        with open(temp_file, "wb") as buffer:
            # Utiliza await al llamar a métodos que son coroutines
            shutil.copyfileobj(file.file, buffer)
        # Preprocesa la imagen
        input_data = preprocess_image(temp_file)
        print("INPUT DATA", input_data)
        # Realiza la predicción utilizando el modelo
        prediction = model.predict(input_data)
        predicted_class = ""
        predicted_class = classes[np.argmax(prediction)]
        # Devuelve la predicción como respuesta JSON
        return JSONResponse(content={"prediction": prediction.tolist(), "predicted_class": predicted_class})

    except Exception as e:
        print(e)
        # Maneja cualquier excepción que pueda ocurrir durante la predicción
        raise HTTPException(status_code=500, detail="Error during prediction")

# for res in openai.completions.create(
#     model="text-davinci-003",
#     prompt="Sabes que es el SAT en Mexico?",
#     temperature=0.5,
#     max_tokens=120,
#     stream=True,
# ):
#     sys.stdout.write(res.choices[0].text)
#     sys.stdout.flush()
