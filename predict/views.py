import os, json
import numpy as np
import tensorflow as tf
from accounts.permissions import IsVerified
from django.conf import settings
from PIL import Image
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


# Loading the JSON containing the class names
CLASS_NAMES_PATH = os.path.join(settings.BASE_DIR, 'class_names.json')

with open(CLASS_NAMES_PATH, 'r') as f:
    CLASS_NAMES = json.load(f)


# Loading the model 
MODEL_PATH = os.path.join(settings.BASE_DIR, 'trained_model.keras')
model = tf.keras.models.load_model(MODEL_PATH)


@api_view(['POST'])
@permission_classes([IsVerified])
def predict_disease(request):
    if request.method == 'POST':
        file = request.FILES.get('image')

        if not file:
            return Response({
                'success':False,
                'message':'No image uploaded'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            img = Image.open(file).convert('RGB')
            img = img.resize((128, 128))
            img_arr = tf.keras.preprocessing.image.img_to_array(img)
            img_arr = np.array([img_arr])

            prediction = model.predict(img_arr)
            predicted_class_index = int(np.argmax(prediction))

            confidence = float(np.max(prediction))

            return Response({
                'success':True,
                'prediction':CLASS_NAMES[str(predicted_class_index)],
                'confidence':confidence
            })
        
        except Exception as e:
            return Response({
                'success':False,
                'message':str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)