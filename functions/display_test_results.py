from robot.api import ExecutionResult, ResultVisitor
import sys

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
        with open(self.markdown_file, "w") as f:
            f.write("## 📝 Robot Framework Test Report\n")
            f.write("| Test | Status |\n")
            f.write("|------|--------|\n")
            for test in self.passed_tests:
                f.write(f"| {test} | ✅ PASS |\n")
            for test in self.failed_tests:
                f.write(f"| {test} | ❌ FAIL |\n")

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else "output.xml"
    markdown_file = sys.argv[2] if len(sys.argv) > 2 else "report.md"
    
    result = ExecutionResult(output_file)
    result.visit(MyResultVisitor(markdown_file))
