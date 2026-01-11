from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from RM.models import contact, items, industry
from django.contrib import messages
from django.http import HttpResponse
import os
import numpy as np
# avoid top-level tensorflow imports
# import keras  # optional, only if you need it; remove if it triggers TF import

# Prefer PIL-based image loading at module import (lightweight)
from PIL import Image
def load_img(path, target_size=None):
    img = Image.open(path).convert("RGB")
    if target_size:
        img = img.resize(target_size)
    return img

def img_to_array(img):
    return np.array(img)

import PIL as pillow
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.admin.views.decorators import staff_member_required

import importlib
import threading

# Create your views here.

# Lazy model and lock
_model = None
_model_lock = threading.Lock()

def get_model():
    """
    Lazy-load tensorflow and the keras model on first use.
    This avoids importing tensorflow during module import/startup.
    """
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                # Import tensorflow only when we actually need it
                tf = importlib.import_module("tensorflow")
                model_path = os.path.join(settings.BASE_DIR, "R_NR_2.h5")

                try:
                    _model = tf.keras.models.load_model(model_path, compile=False)
                    if not getattr(_model, "_is_compiled", True):
                        _model.compile(
                            optimizer="adam",
                            loss="binary_crossentropy",
                            metrics=["accuracy"],
                        )
                except Exception:
                    # Fallback using custom_objects WITHOUT re-importing tensorflow
                    custom_objects = {
                        "BinaryCrossentropy": tf.keras.losses.BinaryCrossentropy
                    }
                    _model = tf.keras.models.load_model(
                        model_path,
                        custom_objects=custom_objects,
                        compile=False,
                    )
                    _model.compile(
                        optimizer="adam",
                        loss="binary_crossentropy",
                        metrics=["accuracy"],
                    )

    return _model



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
        Society = request.POST['Society']
        City = request.POST['City']
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
                user = User.objects.create_user(username=username,first_name=Society,last_name=City,password=password, email=email)
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

def imagePrediction(request):
    global imageUrl
    if request.method == 'POST':
        prediction = False
        recycle = False
        uploadedImage = request.FILES['uploadedImage']
        fs = FileSystemStorage()
        filename = fs.save(uploadedImage.name, uploadedImage)
        uploaded_file_url = fs.url(filename)

        # Load image (PIL) and convert to numpy array
        pil_img = load_img(os.path.join(settings.BASE_DIR, 'media', filename), target_size=(256, 256))
        img_array = img_to_array(pil_img).astype('float32')  # shape (H, W, C)

        # Lazy-import tensorflow only when we actually need it
        try:
            tf = importlib.import_module("tensorflow")
        except Exception as e:
            # TF failed to import — inform user and log
            messages.error(request, "Server error: failed to import TensorFlow.")
            return render(request, 'upload.html')

        # resize (tf accepts numpy arrays but will convert to tensor)
        try:
            resized = tf.image.resize(img_array, (256, 256))
        except Exception:
            # Fallback: if tf.image.resize has issues, use numpy/PIL resize
            resized = img_array  # already resized by load_img target_size

        # Get model (this will lazy-load the model if not yet loaded)
        try:
            model = get_model()
        except Exception as e:
            messages.error(request, "Server error: failed to load model.")
            return render(request, 'upload.html')

        # Predict (normalize to [0,1])
        try:
            batch = np.expand_dims(resized / 255.0, axis=0)
            yhat = model.predict(batch)
        except Exception as e:
            messages.error(request, "Server error during prediction.")
            return render(request, 'upload.html')

        # Interpret result
        result = ''
        if np.asarray(yhat).size and (np.asarray(yhat) > 0.5).any():
            result = 'RECYCLABLE'
            prediction = True
            recycle = True
            imageUrl = os.path.join('media', filename)
        else:
            result = 'NON-RECYCLABLE'
            prediction = True
            recycle = False

        context = {'result': 'The Uploaded Image is ' + result, 'prediction': prediction, 'recycle': recycle, 'imageUrl': imageUrl}
        return render(request, 'upload.html', context)

    return render(request, 'upload.html')


def addItem(request):
    if request.method == 'POST':
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to save items to your profile.')
            return redirect(login)
        
        current_user = request.user
        active_user_id = current_user.id
        
        # Check if imageUrl is set (from previous prediction)
        global imageUrl
        if imageUrl is None:
            messages.error(request, 'No image found. Please upload and predict an image first.')
            return redirect(imagePrediction)
        
        itemName = request.POST.get('itemName', 'Unnamed Item')
        item = items(Name=itemName, img_Link=imageUrl, user_id=active_user_id)
        item.save()
        messages.success(request, 'Item saved to your profile successfully!')
        return redirect(imagePrediction)
        
        

def profile(request):
    current_user = request.user
    active_user_id = current_user.id
    itemData = items.objects.filter(user_id=active_user_id).values()
    context = {'itemData': itemData}
    return render(request, 'profile.html', context)

def deleteItem(request, imgId):
    if request.method == 'POST':
        record = items.objects.get(id=imgId)
        record.delete()
        return redirect('/profile')
    
def resources(request):
    industryData = industry.objects.values()
    # print(industryData)
    context = {'industryData': industryData}
    return render(request, 'resources.html', context)

@staff_member_required(login_url='/login')
def userStats(request):
    return render(request, 'userStats.html')

def findUser(request):
    if request.method == 'POST':
        userName = request.POST['username']
        userData = User.objects.filter(username=userName).values()
        userDataId = userData[0]['id']
        itemData = items.objects.filter(user_id=userDataId).values()
        print(userDataId)
        context = {'userData': userData, 'itemData':itemData}
        return render(request, 'userStats.html',context)
    
def findSociety(request):
    if request.method == 'POST':
        societyName = request.POST['societyName']
        userData = User.objects.filter(first_name=societyName).values()
        context = {'userData':userData}
        return render(request,'userStats.html',context)

@staff_member_required(login_url='/login')   
def viewItems(request,userId):
    itemData = items.objects.filter(user_id=userId).values()
    context = {'itemData':itemData, 'deleteString': 5}
    return render(request, 'viewItem.html', context)
        
        