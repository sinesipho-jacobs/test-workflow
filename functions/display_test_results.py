from robot.api import ExecutionResult, ResultVisitor
import os
import glob

class MyResultVisitor(ResultVisitor):
    def __init__(self, markdown_file='report.md'):
        self.failed_tests = []
        self.passed_tests = []
        self.markdown_file = markdown_file
        self.current_file = ""

    def visit_test(self, test):
        file_name = os.path.basename(self.current_file)

        test_info = {
            "name": test.name,
            "file": file_name,
            "status": test.status,
            "message": test.message if test.status == 'FAIL' else "N/A",
            "lineno": test.lineno if test.lineno else "Unknown"
        }

        if test.status == 'FAIL':
            self.failed_tests.append(test_info)
        elif test.status == 'PASS':
            self.passed_tests.append(test_info)

    def process_file(self, xml_file):
        """ Process each XML file separately and store results. """
        self.current_file = xml_file  # Track the current file being processed
        result = ExecutionResult(xml_file)
        result.visit(self)
        return os.path.basename(xml_file)  # Return file name for reporting

    def generate_report(self, processed_files):
        """ Generate a Markdown report with separate tables for each file. """
        with open(self.markdown_file, "w") as f:
            f.write("# 🏆 Test Results Summary\n\n")

            for file in processed_files:
                tests_in_file = [t for t in self.passed_tests + self.failed_tests if t["file"] == file]
                total_tests = len(tests_in_file)
                passed_count = sum(1 for t in self.passed_tests if t["file"] == file)
                failed_count = sum(1 for t in self.failed_tests if t["file"] == file)

                f.write(f"## 📄 Test Results for `{file}`\n")
                f.write(f"- **Total Tests:** {total_tests}\n")
                f.write(f"- ✅ **Passed:** {passed_count}\n")
                f.write(f"- ❌ **Failed:** {failed_count}\n\n")

                if total_tests > 0:
                    f.write("| Test Name | Status | Message |\n")
                    f.write("|-----------|--------|---------|\n")

                    for test in self.passed_tests:
                        if test["file"] == file:
                            f.write(f"| {test['name']} | {test['file']} | ✅ PASS | |\n")

                    for test in self.failed_tests:
                        if test["file"] == file:
                            f.write(f"| {test['name']} | {test['file']} | ❌ FAIL | {test['message']} |\n")

                f.write("\n---\n")  # Add a separator between test files

        print(f"📄 Report generated: {self.markdown_file}")

if __name__ == '__main__':
    result_dir = "webapp_tests/robot-test-results"
    xml_files = glob.glob(os.path.join(result_dir, "*.xml"))  # Get all XML files

    if not xml_files:
        print("❌ Error: No XML test result files found.")
        exit(1)

    visitor = MyResultVisitor(markdown_file="report.md")
    processed_files = [visitor.process_file(xml_file) for xml_file in xml_files]

    visitor.generate_report(processed_files)
