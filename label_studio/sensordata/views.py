from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SensorDataForm, SensorOffsetForm
from .models import SensorData, SensorOffset
from .parsing.sensor_data import SensorDataParser
from .parsing.video_metadata import VideoMetaData
from .parsing.controllers.project_controller import ProjectController
from pathlib import Path
from django.core.files.uploadedfile import InMemoryUploadedFile
import json
from datetime import timedelta
from sensormodel.models import SensorType
from rest_framework.authtoken.models import Token
import requests
from tempfile import NamedTemporaryFile
from django.conf import settings
import os
import io
import csv
import fnmatch
import zipfile
from django.http import HttpResponseBadRequest


UNITS = {'days': 86400, 'hours': 3600, 'minutes': 60, 'seconds':1, 'milliseconds':0.001}

# Create your views here.
def sensordatapage(request):
    sensordata = SensorData.objects.all().order_by('project_id')
    return render(request, 'sensordatapage.html', {'sensordata':sensordata})

def addsensordata(request):
    if request.method == 'POST':
        sensordataform = SensorDataForm(request.POST, request.FILES)
        if sensordataform.is_valid():
            # Get form data
            name = sensordataform.cleaned_data['name']
            uploaded_file = sensordataform.cleaned_data['file']
            project_id = sensordataform.cleaned_data['project'].id
            sensor = sensordataform.cleaned_data.get('sensor')

            # Check if the uploaded file is a zip file
            if zipfile.is_zipfile(uploaded_file):
                # Process the zip file
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    for file_name in zip_ref.namelist():
                        if file_name.lower().endswith('.csv'):  # Check if the file is a CSV file
                            # Extract each file from the zip to a temporary location
                            temp_file_path = zip_ref.extract(file_name)
                            # Process the individual file
                            process_sensor_file(request, temp_file_path, sensor, name, project_id)
                            # Delete the temporary file
                            os.remove(temp_file_path)
                
                return redirect('sensordata:sensordatapage')

            # Raise an exception if the uploaded file is not a zip file
            raise ValueError("Uploaded file must be a zip file.")

    else:
        sensordataform = SensorDataForm()

    return render(request, 'addsensordata.html', {'sensordataform': sensordataform})

def process_sensor_file(request, file_path, sensor, name, project_id):
    # Process the sensor file based on its type
    sensortype = sensor.sensortype
    if sensortype.sensortype == 'I':  # IMU sensor type
        parse_IMU(request, file_path, sensortype.id, name, project_id)
    elif sensortype.sensortype == 'C':  # Camera sensor type
        parse_camera(request, file_path, sensortype.id, name, project_id)
    elif sensortype.sensortype == 'M':  # Other sensor type (add handling logic here)
        pass
    # Add handling for other sensor types as needed

def handle_uploaded_file(uploaded_file):
    # Handle the uploaded file and return the file path
    if isinstance(uploaded_file, InMemoryUploadedFile):
        # Write the contents of the file to a temporary file on disk
        file = NamedTemporaryFile(delete=False)
        file.write(uploaded_file.read())
        file.close()
        # Access file path of the newly created file
        file_path = file.name
    else:
        # If the file is not InMemoryUploaded, use temporary_file_path
        file_path = uploaded_file.temporary_file_path()

    return file_path


def delete_offset(request, id):
    offset = SensorOffset.objects.get(id=id)
    if request.method == 'POST':
        # Send POST to delete a sensor
        offset.delete()
        return redirect('sensordata:offset')
    else:
        # Go to delete confirmation page
        return render(request, 'deleteOffset.html')

def adjust_offset(request, id):
    offset = SensorOffset.objects.get(id=id)
    if request.method == 'POST':
        # Send POST to adjust a subject
        offsetform = SensorOffsetForm(request.POST, instance=offset)
        if offsetform.is_valid():
            offsetform.save()
            return redirect('sensordata:offset')
    else:
        # Go to subject adjustment page
        offsetform = SensorOffsetForm(instance=offset)
    return render(request, 'editOffset.html', {'offsetform':offsetform})


