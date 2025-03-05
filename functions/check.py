import os
import requests
import time
from datetime import datetime
from robot.api import ExecutionResult
from display_test_results import MyResultVisitor


def get_env_variable(name):
    """Retrieve an environment variable and return None if not set."""
    value = os.getenv(name)
    if not value:
        print(f"Warning: Missing environment variable {name}")
    return value


def post_github_check(results, report_content):
    """Post test results as a GitHub check run."""
    github_token = get_env_variable("GITHUB_TOKEN")
    repository = get_env_variable("GITHUB_REPOSITORY")
    commit_sha = get_env_variable("GITHUB_SHA")
    job_name = os.getenv("GITHUB_JOB", "Unknown Job")
    caller_job_name = get_env_variable("JOB_NAME")

    if caller_job_name:
        job_name = caller_job_name  # Override with actual job name

    if not all([github_token, repository, commit_sha]):
        print("Error: Missing required environment variables. Exiting...")
        return

    api_url = f"https://api.github.com/repos/{repository}/check-runs"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }

    total_tests = results.get("total", 0)
    passed_tests = results.get("passed", 0)
    failed_tests = results.get("failed", 0)
    duration = results.get("duration", 0)
    minutes, seconds = divmod(duration, 60)


    conclusion = "success" if failed_tests == 0 else "failure"

    summary = (f"{report_content}")

    payload_name = f"Test Results - {job_name}"

    payload = {
        "name": payload_name.title(),
        "head_sha": commit_sha,
        "status": "completed",
        "conclusion": conclusion,
        "output": {
            "title": f"Test Results - {job_name} executed in {int(minutes)}m {int(seconds)}s",
            "summary": summary
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 201:
        print("✅ GitHub check posted successfully")
    else:
        print(f"❌ Failed to post GitHub check: {response.status_code} - {response.text}")


def run_robot_tests():
    """Run Robot Framework tests, parse results, and post them to GitHub."""
    print(f"Current Working Directory: {os.getcwd()}")
    main_dir = './webapp_tests'  # Main directory where subdirectories with output.xml are located
    report_file = os.path.abspath('./webapp_tests/robot-test-results/report.md')

    # Collect all output.xml files from subdirectories
    output_files = find_output_files(main_dir)

    if not output_files:
        print(f"❌ Error: No output.xml files found in {main_dir}.")
        return

    test_results = {"total": 0, "passed": 0, "failed": 0, "duration": 0.0}
    
    # Process each output.xml and combine the results
    for output_file in output_files:
        print(f"Processing: {output_file}")
        if validate_output_file(output_file):
            individual_results = process_test_results(output_file, report_file)
            test_results["total"] += individual_results["total"]
            test_results["passed"] += individual_results["passed"]
            test_results["failed"] += individual_results["failed"]
            test_results["duration"] += individual_results["duration"]

    # Read the report content
    report_content = read_report_file(report_file)
    post_github_check(test_results, report_content)


def find_output_files(main_dir):
    """Find all output.xml files in subdirectories."""
    output_files = []
    for root, _, files in os.walk(main_dir):
        if 'output.xml' in files:
            output_files.append(os.path.join(root, 'output.xml'))
    return output_files


def validate_output_file(output_file):
    """Return True if the output file exists, otherwise print an error and return False."""
    exists = os.path.isfile(output_file)
    if not exists:
        print(f"❌ Error: The output file '{output_file}' does not exist.")
    return exists


def process_test_results(output_file: str, report_file: str) -> dict:
    """Processes Robot Framework test results and returns structured data."""
    result = ExecutionResult(output_file)
    visitor = MyResultVisitor(markdown_file=report_file)
    result.visit(visitor)

    total_tests = len(visitor.passed_tests) + len(visitor.failed_tests)
    passed_tests = len(visitor.passed_tests)
    failed_tests = len(visitor.failed_tests)

    generated_timestamp_str = getattr(result.suite, "starttime", None)
    if generated_timestamp_str is None:
        raise AttributeError("ExecutionResult.suite has no attribute 'starttime'. "
                             "Check the correct attribute name in the Robot Framework API.")

    generated_timestamp = datetime.strptime(generated_timestamp_str, "%Y%m%d %H:%M:%S.%f").timestamp()
    duration = round(time.time() - generated_timestamp, 2)

    return {
        "total": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "duration": duration
    }


def read_report_file(report_file: str) -> str:
    """Reads and returns the content of the report.md file."""
    if os.path.isfile(report_file):
        with open(report_file, "r", encoding="utf-8") as file:
            return file.read()
    return "No report file found."


if __name__ == "__main__":
    run_robot_tests()


# import os
# import requests
# import time
# from datetime import datetime
# from robot.api import ExecutionResult
# from display_test_results import MyResultVisitor


# def get_env_variable(name):
#     """Retrieve an environment variable and return None if not set."""
#     value = os.getenv(name)
#     if not value:
#         print(f"Warning: Missing environment variable {name}")
#     return value


# def post_github_check(results, report_content):
#     """Post test results as a GitHub check run."""
#     github_token = get_env_variable("GITHUB_TOKEN")
#     repository = get_env_variable("GITHUB_REPOSITORY")
#     commit_sha = get_env_variable("GITHUB_SHA")
#     job_name = os.getenv("GITHUB_JOB", "Unknown Job")
#     caller_job_name = get_env_variable("JOB_NAME")

#     if caller_job_name:
#         job_name = caller_job_name  # Override with actual job name

#     if not all([github_token, repository, commit_sha]):
#         print("Error: Missing required environment variables. Exiting...")
#         return

#     api_url = f"https://api.github.com/repos/{repository}/check-runs"
#     headers = {
#         "Accept": "application/vnd.github.v3+json",
#         "Authorization": f"Bearer {github_token}",
#         "Content-Type": "application/json"
#     }

#     total_tests = results.get("total", 0)
#     passed_tests = results.get("passed", 0)
#     failed_tests = results.get("failed", 0)
#     duration = results.get("duration", 0)
#     minutes, seconds = divmod(duration, 60)


#     conclusion = "success" if failed_tests == 0 else "failure"

#     summary = (f"{report_content}")

#     payload_name = f"Test Results - {job_name}"

#     payload = {
#         "name": payload_name.title(),
#         "head_sha": commit_sha,
#         "status": "completed",
#         "conclusion": conclusion,
#         "output": {
#             "title": f"Test Results - {job_name} executed in {int(minutes)}m {int(seconds)}s",
#             "summary": summary
#         }
#     }

#     response = requests.post(api_url, headers=headers, json=payload)

#     if response.status_code == 201:
#         print("✅ GitHub check posted successfully")
#     else:
#         print(f"❌ Failed to post GitHub check: {response.status_code} - {response.text}")


# def run_robot_tests():
#     """Run Robot Framework tests, parse results, and post them to GitHub."""
#     print(f"Current Working Directory: {os.getcwd()}")
#     output_file = os.path.abspath('./webapp_tests/robot-test-results/output.xml')
#     report_file = os.path.abspath('./webapp_tests/robot-test-results/report.md')

#     if not validate_output_file(output_file):
#         return

#     test_results = process_test_results(output_file, report_file)

#     report_content = read_report_file(report_file)
#     post_github_check(test_results, report_content)


# def validate_output_file(output_file):
#     """Return True if the output file exists, otherwise print an error and return False."""
#     exists = os.path.isfile(output_file)
#     if not exists:
#         print(f"❌ Error: The output file '{output_file}' does not exist.")
#     return exists


# def process_test_results(output_file: str, report_file: str) -> dict:
#     """Processes Robot Framework test results and returns structured data."""

#     result = ExecutionResult(output_file)
#     visitor = MyResultVisitor(markdown_file=report_file)
#     result.visit(visitor)

#     total_tests = len(visitor.passed_tests) + len(visitor.failed_tests)
#     passed_tests = len(visitor.passed_tests)
#     failed_tests = len(visitor.failed_tests)

#     generated_timestamp_str = getattr(result.suite, "starttime", None)
#     if generated_timestamp_str is None:
#         raise AttributeError("ExecutionResult.suite has no attribute 'starttime'. "
#                              "Check the correct attribute name in the Robot Framework API.")

#     generated_timestamp = datetime.strptime(generated_timestamp_str, "%Y%m%d %H:%M:%S.%f").timestamp()
#     duration = round(time.time() - generated_timestamp, 2)

#     return {
#         "total": total_tests,
#         "passed": passed_tests,
#         "failed": failed_tests,
#         "duration": duration
#     }


# def read_report_file(report_file: str) -> str:
#     """Reads and returns the content of the report.md file."""
#     if os.path.isfile(report_file):
#         with open(report_file, "r", encoding="utf-8") as file:
#             return file.read()
#     return "No report file found."


# if __name__ == "__main__":
#     run_robot_tests()
