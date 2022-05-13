from django.db import models


class Skill (models.Model):

    name = models.CharField(max_length=128)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.name

class Candidate (models.Model):

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    skills = models.ManyToManyField(Skill)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Job (models.Model):

    title = models.CharField(max_length=128)
    skills = models.ManyToManyField(Skill)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.title