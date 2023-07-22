from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import UploadedImage
from .serializers import UploadedImageSerializer
from .image_matching_algorithm.utils import preprocess_and_inference
import os

class ImageUploadView(APIView):
    """
    Uploads two images and an optional text field for processing and matching.

    The API endpoint allows users to upload two images (file1 and file2) and an optional text field
    for processing and matching. The uploaded images will be processed, matched, and the result
    will be visualized in an output image.

    Parameters:
    file1 (image file): The first image to be uploaded.
    file2 (image file): The second image to be uploaded.

    Returns:
    JSON response: The API response will contain the URL of the output image that
    visualizes the matching results.
    """
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(
        operation_id="Image Upload",
        tags=["upload"],
        operation_description="Upload Two images",
        operation_summary="Images can be Indoors or Outdoors",
        responses={
            500:"Internal Server Error",
            400:openapi.Response(
                description="Bad Request",
                examples={
                    "application/json":{
                       "message": "Provide correct input. Images Upload failed"
                    }
                }
            ),
            200:openapi.Response(
                description="Successfull Operation",
                examples={
                    "application/json": [{"output_image_url": "/media/07222023194933.png"}]
                }
            )
        }
    )
    
    def post(self, request, *args, **kwargs):
        if 'file1' not in request.FILES or 'file2' not in request.FILES:
            return Response({'error': 'Two image files (file1 and file2) must be provided.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer1 = UploadedImageSerializer(data={'image': request.FILES['file1']})
        serializer2 = UploadedImageSerializer(data={'image': request.FILES['file2']})

        


        if serializer1.is_valid() and serializer2.is_valid():
            
            serializer1.save()
            serializer2.save()

            fimg1 = serializer1.data['image'][1:]
            fimg2 = serializer2.data['image'][1:]

            output_path = preprocess_and_inference(fimg1,fimg2)
            return Response({
                'output_image_url': f'/media/{output_path}',
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)
