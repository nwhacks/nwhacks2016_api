from django.conf.urls import include, url

from rest_framework import routers, serializers, viewsets

from .models import Registration

import hack16.views

class FormToSerializerBooleanField(serializers.BooleanField):
    ''' workaround to convert django form field to serializer form field
    see my issue https://github.com/tomchristie/django-rest-framework/issues/2394
    '''
    TRUE_VALUES = set(('t', 'T', 'true', 'True', 'TRUE', '1', 1, True,'On','on','ON'))
    FALSE_VALUES = set(('f', 'F', 'false', 'False', 'FALSE', '0', 0, 0.0, False,'Off','off','OFF'))

class RegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    school = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    github = serializers.CharField(allow_blank=True, write_only=True)
    linkedin = serializers.CharField(allow_blank=True, write_only=True)
    personalsite = serializers.CharField(allow_blank=True, write_only=True)
    resume = serializers.FileField(required=False, write_only=True)
    tshirt = serializers.ChoiceField(("S", "M", "L", "XL"), write_only=True)
    travel_reinbursement = FormToSerializerBooleanField(write_only=True)
    first_hackathon = FormToSerializerBooleanField(write_only=True)
    mentor = FormToSerializerBooleanField(write_only=True)
    reason = serializers.CharField(write_only=True)

    def create(self, validated_data):
        reg = Registration()
        reg.email = validated_data.get('email')
        reg.name = validated_data.get('name')
        reg.university = validated_data.get('school')
        reg.location = validated_data.get('city')
        reg.github = validated_data.get('github')
        reg.linkedin = validated_data.get('linkedin')
        reg.personal_site = validated_data.get('personalsite')
        reg.resume = validated_data.get('resume')
        tshirt_size = validated_data.get('tshirt')
        if tshirt_size == 'S':
            reg.tshirt_size = 1
        elif tshirt_size == 'M':
            reg.tshirt_size = 2
        elif tshirt_size == 'L':
            reg.tshirt_size = 3
        elif tshirt_size == 'XL':
            reg.tshirt_size = 4
        else:
            reg.tshirt_size = 2
        reg.travel_subsidy = validated_data.get('travel_reinbursement')
        reg.first_hackathon = validated_data.get('first_hackathon')
        reg.mentor = validated_data.get('mentor')
        reg.status = 0 # applied
        reg.reason = validated_data.get('reason')
        reg.save()
        return reg

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.university = validated_data.get('school', instance.university)
        instance.location = validated_data.get('city', instance.location)
        instance.github = validated_data.get('github', instance.github)
        instance.linkedin = validated_data.get('linkedin', instance.linkedin)
        instance.personal_site = validated_data.get('personalsite', instance.personal_site)
        instance.resume = validated_data.get('resume', instance.resume)
        tshirt_size = validated_data.get('tshirt')
        if tshirt_size == 'S':
            instance.tshirt_size = 1
        elif tshirt_size == 'M':
            instance.tshirt_size = 2
        elif tshirt_size == 'L':
            instance.tshirt_size = 3
        elif tshirt_size == 'XL':
            instance.tshirt_size = 4
        instance.travel_subsidy = validated_data.get('travel_reinbursement', instance.travel_subsidy)
        instance.first_hackathon = validated_data.get('first_hackathon', instance.first_hackathon)
        instance.mentor = validated_data.get('mentor', instance.mentor)
        instance.reason = validated_data.get('reason', instance.reason)
        instance.save()
        return instance

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

router = routers.DefaultRouter()
router.register(r'register', RegistrationViewSet)

urlpatterns = [
    url(r'^$', hack16.views.app),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
