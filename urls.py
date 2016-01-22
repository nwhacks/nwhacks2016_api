from django.conf.urls import include, url
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework import routers, serializers, viewsets, mixins

from .models import Registration

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('name', 'email', 'school', 'city', 'github', 'linkedin', 'personalsite',
                  'resume', 'tshirt', 'travel_reimbursement', 'first_hackathon', 'mentor',
                  'reason')

class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ['post']

    def perform_create(self, serializer):
        # save our instance
        instance = serializer.save()

        # send confirmation email
        message = EmailMultiAlternatives("nwHacks 2016 Registration Confirmation",
                                         render_to_string("nwhacks2016/email.txt", {
                                             "name": instance.name
                                         }),
                                         "nwHacks Registration <noreply@nwhacks.io>",
                                         [instance.email],
                                         reply_to=["apply@nwhacks.io"])

        # attach html content
        message.attach_alternative(render_to_string("nwhacks2016/email.html", {
            "name": instance.name
        }), "text/html")

        # send the message
        message.send()

router = routers.SimpleRouter()
router.register(r'register', RegistrationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
