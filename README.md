# Candidate To Jobs Matching
## Home assignment for Gloat Interview


### Setup:


### Basic API:
#### Input:
* **URL:** Request should be directed to the following suffix of the url:
    > /match/
* **Method**: Expects POST request only with json parameters.
* **Parameters:** 
    * **"title"** - an exact title to find matching to (e.g. "Software Engineer").
    * **"top"** - an optional argument for selecting the maximal candidates number to return. If none given the top 10 candidates are returned.

* **For example** : the following parameters will return the top 5 Software Engineer in the database.
     * ```
        {
          "title": "Software Engineer",
          "top" : 2
        }
        ```
#### Output:
* **Format**: Returns a json format with "top_candidates" entry with list of jsons representing candidates in the following format:
     * ```
        {
            "top candidates": [
                {
                    "first_name": "Tomer",
                    "last_name": "Brown",
                    "title": "Software Engineer",
                    "num_of_skills_required": 5
                },
                {
                    "first_name": "Nadir",
                    "last_name": "Hackerman",
                    "title": "Software Engineer",
                    "num_of_skills_required": 4
                }
            ]
        }
        ```

### Testing:

* Some basic functionality and unit tests are added to the match_app.
* These tests include some:
   * Successful calls to the API and validates results.
   * Unsuccessful calls to the API, e.i. cases where the call should fail.
* Additional testing were conducted using Postman App.
* Call 'python manage.py test' to run all tests.