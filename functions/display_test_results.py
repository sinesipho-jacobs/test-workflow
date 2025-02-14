
import os
import sys
from robot.api import ExecutionResult, ResultVisitor

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
        total_tests = len(self.passed_tests) + len(self.failed_tests)
        passed_count = len(self.passed_tests)
        failed_count = len(self.failed_tests)

        report_path = os.path.join(os.getcwd(), self.markdown_file)

        with open(report_path, "w") as f:
            f.write(f"# 🏆 Robot Framework Report\n\n")
            f.write(f"## 📊 Summary\n")
            f.write(f"- **Total Tests:** {total_tests}\n")
            f.write(f"- ✅ **Passed:** {passed_count}\n")
            f.write(f"- ❌ **Failed:** {failed_count}\n\n")

            f.write("| Test Name | Status |\n")
            f.write("|-----------|--------|\n")
            for test in self.passed_tests:
                f.write(f"| {test} | ✅ PASS |\n")
            for test in self.failed_tests:
                f.write(f"| {test} | ❌ FAIL |\n")

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else "output.xml"
    markdown_file = sys.argv[2] if len(sys.argv) > 2 else "report.md"
    
    result = ExecutionResult(output_file)
    result.visit(MyResultVisitor(markdown_file))
