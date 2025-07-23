Todoist Automation Test Suite
Overview
This Python script automates testing of the Todoist web application using Selenium WebDriver. It performs functional, UI, and boundary testing of core features including login, task creation, editing, completion, deletion, and input validation.

Features Tested
User login functionality
Task creation
Task editing
Task completion (marking as done)
Task deletion
Boundary testing (long task input validation)
=======================================================
Prerequisites
Python 3.7+
Chrome browser installed
ChromeDriver (matching your Chrome version)
Required Python packages (install via pip install -r requirements.txt)
==================================================================
Installation
Clone this repository
Install dependencies:
bash Copy
pip install selenium webdriver-manager
Configuration
Ensure ChromeDriver is in your PATH or update the path in the script:
python Copy
chromedriver_path = r"I:\Souryyyy_work\test\chromedriver.exe"  # Update this path
Running the Tests
Execute the script:

bash Copy
python todoist_automation.py
==========================================================================
You'll be prompted for:

Your Todoist email
Your Todoist password
Whether to run in headless mode (y/n)
Test Execution Flow
Launches Chrome browser (headless or normal)
Logs into Todoist
Creates a test task with timestamp
Edits the created task
Marks the task as complete
Deletes the task
Tests long input validation
Generates logs of all actions
Logging
The script logs all actions with timestamps to the console. Logs include:

Successful operations
Warnings for non-critical failures
Errors for critical failures
=============================================================================
Assumptions
Todoist UI structure remains relatively stable (selectors may need updates if UI changes)
User has a valid Todoist account
ChromeDriver version matches installed Chrome browser version
Internet connection is available during test execution
==================================================================
Customization Options
Change timeout durations by modifying WebDriverWait value
Adjust headless mode default by changing headless=False parameter
Add additional test cases by extending the run_full_test_suite method
Known Limitations
Tests may fail if Todoist UI changes significantly
Running in headless mode may behave slightly differently than normal mode
Requires manual entry of credentials (not recommended for CI/CD pipelines)
Troubleshooting
If tests fail:

Verify ChromeDriver version matches Chrome browser version
Check internet connection
Inspect console logs for specific error messages
Try running in non-headless mode to observe behavior
For security reasons, the script does not store credentials and requires manual entry for each run.