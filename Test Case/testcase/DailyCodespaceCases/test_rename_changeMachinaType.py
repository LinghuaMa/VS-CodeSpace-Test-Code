import pytest
import string
from playwright.sync_api import Page, Playwright, sync_playwright
import re
import autoit
from test_commonmethod import test_newtemplatepage

def test_createPublicGithubRepo(playwright:Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    page.locator('a',has_text="New codespace").nth(1).click()
    create_page=page.wait_for_event('popup')
    assert "Create a new codespace" in create_page.text_content('h2')
    create_page.wait_for_timeout(1000)
    create_page.get_by_role("button", name="Select a repository").click()
    create_page.keyboard.type("microsoft/vscode-remote-try-node")
    create_page.wait_for_timeout(2000)
    create_page.keyboard.press("ArrowDown")
    create_page.keyboard.press("Enter")
    vscstargetselector="div.Box-body.p-0 > form > div:nth-child(5) > div > details > summary"
    create_page.locator(vscstargetselector).click()
    for i in range(3):
        create_page.keyboard.press("ArrowDown")
    create_page.keyboard.press("Enter")
    create_page.wait_for_timeout(1000)
    assert  create_page.locator(vscstargetselector).inner_text()=="pre-production"
    create_page.wait_for_timeout(3000)

@pytest.mark.rename
def test_rename_codespace(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    codespacerename="CodeSpace-RenamedTesting01"
    page=test_newtemplatepage(playwright, tempurl)
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.wait_for_timeout(1000)
    page.get_by_role("menuitem", name="Rename",exact=True).click()
    page.wait_for_timeout(300)
    page.on("dialog", lambda dialog:dialog.accept(codespacerename))
    page.wait_for_timeout(1000)
    page.keyboard.press("Enter")
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    assert codespacerename in page.get_by_role("alert").inner_text()
    page.wait_for_timeout(1000)

@pytest.mark.changemachinetype
def test_change_machine_type_codespace_connected_F1(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    # page.get_by_role("group").filter(has_text="Open in ... Rename Export changes to a branch Change machine type Stop codespace").get_by_role("button", name="Codespace configuration").click()
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Open in ...").click()
    page.get_by_role("menuitem", name="Open in browser").click()
    # page.wait_for_load_state()
    page.wait_for_timeout(30000)
    # page.get_by_role("button", name="remote Codespaces").click()
    page.keyboard.press("F1")
    page.get_by_placeholder("Type the name of a command to run.").fill(">codespace: Change Machine Type")
    page.wait_for_timeout(10000)
    page.keyboard.press("Enter")
    machineTypeInfoBefore = page.get_by_role("option", name=re.compile(".*(Current machine type)")).text_content()
    # page.get_by_placeholder("Select an option to open a Remote Window").click()
    page.wait_for_timeout(2000)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    # page.wait_for_load_state()

    dialog_message = page.locator("#monaco-dialog-message-detail").text_content()

    if "Machine type successfully updated and will take effect on the next restart" in dialog_message:
        page.get_by_role("button", name="Yes", exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_text("Restart codespace").click()
        page.wait_for_timeout(30000)
        page.locator(".monaco-list > .monaco-scrollable-element").nth(0).click()
        page.keyboard.press("F1")
        page.get_by_placeholder("Type the name of a command to run.").fill(">codespace: Change Machine Type")
        page.wait_for_timeout(10000)
        page.keyboard.press("Enter")
        machineTypeInfoAfter= page.get_by_role("option", name=re.compile(".*(Current machine type)")).text_content()
        assert machineTypeInfoBefore not in machineTypeInfoAfter
    elif  "Changing to a machine type with a different amount of storage will require this" in dialog_message:
        page.get_by_role("button", name="Yes", exact=True).click()
        # page.get_by_text("Restart codespace").click()
        page.wait_for_timeout(10000)
        page.wait_for_selector(".static-screen-message", state="attached")
        button_message_first =  page.locator(".container").text_content()
        if "Restart codespace" in button_message_first:
            page.get_by_text("Restart codespace").click()
            status_text = page.get_by_role("heading", name="Codespace is being updated, you will need to wait for a few minutes for the operation to finish").inner_text()
            assert "Codespace is being updated, you will need to wait for a few minutes for the operation to finish" in status_text
            page.wait_for_timeout(600000)# the page will wait for 10 mins, need to find a way to replace this.
            page_current_url = page.url
            page.goto(page_current_url)
            # page.wait_for_timeout(10000)
            page.wait_for_selector(".static-screen-message", state="attached")
            # page.wait_for_selector(".static-screen-message",state="detached")
            button_message_second =  page.locator(".container").text_content()
            if "Restart codespace" in button_message_second:
                page.get_by_text("Restart codespace").click()
            if "Try again" in button_message_second:
                page.get_by_text("Try again").click()
        elif "Try again" in button_message_first:
            status_text = page.get_by_role("heading", name="Codespace is being updated, you will need to wait for a few minutes for the operation to finish").inner_text()
            assert "Codespace is being updated, you will need to wait for a few minutes for the operation to finish" in status_text
            page.wait_for_timeout(600000)
            page_current_url = page.url
            page.goto(page_current_url)
            # page.wait_for_timeout(10000)
            page.wait_for_selector(".static-screen-message", state="attached")
            button_message_third =  page.locator(".container").text_content()
            if "Restart codespace" in button_message_third:
                page.get_by_text("Restart codespace").click()
            if "Try again" in button_message_third:
                page.get_by_text("Try again").click()      
        page.wait_for_timeout(30000)
        page.locator(".monaco-list > .monaco-scrollable-element").nth(0).click()
        page.keyboard.press("F1")
        page.get_by_placeholder("Type the name of a command to run.").fill(">codespace: Change Machine Type")
        page.wait_for_timeout(10000)
        page.keyboard.press("Enter")
        machineTypeInfoAfter= page.get_by_role("option", name=re.compile(".*(Current machine type)")).text_content()
        assert machineTypeInfoBefore not in machineTypeInfoAfter
        
    else:
        print("Have change the machine type successfully")


@pytest.mark.changemachinetype
def test_change_machine_type_codespace_disconnected(playwright : Playwright):
    tempurl="https://github.com/codespaces?unpublished=true"
    page=test_newtemplatepage(playwright, tempurl)
    page.get_by_role("button", name="Codespace configuration").first.click()
    machine_type_info_before = page.get_by_text(re.compile(".*-core")).first.text_content().replace("\n","").strip()
    page.get_by_role("menuitem", name="Change machine type").click()
    page.wait_for_timeout(1000)
    page.locator("label").filter(has_text=machine_type_info_before).click()
    page.keyboard.press("ArrowDown")
    page.get_by_role("button", name="Update codespace").click()
    if("2-core" in machine_type_info_before):
        alert_message = page.get_by_text(re.compile(".*Changes will take effect the next time your codespace restarts")).text_content()
        assert "Changes will take effect the next time your codespace restarts" in alert_message
    else:
        alert_message = page.get_by_text(re.compile(".*Your codespace will be stopped and unavailable during the update")).text_content()
        assert "Your codespace will be stopped and unavailable during the update" in alert_message
    
    for i in range(20):
        if page.locator("p.f6.mb-0.mr-2.text-small.color-fg-muted", has_text="Changing machine types...").count()>0:
            page.wait_for_timeout(6000)
            page.reload()
        else:
            break
    machine_type_info_after = page.get_by_text(re.compile(".*-core")).first.text_content().replace("\n","").strip()
    assert machine_type_info_after not in machine_type_info_before

def test_stop_codespace_from_index_page(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    codeSpaceStatusBefore = page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(4) > div > div.Box-row > div > div:nth-child(2) > div")
    codeSpaceStatustxtBefore = list(filter(None, codeSpaceStatusBefore.nth(0).text_content().replace("\n","").split(" ")))
    if "Active" in codeSpaceStatustxtBefore:
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Stop codespace").click()
    else:
        print("The codespace status is stopped")
    page.wait_for_timeout(1000)
    # page.close()
    page.reload()
    codeSpaceStatusAfter = page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(4) > div > div.Box-row > div > div:nth-child(2) > div")
    codeSpaceStatustxtAfter = list(filter(None, codeSpaceStatusAfter.nth(0).text_content().replace("\n","").split(" ")))
    assert "Active" not in codeSpaceStatustxtAfter

