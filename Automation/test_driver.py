from fixtures.browser_fixture import create_driver

driver = create_driver()

driver.get("https://google.com")

input("Press Enter to close...")

driver.quit()