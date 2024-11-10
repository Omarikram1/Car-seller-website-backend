import json
from rest_framework.views import APIView,Response
from django.http import JsonResponse
from mainapp.models import Car,Model
from rest_framework.permissions import AllowAny



class GetType(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        # Fetch distinct types from the Car model
        distinct_types = Car.objects.values_list('type',flat=True).distinct()
        distinct_conditions = Car.objects.values_list('condition',flat=True).distinct()
        distinct_models = Model.objects.values_list('name',flat=True).distinct()
        # cars = Car.objects.all()[:4]
        typelist = list(distinct_types)
        conditionslist = list(distinct_conditions)
        modelslist = list(distinct_models)
        # car_data = [{"id": car.id, "model": car.model.name if car.model else "Unknown Model"
        #              ,"price": car.price, "condition": car.condition, 'image': 
        #              car.image.url if car.image else None} for car in cars]
        
        return JsonResponse({'distinct_types': typelist , 'distinct_conditions' : conditionslist , 'distinct_models':
                              modelslist, },status = 200)
    

