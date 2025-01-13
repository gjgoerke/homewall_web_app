from django import forms
from .models import Boulder, Circuit, BoulderAscent

class BoulderForm(forms.ModelForm):
    GRADE_CHOICES = [(None, 'Project')] + [(i, 'V' + str(i)) for i in range(0, 18)]

    grade = forms.TypedChoiceField(
        choices=GRADE_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_value=None
    )

    class Meta:
        model = Boulder
        fields = ['name', 'grade', 'description', 'holds_hands_only', 'holds_feet_only', 'holds_general', 'holds_finish', 'holds_start']
        
        hold_fields = ['holds_start', 'holds_general', 'holds_finish', 'holds_feet_only', 'holds_hands_only']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            **{field: forms.HiddenInput(attrs={'class': 'form-control boulder-hold-input'}) for field in hold_fields}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and isinstance(self.instance.grade, int):
            self.initial['grade'] = self.instance.grade

    def clean_grade(self):
        grade = self.cleaned_data['grade']
        if grade is None:
            return None
        return int(grade)

class CircuitForm(forms.ModelForm):
    class Meta:
        model = Circuit
        fields = ['name', 'grade', 'sections']

class LogBoulderAscentForm(forms.ModelForm):
    attempts = forms.TypedChoiceField(
        choices=[(i+1, str(i+1)) for i in range(999)],
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    class Meta:
        model = BoulderAscent
        fields = ['attempts', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional: Add notes about your ascent...'
            })
        }