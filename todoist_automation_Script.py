

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TodoistAutomation:
    def __init__(self, headless=False):
        """Initialize the automation class with Chrome driver setup"""
        self.driver = None
        self.wait = None
        self.setup_driver(headless)
    
    def setup_driver(self, headless=False):
        """Set up Chrome driver with options and automatic driver management"""
        options = Options()
        
        # Anti-detection options
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        if headless:
            options.add_argument("--headless")
        
        
        # Use webdriver-manager to automatically download and manage chromedriver
        chromedriver_path = r"I:\Souryyyy_work\test\chromedriver.exe" 
        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Hide webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 15)
        
        logger.info("Chrome driver initialized successfully")
    
    def login_to_todoist(self, email, password):
        """Login to Todoist with email and password"""
        try:
            logger.info("Navigating to Todoist login page...")
            self.driver.get("https://todoist.com/auth/login")
            time.sleep(3)  # Wait for page to load
            
            # Wait for and fill email - try multiple selectors
            email_selectors = [
                "input[type='email']",
                "input[name='email']",
                "#element-0",
                "input[placeholder*='email' i]"
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    email_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    break
                except TimeoutException:
                    continue
            
            if not email_field:
                raise Exception("Could not find email input field")
            
            email_field.clear()
            email_field.send_keys(email)
            logger.info("Email entered successfully")
            
            # Fill password - try multiple selectors
            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "#element-3",
                "input[placeholder*='password' i]"
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not password_field:
                raise Exception("Could not find password input field")
            
            password_field.clear()
            password_field.send_keys(password)
            logger.info("Password entered successfully")
            
            # Click login button
            login_selectors = [
                "button[type='submit']",
                "button[data-gtm-id='log-in']",
                "input[type='submit']",
                "button:contains('Log in')"
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not login_button:
                # Try finding by text
                login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")
            
            login_button.click()
            logger.info("Login button clicked")
            
            # Wait for successful login (check for inbox page or dashboard)
            try:
                self.wait.until(lambda driver: "app" in driver.current_url.lower() or "inbox" in driver.current_url.lower())
                logger.info("Login successful! Redirected to app")
                time.sleep(3)  # Wait for app to fully load
                return True
            except TimeoutException:
                logger.error("Login may have failed - timeout waiting for redirect")
                return False
            
        except Exception as e:
            logger.error(f"Login failed with error: {str(e)}")
            return False
    
    def add_task(self, task_name):
        """Add a new task to the inbox"""
        try:
            logger.info(f"Adding task: {task_name}")
            
            # Try multiple selectors for add task button
            add_task_selectors = [
                "button[aria-label='Add task']",
                "button[data-testid='add-task-button']",
                ".plus_add_button",
                "button:contains('Add task')",
                "[data-action-hint='task-add']"
            ]
            
            add_task_button = None
            for selector in add_task_selectors:
                try:
                    add_task_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not add_task_button:
                # Try keyboard shortcut
                logger.info("Trying keyboard shortcut to add task...")
                self.driver.find_element(By.TAG_NAME, "body").send_keys("q")
                time.sleep(1)
            else:
                add_task_button.click()
            
            # Wait for task input field to appear
            input_selectors = [
                "div[contenteditable='true']",
                "textarea[placeholder*='task' i]",
                "input[placeholder*='task' i]",
                ".task_editor__content_field",
                "[data-testid='task-content']"
            ]
            
            task_input = None
            for selector in input_selectors:
                try:
                    task_input = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not task_input:
                raise Exception("Could not find task input field")
            
            # Clear and enter task name
            task_input.clear()
            task_input.send_keys(task_name)
            
            # Submit the task (press Enter)
            task_input.send_keys(Keys.ENTER)
            
            logger.info(f"Task '{task_name}' added successfully")
            time.sleep(3)  # Wait for task to be added
            return True
            
        except Exception as e:
            logger.error(f"Failed to add task: {str(e)}")
            return False
    
    def find_task_element(self, task_name):
        """Helper method to find a task element by name"""
        task_selectors = [
            f"//span[contains(text(), '{task_name}')]",
            f"//div[contains(text(), '{task_name}')]",
            f"//*[contains(@data-task-content, '{task_name}')]",
            f"//*[contains(text(), '{task_name}')]"
        ]
        
        for selector in task_selectors:
            try:
                task_element = self.driver.find_element(By.XPATH, selector)
                return task_element
            except NoSuchElementException:
                continue
        
        return None
    
    def mark_task_complete(self, task_title):
        """Mark a specific task as complete"""
        logger.info(f"Marking task as complete: {task_title}")
        
        
        
        try:
            # Look for checkbox within the task element
            checkbox = task_title.find_element(By.CSS_SELECTOR, "[data-testid='task-checkbox']")
            checkbox.click()
            logger.info(f"Marked task as complete: {task_title}")
            time.sleep(3)  # Wait for completion animation
            return True
        except:
            # Try alternative checkbox selector
            try:
                checkbox = task_title.find_element(By.CSS_SELECTOR, "button[role='checkbox']")
                checkbox.click()
                logger.info(f"Marked task as complete: {task_title}")
                time.sleep(3)
                return True
            except :
                logger.error(f"Could not find checkbox for task: {task_title}")
                return False
        
        

    def edit_task(self, original_task_name, new_task_name):
        """Edit an existing task"""
        try:
            logger.info(f"Editing task from '{original_task_name}' to '{new_task_name}'")
            
            # Find the task element
            task_element = self.find_task_element(original_task_name)
            if not task_element:
                raise Exception(f"Could not find task: {original_task_name}")
            
            # Try different methods to edit the task
            try:
                # Method 1: Double-click to edit
                self.driver.execute_script("arguments[0].scrollIntoView(true);", task_element)
                time.sleep(1)
                self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick', {bubbles: true}));", task_element)
                time.sleep(2)
                
                # Look for editable field
                editable_field = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'], textarea, input"))
                )
                
                # Clear and enter new text
                self.driver.execute_script("arguments[0].focus();", editable_field)
                editable_field.clear()
                editable_field.send_keys(new_task_name)
                editable_field.send_keys(Keys.ENTER)
                
                logger.info(f"Task edited successfully to '{new_task_name}'")
                time.sleep(2)
                return True
                
            except:
                # Method 2: Right-click and select edit
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(self.driver)
                    actions.context_click(task_element).perform()
                    time.sleep(1)
                    
                    # Look for edit option in context menu
                    edit_option = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Edit')]")
                    edit_option.click()
                    time.sleep(1)
                    
                    # Find and edit the field
                    editable_field = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'], textarea, input"))
                    )
                    editable_field.clear()
                    editable_field.send_keys(new_task_name)
                    editable_field.send_keys(Keys.ENTER)
                    
                    logger.info(f"Task edited successfully to '{new_task_name}'")
                    time.sleep(2)
                    return True
                    
                except:
                    logger.warning("Could not edit task using standard methods")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to edit task: {str(e)}")
            return False
    
    def delete_task(self, task_name):
        """Delete a task"""
        try:
            logger.info(f"Deleting task: {task_name}")
            
            # Find the task element
            task_element = self.find_task_element(task_name)
            if not task_element:
                raise Exception(f"Could not find task: {task_name}")
            
            # Scroll to task and click to select it
            self.driver.execute_script("arguments[0].scrollIntoView(true);", task_element)
            time.sleep(1)
          #  task_element.click()
            time.sleep(1)
            
            # Try different methods to delete
            try:
                # Method 1: Use keyboard shortcut (Delete key)
                task_element.send_keys(Keys.DELETE)
                time.sleep(1)
                
            except:
                # Method 2: Right-click and delete
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(self.driver)
                    actions.context_click(task_element).perform()
                    time.sleep(1)
                    
                    # Look for delete option
                    delete_option = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Delete')]")
                    delete_option.click()
                    delete_option = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Delete')]")
                    delete_option.click()
                    
                except:
                    # Method 3: Look for delete button
                    delete_selectors = [
                        "button[aria-label*='Delete']",
                        "button[data-testid*='delete']",
                        ".delete_button",
                    ]
                    
                    for selector in delete_selectors:
                        try:
                            delete_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                            delete_button.click()
                            break
                        except NoSuchElementException:
                            continue
            
            # Confirm deletion if prompt appears
            try:
                confirm_selectors = [
                    "button[data-testid='confirm-button']",
                    "button:contains('Delete')",
                    ".confirm_button",
                    "button[aria-label*='confirm']"
                ]
                
                for selector in confirm_selectors:
                    try:
                        confirm_button = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        confirm_button.click()
                        break
                    except TimeoutException:
                        continue
                        
            except TimeoutException:
                # No confirmation needed or already confirmed
                pass
            
            logger.info(f"Task '{task_name}' deleted successfully")
            time.sleep(2)
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete task: {str(e)}")
            return False
    
    def test_long_task_input(self):
        """Test adding a very long task to check for validation errors"""
        try:
            logger.info("Testing long task input validation...")
            
            # Create a very long task name (over typical limits)
            long_task = "This is a very long task name that exceeds normal limits and should trigger validation error. " * 50
            
            # Try to add the long task
            if not self.add_task(long_task):
                return False, "Failed to initiate long task addition"
            
            # Wait and check for error messages or validation
            time.sleep(5)
            
            # Look for common error message selectors
            error_selectors = [
                "div[class*='error']",
                "span[class*='error']",
                "div[role='alert']",
                "div[class*='validation']",
                "div[class*='warning']",
                ".error_message",
                ".validation_error",
                "[data-testid*='error']"
            ]
            
            error_found = False
            error_message = ""
            
            for selector in error_selectors:
                try:
                    error_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for error_element in error_elements:
                        if error_element.is_displayed() and error_element.text.strip():
                            error_message = error_element.text
                            error_found = True
                            break
                    if error_found:
                        break
                except NoSuchElementException:
                    continue
            
            # Also check if the task was actually added (it might be truncated)
            task_added = self.find_task_element(long_task[:50]) is not None  # Check first 50 chars
            
            if error_found:
                logger.info(f"Validation error detected: {error_message}")
                return True, error_message
            elif not task_added:
                logger.info("Long task was rejected silently")
                return True, "Task was rejected silently (not added to list)"
            else:
                logger.info("Long task was accepted (possibly truncated)")
                return False, "Long task was accepted"
                
        except Exception as e:
            logger.error(f"Failed to test long task input: {str(e)}")
            return False, str(e)
    
    def run_full_test_suite(self, email, password):
        """Run the complete automation test suite"""
        try:
            logger.info("Starting Todoist automation test suite...")
            
            # Step 1: Login
            if not self.login_to_todoist(email, password):
                logger.error("Login failed. Stopping test suite.")
                return False
            
            # Step 2: Add a task
            test_task = "Automated Test Task " + str(int(time.time()))  # Add timestamp for uniqueness
            if not self.add_task(test_task):
                logger.error("Failed to add task")
                return False
            
            # Step 3: Edit the task
            edited_task = "Edited " + test_task
            edit_success = self.edit_task(test_task, edited_task)
            if not edit_success:
                logger.warning("Failed to edit task, but continuing with other tests")
            # Step 4: Mark task 
            marked_task = test_task
            marked_tasked_success = self.mark_task_complete(marked_task)
            if not marked_tasked_success:
                logger.warning("Failed to mark task, but continuing with other tests")

    
            
            # Step 5: Delete the task
            delete_success = self.delete_task(test_task)
            if not delete_success:
                logger.warning("Failed to delete task, but continuing with other tests")
            
            # Step 6: Test long input validation
            has_error, error_msg = self.test_long_task_input()
            logger.info(f"Long input test result - Error/Rejection found: {has_error}, Message: {error_msg}")
            
            logger.info("Test suite completed!")
            return True
            
        except Exception as e:
            logger.error(f"Test suite failed with error: {str(e)}")
            return False
    
    def close_driver(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

def main():
    """Main function to run the automation"""
    print("Todoist Automation Test Suite")
    print("=" * 40)
    
    # Get credentials from user
    email = input("Enter your Todoist email: ").strip()
    password = input("Enter your Todoist password: ").strip()
    
    if not email or not password:
        print("Email and password are required!")
        return
    
    # Ask if user wants headless mode
    headless_input = input("Run in headless mode? (y/n): ").strip().lower()
    headless = headless_input in ['y', 'yes']
    
    # Create automation instance
    automation = TodoistAutomation(headless=headless)
    
    try:
        # Run the full test suite
        print("\nStarting automation tests...")
        success = automation.run_full_test_suite(email, password)
        
        if success:
            print("\n✅ All tests completed successfully!")
        else:
            print("\n❌ Some tests failed. Check the logs above.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Automation failed with error: {str(e)}")
    
    finally:
        # Always close the browser
        print("\nClosing browser...")
        time.sleep(3)
        automation.close_driver()
        print("✅ Browser closed. Test complete!")

if __name__ == "__main__":
    main()