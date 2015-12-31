from django.conf.urls import include, url

from rest_framework import routers, serializers, viewsets, mixins

from .models import Registration

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('name', 'email', 'school', 'city', 'github', 'linkedin', 'personalsite',
                  'resume', 'tshirt', 'travel_reinbursement', 'first_hackathon', 'mentor',
                  'reason')

class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ['post']

router = routers.SimpleRouter()
router.register(r'register', RegistrationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
