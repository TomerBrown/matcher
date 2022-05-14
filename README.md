# Candidate To Jobs Matching
## Home assignment for Gloat Interview
## By Tomer Brown

### Setup:
* Make sure docker and docker-compose are installed.
* Run the following command:
     * ```
        docker-compose up
        ```
*note: it might take a couple of minutes to setup.  
### Admin Interface:
* An automated super user with the following parameters is initialized:
    * Username : admin
    * Password: admin 
* can be accessed via the url: ```http://127.0.0.1:8000/admin/```
### Basic API:
#### Input:
* **URL:** Request should be directed to the following suffix of the url:
    > /match/
* **Method**: Expects POST request only with json parameters.
* **Parameters:** 
    * **"title"** - an exact title to find matching to (e.g. "Software Engineer").
    * **"top"** - an optional argument for selecting the maximal candidates number to return. If none given the top 10 candidates (or all of the qualified ones) are returned.

* **For example** : the following parameters will return the top 2 Software Engineer in the database.
     * ```
        {
          "title": "Software Engineer",
          "top" : 2
        }
        ```
#### Output:
* **Format**: Returns a json format with "top_candidates" entry with list of jsons representing candidates in the following format:
meaning an ordered list (descending order) of qualified candidates for the job. The order is determined by the number of required skills for the job that the candidate have.
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
#### Error Handling:
 * **Examples for errors that might occur":**
    * Wrong Method of request e.g. (GET instead of POST).
    * "title" isn't in the parameters json.
    * "top" isn't an int or is non positive number.
    * The requested title isn't in the database.
 * On all of the errors above, the response's status code would be 400
 * For example:
        
    * The Request:
           
        *   ```
            {
                "title": "Head of Fun"
            }
            ```
    * The Response (Assuming Head of Fun not in the DB):        
        *   ```
            {
                "Error": "There is no such job as Head of Fun in the database. Please try a different job title"
            }
            ```


### Testing:

* Some basic functionality and unit tests are added to the match_app.
* These tests include some:
   * Successful calls to the API and validates results.
   * Unsuccessful calls to the API, e.i. cases where the call should fail.
* Additional testing were conducted using Postman App.
* To run all of the tests just run the following command:
     * ```
        docker-compose run web python3 manage.py test
        ```
