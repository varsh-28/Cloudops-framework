from playwright.sync_api import Page


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("#login-error")

    def open(self):
        self.page.goto("http://127.0.0.1:8000")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self):
        return self.error_message.text_content()