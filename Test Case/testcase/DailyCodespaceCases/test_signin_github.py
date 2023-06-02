import pytest
import string
import getpass
from playwright.sync_api import Page, Playwright
from test_commonmethod import test_open_page_sso,test_create_ppe_codespace,test_newtemplatepage
from test_delete_codespace import test_deleteAllCodespace 

@pytest.mark.daily
@pytest.mark.signinOnportal
def test_delete_all_codespaces(playwright: Playwright):
    test_deleteAllCodespace(playwright)

@pytest.mark.daily
@pytest.mark.signinOnportal
def test_goto_docs(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    try:
        page.locator("a", has_text="Go to docs").click()
        page.wait_for_timeout(2500)
        assert "GitHub Codespaces Documentation" in page.text_content("h1")
        page.go_back()
        page.locator("a", has_text="Start here").click()
        page.wait_for_timeout(2500)
        assert "GitHub Codespaces Documentation" in page.text_content("h1")
        page.go_back()
        page.locator("a", has_text="secret management").click()
        page.wait_for_timeout(2500)
        assert "Managing encrypted secrets for your codespaces" in page.text_content("h1")
        page.go_back()
        page.locator("a", has_text="port forwarding").click()
        page.wait_for_timeout(2500)
        assert "Forwarding ports in your codespace" in page.text_content("h1")
        page.go_back()
        page.locator("a", has_text="Visual Studio Code").click()
        page.wait_for_timeout(2500)
        assert "Using GitHub Codespaces in Visual Studio Code" in page.text_content("h1")
        page.go_back()
        page.locator("a", has_text="JetBrains").click()
        page.wait_for_timeout(2500)
        assert "Using GitHub Codespaces in your JetBrains IDE" in page.text_content("h1")
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.signinOnportal
def test_check_links_on_loading_interstitial(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?location=EastUs"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        test_create_ppe_codespace(page, "Microsoft/vscode-remote-try-rust")
        page.get_by_role("button", name="Create codespace").click()
        page.wait_for_timeout(1000)
        page.locator("a", has_text="Learn more").click()
        assert page.context.pages[-1].get_by_role("link", name="GitHub Docs").is_visible()
        page.wait_for_timeout(2000)
        page.close()
    finally:
        page.context.pages[-1].close()

@pytest.mark.daily
@pytest.mark.signinOnportal
def test_check_links_on_index_page(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    try:
        page.locator("a", has_text="Terms").click()
        page.wait_for_timeout(2500)
        assert "GitHub Terms of Service" in page.text_content("h1")
        page.go_back()
        page.locator("a", has_text="Privacy").click()
        page.wait_for_timeout(2500)
        assert "GitHub Privacy Statement" in page.text_content("h1")
        page.go_back()
        page.locator("a", has_text="Security").click()
        page.wait_for_timeout(2500)
        assert page.get_by_role("main").get_by_text("GitHub Security", exact=True).is_visible()
        page.go_back()
        page.locator("a", has_text="Status").click()
        page.wait_for_timeout(2500)
        assert page.locator("span", has_text="All Systems Operational").is_visible()
        page.go_back()
        page.get_by_role("link", name="Docs", exact=True).click()
        page.wait_for_timeout(2500)
        assert "GitHub Docs" in page.text_content("h1")
        page.go_back()
        page.locator("a", has_text="Contact GitHub").click()
        page.wait_for_timeout(2500)
        assert "what can we help with?" in page.text_content("h1")
        page.go_back()
        page.locator("a", has_text="Pricing").click()
        page.wait_for_timeout(2500)
        assert page.locator("main", has_text="Get the complete developer platform.").is_visible()
        page.go_back()
        page.locator("a", has_text="API").click()
        page.wait_for_timeout(2500)
        assert page.locator("p", has_text="Help for wherever you are on your GitHub journey.").is_visible()
        page.go_back()
        page.locator("a", has_text="Training").click()
        page.wait_for_timeout(2500)
        assert page.locator("main", has_text="The GitHub Expert Services Team").is_visible()
        page.go_back()
        page.locator("a", has_text="Blog").click()
        page.wait_for_timeout(2500)
        assert "Highlights from Git" in page.text_content("h3")
        page.go_back()
        page.locator("a", has_text="About").click()
        page.wait_for_timeout(2500)
        assert page.locator("main", has_text="Let's build from here").is_visible()
    finally:
        page.close()