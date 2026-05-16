
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from api.auth_api import AuthAPI
from api.notes_api import NotesAPI
from config.environment import BASE_URL, API_URL, USERNAME, PASSWORD
from utils.logger import get_logger
from utils.screenshot import take_screenshot

logger = get_logger(__name__)

@pytest.mark.usefixtures("driver")
class TestCreateNote:
    """Test suite for Create Note functionality on the Notes App."""

    def setup_method(self, driver):
        """Setup method to initialize pages and authenticate before each test."""
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.notes_page = NotesPage(driver)
        self.auth_api = AuthAPI(API_URL)
        self.notes_api = NotesAPI(API_URL)
        
        # Login via UI to ensure session is active
        self.driver.get(BASE_URL)
        self.login_page.login(USERNAME, PASSWORD)
        WebDriverWait(driver, 10).until(
            EC.url_contains("/notes")
        )
        logger.info("Successfully logged in and navigated to notes page")

    def test_valid_note_creation_with_title_and_description(self, driver):
        """Test creating a note with valid title and description."""
        title = "Test Note Title"
        description = "This is a test note description."
        
        self.notes_page.click_create_note_button()
        self.notes_page.enter_note_title(title)
        self.notes_page.enter_note_description(description)
        self.notes_page.click_save_note_button()
        
        # Wait for success message or note to appear in list
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(), '{title}')]"))
        )
        
        # Verify note appears in the list
        assert self.notes_page.is_note_in_list(title), "Created note should appear in the notes list"
        logger.info(f"Successfully created note with title: {title}")

    def test_note_creation_with_empty_title_shows_validation_error(self, driver):
        """Test that creating a note with empty title shows validation error."""
        description = "This is a test note description."
        
        self.notes_page.click_create_note_button()
        self.notes_page.enter_note_title("")
        self.notes_page.enter_note_description(description)
        self.notes_page.click_save_note_button()
        
        # Wait for validation error message
        error_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Title is required') or contains(text(), 'Title cannot be empty')]"))
        )
        
        assert error_element.is_displayed(), "Validation error should be displayed for empty title"
        logger.info("Validation error correctly shown for empty title")

    def test_note_creation_with_empty_description_shows_validation_error(self, driver):
        """Test that creating a note with empty description shows validation error."""
        title = "Test Note Title"
        
        self.notes_page.click_create_note_button()
        self.notes_page.enter_note_title(title)
        self.notes_page.enter_note_description("")
        self.notes_page.click_save_note_button()
        
        # Wait for validation error message
        error_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Description is required') or contains(text(), 'Description cannot be empty')]"))
        )
        
        assert error_element.is_displayed(), "Validation error should be displayed for empty description"
        logger.info("Validation error correctly shown for empty description")

    def test_newly_created_note_appears_in_notes_list(self, driver):
        """Test that a newly created note appears in the notes list."""
        title = "Newly Created Note"
        description = "This note should appear in the list after creation."
        
        # Get initial count of notes
        initial_notes = self.notes_page.get_notes_list()
        initial_count = len(initial_notes)
        
        # Create new note
        self.notes_page.click_create_note_button()
        self.notes_page.enter_note_title(title)
        self.notes_page.enter_note_description(description)
        self.notes_page.click_save_note_button()
        
        # Wait for note to appear in list
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(), '{title}')]"))
        )
        
        # Verify note count increased and note is present
        updated_notes = self.notes_page.get_notes_list()
        updated_count = len(updated_notes)
        
        assert updated_count == initial_count + 1, "Note count should increase by 1 after creation"
        assert self.notes_page.is_note_in_list(title), "Newly created note should be visible in the list"
        logger.info(f"Note '{title}' successfully appeared in the notes list")
