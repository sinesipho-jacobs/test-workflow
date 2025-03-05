from robot.api import ExecutionResult, ResultVisitor
import sys
import os
import glob
import xml.etree.ElementTree as ET


class MyResultVisitor(ResultVisitor):
    def __init__(self, markdown_file='./webapp_tests/robot-test-results/report.md', xml_file='./webapp_tests/robot-test-results/output.xml'):
        self.failed_tests = []
        self.passed_tests = []
        self.markdown_file = markdown_file
        self.xml_file = xml_file

        self._ensure_directory_exists()
        
    def _ensure_directory_exists(self):
        directory = os.path.dirname(self.markdown_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def visit_test(self, test):
        file_name = os.path.basename(test.source) if test.source else "Unknown File"

        test_info = {
            "name": test.name,
            "file": file_name,
            "status": test.status,
            "message": test.message if test.status == 'FAIL' else "N/A",
        }

        if test.status == 'FAIL':
            self.failed_tests.append(test_info)
        elif test.status == 'PASS':
            self.passed_tests.append(test_info)

    def write_report(self):
        total_tests = len(self.passed_tests) + len(self.failed_tests)
        passed_count = len(self.passed_tests)
        failed_count = len(self.failed_tests)

        # Writing Markdown Report
        with open(self.markdown_file, "w") as f:
            f.write("### Test Results Summary\n\n")
            f.write(f"- 📊 **Total Tests:** {total_tests}\n")
            f.write(f"- ✅ **Passed:** {passed_count}\n")
            f.write(f"- ❌ **Failed:** {failed_count}\n\n")

            if total_tests > 0:
                f.write("| Test Name | File | Status | Message |\n")
                f.write("|-----------|------|--------|---------|\n")
                
                for test in self.passed_tests:
                    f.write(f"| {test['name']} | {test['file']} | ✅ PASS | |\n")

                for test in self.failed_tests:
                    f.write(f"| {test['name']} | {test['file']} | ❌ FAIL | {test['message']} |\n")

        print(f"📄 Report generated: {self.markdown_file}")
        
        # Writing XML Output
        root = ET.Element("testResults")
        for test in self.passed_tests + self.failed_tests:
            test_element = ET.SubElement(root, "test")
            test_element.set("name", test["name"])
            test_element.set("file", test["file"])
            test_element.set("status", test["status"])
            if test["status"] == "FAIL":
                ET.SubElement(test_element, "message").text = test["message"]
        
        tree = ET.ElementTree(root)
        tree.write(self.xml_file)

        print(f"📄 XML Output generated: {self.xml_file}")


if __name__ == '__main__':
    # Set base directory where output.xml files are expected
    base_dir = "./webapp_tests/robot-test-results"
    markdown_file = os.path.join(base_dir, "report.md")
    xml_output_file = os.path.join(base_dir, "output.xml")

    # Find all output.xml files in subdirectories
    xml_files = glob.glob(f"{base_dir}/**/output.xml", recursive=True)

    if not xml_files:
        print(f"❌ Error: No 'output.xml' files found in {base_dir}.")
        sys.exit(1)

    visitor = MyResultVisitor(markdown_file=markdown_file, xml_file=xml_output_file)

    for xml_file in xml_files:
        print(f"📂 Processing: {xml_file}")
        result = ExecutionResult(xml_file)
        result.visit(visitor)

    visitor.write_report()


# from robot.api import ExecutionResult, ResultVisitor
# import sys
# import os
# import glob


# class MyResultVisitor(ResultVisitor):
#     def __init__(self, markdown_file='./webapp_tests/robot-test-results/report.md'):
#         self.failed_tests = []
#         self.passed_tests = []
#         self.markdown_file = markdown_file

#         self._ensure_directory_exists()
        
#     def _ensure_directory_exists(self):
#         directory = os.path.dirname(self.markdown_file)
#         if directory and not os.path.exists(directory):
#             os.makedirs(directory)

#     def visit_test(self, test):
#         file_name = os.path.basename(test.source) if test.source else "Unknown File"

#         test_info = {
#             "name": test.name,
#             "file": file_name,
#             "status": test.status,
#             "message": test.message if test.status == 'FAIL' else "N/A",
#         }

#         if test.status == 'FAIL':
#             self.failed_tests.append(test_info)
#         elif test.status == 'PASS':
#             self.passed_tests.append(test_info)

#     def write_report(self):
#         total_tests = len(self.passed_tests) + len(self.failed_tests)
#         passed_count = len(self.passed_tests)
#         failed_count = len(self.failed_tests)

#         with open(self.markdown_file, "w") as f:
#             f.write("### Test Results Summary\n\n")
#             f.write(f"- 📊 **Total Tests:** {total_tests}\n")
#             f.write(f"- ✅ **Passed:** {passed_count}\n")
#             f.write(f"- ❌ **Failed:** {failed_count}\n\n")

#             if total_tests > 0:
#                 f.write("| Test Name | File | Status | Message |\n")
#                 f.write("|-----------|------|--------|---------|\n")
                
#                 for test in self.passed_tests:
#                     f.write(f"| {test['name']} | {test['file']} | ✅ PASS | |\n")

#                 for test in self.failed_tests:
#                     f.write(f"| {test['name']} | {test['file']} | ❌ FAIL | {test['message']} |\n")

#         print(f"📄 Report generated: {self.markdown_file}")


# if __name__ == '__main__':
#     # Set base directory where output.xml files are expected
#     base_dir = "./webapp_tests/robot-test-results"
#     markdown_file = os.path.join(base_dir, "report.md")

#     # Find all output.xml files in subdirectories
#     xml_files = glob.glob(f"{base_dir}/**/output.xml", recursive=True)

#     if not xml_files:
#         print(f"❌ Error: No 'output.xml' files found in {base_dir}.")
#         sys.exit(1)

#     visitor = MyResultVisitor(markdown_file=markdown_file)

#     for xml_file in xml_files:
#         print(f"📂 Processing: {xml_file}")
#         result = ExecutionResult(xml_file)
#         result.visit(visitor)

#     visitor.write_report()


# from robot.api import ExecutionResult, ResultVisitor
# import os
# import glob

# class MyResultVisitor(ResultVisitor):
#     def __init__(self, markdown_file='report.md'):
#         self.failed_tests = []
#         self.passed_tests = []
#         self.markdown_file = markdown_file
#         self.current_file = ""

#     def visit_test(self, test):
#         file_name = os.path.basename(self.current_file)

#         test_info = {
#             "name": test.name,
#             "file": file_name,
#             "status": test.status,
#             "message": test.message if test.status == 'FAIL' else "N/A",
#             "lineno": test.lineno if test.lineno else "Unknown"
#         }

#         if test.status == 'FAIL':
#             self.failed_tests.append(test_info)
#         elif test.status == 'PASS':
#             self.passed_tests.append(test_info)

#     def process_file(self, xml_file):
#         """ Process each XML file separately and store results. """
#         self.current_file = xml_file  # Track the current file being processed
#         result = ExecutionResult(xml_file)
#         result.visit(self)
#         return os.path.basename(xml_file)  # Return file name for reporting

#     def generate_report(self, processed_files):
#         """ Generate a Markdown report with separate tables for each file. """
#         with open(self.markdown_file, "w") as f:
#             f.write("# 🏆 Test Results Summary\n\n")

#             for file in processed_files:
#                 tests_in_file = [t for t in self.passed_tests + self.failed_tests if t["file"] == file]
#                 total_tests = len(tests_in_file)
#                 passed_count = sum(1 for t in self.passed_tests if t["file"] == file)
#                 failed_count = sum(1 for t in self.failed_tests if t["file"] == file)

#                 f.write(f"## 📄 Test Results for `{file}`\n")
#                 f.write(f"- **Total Tests:** {total_tests}\n")
#                 f.write(f"- ✅ **Passed:** {passed_count}\n")
#                 f.write(f"- ❌ **Failed:** {failed_count}\n\n")

#                 if total_tests > 0:
#                     f.write("| Test Name | Status | Message |\n")
#                     f.write("|-----------|--------|---------|\n")

#                     for test in self.passed_tests:
#                         if test["file"] == file:
#                             f.write(f"| {test['name']} | {test['file']} | ✅ PASS | |\n")

#                     for test in self.failed_tests:
#                         if test["file"] == file:
#                             f.write(f"| {test['name']} | {test['file']} | ❌ FAIL | {test['message']} |\n")

#                 f.write("\n---\n")  # Add a separator between test files

#         print(f"📄 Report generated: {self.markdown_file}")

# if __name__ == '__main__':
#     result_dir = "webapp_tests/robot-test-results"
#     xml_files = glob.glob(os.path.join(result_dir, "*.xml"))  # Get all XML files

#     if not xml_files:
#         print("❌ Error: No XML test result files found.")
#         exit(1)

#     visitor = MyResultVisitor(markdown_file="report.md")
#     processed_files = [visitor.process_file(xml_file) for xml_file in xml_files]

#     visitor.generate_report(processed_files)
