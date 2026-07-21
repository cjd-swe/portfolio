from django.db import models

# Create your models here.
class Job(models.Model):
	#Properties
	image = models.ImageField(upload_to='static/images/')
	summary = models.CharField(max_length = 200)

	def __str__(self):
		return self.summary

class Skill(models.Model):
	#Properties
	image = models.ImageField(upload_to='static/job_logos')
	summary = models.CharField(max_length = 30)

	def __str__(self):
		return self.summary