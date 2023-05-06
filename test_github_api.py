import base64
import logging
import requests
import random
from abs_class import GitHubAPITest

num = random.randint(100, 999)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class TestGitHubAPI(GitHubAPITest):
    def test_authorization(self):
        logger.info("Running test_authorization")
        response = requests.get(self.base_url, headers=self.headers)
        logger.info(f"Response status code: {response.status_code}")
        assert response.status_code == 200
        logger.info("test_authorization passed!")


    def test_get_all_repositories(self):
        logger.info("Running test_get_all_repositories")
        url = self.base_url + "user/repos"
        response = requests.get(url, headers=self.headers)
        logger.info(f"Response status code: {response.status_code}")
        repo_names = [repo["name"] for repo in response.json()]
        expected_repos = ["prj-nlp-2020", "test-repo", "test-task", "uk-nlp-workshop"]
        for expected_repo in expected_repos:
            assert expected_repo in repo_names, f"Expected repository {expected_repo} not found in the response"
        assert response.status_code == 200
        logger.info("test_get_all_repositories passed!")


    def test_get_all_branches(self):
        logger.info("Running test_get_all_branches")
        url = self.base_url + f"repos/{self.repo_name}/branches"
        response = requests.get(url, headers=self.headers)
        logger.info(f"Response status code: {response.status_code}")
        assert response.status_code == 200
        logger.info("test_get_all_branches passed!")


    def test_get_pull_requests(self):
        logger.info("Running test_get_pull_requests")
        url = self.base_url + f"repos/{self.repo_name}/pulls"
        response = requests.get(url, headers=self.headers)
        logger.info(f"Response status code: {response.status_code}")
        assert response.status_code == 200
        logger.info("test_get_pull_requests passed!")


    def test_create_pull_request(self):
        logger.info("Running test_create_pull_request")
          # Create a new branch
        branch_name = f"test-branch-{num}"
        url = self.base_url + f"repos/{self.repo_name}/git/refs"
        response = requests.get(url, headers=self.headers)
        sha = response.json()[0]["object"]["sha"]
        payload = {
            "ref": f"refs/heads/{branch_name}",
            "sha": sha
        }
        response = requests.post(url, headers=self.headers, json=payload)
        assert response.status_code == 201
          # Create a new file in the new branch
        url = self.base_url + f"repos/{self.repo_name}/contents/new_file.py"
        payload = {
            "message": "Create new_file.py",
            "content": base64.b64encode("print('Something')".encode()).decode(),
            "branch": branch_name
        }
        response = requests.put(url, headers=self.headers, json=payload)
        assert response.status_code == 201
          # Create a pull request for the new branch
        url = self.base_url + f"repos/{self.repo_name}/pulls"
        payload = {
            "title": "Test Pull Request",
            "head": branch_name,
            "base": "main"
        }
        pull_request_response = requests.post(url, headers=self.headers, json=payload)
        logger.info(f"Response status code: {pull_request_response.status_code}")
        assert pull_request_response.status_code == 201
        logger.info("test_create_pull_request passed!")


    def test_delete_pull_request(self):
        logger.info("Running test_delete_pull_request")
        url = self.base_url + f"repos/{self.repo_name}/pulls"
        payload = {
            "title": "Test Pull Request",
            "head": "test-branch-"+str(num),
            "base": "main"
        }
        response = requests.get(url, headers=self.headers)
        data = response.json()
        for pr in data:
            if pr["title"] == payload["title"] and pr["state"] == "open":
                pr_number = pr["number"]

                delete_url = self.base_url + f"repos/{self.repo_name}/pulls/{pr_number}"
                payload = {"state" : "closed"}
                delete_response = requests.post(delete_url, headers=self.headers, json=payload)
                logger.info(f"Response status code: {delete_response.status_code}")

                assert delete_response.status_code == 200
                logger.info("test_delete_pull_request passed!")
                return
        assert False, "test_delete_pull_request failed"


    def test_merge_pull_request(self):
        logger.info("Running test_approve_pull_request")
        url = self.base_url + f"repos/{self.repo_name}/pulls"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        for pr in data:
            if pr["head"]["ref"] == "test-branch-"+str(num):
                pr_number = pr["number"]
                review_url = self.base_url + f"repos/{self.repo_name}/pulls/{pr_number}/merge" 
                review_payload = {
                    "commit_title": "Merge pull request",
                    "commit_message": "Automatically merged pull request"
                }
                response = requests.put(review_url, headers=self.headers, json=review_payload)
                logger.info(f"Response status code: {response.status_code}")
                assert response.status_code == 200
                logger.info("test_approve_pull_request passed!")


test_api = TestGitHubAPI()
test_api.test_authorization()
test_api.test_get_all_repositories()
test_api.test_get_all_branches()
test_api.test_get_pull_requests()
test_api.test_create_pull_request() 
test_api.test_delete_pull_request() 
test_api.test_merge_pull_request()