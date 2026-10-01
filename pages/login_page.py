from playwright.sync_api import Page, expect


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

        # Page elements
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role(
            "button",
            name="Login"
        )

        self.login_success_message = page.locator(
            "#login-success-message"
        )

        self.dashboard_button = page.get_by_role(
            "button",
            name="Open Dashboard"
        )

    def open(self):
        self.page.goto("/")

    def enter_username(self, username: str):
        self.username_input.fill(username)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def verify_login_success(self, username: str):
        expect(
            self.login_success_message
        ).to_contain_text(
            f"Login successful. Welcome {username}."
        )

    def verify_dashboard_button_visible(self):
        expect(
            self.dashboard_button
        ).to_be_visible()

    def open_dashboard(self):
        self.dashboard_button.click()