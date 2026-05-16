import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import BASE_URL, USER_EMAIL, USER_PASSWORD
from utils.logger import get_logger
from utils.screenshot import take_screenshot

logger = get_logger(__name__)

class TestLoginPage:
    """Test suite for the Login page functionality."""

    def test_valid_login_with_correct_email_and_password(self, driver):
        """Test successful login with valid email and password."""
        logger.info("Starting test: Valid login with correct email and password")
        login_page = LoginPage(driver)
        driver.get(f"{BASE_URL}/login")
        
        login_page.enter_email(USER_EMAIL)
        login_page.enter_password(USER_PASSWORD)
        login_page.click_login_button()
        
        # Wait for redirect to notes page
        WebDriverWait(driver, 10).until(
            EC.url_contains("/notes")
        )
        
        assert "/notes" in driver.current_url, "User was not redirected to notes page after login"
        logger.info("Test passed: Valid login successful")

    def test_invalid_login_with_wrong_password(self, driver):
        """Test login failure with incorrect password."""
        logger.info("Starting test: Invalid login with wrong password")
        login_page = LoginPage(driver)
        driver.get(f"{BASE_URL}/login")
        
        login_page.enter_email(USER_EMAIL)
        login_page.enter_password("wrong_password")
        login_page.click_login_button()
        
        # Wait for error message to appear
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(login_page.error_message_locator)
        )
        
        assert error_message.is_displayed(), "Error message not displayed for invalid login"
        assert "invalid" in error_message.text.lower() or "incorrect" in error_message.text.lower(), \
            f"Unexpected error message: {error_message.text}"
        logger.info("Test passed: Invalid login correctly rejected")

    def test_login_with_empty_email_field(self, driver):
        """Test login attempt with empty email field."""
        logger.info("Starting test: Login with empty email field")
        login_page = LoginPage(driver)
        driver.get(f"{BASE_URL}/login")
        
        login_page.enter_email("")
        login_page.enter_password(USER_PASSWORD)
        login_page.click_login_button()
        
        # Wait for validation error or check if still on login page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='email']//following::div[contains(@class, 'error')] | //div[contains(text(), 'email') and contains(text(), 'required')]"))
        )
        
        assert "/login" in driver.current_url, "User was redirected despite empty email field"
        logger.info("Test passed: Empty email field correctly handled")

    def test_login_with_empty_password_field(self, driver):
        """Test login attempt with empty password field."""
        logger.info("Starting test: Login with empty password field")
        login_page = LoginPage(driver)
        driver.get(f"{BASE_URL}/login")
        
        login_page.enter_email(USER_EMAIL)
        login_page.enter_password("")
        login_page.click_login_button()
        
        # Wait for validation error or check if still on login page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']//following::div[contains(@class, 'error')] | //div[contains(text(), 'password') and contains(text(), 'required')]"))
        )
        
        assert "/login" in driver.current_url, "User was redirected despite empty password field"
        logger.info("Test passed: Empty password field correctly handled")

    def test_verify_redirect_to_notes_dashboard_after_successful_login(self, driver):
        """Test that user is redirected to notes dashboard after successful login."""
        logger.info("Starting test: Verify redirect to notes dashboard after successful login")
        login_page = LoginPage(driver)
        notes_page = NotesPage(driver)
        driver.get(f"{BASE_URL}/login")
        
        login_page.enter_email(USER_EMAIL)
        login_page.enter_password(USER_PASSWORD)
        login_page.click_login_button()
        
        # Wait for notes page to load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(notes_page.notes_container_locator)
        )
        
        assert "/notes" in driver.current_url, "User was not redirected to notes dashboard"
        assert notes_page.is_notes_container_displayed(), "Notes dashboard is not displayed"
        logger.info("Test passed: Successfully redirected to notes dashboard after login")
