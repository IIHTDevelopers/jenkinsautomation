import os
import unittest
import requests

class TestPipelineStructureFromJenkinsLogs(unittest.TestCase):

    def setUp(self):
        self.jenkins_url = "http://localhost:8080"  # Update with your Jenkins URL
        self.job_name = "Directory validation"  # Update with your Jenkins job name
        self.api_token = "11d0bc7300900dc8f693bbf8838b43ddad"  # Update with your Jenkins API token
        self.username = "admin"  # Update with your Jenkins username

    def fetch_jenkins_logs(self, build_number):
        """Fetch logs from a specific Jenkins build."""
        url = f"{self.jenkins_url}/job/{self.job_name}/{build_number}/consoleText"
        response = requests.get(url, auth=(self.username, self.api_token))
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def fetch_build_status(self, build_number):
        """Fetch the build status of a specific Jenkins build."""
        url = f"{self.jenkins_url}/job/{self.job_name}/{build_number}/api/json"
        response = requests.get(url, auth=(self.username, self.api_token))
        if response.status_code == 200:
            build_info = response.json()
            return build_info.get("result", "UNKNOWN")
        else:
            response.raise_for_status()

    def test_pipeline_logs_and_status(self):
        # Fetch the latest build number
        url = f"{self.jenkins_url}/job/{self.job_name}/lastBuild/api/json"
        response = requests.get(url, auth=(self.username, self.api_token))
        if response.status_code == 200:
            build_info = response.json()
            build_number = build_info['number']
        else:
            self.fail("Failed to fetch the latest build information from Jenkins.")

        # Fetch logs from the latest build
        logs = self.fetch_jenkins_logs(build_number)

        # Check for pipeline stages in logs
        expected_stages = ["Setup", "Validate Directory Structure", "Post Actions"]
        missing_stages = []
        for stage in expected_stages:
            if stage not in logs:
                missing_stages.append(stage)

        # Check the build status
        build_status = self.fetch_build_status(build_number)

        # Assertions
        self.assertEqual(len(missing_stages), 0, f"Missing pipeline stages: {missing_stages}")
        self.assertEqual(build_status, "SUCCESS", f"Build status is not successful: {build_status}")

if __name__ == "__main__":
    unittest.main()
