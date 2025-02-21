from robot.api import ExecutionResult, ResultVisitor
import sys
import os


class MyResultVisitor(ResultVisitor):
    def __init__(self, markdown_file='webapp_tests/robot-test-results/report.md', test_type=None):
        self.failed_tests = []
        self.passed_tests = []
        self.total_duration_ms = 0
        self.markdown_file = markdown_file
        self.test_type = test_type.lower()

        self.grouped_tests = {f"{self.test_type.capitalize()} Tests": {"passed": [], "failed": []}}
        self.test_counts = {f"{self.test_type.capitalize()} Tests": {"total": 0, "passed": 0, "failed": 0}}

        self._ensure_directory_exists()
        self._load_existing_report()
        
    def _ensure_directory_exists(self):
        directory = os.path.dirname(self.markdown_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _load_existing_report(self):
        """Load existing test results if the markdown file exists."""
        if os.path.exists(self.markdown_file):
            with open(self.markdown_file, "r") as f:
                self.existing_content = f.read()
        else:
            self.existing_content = ""

    def visit_test(self, test):
        file_name = os.path.basename(test.source) if test.source else "Unknown File"
        
        # Extract test duration in milliseconds
        test_duration_ms = test.elapsedtime  # duration in ms
        
        # Add to total duration
        self.total_duration_ms += test_duration_ms

        test_info = {
            "name": test.name,
            "file": file_name,
            "status": test.status,
            "message": test.message if test.status == 'FAIL' else "N/A",
            "duration": test_duration_ms
        }
        
        category = f"{self.test_type.capitalize()} Tests"

        # Update the grouped tests and counts
        if test.status == 'FAIL':
            self.grouped_tests[category]["failed"].append(test_info)
            self.test_counts[category]["failed"] += 1
        else:
            self.grouped_tests[category]["passed"].append(test_info)
            self.test_counts[category]["passed"] += 1
        
        self.test_counts[category]["total"] += 1

    def end_result(self, result):
        """Generate the Markdown report, preserving existing results."""
        new_content = ""
        if not self.existing_content:
            new_content += "# 📝 Test Results Summary\n\n"

        for category, tests in self.grouped_tests.items():
            total = self.test_counts[category]["total"]
            passed = self.test_counts[category]["passed"]
            failed = self.test_counts[category]["failed"]
            # duration_str = self._format_duration(self.test_counts[category]["duration_ms"])

            # 📊 Stats for each category
            new_content += f"## {category}\n\n"
            new_content += f"- 📊 **Total Tests ({category}):** {total}\n"
            new_content += f"- ✅ **Passed:** {passed}\n"
            new_content += f"- ❌ **Failed:** {failed}\n"
            # new_content += f"- ⏱️ **Total Duration:** {duration_str}\n\n"

            # 📝 Test Results Table
            new_content += "| Test Name | File | Status | Message |\n"
            new_content += "|-----------|------|--------|---------|\n"
            for test in tests:
                new_content += f"| {test['name']} | {test['file']} | {test['status']} | {test['message']} |\n"

            new_content += "\n"

        # Append new content to existing content
        with open(self.markdown_file, "w") as f:
            f.write(self.existing_content + new_content)

        print(f"📄 Report updated: {self.markdown_file}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("❌ Error: Missing arguments. Usage: python generate_report.py <output.xml> <test_type>")
        sys.exit(1)

    output_file = sys.argv[1]  # e.g., test-results/output.xml
    test_type = sys.argv[2].lower()  # 'api', 'web', or 'all'

    markdown_file = "webapp_tests/robot-test-results/report.md"

    if not os.path.isfile(output_file):
        print(f"❌ Error: The output file '{output_file}' does not exist.")
        sys.exit(1)

    result = ExecutionResult(output_file)
    result.visit(MyResultVisitor(markdown_file=markdown_file, test_type=test_type))





# from robot.api import ExecutionResult, ResultVisitor
# import sys
# import os

# class MyResultVisitor(ResultVisitor):
#     def __init__(self, markdown_file='report.md'):
#         self.failed_tests = []
#         self.passed_tests = []
#         self.markdown_file = markdown_file

#     def visit_test(self, test):
#         file_name = os.path.basename(test.source) if test.source else "Unknown File"  # Extract file name

#         test_info = {
#             "name": test.name,
#             "file": file_name,  # Use file name instead of suite
#             "status": test.status,
#             "message": test.message if test.status == 'FAIL' else "N/A",
#             "lineno": test.lineno if test.lineno else "Unknown"
#         }

#         if test.status == 'FAIL':
#             self.failed_tests.append(test_info)
#         elif test.status == 'PASS':
#             self.passed_tests.append(test_info)

#     def end_result(self, result):
#         total_tests = len(self.passed_tests) + len(self.failed_tests)
#         passed_count = len(self.passed_tests)
#         failed_count = len(self.failed_tests)
        
#         with open(self.markdown_file, "w") as f:
#             f.write("# 🏆 Test Results Summary\n\n")
#             f.write("## 📊 Summary\n")
#             f.write(f"- **Total Tests:** {total_tests}\n")
#             f.write(f"- ✅ **Passed:** {passed_count}\n")
#             f.write(f"- ❌ **Failed:** {failed_count}\n\n")

#             if passed_count > 0:
#                 f.write("## ✅ Passed Tests\n")
#                 f.write("| Test Name | File | Status |\n")
#                 f.write("|-----------|--------|--------|\n")
#                 for test in self.passed_tests:
#                     f.write(f"| {test['name']} | {test['file']} | ✅ PASS |\n")

#             if failed_count > 0:
#                 f.write("\n## ❌ Failed Tests\n")
#                 f.write("| Test Name | File | Failure Message | Line No. |\n")
#                 f.write("|-----------|--------|----------------|---------|\n")
#                 for test in self.failed_tests:
#                     f.write(f"| {test['name']} | {test['file']} | {test['message']} | {test['lineno']} |\n")

#         print(f"📄 Report generated: {self.markdown_file}")

# if __name__ == '__main__':
#     try:
#         output_file = sys.argv[1]
#     except IndexError:
#         output_file = "webapp_tests/robot-test-results/output.xml"  # Default location

#     try:
#         markdown_file = sys.argv[2]
#     except IndexError:
#         markdown_file = "report.md"  # Default markdown file name

#     if not os.path.isfile(output_file):
#         print(f"❌ Error: The output file '{output_file}' does not exist.")
#         sys.exit(1)

#     result = ExecutionResult(output_file)
#     result.visit(MyResultVisitor(markdown_file=markdown_file))
