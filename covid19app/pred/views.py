# pred/views.py
from django.shortcuts import render,redirect
from .models import Members
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages
import numpy as np
import cv2
import tensorflow as tf

# Path to your saved TensorFlow model
model_path = r"C:\Users\mahmoud\PycharmProjects\pythonProject\covid19\models ai\covid_19.h5"
classifier = tf.keras.models.load_model(model_path)

#def login_index(request):
    #return render(request, 'covid/covid.html')

def login_index(request):
    if request.POST:
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        name = f"{first_name} {last_name}"
        email = request.POST["email"]
        phone = request.POST["phone"]
        gender = request.POST["gender"]
        age = request.POST["age"]
        file = request.FILES["file"]


        #save image path
        fs = FileSystemStorage()
        filename = fs.save(file.name,file)
        #img_file = fs.url(filename)
        file_path = fs.path(filename)
        # Read and process the image using OpenCV
        img = cv2.imread(file_path)
        if img is None:
            print("Image not loaded")

        img = cv2.resize(img, (224, 224))
        img = img.reshape(1, 224, 224, 3)
        img = img / 255.0

        # Perform prediction using the loaded TensorFlow model
        pred = classifier.predict(img)
        prediction = "positive" if pred >= 0.5 else 'negative'

        # Save the data to the database using Django model
        patient = Members()
        patient.name = name
        patient.email = email
        patient.phone = phone
        patient.gender = gender
        patient.age = age
        patient.image = file_path
        patient.prediction = prediction
        patient.save()

        data = Members.objects.filter(email=email)
        return render(request, 'resltc/resltc.html',
                      {'data': data
                       }
                      )

    return render(request,"covid/covid.html")














