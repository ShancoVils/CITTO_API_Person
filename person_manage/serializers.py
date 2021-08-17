from django.db.models.fields import CharField
from rest_framework import serializers
from .models import CustomUser,TestResults
# from .models import DetailedTestResult as dtr

# Сериалайзер для создания и просмотра и изменения данных пользователей

class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    email = serializers.CharField(max_length=120)
    first_name = serializers.CharField()
    namej = serializers.CharField()
    last_name = serializers.CharField()
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
        instance.namej = validated_data.get('namej', instance.namej)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.official = validated_data.get('official', instance.official)
        instance.person_group_id = validated_data.get('person_group_id', instance.person_group_id)
        instance.save()
        return instance

# Сериалайзер получения сгенерированных вопросов

class GenerateQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField(max_length=120)
    answer = serializers.CharField()
    factor = serializers.FloatField()

# #Сериалайзер для создания и просмотра результатов тестирования

class TestResultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    tested_user = serializers.CharField(read_only = True)
    test_questions = serializers.JSONField()
    test_answers = serializers.JSONField(required = False)
    test_sum_factor = serializers.IntegerField(required = False)
    test_result = serializers.CharField(required = False)
    tested_user_id = serializers.IntegerField(write_only = True)
    test_time_begin = serializers.TimeField()
    test_time_end = serializers.TimeField(required = False)

    def create(self, validated_data):
        return TestResults.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.test_answers = validated_data.get('test_answers', instance.test_answers)
        instance.test_sum_factor = validated_data.get('test_sum_factor', instance.test_sum_factor)
        instance.test_result = validated_data.get('test_result', instance.test_result)
        instance.test_time_end = validated_data.get('test_time_end', instance.test_time_end)
        instance.save()
        return instance