from django.db import models

# Create your models here.
class Registration(models.Model):
    TSHIRT_SIZES = [
        ('XS', "extra small"),
        ('S', "small"),
        ('M', "medium"),
        ('L', "large"),
        ('XL', "extra large")]
    STATUS = [
        (0, "applied"),
        (1, "accepted"),
        (2, "waitlisted"),
        (3, "rejected")]

    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    github = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)
    personalsite = models.CharField(max_length=200, blank=True, null=True)
    resume = models.FileField(blank=True, null=True)
    tshirt = models.CharField(max_length=4, choices=TSHIRT_SIZES)
    travel_reinbursement = models.BooleanField()
    first_hackathon = models.BooleanField()
    mentor = models.BooleanField()
    reason = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.name
