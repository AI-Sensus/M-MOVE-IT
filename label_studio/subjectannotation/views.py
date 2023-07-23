from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SubjectAnnotationForm
from .utils.annotationtemplate import createSubjectAnnotationTemplate
import requests
from rest_framework.authtoken.models import Token
from tasks.models import Task, Annotation
from subjectannotation.models import SubjectPresence
from sensormodel.models import Subject

# Create your views here.
def annotationtaskpage(request):
    subjectannotationform = SubjectAnnotationForm()
    return render(request, 'annotationtaskpage.html', {'subjectannotationform':subjectannotationform})

def createannotationtask(request):
    # Functions that creates an API call to create a task with a video and the corresponding subjects as labels for subject annotation
    if request.method == 'POST':
        subjectannotationform = SubjectAnnotationForm(request.POST, request.FILES)
        if subjectannotationform.is_valid():
            ## Create project
            deployment = subjectannotationform.cleaned_data.get("deployment")
            deployment.CreateLists()
            sensorlist, subjectlist = deployment.sensorlist, deployment.subjectlist
            # Create a XML markup for annotating
            template = createSubjectAnnotationTemplate(subjectlist)
            title = str(deployment)
            
            # Get url for displaying all projects
            projects_url = request.build_absolute_uri(reverse('projects:api:project-list'))
            
            # Get current user token for authentication
            user = request.user
            token = Token.objects.get(user=user)

            # Create project using LS API
            requests.post(projects_url, headers={'Authorization': f'Token {token}'}, 
                          data={'label_config':template, 'title':title})
            
            ## Import data
            # Get ID of last created project    
            list_projects_response = requests.get(projects_url, headers={'Authorization': f'Token {token}'})
            last_project_id = list_projects_response.json()["results"][0]["id"]

            # Get url for importing data to the correct project
            import_url = request.build_absolute_uri(reverse('data_import:api-projects:project-import',
                                                            kwargs={'pk':last_project_id}))
            # Get temporary file URL from the form
            file_url = request.FILES['file'].temporary_file_path()
            files = {f'{request.FILES["file"]}': open(file_url, 'rb')}
            # Import the video to the correct project
            requests.post(import_url, headers={'Authorization': f'Token {token}'}, files=files)
            # Go the projects page
            return redirect('projects:project-index')

    subjectannotationform = SubjectAnnotationForm()
    return render(request, 'annotationtaskpage.html', {'subjectannotationform':subjectannotationform})


def parse_subject_presence_annotations(request, project):
    annotations = Annotation.objects.filter(project= project)
    for annotation in annotations:
        file_upload = Task.objects.get(id=annotation.task_id).file_upload
        results= annotation.result
        for result in results:
            labels = result['value']['labels']
            start_time = result['value']['start']
            end_time = result['value']['end']
            for label in labels:
                subject = Subject.objects.get(name=label.replace('Subject: ',''))
                if not SubjectPresence.objects.filter(file_upload=file_upload,project=project,subject=subject,
                                                 start_time=start_time,end_time=end_time).exists():
                    SubjectPresence.objects.create(file_upload=file_upload,project=project,subject=subject,
                                                 start_time=start_time,end_time=end_time)
                

