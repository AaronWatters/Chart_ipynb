
Unit tests for Python code.

These tests mainly exercise the code paths.
To test the underlying functionality, use the end_to_end_tests.

To run the tests in the parent directory:

$ nosetests --with-coverage --cover-html-dir=coverage --cover-xml --cover-package=chart_ipynb --cover-html

To view the HTML report from the parent directory:

$ open coverage/index.html

TO DO:
------

Add test files for all modules of the package.

Try to get test coverage close to 100%.

Set up with Travis continuous integration.

Set up with codecov

Add convenience functions for simple chart cases, similar to

[1] pie_chart(title="People", data={"men": 10, "women": 12, "boys": 3, "girls":7})

The above should create a bar chart with default size and color choices, etcetera.

Make a convenience function like this for each of the chart types.

Add at least one end to end test.
