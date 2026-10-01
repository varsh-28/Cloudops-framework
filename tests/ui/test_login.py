from pages.login_page import LoginPage


def test_valid_login(page):
    login_page = LoginPage(page)

    login_page.open()

    login_page.login(
        username="admin",
        password="admin123"
    )

    login_page.verify_login_success("admin")
    login_page.verify_dashboard_button_visible()