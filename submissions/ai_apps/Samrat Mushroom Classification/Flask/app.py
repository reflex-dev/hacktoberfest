# importing libraries
from flask import Flask, render_template, url_for, request
from keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Load our saved model (Mushroom classification model)
model_path = "Mushroom Classification Model.h5"
model = None

def load_mushroom_model():
    global model
    model = load_model(model_path)

# Load the model outside of the Flask app
load_mushroom_model()

# initialize the flask
app = Flask(__name__)

# Set the static folder
app.static_folder = 'static'

# routing 
@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/Mushroom-classification-predict")
def predict_page():
    return render_template("input.html")


@app.route("/Mushroom-classification-predict", methods = ["POST"])
def predict():
    imageFile = request.files["image_file"]
    imagePath = os.path.join("uploads/", imageFile.filename)
    imageFile.save(imagePath)
    inputImage = image.load_img(imagePath, target_size=(224, 224))
    inputImage = image.img_to_array(inputImage)
    inputImage = np.expand_dims(inputImage, axis=0)
    inputImage = inputImage / 255.0
    prediction = model.predict(inputImage)
    predicted_class_index = np.argmax(prediction)
    class_names = ['Boletus', 'Lactarius', 'Russula']
    predicted_class = class_names[predicted_class_index]
    return render_template("input.html",  prediction=predicted_class)


# run the application
if __name__ == "__main__" :
    app.run( debug=True )
