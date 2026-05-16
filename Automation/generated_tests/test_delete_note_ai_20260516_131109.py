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
class TestDeleteNote:
    """Test suite for Delete Note functionality."""

    def setup_method(self, driver):
        """Setup method to initialize pages and authenticate via API."""
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.notes_page = NotesPage(driver)
        self.auth_api = AuthAPI(API_URL)
        self.notes_api = NotesAPI(API_URL)
        
        # Authenticate via API to get token
        auth_response = self.auth_api.login(USERNAME, PASSWORD)
        assert auth_response.status_code == 200, "API login failed"
        self.token = auth_response.json().get("token")
        self.notes_api.set_token(self.token)

    def test_delete_existing_note_and_verify_removal(self, driver):
        """Test deleting an existing note and verify it is removed from the list."""
        logger.info("Starting test: Delete existing note and verify removal")
        
        # Create a note via API
        note_data = {"title": "Test Note for Deletion", "content": "This note will be deleted"}
        create_response = self.notes_api.create_note(note_data)
        assert create_response.status_code == 201, "Failed to create note via API"
        note_id = create_response.json().get("id")
        
        # Navigate to notes page
        driver.get(f"{BASE_URL}/notes")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "notes-list"))
        )
        
        # Verify note exists
        assert self.notes_page.is_note_present(note_data["title"]), "Note not found in UI"
        
        # Delete the note
        self.notes_page.delete_note_by_title(note_data["title"])
        
        # Confirm deletion
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Delete')]"))
        ).click()
        
        # Wait for note to be removed
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, f"//div[contains(text(), '{note_data['title']}')]"))
        )
        
        # Verify note is no longer present
        assert not self.notes_page.is_note_present(note_data["title"]), "Note still present after deletion"
        logger.info("Note successfully deleted and verified removal from UI")

    def test_cancel_delete_and_verify_note_still_exists(self, driver):
        """Test canceling delete action and verify note still exists."""
        logger.info("Starting test: Cancel delete and verify note still exists")
        
        # Create a note via API
        note_data = {"title": "Test Note for Cancel Delete", "content": "This note should remain"}
        create_response = self.notes_api.create_note(note_data)
        assert create_response.status_code == 201, "Failed to create note via API"
        note_id = create_response.json().get("id")
        
        # Navigate to notes page
        driver.get(f"{BASE_URL}/notes")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "notes-list"))
        )
        
        # Verify note exists
        assert self.notes_page.is_note_present(note_data["title"]), "Note not found in UI"
        
        # Initiate delete but cancel
        self.notes_page.delete_note_by_title(note_data["title"])
        
        # Cancel deletion
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Cancel')]"))
        ).click()
        
        # Verify note is still present
        assert self.notes_page.is_note_present(note_data["title"]), "Note was deleted despite cancel action"
        logger.info("Delete was canceled and note still exists in UI")

    def test_delete_via_api_and_confirm_ui_reflects_removal(self, driver):
        """Test deleting a note via API and confirm UI reflects the removal."""
        logger.info("Starting test: Delete via API and confirm UI reflects removal")
        
        # Create a note via API
        note_data = {"title": "API Deleted Note", "content": "This note will be deleted via API"}
        create_response = self.notes_api.create_note(note_data)
        assert create_response.status_code == 201, "Failed to create note via API"
        note_id = create_response.json().get("id")
        
        # Navigate to notes page
        driver.get(f"{BASE_URL}/notes")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "notes-list"))
        )
        
        # Verify note exists in UI
        assert self.notes_page.is_note_present(note_data["title"]), "Note not found in UI before API deletion"
        
        # Delete note via API
        delete_response = self.notes_api.delete_note(note_id)
        assert delete_response.status_code == 200, "Failed to delete note via API"
        
        # Refresh page to reflect changes
        driver.refresh()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "notes-list"))
        )
        
        # Verify note is no longer present in UI
        assert not self.notes_page.is_note_present(note_data["title"]), "Note still present in UI after API deletion"
        logger.info("Note deleted via API and UI correctly reflects removal")
