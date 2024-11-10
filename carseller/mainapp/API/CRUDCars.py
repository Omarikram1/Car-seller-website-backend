from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from mainapp.models import Car, Model
from mainapp.serializers import CarSerializer
import json

class CarCrudApi(APIView):
    permission_classes = [AllowAny]  

    #Gets the data of car through car_id in query parameter of url
    def get(self, request):
        car_id = request.GET.get('car_id', None)
                                            
        if car_id:
            car = get_object_or_404(Car, id=car_id)  # Get a specific car by ID
            serializer = CarSerializer(car)
            return JsonResponse(serializer.data, status=200)
        else:
             return JsonResponse({"error": "Car id not provided" }, status = 404)

    # Create a new car but send model name in model field rest all the fields 
    # It does not take id as it is auto generated (front end work)
    def post(self, request):             
        try:
            data = json.loads(request.body)  
            model_name = data.get('model') 

            if model_name:
                                
                model_instance = get_object_or_404(Model,name=model_name)
                data['model'] = model_instance.id
              
                serializer = CarSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()  
                    return JsonResponse(serializer.data, status=201)  
                else:
                    return JsonResponse(serializer.errors, status=400)

            else:
                return JsonResponse({'error': 'Model name is missing'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)




    # This catches the car instance by the car_id passed in query parameter of url after ? like: https:127.0.0.1/specefiedcars/?car_id=1
    # It sends the values to update in the body of request
    
     
    def put(self, request):
            car_id = request.GET.get('car_id', None)
            
            if not car_id:
                return JsonResponse({'error': 'Car id not provided'}, status=400)
            
            car = get_object_or_404(Car, id=car_id)
            try:
                data = json.loads(request.body)  
                model_name = data.get('model') 

                if model_name:
                                    
                    model_instance = get_object_or_404(Model,name=model_name)
                    data['model'] = model_instance.id
                
                    serializer = CarSerializer(car,data = data)

                    if serializer.is_valid():
                        serializer.save()  
                        return JsonResponse(serializer.data, status=201)  
                    else:
                        return JsonResponse(serializer.errors, status=400)

                else:
                    return JsonResponse({'error': 'Model name is missing'}, status=400)

            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)





    # It deletes the car instance by fetching it from the car_id query parameter from request url 

    def delete(self, request):
        car_id = request.GET.get('car_id', None)
        
        if not car_id:
            return JsonResponse({'error': 'Car ID is required for deletion'}, status=400)
        
        car = get_object_or_404(Car, id=car_id)
        car.delete()  # Delete the car from the database
        return JsonResponse({'message': 'Car deleted successfully'}, status=200)
    



#Note: Put or patch 
# Put completely record ko naya banata ha agr puri fields fill na ho tou baqi ki fields me default ya empty values ajati ha
# Patch partially record ko fill krta ha baqi ka retain krke
# Ap jab ek update ka form pe redirect krwate ho user ko tou sbse pahle uski info get krwa k un fields me show krwate ho
# Uske bad ap data get kr lete ho to to changes 