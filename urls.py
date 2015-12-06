from django.conf.urls import include, url

from rest_framework import routers, serializers, viewsets

from .models import Registration, Link

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('name', 'url')

class RegistrationSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True)

    class Meta:
        model = Registration
        fields = ('email', 'name', 'university', 'location', 'tshirt_size',
                  'travel_subsidy', 'status', 'links')

    def create(self, validated_data):
        links_data = validated_data.pop('links')
        registration = Registration.objects.create(**validated_data)
        for link_data in links_data:
            Link.objects.create(registration=registration, **link_data)
        return registration

    def update(self, instance, validated_data):
        # pop links data
        links_data = validated_data.pop('links')

        # update regular fields
        instance.__dict__.update(validated_data)

        # update links
        if links_data is not None:
            # delete old objects
            for link in instance.links.all():
                link.delete()
            # create the new ones
            for link_data in links_data:
                Link.objects.create(registration=instance, **link_data)
        return instance

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

router = routers.DefaultRouter()
router.register(r'user', RegistrationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
