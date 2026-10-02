from playwright.sync_api import expect


def test_dashboard_page(page):
    """
    Verify that the CloudOps dashboard renders
    and displays all configured services.
    """

    page.goto("/dashboard")

    expect(
        page.get_by_role("heading", name="CloudOps Dashboard")
    ).to_be_visible()

    expect(
        page.get_by_text("payment-service")
    ).to_be_visible()

    expect(
        page.get_by_text("user-service")
    ).to_be_visible()

    expect(
        page.get_by_text("order-service")
    ).to_be_visible()

    expect(
        page.get_by_text("Environment")
    ).to_be_visible()