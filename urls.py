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

class RegistrationSerializer(serializers.ModelSerializer):
    travel_reinbursement = FormToSerializerBooleanField()
    first_hackathon = FormToSerializerBooleanField()
    mentor = FormToSerializerBooleanField()

    class Meta:
        model = Registration
        fields = ('name', 'email', 'school', 'city', 'github', 'linkedin', 'personalsite',
                  'resume', 'tshirt', 'travel_reinbursement', 'first_hackathon', 'mentor',
                  'reason')

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

router = routers.DefaultRouter()
router.register(r'register', RegistrationViewSet)

urlpatterns = [
    # this serves the application page, remove in production
    url(r'^$', hack16.views.app),
    url(r'^api/', include(router.urls)),
]
