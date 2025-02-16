def end_result(self, result):
    total_tests = len(self.passed_tests) + len(self.failed_tests)
    passed_count = len(self.passed_tests)
    failed_count = len(self.failed_tests)
    
    # Create a new markdown file
    with open(self.markdown_file, "w") as f:
        f.write("# 🏆 Test Results Summary\n\n")  # Double newline
        f.write("## 📊 Summary\n\n")
        f.write(f"- **Total Tests:** `{total_tests}`  \n")  # Single space `  \n` for line break
        f.write(f"- ✅ **Passed:** `{passed_count}`  \n")
        f.write(f"- ❌ **Failed:** `{failed_count}`  \n\n")

        # Adding Markdown Table
        f.write("| **Test Name** | **Status** |\n")
        f.write("|--------------|-----------|\n")
        for test in self.passed_tests:
            f.write(f"| `{test}` | ✅ **PASS** |\n")
        for test in self.failed_tests:
            f.write(f"| `{test}` | ❌ **FAIL** |\n")

    print(f"📄 Report generated: {self.markdown_file}")

    # Ensure GitHub renders properly
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "w") as gh_summary:
            gh_summary.write("\n")  # Start with a newline to ensure proper rendering
            with open(self.markdown_file, "r") as report:
                gh_summary.write(report.read())
                gh_summary.write("\n")  # End with a newline
