from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt

from .models import Job, Skill, Candidate
import json

error_messages = {
    "invalid_req": 'The request is invalid. please check the format. '
                   'should be POST request with json parameters as follows:{title:<title_name> , top: <int> (optional)}',
    "invalid_job": 'There is no such job as {title} in the database. Please try a different job title'
}


def is_valid_request(request: HttpRequest):
    """ Given a django HTTP Request returns whether it is valid request """

    if request.method != 'POST':
        return False

    req = json.loads(request.body.decode('utf-8'))
    if 'title' not in req:
        return False

    if 'top' in req:
        if not type(req['top']) is int or req['top'] <= 0:
            return False

    return True

@csrf_exempt
def find_matches(request: HttpRequest):
    """ The main view that deals with the request and queries the database """
    # First check whether the request is valid (type and content of request)
    if not is_valid_request(request):
        return JsonResponse({"Error": error_messages['invalid_req']}, status=400)

    # Take the request parameter - title
    req = json.loads(request.body.decode('utf-8'))
    job_title = req["title"]
    top = req["top"] if "top" in req else 10

    # Try to find the title in the database and return an error message if it does not exists
    try:
        job = Job.objects.get(title=job_title)
    except Job.DoesNotExist:
        return JsonResponse({"Error": error_messages['invalid_job'].format(title=job_title)}, status=400)

    skills_required_for_job = job.skills.all()

    # query the dataset to get candidates with maximal number of required skills
    # Firstly, take those who fit the job title
    sorted_candidates = Candidate.objects.filter(title__title=job_title)
    # Secondly , Over those who got the correct title ,sort candidates by number of required skills for job
    sorted_candidates = sorted_candidates.annotate(num_skills=Count('skills', filter=Q(skills__in=skills_required_for_job))).order_by('-num_skills')

    top_candidates = [candidate.to_json(candidate.num_skills) for candidate in sorted_candidates[:top]]
    return JsonResponse({"top candidates": top_candidates}, content_type='application/json')
