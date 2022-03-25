from rest_framework import serializers
from .models import Requesteditem, onePerson , Donateditem

class onePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = onePerson
        fields = '__all__'

class requestedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requesteditem
        fields = '__all__'

class donatedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donateditem
        fields = '__all__'
