from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint

class Organisation(models.Model):
    name = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=120)
    address_line1 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=80, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['organisation', 'name'], name='unique_location_name_per_org'),
        ]

    def __str__(self):
        return f"{self.organisation.name} - {self.name}"

class UserProfile(models.Model):
    ROLE_CUSTOMER = 'customer'
    ROLE_ORG_ADMIN = 'org_admin'
    ROLE_CHOICES = [
        (ROLE_CUSTOMER, 'Customer'),
        (ROLE_ORG_ADMIN, 'Organisation Admin'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)
    paid_access = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile: {self.user.username}"
