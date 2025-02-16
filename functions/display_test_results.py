def end_result(self, result):
    total_tests = len(self.passed_tests) + len(self.failed_tests)
    passed_count = len(self.passed_tests)
    failed_count = len(self.failed_tests)
    
    # Create a new markdown file
    with open(self.markdown_file, "w") as f:
        f.write("# 🏆 Test Results Summary\n\n")  # Add extra newlines
        f.write("## 📊 Summary\n\n")  # Extra newline here
        f.write(f"- **Total Tests:** {total_tests}\n")
        f.write(f"- ✅ **Passed:** {passed_count}\n")
        f.write(f"- ❌ **Failed:** {failed_count}\n\n")
        
        f.write("| Test Name | Status |\n")
        f.write("|-----------|--------|\n")
        for test in self.passed_tests:
            f.write(f"| {test} | ✅ PASS |\n")
        for test in self.failed_tests:
            f.write(f"| {test} | ❌ FAIL |\n")

    print(f"📄 Report generated: {self.markdown_file}")

    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "w") as gh_summary:
            with open(self.markdown_file, "r") as report:
                gh_summary.write(report.read())
