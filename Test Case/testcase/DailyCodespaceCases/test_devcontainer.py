import pytest
import string
from playwright.sync_api import Page, Playwright
from test_commonmethod import test_newtemplatepage,test_create_ppe_codespace

# 4-core EastUs
@pytest.mark.devcontainer   
def test_no_devcontainer(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?location=EastUs"
    page=test_newtemplatepage(playwright, tempurl)
    test_create_ppe_codespace(page, "VSLSTest2/BookShop")
    test_open_createion_log(page,"4-core")
    page.wait_for_timeout(1000)
    assert "Using image: mcr.microsoft.com/devcontainers/universal" in page.locator("div[class=editor-instance]").inner_text().replace("\xa0"," ")
    page.wait_for_timeout(3000)

# 16-core EastUs
@pytest.mark.devcontainer   
def test_single_devcontainer(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?location=EastUs"
    page=test_newtemplatepage(playwright, tempurl)
    test_create_ppe_codespace(page, "codespaces-contrib/Ghost")
    test_open_createion_log(page,"16-core")
    page.wait_for_timeout(1000)
    assert "Using image: mcr.microsoft.com/devcontainers/universal" in page.locator("div[class=editor-instance]").inner_text().replace("\xa0"," ")
    page.wait_for_timeout(3000)

# 2-core EastUs
@pytest.mark.devcontainer   
def test_single_customer_devcontainer(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?location=EastUs"
    page=test_newtemplatepage(playwright, tempurl)
    test_create_ppe_codespace(page, "cltest02/vscode-remote-try-node")
    page.get_by_role("button", name="Create codespace").click()
    page.wait_for_timeout(75000)
    if page.get_by_role("treeitem").filter(has_text=".devcontainer").is_visible():
        page.get_by_role("treeitem").filter(has_text=".devcontainer").click()
        page.wait_for_timeout(500)
    if page.get_by_role("treeitem").filter(has_text="devcontainer.json").is_visible():
        page.get_by_role("treeitem").filter(has_text="devcontainer.json").dblclick()
        page.wait_for_timeout(500)

        extenName=page.locator("div[class=editor-instance]").inner_text().replace("\xa0"," ").split('extensions": [')[1].split(']')[0]
        page.keyboard.press("Control+Shift+X")
        extention=page.locator("div[class=extension-list-item]").inner_text().split("\n")[0]
        assert extention.lower() in extenName
    page.wait_for_timeout(1000)
    assert "Using image: mcr.microsoft.com/devcontainers/universal" in page.locator("div[class=editor-instance]").inner_text().replace("\xa0"," ")
    page.wait_for_timeout(3000)

def test_open_createion_log(page:Page, machinetype: string):
    page.wait_for_timeout(500)
    page.get_by_role("button", name="2-core").click()
    page.wait_for_timeout(500)
    page.locator(".d-flex.flex-justify-between.mb-1", has_text=machinetype).click()
    page.wait_for_timeout(1000)
    assert page.get_by_role("button", name=machinetype).count()==1

    page.get_by_role("button", name="Create codespace").click()
    page.wait_for_timeout(75000)
    
    page.keyboard.press("Control+Shift+P")
    page.keyboard.type("Codespaces: View creation Log")
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")