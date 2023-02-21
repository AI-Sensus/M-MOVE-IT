from django.shortcuts import render, redirect 
from .models import Sensor, Deployment,  Subject, SensorType
from . import forms
from .utils.validate_config_json import validateConfigJSON
import os
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
import json

# Create your views here.
def tablepage(request):
    sensors = Sensor.objects.all().order_by('sensor_id')
    subjects = Subject.objects.all().order_by('name')
    deployments = Deployment.objects.all().order_by('begin_datetime')
    sensortypes = SensorType.objects.all().order_by('manufacturer')
    for deployment in deployments:
        deployment.CreateLists()
    return render(request, 'tablepage.html', {'sensors': sensors, 'subjects': subjects, 'deployments': deployments, 'sensortypes': sensortypes})

def add(request):
    if request.method == 'POST':
        sensorform = forms.SensorForm(request.POST)
        if sensorform.is_valid():
            sensorform.save()
            return redirect('sensormodel:tablepage')
        subjectform = forms.SubjectForm(request.POST)
        if subjectform.is_valid():
            subjectform.save()
            return redirect('sensormodel:tablepage')
        deploymentform = forms.DeploymentForm(request.POST)
        if deploymentform.is_valid():
            deploymentform.save()
            return redirect('sensormodel:tablepage')
        else:
            sensorform = forms.SensorForm()
            subjectform = forms.SubjectForm()
            return render(request, 'add.html', {'sensorform':sensorform, 'subjectform':subjectform, 'deploymentform':deploymentform})
    else:
        sensorform = forms.SensorForm(request.POST)
        subjectform = forms.SubjectForm(request.POST)
        deploymentform = forms.DeploymentForm(request.POST)
    return render(request, 'add.html', {'sensorform':sensorform, 'subjectform':subjectform, 'deploymentform':deploymentform})


def adjust_deployment(request, id):
    deployment = Deployment.objects.get(id=id)
    if request.method == 'POST':
        deploymentform = forms.DeploymentForm(request.POST, instance=deployment)
        if deploymentform.is_valid():
            deploymentform.save()
            return redirect('sensormodel:tablepage')
    else:
        deploymentform = forms.DeploymentForm(instance=deployment)
    return render(request, 'deployment.html', {'deploymentform':deploymentform})
    
def adjust_sensor(request, id):
    sensor = Sensor.objects.get(id=id)
    if request.method == 'POST':
        sensorform = forms.SensorForm(request.POST,instance=sensor)
        if sensorform.is_valid():
            sensorform.save()
            return redirect('sensormodel:tablepage')
    else:
        sensorform = forms.SensorForm(instance=sensor)
    return render(request, 'sensor.html', {'sensorform':sensorform})


def adjust_subject(request, id):
    subject = Subject.objects.get(id=id)
    if request.method == 'POST':
        subjectform = forms.SubjectForm(request.POST, instance=subject)
        if subjectform.is_valid():
            subjectform.save()
            return redirect('sensormodel:tablepage')
    else:
        subjectform = forms.SubjectForm(instance=subject)
    return render(request, 'subject.html', {'subjectfrom':subjectform})
    
def delete_deployment(request, id):
    deployment = Deployment.objects.get(id=id)
    if request.method == 'POST':
        deployment.delete()
        return redirect('sensormodel:tablepage')
    else:
        return render(request, 'deleteconfirmation.html')
    
def delete_sensor(request, id):
    sensor = Sensor.objects.get(id=id)
    if request.method == 'POST':
        sensor.delete()
        return redirect('sensormodel:tablepage')
    else:
        return render(request, 'deleteconfirmation.html')


def delete_subject(request, id):
    subject = Subject.objects.get(id=id)
    if request.method == 'POST':
        subject.delete()
        return redirect('sensormodel:tablepage')
    else:
        return render(request, 'deleteconfirmation.html')

def sync_sensor_parser_templates(request):
    if request.method == 'POST':
        path = Path(__file__).parents[2]/ 'sensortypes'
        parser_files = []
        files = os.listdir(path)
        for file in files:
            name, ext = os.path.splitext(file)
            if ext == '.yaml':
                parser_files.append(file) 
        SensorType.objects.all().delete()
        for parser_file in parser_files:
            file_name = str(parser_file).split('.')[0]
            manufacturer, name, version = file_name.split('_')
            
            if not SensorType.objects.filter(manufacturer=manufacturer,name=name, version=version).exists():
                with open(path / str(parser_file)) as f:
                    config = yaml.load(f, Loader=SafeLoader)
                    config = str(config).replace("\'", "\"")
                    config = config.replace("None", "\"\"")
                    
                    
                if validateConfigJSON(str(config)):
                    config = json.loads(config)
                    SensorType.objects.create(manufacturer=manufacturer,name=name, version=version, **config).save()
    return redirect('sensormodel:tablepage')


