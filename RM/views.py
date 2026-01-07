from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from RM.models import contact, items, industry
from django.contrib import messages
from django.http import HttpResponse
import tensorflow as tf
import numpy as np
import keras
try:
    from tensorflow.keras.utils import load_img, img_to_array
except ImportError:
    try:
        from keras.utils import load_img, img_to_array
    except ImportError:
        # Fallback: use PIL directly
        from PIL import Image
        def load_img(path, target_size=None):
            img = Image.open(path)
            if target_size:
                img = img.resize(target_size)
            return img
        def img_to_array(img):
            return np.array(img)
from tensorflow.keras.models import load_model
import PIL as pillow
from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

#request -> respond
#request handler 
# user sees

# def say_hello(request): #func
#     # return HttpResponse('hello world')
#     return render(request, 'hello.html', {'name': 'Amit'})

# Load model lazily to avoid compatibility issues at import time
_model = None
imageUrl = None  # Global variable to store the last predicted image URL

def get_model():
    global _model
    if _model is None:
        # Load model with compile=False to avoid reduction='auto' compatibility issue
        # Then recompile with compatible settings
        try:
            _model = tf.keras.models.load_model("R_NR_2.h5", compile=False)
            # Recompile with compatible settings if needed
            if not _model._is_compiled:
                _model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        except Exception as e:
            # If compile=False doesn't work, try with custom_objects
            from tensorflow.keras.losses import BinaryCrossentropy
            custom_objects = {'BinaryCrossentropy': BinaryCrossentropy}
            _model = tf.keras.models.load_model("R_NR_2.h5", custom_objects=custom_objects, compile=False)
            _model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
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

        # Load and preprocess image
        img = load_img('media/'+filename, target_size=(256, 256))
        # Convert PIL image to numpy array, then to tensor
        img_array = img_to_array(img)
        resize = tf.image.resize(img_array, (256, 256))
        #img = cv2.imread('bottle.jpg')
        model = get_model()
        yhat = model.predict(np.expand_dims(resize/255, 0))
        # yhat
        result = ''
        if yhat > 0.5: 
            result = 'RECYCLABLE'
            prediction = True
            recycle = True
            imageUrl = 'media/'+filename
        else:
            result = 'NON-RECYCLABLE'
            prediction = True
            recycle = False
            
        context = {'result': 'The Uploaded Image is ' + result , 'prediction': prediction, 'recycle': recycle}
        return render(request, 'upload.html', context)
        
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
        
        