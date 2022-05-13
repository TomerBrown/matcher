from django.test import TestCase , Client
import json
from .views import error_messages
from django.http import JsonResponse
from .models import Job, Candidate, Skill


def get_data_dic(title, top=None):
    data = {
        "title": title
    }
    if top is not None:
        data['top'] = top
    return data


class MatchUpTests(TestCase):
    # Load some pre-defined database (with few entries) to test our app's basic functionality
    fixtures = ['match_app/fixtures/match_app.yaml']
    client = Client()

    def get_request(self, data: dict) -> JsonResponse:
        return self.client.generic("GET", '/match/', data=json.dumps(data), content_type='application/json')

    def check_errors(self, res: JsonResponse, err_msg: str, job_name: str = ""):
        self.assertEqual(res.status_code, 400)
        if err_msg != 'invalid_job':
            self.assertEqual(res.json()["Error"], error_messages[err_msg])
        else:
            self.assertEqual(res.json()["Error"], error_messages['invalid_job'].format(title=job_name))

    def test_job_does_not_exists(self):
        job_name = "Head of Fun"
        res = self.get_request(get_data_dic(job_name))
        self.check_errors(res, 'invalid_job', job_name)


    def test_incorrect_method(self):
        res = self.client.generic("PUT", '/match/', data=json.dumps(get_data_dic("Software Engineer")), content_type='application/json')
        self.check_errors(res, 'invalid_req')


    def test_invalid_parameter(self):
        data = {"Title": "Software Engineer"}
        res = self.get_request(data)
        self.check_errors(res, 'invalid_req')

    def test_legit_request_works_and_sorted(self):
        title = "Software Engineer"
        res = self.get_request(get_data_dic(title))
        self.assertEqual(res.status_code, 200)
        top_candidates = res.json()["top candidates"]

        # Make sure every candidate is indeed with the right title, and returned list is sorted.
        for i, candidate in enumerate(top_candidates):
            self.assertEqual(candidate['title'], title)
            if i < len(top_candidates)-1:
                self.assertTrue(candidate['num_of_skills_required'] >= top_candidates[i+1]['num_of_skills_required'])

    def test_legit_request_with_change_top(self):
        """ Test whether the mechanism of returning the top k candidates works"""
        title = "Software Engineer"
        num_engineers = len(Candidate.objects.filter(title__title=title))
        for top in range(1, 10):
            res = self.get_request(get_data_dic(title , top))
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(res.json()["top candidates"]), min(top, num_engineers))

    def test_non_legit_request_with_change_top(self):
        title = "Software Engineer"
        for top in range(-5, 1):
            res = self.get_request(get_data_dic(title,top))
            self.check_errors(res, 'invalid_req')

    def test_job_with_no_candidates(self):
        res = self.get_request(get_data_dic("God"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['top candidates']), 0)

    def test_another_job(self):
        title = "Finance"
        res = self.get_request(get_data_dic(title))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['top candidates']), len(Candidate.objects.filter(title__title=title)))

