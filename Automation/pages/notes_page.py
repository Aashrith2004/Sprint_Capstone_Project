import time
import allure

from selenium.common.exceptions import (
    StaleElementReferenceException,
)

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import (
    WebDriverWait,
    Select,
)

from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.logger import get_logger
from utils.self_healing_locator import (
    find_element_with_fallback,
)

logger = get_logger(__name__)


class NotesPage(BasePage):

    _ADD_NOTE_BUTTON = [
        (
            By.CSS_SELECTOR,
            "button[data-testid='add-new-note']",
        ),
    ]

    _TITLE_INPUT = [
        (
            By.ID,
            "title",
        ),
    ]

    _DESCRIPTION_INPUT = [
        (
            By.ID,
            "description",
        ),
    ]

    _CATEGORY_DROPDOWN = [
        (
            By.ID,
            "category",
        ),
    ]

    _SAVE_BUTTON = [
        (
            By.XPATH,
            "//button[contains(text(),'Create')]",
        ),
    ]

    _NOTE_TITLES = (
        By.CSS_SELECTOR,
        "[data-testid='note-card-title']",
    )

    _TITLE_REQUIRED_ERROR = (
        By.XPATH,
        "//div[contains(text(),'Title is required')]"
    )

    _DESCRIPTION_REQUIRED_ERROR = (
        By.XPATH,
        "//div[contains(text(),'Description is required')]"
    )

    def __init__(self, driver: WebDriver):

        super().__init__(driver)


    def safe_click(self, locator, timeout=20):

        last_exception = None

        for _ in range(3):

            try:

                element = WebDriverWait(
                    self.driver,
                    timeout
                ).until(
                    EC.element_to_be_clickable(locator)
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    element
                )

                try:
                    element.click()

                except Exception:
                    self.driver.execute_script(
                        "arguments[0].click();",
                        element
                    )

                return

            except (
                StaleElementReferenceException,
            ) as e:

                last_exception = e
                time.sleep(1)

        raise last_exception


    @allure.step("Click Add Note button")
    def click_add_note(self) -> None:

        locator = (
            By.CSS_SELECTOR,
            "button[data-testid='add-new-note']"
        )

        self.safe_click(locator)

        logger.info(
            "Add Note button clicked"
        )

    @allure.step("Enter note title")
    def enter_title(
        self,
        title: str
    ) -> None:

        element = find_element_with_fallback(
            self.driver,
            self._TITLE_INPUT,
        )

        WebDriverWait(
            self.driver,
            20
        ).until(
            EC.visibility_of(element)
        )

        element.clear()

        element.send_keys(title)

        logger.info(
            f"Title entered: {title}"
        )

    @allure.step("Enter note description")
    def enter_description(
        self,
        description: str,
    ) -> None:

        element = find_element_with_fallback(
            self.driver,
            self._DESCRIPTION_INPUT,
        )

        WebDriverWait(
            self.driver,
            20
        ).until(
            EC.visibility_of(element)
        )

        element.clear()

        element.send_keys(description)

        logger.info(
            "Description entered"
        )

    @allure.step("Select note category")
    def select_category(
        self,
        category: str,
    ) -> None:

        dropdown_element = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.visibility_of_element_located(
                (By.ID, "category")
            )
        )

        dropdown = Select(
            dropdown_element
        )

        dropdown.select_by_visible_text(
            category
        )

        logger.info(
            f"Category selected: {category}"
        )

    @allure.step("Click Save button")
    def click_save(self) -> None:

        locator = (
            By.XPATH,
            "//button[contains(text(),'Create')]"
        )

        self.safe_click(locator)

        logger.info(
            "Save/Create button clicked"
        )

    @allure.step("Create new note")
    def create_note(
        self,
        title: str,
        description: str,
        category: str = "Home",
    ) -> None:

        self.click_add_note()

        self.enter_title(title)

        self.enter_description(description)

        self.select_category(category)

        self.click_save()

        self.wait_for_note_visible(title)

        logger.info(
            f"Note created: {title}"
        )
    def get_note_titles(self):

        for _ in range(3):

            try:

                WebDriverWait(
                    self.driver,
                    20
                ).until(
                    EC.presence_of_all_elements_located(
                        self._NOTE_TITLES
                    )
                )

                elements = self.driver.find_elements(
                    *self._NOTE_TITLES
                )

                return [
                    element.text.strip()
                    for element in elements
                ]

            except StaleElementReferenceException:

                time.sleep(1)

        return []

    def is_note_present(
        self,
        title: str,
        timeout: int = 30,
    ) -> bool:

        try:

            WebDriverWait(
                self.driver,
                timeout
            ).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    f"//*[contains(text(), '{title}')]"
                ))
            )

            return True

        except Exception:

            return False

    def refresh_notes_page(self):
        """
        Refresh notes page safely.
        """

        try:

            self.driver.set_page_load_timeout(20)

            self.driver.refresh()

        except Exception as e:

            logger.warning(
                f"Refresh failed: {e}"
            )

            self.driver.get(
                self.driver.current_url
            )
    def is_title_required_error_displayed(
        self,
    ) -> bool:

        return self.is_visible(
            self._TITLE_REQUIRED_ERROR,
            timeout=5,
        )

    def is_description_required_error_displayed(
        self,
    ) -> bool:

        return self.is_visible(
            self._DESCRIPTION_REQUIRED_ERROR,
            timeout=5,
        )

    @allure.step("Wait for note visible")
    def wait_for_note_visible(
        self,
        title: str,
        timeout: int = 30,
    ):

        WebDriverWait(
            self.driver,
            timeout
        ).until(
            EC.visibility_of_element_located((
                By.XPATH,
                f"//*[contains(text(), '{title}')]"
            ))
        )

    @allure.step("Delete note")
    def delete_note(self):

        locator = (
            By.CSS_SELECTOR,
            "[data-testid='note-delete']"
        )

        self.safe_click(locator)

        logger.info(
            "Delete button clicked"
        )

    @allure.step("Confirm delete")
    def confirm_delete(self):

        locator = (
            By.CSS_SELECTOR,
            "[data-testid='note-delete-confirm']"
        )

        self.safe_click(locator)

        logger.info(
            "Delete confirmed"
        )

    @allure.step("Wait for note removed")
    def wait_for_note_gone(
        self,
        title: str,
        timeout: int = 20,
    ):

        return WebDriverWait(
            self.driver,
            timeout
        ).until(
            EC.invisibility_of_element_located((
                By.XPATH,
                f"//*[contains(text(), '{title}')]"
            ))
        )
