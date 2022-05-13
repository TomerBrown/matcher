from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from .models import Job, Skill, Candidate
import json

error_messages = {
    "invalid_req": 'The request is invalid. please check the format. '
                   'should be GET request with json parameters as follows:{title:<title_name>}',
    "invalid_job": 'There is no such job as {title} in the database. Please try a different job title'
}


def is_valid_request(request: HttpRequest):
    """ Given a django HTTP Request returns whether it is valid request """

    # Check if it the correct method
    if request.method != 'GET':
        return False

    # Check if it contains the title (Other parameters will be ignored)
    req = json.loads(request.body.decode('utf-8'))
    if 'title' not in req:
        return False

    return True


def find_matches(request: HttpRequest):
    """ The main view that deals with the request and queries the database """

    # First check whether the request is valid (type and content of request)
    if not is_valid_request(request):
        return JsonResponse({"Error": error_messages['invalid_req']}, status=400)

    # Take the request parameter - title
    req = json.loads(request.body.decode('utf-8'))
    job_title = req["title"]

    # Try to find the title in the database and return an error message if it does not exists
    try:
        job = Job.objects.get(title=job_title)
    except Job.DoesNotExist:
        return JsonResponse({"Error": error_messages['invalid_job'].format(title=job_title)}, status=400)

    # Get all skills of the given job
    skills_required_for_job = job.skills.all()

    candidate_to_num_of_skills = []
    all_candidates = Candidate.objects.all()
    for candidate in all_candidates:
        candidate_to_num_of_skills.append({
            "first_name": candidate.first_name,
            "last_name": candidate.last_name,
            "num_of_required_skills": candidate.count_required_skills(skills_required_for_job)
        })
    candidate_to_num_of_skills.sort(key=lambda x: x["num_of_required_skills"], reverse=True)
    return JsonResponse({"top candidates":candidate_to_num_of_skills[:10]})