def parse_IMU(request, file_path, sensor_type_id, name, project_id):
    sensortype = SensorType.objects.get(id=sensor_type_id)
    # Parse data

    project_controller = ProjectController()
    sensor_data = SensorDataParser(project_controller, Path(file_path),sensortype.id)
    # Get parsed data
    sensor_df = sensor_data.get_data()
    # Now that the sensordata has been parsed it has to be transformed back to a .csv file and uploaded to the correct project
    # Create NamedTemporary file of type csv
    with NamedTemporaryFile(suffix='.csv', prefix=('IMU_sensor_'+ str(name)) ,mode='w', delete=False) as csv_file:
        # Write the dataframe to the temporary file
        sensor_df.to_csv(csv_file.name, index=False)
        file_path=csv_file.name

    # Upload parsed sensor(IMU) data to corresponding project
    upload_sensor_data(request=request, name=name, file_path=file_path ,project_id=project_id)
 
    # Parse to JSON to get begin and end datetime   
    sensor_data_json_string = sensor_df.to_json()
    sensor_data_json = json.loads(sensor_data_json_string)
    begin_datetime = sensor_data.metadata.utc_dt
    relative_absolute = sensortype.relative_absolute
    # Get time key
    keys = list(sensor_data_json.keys())
    time_key = keys[sensortype.timestamp_column]
    times = sensor_data_json[time_key]
    sorted_keys = sorted(times.keys(), key=int)
    penultimate_key = sorted_keys[-2]
    end_time = times[penultimate_key]
    if relative_absolute == 'relative':
        # Get end datetime if the timestamp is relative
        time_unit = sensortype.timestamp_unit
        delta = timedelta(seconds= float(end_time) * UNITS[time_unit])
        end_datetime =  begin_datetime + delta
    elif relative_absolute == 'absolute':
        # Get end datetime if the timestamp is absolute (needs to be checked with )
        pass
        # !! NOT YET WORKING !!
        # timestamp_unit = sensortype.timestamp_unit
        # end_time = dateutil.parser.parse(end_time)
        
        # end_datetime = begin_datetime + end_time

    # Create SensorData object with parsed data
    SensorData.objects.create(name=name, sensortype=sensortype,\
        begin_datetime=begin_datetime, end_datetime=end_datetime, project_id=project_id).save()
    


def parse_camera(request, file_path, sensor_type_id, name, project_id):
    # Upload video to project
    upload_sensor_data(request=request, name=name, file_path=file_path ,project_id=project_id)
    # Get sensortype config
    sensortype = SensorType.objects.get(id=sensor_type_id)
    sensor_timezone = sensortype.timezone
    # Parse video meta data
    videometadata = VideoMetaData(file_path=file_path,sensor_timezone=sensor_timezone)
    
    # Use parsed data from metadata to create SensorData object
    # Get the begin datetime and duration to determine the end datetime 
    begin_datetime = videometadata.video_begin_time
    video_duration = videometadata.video_duration # in seconds
    delta = timedelta(seconds= float(video_duration))
    end_datetime =  begin_datetime + delta

    # Create SensorData object with parsed data
    SensorData.objects.create(name=name, sensortype=sensortype,\
        begin_datetime=begin_datetime, end_datetime=end_datetime, project_id=project_id).save()
    
def upload_sensor_data(request, name, file_path, project_id):
    user = request.user
    token = Token.objects.get(user=user)
    # Get url for importing data to the correct project
    import_url = request.build_absolute_uri(reverse('data_import:api-projects:project-import',kwargs={'pk':project_id}))
    # Get temporary file URL from the form
    files = {f'{name}': open(file_path, 'rb')}
    # Import the video to the correct project
    requests.post(import_url, headers={'Authorization': f'Token {token}'}, files=files) 


def deletesensordata(request, id):
    sensordata = SensorData.objects.get(id=id)           
    if request.method == 'POST':
        # Send POST to delete a sensor
        
        sensordata.delete()
        return redirect('sensordata:sensordatapage')
    else:
        # Go to delete confirmation page
        return render(request, 'deleteconfirmation.html')             
    
def offset(request):
    sensoroffset = SensorOffset.objects.all().order_by('offset_Date')
    if request.method == 'POST':
        sensoroffsetform = SensorOffsetForm(request.POST)
        if sensoroffsetform.is_valid():
            sensorA = sensoroffsetform.cleaned_data['sensor_A']
            sensorB = sensoroffsetform.cleaned_data['sensor_B']
            offset = sensoroffsetform.cleaned_data['offset']
            offset_date = sensoroffsetform.cleaned_data['offset_Date']
            # create and save the new SensorOffset instance
            sensoroffsetform.save()
            # redirect to the offset view and pass the sensoroffset queryset to the context
            return redirect('sensordata:offset')
    else:
        sensoroffsetform = SensorOffsetForm()
    return render(request, 'offset.html', {'sensoroffsetform':sensoroffsetform, 'sensoroffset':sensoroffset})
