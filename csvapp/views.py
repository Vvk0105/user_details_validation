from django.shortcuts import render
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserDetails
from .serializers import UserDetailSerializer
# Create your views here.


class CsvUploadAPiView(APIView):
    def post(self, request):
        #get file
        file = request.FILES.get('file')
        print(file)
        #check if the file is csv or not
        if not file or file.name.lower()[-4:] != '.csv':
            return Response({'error':'Please upload a csv file'}, status=status.HTTP_400_BAD_REQUEST)
        
        saved_count = 0
        rejected_count = 0
        errors = []

        #read csv file and convert binary stream to text
        content = file.read().decode('utf-8')
        reader = csv.DictReader(content)
        
        #looping through each row except 1st because 1st row is the heading
        for id, row in enumerate(reader, start=2):
            email = row.get('email')
            #email validation and storing to db
            if UserDetails.objects.filter(email=email).exists():
                rejected_count += 1
                errors.append({
                    "row":id, 
                    "error":{"email":['Duplicate email']}, 
                    "data":row
                })
                continue

            #validate the rows
            serializer = UserDetailSerializer(data=row)
            if serializer.is_valid():
                serializer.save()
                saved_count += 1
            else:
                rejected_count += 1
                errors.append({
                    "row": id,
                    "errors": serializer.errors,
                    "row_data": row
                })
    
        return Response({
            "saved_count":saved_count,
            "rejected_count":rejected_count,
            "errors":errors 
        }, status=status.HTTP_200_OK) 