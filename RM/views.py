from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from RM.models import contact
from django.contrib import messages
from django.http import HttpResponse
import tensorflow as tf
import numpy as np
import keras
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.models import load_model
import PIL as pillow
from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.

#request -> respond
#request handler 
# user sees

# def say_hello(request): #func
#     # return HttpResponse('hello world')
#     return render(request, 'hello.html', {'name': 'Amit'})

model = tf.keras.models.load_model("R_NR_2.h5")

def home(request):
    return render(request,'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(home)
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect(login)
        
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect(login)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect(login)
            else:
                user = User.objects.create_user(username=username,password=password, email=email)
                user.save()
                
                return redirect(login)
        
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
        
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect(home)

def feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        feedback = contact(name=name , email=email , message=message)
        feedback.save()

    return render(request,'index.html')


def logout(request):
    auth.logout(request)
    return redirect(home)

def imagePrediction(request):
    if request.method == 'POST':
        uploadedImage = request.FILES['uploadedImage']
        fs = FileSystemStorage()
        filename = fs.save(uploadedImage.name, uploadedImage)
        uploaded_file_url = fs.url(filename)

        img = load_img('media/'+filename, target_size=(256, 256))
        resize = tf.image.resize(img, (256,256))
        #img = cv2.imread('bottle.jpg')
        yhat = model.predict(np.expand_dims(resize/255, 0))
        # yhat
        if yhat > 0.5: 
            print(f'Predicted class is Recyclable')
        else:
            print(f'Predicted class is Non-Recyclable')
        
        # # model.save('R_NR_2.h5')
        # img = request.FILES['uploadedImage']
        # new_model = load_model('R_NR_2.h5')
        # resize = tf.image.resize(img, (256,256))
        # yhat_new = new_model.predict(np.expand_dims(resize/255, 0))

        # if yhat_new > 0.5: 
        #     print(f'Predicted class is Recyclable')
        # else:
        #     print(f'Predicted class is Non-Recyclable')
        
    return render(request, 'upload.html')