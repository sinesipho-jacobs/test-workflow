from robot.api import ExecutionResult, ResultVisitor
import sys
import os

class MyResultVisitor(ResultVisitor):
    def __init__(self, markdown_file='report.md'):
        self.failed_tests = []
        self.passed_tests = []
        self.markdown_file = markdown_file

    def visit_test(self, test):
        if test.status == 'FAIL':
            self.failed_tests.append(test.name)
        elif test.status == 'PASS':
            self.passed_tests.append(test.name)

    def end_result(self, result):
        # Create or append to the markdown file
        with open(self.markdown_file, "w") as f:
            f.write("# 🏆 Robot Framework Report\n\n")
            f.write("## 📊 Summary\n")
            f.write(f"- **Total Tests:** {len(self.passed_tests) + len(self.failed_tests)}\n")
            f.write(f"- ✅ **Passed:** {len(self.passed_tests)}\n")
            f.write(f"- ❌ **Failed:** {len(self.failed_tests)}\n\n")
            
            f.write("| Test Name | Status |\n")
            f.write("| --------- | ------ |\n")
            for test in self.passed_tests:
                f.write(f"| {test} | ✅ PASS |\n")
            for test in self.failed_tests:
                f.write(f"| {test} | ❌ FAIL |\n")

if __name__ == '__main__':
    try:
        output_file = sys.argv[1]
    except IndexError:
        output_file = "webapp_tests/robot-test-results/output.xml"  # Default location inside webapp_tests
    try:
        markdown_file = sys.argv[2]
    except IndexError:
        markdown_file = "report.md"  # Default markdown file name

    # Check if the output file exists
    if not os.path.isfile(output_file):
        print(f"❌ Error: The output file '{output_file}' does not exist.")
        sys.exit(1)

    result = ExecutionResult(output_file)
    result.visit(MyResultVisitor(markdown_file=markdown_file))
