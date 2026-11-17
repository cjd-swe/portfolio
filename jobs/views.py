from textwrap import shorten

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.templatetags.static import static
from django.views.static import serve
from .models import Job, Project

# Create your views here.
def homepage(request):
	jobs = Job.objects.all()
	projects = Project.objects.all()
	return render(request, 'jobs/home.html', {
		'jobs': jobs, 'projects': projects,
		'page_title': 'Cameron J. Davis — Forward Deployed Engineer',
		'page_description': 'Cameron J. Davis is a Forward Deployed Engineer building secure backend systems, cloud infrastructure, and delivery pipelines.',
	})

def detail(request, job_id):
	job_detail = get_object_or_404(Job, pk = job_id)
	description = shorten(job_detail.description, width=150, placeholder='…')
	return render(request, 'jobs/detail.html', {
		'job': job_detail,
		'page_title': f'{job_detail.title} at {job_detail.company} | Cameron J. Davis',
		'page_description': f'{job_detail.title} at {job_detail.company}. {description}',
	})


def media(request, path):
	response = serve(request, path, document_root=settings.MEDIA_ROOT)
	response['Cache-Control'] = 'public, max-age=86400'
	return response


def root_icon(request, filename):
	# Temporary redirect: the target is a content-hashed file name that changes
	# whenever the icon does, so browsers must not cache this hop forever.
	return redirect(static(filename))


def robots(request):
	return render(request, 'jobs/robots.txt', content_type='text/plain')


def sitemap(request):
	return render(request, 'jobs/sitemap.xml', {'jobs': Job.objects.all()}, content_type='application/xml')

