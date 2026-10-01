from playwright.sync_api import Page, expect


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")

        self.login_button = page.get_by_role(
            "button",
            name="Login",
        )

        self.success_message = page.locator(
            "#login-success-message"
        )

        self.error_message = page.locator(
            "#login-error-message"
        )

        self.dashboard_button = page.get_by_role(
            "button",
            name="Open Dashboard",
        )

    def open(self):
        self.page.goto("/")

    def login(self, username: str, password: str):

        self.username_input.fill(username)
        self.password_input.fill(password)

        self.login_button.click()

    def verify_login_success(self, username: str):

        expect(
            self.success_message
        ).to_contain_text(
            f"Login successful. Welcome {username}."
        )

    def verify_login_error(self, message: str):

        expect(
            self.error_message
        ).to_contain_text(message)

    def verify_dashboard_button_visible(self):

        expect(
            self.dashboard_button
        ).to_be_visible()