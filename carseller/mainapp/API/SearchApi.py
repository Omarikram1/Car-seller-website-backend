import json
from rest_framework.views import APIView,Response
from django.shortcuts import redirect, render
from mainapp.models import Car, Model
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator



def build_car_list(cars):
    return [
        {
            "id": car.id,
            "name": car.model.name if car.model else 'Unknown Model',
            "condition": car.condition,
            "image": car.image.url if car.image else None,
            "price": car.price if car.price else 0,
        }
        for car in cars
    ]







# class FilterCarsApi(APIView):
#     permission_classes = [AllowAny] 
#     def post(self, request, *args):
#         try:
#             data = json.loads(request.body)  # Parse JSON body
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        
#         limit = int(request.GET.get('limit', 4))  # Default limit is 4
#         offset = int(request.GET.get('offset', 0))  # Default offset is 0

#         query = Q()
#         filter_mapping = {
#             'condition': 'condition',
#             'model': 'model__name',
#             'price': 'price__lte',
#             'type': 'type'
#         }

#         # Dynamically add filters for condition, model, and price
#         for key, value in data.items():
#             if key in filter_mapping and value:
#                 query &= Q(**{filter_mapping[key]: value})
                                        

#         # Apply the filters and return the result
#         if query:
#             cars = Car.objects.filter(query)

#         else:
#             paginationcars = Car.objects.all()[offset:offset + limit]
#             total_count = Car.objects.filter(query).count()

#         if cars.exists():
#             return JsonResponse({'CarsSet': build_car_list(cars),
#             }, status=200)
#         else:
#             return JsonResponse({'NoCars': 'No cars found'}, status=200)





class FilterCarsApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args):
        try:
            data = json.loads(request.body)  # Parse JSON body for filters
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Determine the pagination size (based on request - search or reload)
        limit = int(request.GET.get('limit', 4))  # Default to 4 (for reloads)
        offset = int(request.GET.get('offset', 0))  # Default offset to 0

        # Initialize query object
        query = Q()

        # Define the filter mapping
        filter_mapping = {
            'condition': 'condition',
            'model': 'model__name',
            'price': 'price__lte',
            'type': 'type'
        }

        # Dynamically add filters based on the provided data
        for key, value in data.items():
            if key in filter_mapping and value:
                query &= Q(**{filter_mapping[key]: value})

        # Apply the filters and slice the result using limit and offset
        if query.children:  # Filters applied
            cars = Car.objects.filter(query)[offset:offset + limit]
            total_count = Car.objects.filter(query).count()
        else:  # No filters applied, return all cars
            cars = Car.objects.all()[offset:offset + limit]
            total_count = Car.objects.all().count()

    

        # Return paginated data with metadata
        return JsonResponse({
            'CarsSet': build_car_list(cars),  # The paginated result
            'count': total_count,  # Total number of cars
            'has_next': (offset + limit) < total_count,  # Check if there's a next page
            'has_previous': offset > 0  # Check if there's a previous page
        }, status=200)