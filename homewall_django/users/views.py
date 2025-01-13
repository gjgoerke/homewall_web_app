from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from boulders.models import BoulderAscent, ClimberProfile

# Create your views here.
class UserAscentListView(LoginRequiredMixin, ListView):
    template_name = 'users/ascents.html'
    context_object_name = 'ascents'
    paginate_by = 150
    
    def get_queryset(self):
        # Get or create the user's climber profile
        climber_profile, _ = ClimberProfile.objects.get_or_create(
            user=self.request.user
        )
        ascents =  BoulderAscent.objects.filter(
            climber_id=climber_profile.id
        ).order_by('-date_time')
        return ascents
    