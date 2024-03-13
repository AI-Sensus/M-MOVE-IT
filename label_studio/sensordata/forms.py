from django import forms
import zipfile
from django.core.exceptions import ValidationError
from sensormodel.models import Sensor
from sensordata.models import SensorOffset, SensorData
from projects.models import Project


class SensorDataForm(forms.Form):
    sensor = forms.ModelChoiceField(Sensor.objects.all())
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  # Remove 'project' from kwargs
        super(SensorDataForm, self).__init__(*args, **kwargs)

        # Filter the sensor queryset based on the provided project
        if project:
            self.fields['sensor'].queryset = Sensor.objects.filter(project=project)
    
    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            if not (zipfile.is_zipfile(uploaded_file) or uploaded_file.name.lower().endswith('.csv') or uploaded_file.name.lower().endswith('.mp4')):
                raise ValidationError("Uploaded file must be a valid zipfile or a single mp4 or csv file!")
        return uploaded_file


class SensorOffsetForm(forms.ModelForm):
    class Meta:
        model = SensorOffset
        fields = ['sensor_A', 'sensor_B', 'offset', 'offset_Date']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  # Remove 'project' from kwarg
        super().__init__(*args, **kwargs)

        # Filter camera choices to show only sensors with sensortype 'C'
        if project:
            self.fields['sensor_A'].queryset = Sensor.objects.filter(project=project)

        # Filter imu choices to show only sensors with sensortype 'I'
        if project:
            self.fields['sensor_B'].queryset = Sensor.objects.filter(project=project)

class OffsetAnnotationForm(forms.Form):
    sync_sensordata = forms.ModelMultipleChoiceField(
        queryset=SensorData.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
     
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(OffsetAnnotationForm, self).__init__(*args, **kwargs)

        if project is not None:
            queryset = SensorData.objects.filter(project=project)
            self.fields['sync_sensordata'].queryset = queryset

            # Include additional fields in the queryset
            # self.fields['sync_sensordata'].queryset = queryset.values(
            #     'id','name', 'begin_datetime', 'end_datetime', 'sensor__manual_offset'
            # )

   
class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['manual_offset']
        widgets = {
            'manual_offset': forms.TextInput(attrs={'placeholder': 'Optional. Give offset in seconds (integer)'}),
        }

        def __init__(self, *args, **kwargs):
            project = kwargs.pop('project', None)
            super(SubjectForm, self).__init__(*args, **kwargs)
            self.instance.project = project
