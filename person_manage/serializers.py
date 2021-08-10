from os import write
from django.utils.functional import empty
from rest_framework import serializers
from .models import CustomUser,TestResults


class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    email = serializers.CharField(max_length=120)
    fio = serializers.CharField()
    official = serializers.CharField()
    person_group_id = serializers.IntegerField()
    activate_code = serializers.CharField(write_only=True)
    person_group = serializers.StringRelatedField()
    password = serializers.CharField(write_only=True)
    depth = 1

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.Official = validated_data.get('Official', instance.Official)
        instance.person_group_id = validated_data.get('person_group_id', instance.person_group_id)
        instance.save()
        return instance

class GenerateQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField(max_length=120)
    answer = serializers.CharField()
    factor = serializers.FloatField()

class TestResult(serializers.Serializer):
    test_result = serializers.FloatField()
    test_mark = serializers.CharField()
    tested_user_id = serializers.IntegerField()

    def create(self, validated_data):
        return TestResults.objects.create(**validated_data)