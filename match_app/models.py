from django.db import models


class Skill (models.Model):

    name = models.CharField(max_length=128)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.name

    def __eq__(self , other):
        if type(self) is not type(other):
            return False
        return self.name == other.name

class Candidate (models.Model):

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    skills = models.ManyToManyField(Skill)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def count_required_skills(self, required_skills):
        """ Given a candidate and a list of required skills , returns how many of
        those skills does the candidate have."""

        skills = self.skills.all()
        return len(skills.intersection(required_skills))


class Job (models.Model):

    title = models.CharField(max_length=128)
    skills = models.ManyToManyField(Skill)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.title
