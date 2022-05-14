from django.db import models
import json

MAX_LEN = 128


class Skill (models.Model):

    name = models.CharField(max_length=MAX_LEN, unique=True)

    def __str__(self):
        return self.name

    def __eq__(self , other):
        if type(self) is not type(other):
            return False
        return self.name == other.name

class Job (models.Model):

    title = models.CharField(max_length=128, unique=True)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.title


class Candidate (models.Model):

    first_name = models.CharField(max_length=MAX_LEN)
    last_name = models.CharField(max_length=MAX_LEN)
    title = models.ForeignKey(Job, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def count_required_skills(self, required_skills):
        """ Given a candidate and a list of required skills , returns how many of
        those skills does the candidate have."""

        skills = self.skills.all()
        return len(skills.intersection(required_skills))

    def to_json(self, num_skills_required):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'title': str(self.title),
            'num_of_skills_required': num_skills_required
        }


