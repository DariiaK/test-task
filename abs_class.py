from abc import ABC, abstractmethod
from config import ACCESS_TOKEN, REPO_NAME

class GitHubAPITest(ABC):
    def __init__(self):
        self.base_url = "https://api.github.com/"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {ACCESS_TOKEN}"
        }
        self.repo_name = REPO_NAME

    @abstractmethod
    def test_authorization(self):
        pass

    @abstractmethod
    def test_get_all_repositories(self):
        pass

    @abstractmethod
    def test_get_all_branches(self):
        pass

    @abstractmethod
    def test_get_pull_requests(self):
        pass

    @abstractmethod
    def test_create_pull_request(self):
        pass

    @abstractmethod
    def test_delete_pull_request(self):
        pass

    @abstractmethod
    def test_merge_pull_request(self):
        pass