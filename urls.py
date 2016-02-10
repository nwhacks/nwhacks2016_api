from django.conf.urls import include, url
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import routers, serializers, viewsets, mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Registration

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('id', 'name', 'email', 'school', 'city', 'github', 'linkedin', 'personalsite',
                  'resume', 'tshirt', 'travel_reimbursement', 'first_hackathon', 'mentor',
                  'reason', 'status', 'response', 'acceptance_sent', 'checked_in')

class IsCreationOrIsAuthenticated(BasePermission, SessionAuthentication):
    def has_permission(self, request, view):
        return view.action == 'create' or request.user.is_authenticated()

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class RegistrationViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ['get', 'post', 'patch']


    authentication_classes = (IsCreationOrIsAuthenticated, BasicAuthentication)
    permission_classes = (IsCreationOrIsAuthenticated, )

    def perform_create(self, serializer):
        # save our instance
        serializer.status = 0
        serializer.id = 0
        serializer.acceptance_sent = None
        serializer.checked_in = False
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

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RegistrationSerializer(instance, data=request.data, partial=True)
        serializer.is_valid()
        instance = serializer.save()
        return Response(serializer.data)


router = routers.SimpleRouter()
router.register(r'register', RegistrationViewSet)

@api_view(['POST'])
def record_response(request, registration_id, token, response_status):
    registration = get_object_or_404(Registration, pk=registration_id)

    if registration.token != token:
        # fail if token does not match
        raise Http404("Registration not found")

    # otherwise set the response status
    registration.response = response_status

    # save the object
    registration.save()

    # return a serialized object
    serializer = RegistrationSerializer(registration)
    return Response(serializer.data)

urlpatterns = [
    url(r'^rsvp/(?P<registration_id>\d+)/(?P<token>[a-zA-Z0-9]+)/(?P<response_status>\d+)$', record_response),
    url(r'^', include(router.urls)),
]
