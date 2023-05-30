import pytest
from playwright.sync_api import Page, Playwright
import string
from test_commonmethod import test_open_page_sso,test_create_ppe_codespace,test_createAndinstall
from test_delete_codespace import test_deleteAllCodespace 

@pytest.mark.manageSecrets
def test_delete_all_codespaces(playwright: Playwright):
    test_deleteAllCodespace(playwright)

@pytest.mark.manageSecrets
def test_add_secret_within_codespace(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?location=SouthEastAsia"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        test_create_ppe_codespace(page, "Microsoft/vscode-remote-try-go")
        
        test_createAndinstall(page, "8-core")
        page.wait_for_timeout(300)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Manage User Secrets")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")

        page.locator("a", has_text="Add a new secret").click()
        page.get_by_placeholder("Enter Secret Name").fill("TESTSECRET01")
        page.keyboard.press("Enter")
        page.get_by_placeholder("Enter Secret Value").fill("secret01")
        page.keyboard.press("Enter")
        page.get_by_title("Reload to apply").click()
        page.wait_for_timeout(7500)
        page.get_by_label("Terminal 1, bash").fill("echo $TESTSECRET01")
        page.keyboard.press("Enter")
        page.wait_for_timeout(999)
        page.locator(".codicon-terminal-decoration-success").click()
        for i in range(3):
            page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.keyboard.press("Control+Shift+F")
        page.get_by_placeholder("Search").click()
        page.get_by_placeholder("Search").clear()
        page.keyboard.press("Control+V")
        assert page.get_by_placeholder("Search").input_value().replace("\n","")=="secret01"

    finally:
        page.close()


@pytest.mark.manageSecrets
def test_manage_secret_on_github(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()    
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(30000)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Manage User Secrets")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.locator("a", has_text="Manage on GitHub.com").click()
        page.wait_for_timeout(999)
        assert page.context.pages[1].url=="https://github.com/settings/codespaces"
        page.context.pages[1].close()
    finally:
        page.close()

@pytest.mark.manageSecrets
def test_remove_then_add_secret_to_current_repo(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()    
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(30000)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Manage User Secrets")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)
        page.locator("a", has_text="TESTSECRET01").click()
        page.locator("a", has_text="Remove this secret from the current repository").click()
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Manage User Secrets")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)
        page.locator("a", has_text="TESTSECRET01").click()
        page.wait_for_timeout(800)
        assert page.get_by_role("option", name="Add this secret to the current repository", exact=True).locator("a").is_visible()

        page.get_by_role("option", name="Add this secret to the current repository", exact=True).click()
        page.get_by_title("Reload to apply").click()
        page.wait_for_timeout(6000)
        page.get_by_label("Terminal 1, bash").fill("echo $TESTSECRET01")
        page.keyboard.press("Enter")
        page.wait_for_timeout(999)
        page.locator(".codicon-terminal-decoration-success").click()
        for i in range(3):
            page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.keyboard.press("Control+Shift+F")
        page.get_by_placeholder("Search").click()
        page.get_by_placeholder("Search").clear()
        page.keyboard.press("Control+V")
        assert page.get_by_placeholder("Search").input_value().replace("\n","")=="secret01"
    finally:
        page.close()


@pytest.mark.manageSecrets
def test_update_the_secret_value(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()    
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(30000)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Manage User Secrets")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)
        page.locator("a", has_text="TESTSECRET01").click()
        page.locator("a", has_text="Update the secret value").click()
        page.get_by_placeholder("Enter Secret Value").fill("secretupdated01")
        page.keyboard.press("Enter")
        page.get_by_title("Reload to apply").click()
        page.wait_for_timeout(6000)
        page.get_by_label("Terminal 1, bash").fill("echo $TESTSECRET01")
        page.keyboard.press("Enter")
        page.wait_for_timeout(999)
        page.locator(".codicon-terminal-decoration-success").click()
        for i in range(3):
            page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.keyboard.press("Control+Shift+F")
        page.get_by_placeholder("Search").click()
        page.get_by_placeholder("Search").clear()
        page.keyboard.press("Control+V")
        assert page.get_by_placeholder("Search").input_value().replace("\n","")=="secretupdated01"
    finally:
        page.close()

@pytest.mark.manageSecrets
def test_delete_update_secret_isnot_applied_current(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()    
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(30000)
        
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Manage User Secrets")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.locator("a", has_text="TEST01").click()
        if page.locator("a", has_text="Update the secret value").is_visible():
            page.locator("a", has_text="Update the secret value").click()
        else:
            if page.locator("a", has_text="Update the value and add this secret to the current repository").is_visible():
                page.locator("a", has_text="Update the value and add this secret to the current repository").click() 
        page.get_by_placeholder("Enter Secret Value").fill("secret01")
        page.keyboard.press("Enter")
        if page.get_by_title("Reload to apply").is_visible():
            page.get_by_title("Reload to apply").click()
            page.wait_for_timeout(7500)

        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Manage User Secrets")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.locator("a", has_text="TESTSECRET01").click()
        assert page.get_by_placeholder("What would you like to do?").is_visible()
        page.locator("a", has_text="Delete the secret").click()
        page.get_by_role("button", name="Yes").click()
        page.wait_for_timeout(999)
        page.goto("https://github.com/settings/codespaces")
        page.wait_for_timeout(999)
        assert not page.locator('a[href="/settings/codespaces/secrets/TESTSECRET01/edit"]').is_visible()
        page.locator('a[href="/settings/codespaces/secrets/TEST01/edit"]').click()
        page.wait_for_timeout(999)
        page.get_by_label("microsoft/vscode-remote-try-go").click()
        page.locator("button", has_text="Save changes").click()
    finally:
        page.close()