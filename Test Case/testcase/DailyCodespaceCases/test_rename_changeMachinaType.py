import pytest
import string
from playwright.sync_api import Page, Playwright, sync_playwright
import re
import autoit
from test_commonmethod import test_newtemplatepage,test_create_ppe_codespace,test_open_page_sso,test_createAndinstall
from test_delete_codespace import test_deleteAllCodespace 

@pytest.mark.daily
@pytest.mark.rename
def test_delete_all_codespaces(playwright: Playwright):
    test_deleteAllCodespace(playwright)

@pytest.mark.daily
@pytest.mark.rename
def test_rename_a_codespace(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?location=SouthEastAsia"
    page=test_open_page_sso(playwright, tempurl)
    codespacerename="CodeSpace-RenamedTesting01"
    try:
        page.context.pages[-2].close()
        test_create_ppe_codespace(page, "Microsoft/vscode-remote-try-php")
        
        test_createAndinstall(page, "2-core")
        page.wait_for_timeout(300)
        page.goto("https://github.com/codespaces")
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.wait_for_timeout(1000)
        page.get_by_role("menuitem", name="Rename",exact=True).click()
        page.wait_for_timeout(300)
        page.on("dialog", lambda dialog:dialog.accept(codespacerename))
        page.wait_for_timeout(650)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)
        page.reload()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.wait_for_timeout(1000)
        page.get_by_role("menuitem", name="Rename",exact=True).click()
        assert page.locator("a", has_text=codespacerename).is_visible()
        page.wait_for_timeout(1000)
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.changemachinetype
def test_change_machine_type_codespace_connected_F1(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(60000)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("codespaces: Change Machine Type")
        page.wait_for_timeout(400)
        page.keyboard.press("Enter")
        machineTypeInfoBefore = page.get_by_role("option", name=re.compile(".*(Current machine type)")).text_content()
        page.wait_for_timeout(2000)
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        dialog_message = page.locator("#monaco-dialog-message-detail").text_content()

        if "Machine type successfully updated and will take effect on the next restart" in dialog_message:
            page.get_by_role("button", name="Yes", exact=True).click()
            page.wait_for_timeout(13000)
            page.get_by_text("Restart codespace").click()
            page.wait_for_timeout(30000)
            page.keyboard.press("Control+Shift+P")
            page.keyboard.type("codespaces: Change Machine Type")
            page.wait_for_timeout(1000)
            page.keyboard.press("Enter")
            machineTypeInfoAfter= page.get_by_role("option", name=re.compile(".*(Current machine type)")).text_content()
            assert machineTypeInfoBefore not in machineTypeInfoAfter
        elif  "Changing to a machine type with a different amount of storage will require this" in dialog_message:
            page.get_by_role("button", name="Yes", exact=True).click()
            page.wait_for_timeout(16000)
            page.wait_for_selector(".static-screen-message", state="attached")
            button_message_first =  page.locator(".container").text_content()
            if "Restart codespace" in button_message_first:
                page.get_by_text("Restart codespace").click()
                page.wait_for_timeout(30000)
            status_text = page.get_by_role("heading", name="Codespace is being updated, you will need to wait for a few minutes for the operation to finish").inner_text()
            assert "Codespace is being updated, you will need to wait for a few minutes for the operation to finish" in status_text
            page.wait_for_timeout(1000)# the page will wait for 10 mins, need to find a way to replace this.
            page.goto(tempurl)
            for i in range(20):
                if page.locator("p.f6.mb-0.mr-2.text-small.color-fg-muted", has_text="Changing machine types...").is_visible():
                    page.wait_for_timeout(90000)
                    page.reload()
                else:
                    break
            page.get_by_role("button", name="Codespace configuration").nth(0).click()
            page.get_by_role("menuitem", name="Open in ...").click()
            page.get_by_role("menuitem", name="Open in browser").click()
            page.wait_for_timeout(10000)
            if page.locator("button", has_text='Restart codespace').is_visible():
                page.locator("button", has_text='Restart codespace').click()
            page.wait_for_timeout(60000)
            page.keyboard.press("Control+Shift+P")
            page.keyboard.type("codespaces: Change Machine Type")
            page.wait_for_timeout(1000)
            page.keyboard.press("Enter")
            machineTypeInfoAfter= page.get_by_role("option", name=re.compile(".*(Current machine type)")).text_content()
            assert machineTypeInfoBefore not in machineTypeInfoAfter   
        else:
            print("Have change the machine type successfully")
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.changemachinetype
def test_stop_codespace_from_index_page(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        machine_type_info_before = page.get_by_text(re.compile(".*-core")).first.text_content().replace("\n","").strip()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Change machine type").click()
        page.wait_for_timeout(1000)
        page.get_by_role("radio", checked=True).click()
        page.keyboard.press("ArrowDown")
        page.get_by_role("button", name="Update codespace").click()
        if("2-core" in machine_type_info_before):
            alert_message = page.get_by_text(re.compile(".*Changes will take effect the next time your codespace restarts")).text_content()
            assert "Changes will take effect the next time your codespace restarts" in alert_message
        else:
            alert_message = page.get_by_text(re.compile(".*Your codespace will be stopped and unavailable during the update")).text_content()
            assert "Your codespace will be stopped and unavailable during the update" in alert_message
        
        for i in range(20):
            if page.locator("p.f6.mb-0.mr-2.text-small.color-fg-muted", has_text="Changing machine types...").is_visible():
                page.wait_for_timeout(90000)
                page.reload()
            else:
                break
        machine_type_info_after = page.get_by_text(re.compile(".*-core")).first.text_content().replace("\n","").strip()
        assert machine_type_info_after not in machine_type_info_before
    finally:
        page.close()

