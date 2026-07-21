from django.db import models

# Create your models here.
class Job(models.Model):
	#Properties
	title = models.CharField(max_length=100)
	company = models.CharField(max_length=100)
	date_range = models.CharField(max_length=100)
	description = models.TextField()
	logo = models.ImageField(upload_to='static/job_logos/', blank=True, null=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['order']

	def __str__(self):
		return f'{self.title} at {self.company}'

class Project(models.Model):
	#Properties
	name = models.CharField(max_length=100)
	description = models.TextField()
	url = models.URLField(blank=True, null=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['order']

	def __str__(self):
		return self.name

class Skill(models.Model):
	#Properties
	image = models.ImageField(upload_to='static/job_logos')
	summary = models.CharField(max_length = 30)

	def __str__(self):
		return self.summary