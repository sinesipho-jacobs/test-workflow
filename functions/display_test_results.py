from robot.api import ExecutionResult, ResultVisitor
import sys
import os

class MyResultVisitor(ResultVisitor):
    def __init__(self, markdown_file='report.md'):
        self.failed_tests = []
        self.passed_tests = []
        self.markdown_file = markdown_file

    def visit_test(self, test):
        test_info = {
            "name": test.name,
            "suite": test.parent.name,  # Get suite name
            "status": "✅ PASS" if test.status == 'PASS' else "❌ FAIL",
            "message": test.message if test.status == 'FAIL' else "N/A",
            "lineno": test.lineno if test.lineno else "Unknown"
        }

        if test.status == 'FAIL':
            self.failed_tests.append(test_info)
        elif test.status == 'PASS':
            self.passed_tests.append(test_info)

    def end_result(self, result):
        total_tests = len(self.passed_tests) + len(self.failed_tests)
        passed_count = len(self.passed_tests)
        failed_count = len(self.failed_tests)
        
        with open(self.markdown_file, "w") as f:
            f.write("# 🏆 Test Results Summary\n\n")
            f.write("## 📊 Summary\n")
            f.write(f"- **Total Tests:** {total_tests}\n")
            f.write(f"- ✅ **Passed:** {passed_count}\n")
            f.write(f"- ❌ **Failed:** {failed_count}\n\n")

            if passed_count > 0:
                f.write("## ✅ Passed Tests\n")
                f.write("| Test Name | Suite | Status |\n")
                f.write("|-----------|--------|--------|\n")
                for test in self.passed_tests:
                    f.write(f"| {test['name']} | {test['suite']} | {test['status']} |\n")
                f.write("\n")

            if failed_count > 0:
                f.write("## ❌ Failed Tests\n")
                f.write("| Test Name | Suite | Status | Failure Message | Line No. |\n")
                f.write("|-----------|--------|--------|----------------|---------|\n")
                for test in self.failed_tests:
                    f.write(f"| {test['name']} | {test['suite']} | {test['status']} | {test['message']} | {test['lineno']} |\n")
                f.write("\n")

        print(f"📄 Report generated: {self.markdown_file}")

if __name__ == '__main__':
    try:
        output_file = sys.argv[1]
    except IndexError:
        output_file = "webapp_tests/robot-test-results/output.xml"

    try:
        markdown_file = sys.argv[2]
    except IndexError:
        markdown_file = "report.md"

    if not os.path.isfile(output_file):
        print(f"❌ Error: The output file '{output_file}' does not exist.")
        sys.exit(1)

    result = ExecutionResult(output_file)
    result.visit(MyResultVisitor(markdown_file=markdown_file))
