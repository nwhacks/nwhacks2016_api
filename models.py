from django.db import models

# Create your models here.
class Registration(models.Model):
    TSHIRT_SIZES = [
        (0, "extra small"),
        (1, "small"),
        (2, "medium"),
        (3, "large"),
        (4, "extra large")]
    STATUS = [
        (0, "accepted"),
        (1, "waitlisted")]

    email = models.EmailField()
    name = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    tshirt_size = models.PositiveSmallIntegerField(choices=TSHIRT_SIZES)
    travel_subsidy = models.PositiveSmallIntegerField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS)

    def __str__(self):
        return self.name

class Link(models.Model):
    registration = models.ForeignKey(Registration, related_name="links")
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return "%s %s" % (self.registration, self.name)
