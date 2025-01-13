from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ValidationError


class BaseClimb(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_set = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

class Boulder(BaseClimb):
    grade = models.IntegerField(null=True, blank=True)
    holds_hands_only = models.JSONField(default=list, blank=True)
    holds_feet_only = models.JSONField(default=list, blank=True)
    holds_general = models.JSONField(default=list, blank=True)
    holds_finish = models.JSONField(default=list)
    holds_start = models.JSONField(default=list)
    def save(self, *args, **kwargs):
        # Remove duplicates from holds lists before saving. Note that this only works on each individual list,
        # so we might still have duplicates in the combined list (fix later).
        if self.holds_hands_only:
            self.holds_hands_only = list(dict.fromkeys(self.holds_hands_only))
        if self.holds_feet_only:
            self.holds_feet_only = list(dict.fromkeys(self.holds_feet_only))
        if self.holds_general:
            self.holds_general = list(dict.fromkeys(self.holds_general))
        if self.holds_finish:
            self.holds_finish = list(dict.fromkeys(self.holds_finish))
        if self.holds_start:
            self.holds_start = list(dict.fromkeys(self.holds_start))
        super().save(*args, **kwargs)

class Circuit(BaseClimb):
    grade = models.IntegerField(null=True, blank=True)  # Different grading system
    sections = models.ManyToManyField(
        Boulder,
        through='CircuitSection',
        related_name='circuits',
    )
    
    class Meta:
        verbose_name = "Circuit"
        verbose_name_plural = "Circuits"

class CircuitSection(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    boulder = models.ForeignKey(Boulder, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()  # For maintaining sequence
    
    class Meta:
        ordering = ['order']
        unique_together = ['circuit', 'order']  # Prevent duplicate ordering
    
    def clean(self):
        # Validate that order is unique within this circuit
        if CircuitSection.objects.filter(
            circuit=self.circuit, 
            order=self.order
        ).exclude(id=self.id).exists():
            raise ValidationError('This order number is already in use for this circuit.')
    
class ClimberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="climber_profile")
    @property
    def num_sessions(self):
        return self.ascents.dates('date_time', 'day').count()

# Automatically create/update profile when User is created/updated
@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile when User is saved"""
    if created:
        # If this is a new user, create their profile
        ClimberProfile.objects.create(user=instance)
    else:
        # If this is an existing user, save their profile if it exists
        # or create it if it doesn't
        try:
            instance.climber_profile.save()
        except ClimberProfile.DoesNotExist:
            ClimberProfile.objects.create(user=instance)
     
class Ascent(models.Model):
    climber = models.ForeignKey(ClimberProfile, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=1)
    comment = models.TextField(blank=True)
    class Meta:
        abstract = True
    
class BoulderAscent(Ascent):
    boulder = models.ForeignKey(Boulder, on_delete=models.SET_NULL, null=True, related_name='ascents')
    climber = models.ForeignKey(ClimberProfile, on_delete=models.CASCADE, related_name='boulder_ascents')

class CircuitAscent(Ascent):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='ascents')
    climber = models.ForeignKey(ClimberProfile, on_delete=models.CASCADE, related_name='circuit_ascents')
