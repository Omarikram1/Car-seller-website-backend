
from rest_framework.views import APIView,Response
from django.shortcuts import redirect, render


class home(APIView):
    
    def get(self, request):
        
        return render(request, 'homepage.html')



# class specifiedcarsview(APIView):
    
#     def get(self, request):
        
#         return render(request, 'specifiedcarsview.html')
