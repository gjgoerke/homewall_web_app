from django.contrib import admin
from .models import Boulder, Circuit, CircuitSection, ClimberProfile, BoulderAscent, CircuitAscent

admin.site.register(Boulder)
admin.site.register(Circuit)
admin.site.register(CircuitSection)
admin.site.register(ClimberProfile)
admin.site.register(BoulderAscent)
admin.site.register(CircuitAscent)