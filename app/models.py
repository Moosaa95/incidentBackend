# from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth import get_user_model


# # Create your models here.



from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    TYPE_CHOICES = (("user", "user"), ("admin", "admin"))

    first_name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(max_length=255)  # Business address
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="user")
    is_staff = models.BooleanField(default=True)
    can_login_web = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return "%s %s" % (self.first_name, self.surname)


class Location(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)

    @classmethod
    def add_location(cls, name):
        return cls.objects.create(name=name)

    @classmethod
    def get_location(cls, location_id):
        try:
            return cls.objects.get(pk=location_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def edit_location(cls, location_id, name):
        location = cls.get_location(location_id)
        if location:
            location.name = name
            location.save()
            return location
        return None

    @classmethod
    def delete_location(cls, location_id):
        location = cls.get_location(location_id)
        if location:
            location.delete()


class Incident(models.Model):
    SEVERITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("critical", "Critical"),
    ]

    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("investigating", "Investigating"),
        ("resolved", "Resolved"),
    ]

    title = models.CharField(max_length=200)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    reporter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=200)
    date_created = models.DateField(auto_now_add=timezone.now(), blank=True, null=True)


    @classmethod
    def add_incident(cls, title, severity, status, location, description):
        return cls.objects.create(
            title=title,
            severity=severity,
            status=status,
            location=location,
            description=description,
        )

    @classmethod
    def get_incident(cls, incident_id):
        try:
            return cls.objects.get(pk=incident_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def edit_incident(cls, incident_id, title, severity, status, location, description):
        incident = cls.get_incident(incident_id)
        if incident:
            incident.title = title
            incident.severity = severity
            incident.status = status
            incident.location = location
            incident.description = description
            incident.save()
            return incident
        return None

    @classmethod
    def delete_incident(cls, incident_id):
        incident = cls.get_incident(incident_id)
        if incident:
            incident.delete()


class Report(models.Model):
    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("investigating", "Investigating"),
        ("resolved", "Resolved"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, blank=True, null=True)
    

    def __str__(self):
        return self.title