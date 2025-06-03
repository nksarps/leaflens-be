import os, json
import numpy as np
import tensorflow as tf
from accounts.permissions import IsVerified
from django.conf import settings
from PIL import Image
from predict.models import DiseasePrediction
from predict.serializers import DiseasePredictionSerializer
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

            DiseasePrediction.objects.create(
                user=request.user,
                image=file,
                prediction=CLASS_NAMES[str(predicted_class_index)]
            )

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


@api_view(['GET'])
@permission_classes([IsVerified])
def get_all_predictions(request):
    if request.method == 'GET':
        user = request.user

        predictions = DiseasePrediction.objects.filter(user=user)

        serializer = DiseasePredictionSerializer(predictions, many=True)

        return Response({
            'success':True,
            'predictions':serializer.data
        }, status=status.HTTP_200_OK)