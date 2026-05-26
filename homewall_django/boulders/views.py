import json
from urllib import request as urllib_request

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Boulder, Circuit, CircuitSection, Ascent, BoulderAscent, CircuitAscent, ClimberProfile
from .forms import BoulderForm, CircuitForm, LogBoulderAscentForm

@csrf_exempt
@require_POST
def proxy_lights(request):
    url = f"http://{settings.ESP32_IP}/lights"
    try:
        req = urllib_request.Request(
            url,
            data=request.body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib_request.urlopen(req, timeout=5) as resp:
            return JsonResponse(json.loads(resp.read().decode()))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=502)


# Boulders
class IndexView(ListView):
    model = Boulder
    template_name = 'boulders/index.html'
    context_object_name = 'boulders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grade_range'] = range(18)
        return context

class BoulderView(DetailView):
    model = Boulder
    template_name = 'boulders/boulder.html'

class NewBoulderView(View):
    def get(self, request):
        return render(request, 'boulders/new.html', {'form': BoulderForm()})
    
    def post(self, request):
        form = BoulderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('boulders:index')
        return render(request, 'boulders/new.html', {'form': form})

class EditBoulderView(UpdateView):
    model = Boulder
    form_class = BoulderForm
    template_name = 'boulders/edit.html'
    success_url = reverse_lazy('boulders:index')

class LogBoulderAscentView(LoginRequiredMixin, CreateView):
    model = BoulderAscent
    form_class = LogBoulderAscentForm
    template_name = "boulders/log_ascent.html"
    success_url = reverse_lazy('boulders:index')  # Redirect to index after success
    
    def form_valid(self, form):
        # Get boulder ID from URL parameter
        boulder = get_object_or_404(Boulder, pk=self.kwargs['pk'])
        form.instance.boulder = boulder
        form.instance.climber = self.request.user.climber_profile
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boulder'] = get_object_or_404(Boulder, pk=self.kwargs['pk'])
        return context

# Circuits
class CircuitListView(ListView):
    model = Circuit
    template_name = 'boulders/circuits.html'
    context_object_name = 'circuits'

class CircuitView(DetailView):
    model = Circuit
    template_name = 'boulders/circuit_detail.html'

class NewCircuitView(View):
    def get(self, request):
        return render(request, 'boulders/new_circuit.html', {'form': CircuitForm()})

class EditCircuitView(UpdateView):
    model = Circuit
    form_class = CircuitForm
    template_name = 'boulders/edit_circuit.html'
    success_url = reverse_lazy('boulders:circuit_list')

# Accounts
class BouldersLoginView(LoginView):
    template_name='boulders/login.html'
    success_url = reverse_lazy('boulders:index')  # Where to redirect after login
    redirect_authenticated_user = True   # Redirect if user is already logged in

    def form_invalid(self,form):
        form.add_error(None, "Invalid username or password.")
        return super().form_invalid(form)
    
class BouldersLogoutView(LogoutView):
    next_page = 'boulders:index'  # Redirect after logout
    template_name = 'boulders/index.html'  # Optional: template to render

class BouldersRegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("boulders:login")
    template_name = "boulders/register.html"

