from rest_framework import serializers
from .models import CustomUser,TestResults
from .models import DetailedTestResult as dtr

# Сериалайзер для создания и просмотра и изменения данных пользователей

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

# Сериалайзер получения сгенерированных вопросов

class GenerateQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField(max_length=120)
    answer = serializers.CharField()
    factor = serializers.FloatField()

# Сериалайзер для создания детальных результатов тестирования

class DetailedTestResultSerializer(serializers.Serializer):
    test_number_id = serializers.IntegerField()
    test_number = serializers.IntegerField(read_only = True)
    question = serializers.CharField()
    qustion_result = serializers.CharField()
    factor = serializers.FloatField()

    def create(self, validated_data):
        return dtr.objects.create(**validated_data)

# Сериалайзер для просмотра детальных результатов тестирования

class DetailedTestResultView(serializers.ModelSerializer):
    class Meta:
        model = dtr
        fields = ['question','qustion_result',]

# Сериалайзер для просмотра результатов тестирования всех пользователей

class TestResultSerializerView(serializers.ModelSerializer):
    tested_user = serializers.CharField(read_only = True)
    test_detail = DetailedTestResultView(read_only=True, many=True)
    class Meta:
        model = TestResults
        fields = ['id','tested_user','test_result','test_mark','test_detail']
        depth  = 1

#Сериалайзер для создания результатов тестирования всех пользователей

class TestResultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    tested_user = serializers.CharField(read_only = True)
    test_result = serializers.FloatField()
    test_mark = serializers.CharField()
    tested_user_id = serializers.IntegerField(write_only = True)

    def create(self, validated_data):
        return TestResults.objects.create(**validated_data)
