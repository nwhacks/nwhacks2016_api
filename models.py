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
        (0, "applied"),
        (1, "accepted"),
        (2, "waitlisted"),
        (3, "rejected")]

    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    github = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)
    personal_site = models.CharField(max_length=200, blank=True, null=True)
    tshirt_size = models.PositiveSmallIntegerField(choices=TSHIRT_SIZES)
    travel_subsidy = models.BooleanField()
    first_hackathon = models.BooleanField()
    mentor = models.BooleanField()
    resume = models.FileField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS)
    reason = models.TextField()

    def __str__(self):
        return self.name
