from rest_framework import serializers
from .models import Car


#Explanation: EK normal serializer me mje field or unki types or probably validations b mention krni prti ha
#Ye ek ModelSerializer ha jo Meta class me model ka nama le leta ha or fields puch leta ha kitne serialize krni ha
#Jitni fields di ho uski validation b wo Model me likhi validation k mutabik krega
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['name', 'model','category',  'condition', 'type','color','make' ,'year','transmission','fueltype','mileage',
                  'enginesize','cylinder','door', 'image', 'price'] 