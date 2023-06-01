import pytest
from playwright.sync_api import Page, Playwright
import string
from test_commonmethod import test_newtemplatepage,test_open_page_sso,test_create_ppe_codespace,test_createAndinstall
from test_delete_codespace import test_deleteAllCodespace 

@pytest.mark.daily
@pytest.mark.forwardport
def test_delete_all_codespaces(playwright: Playwright):
    test_deleteAllCodespace(playwright)

@pytest.mark.daily
@pytest.mark.forwardport
def test_codespace_copyports(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?location=SouthEastAsia"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        test_create_ppe_codespace(page, "cltest02/publicguestbook")
        
        test_createAndinstall(page, "8-core")

        page.locator("a", has_text="Ports").click()
        page.get_by_role("button", name="Forward a Port").click()
        test_addport(page, "3071")
        page.locator(".monaco-icon-label-container", has_text="3071").nth(0).click()
        page.locator(".monaco-icon-label-container", has_text="3071").nth(0).click(button="right")
        page.click("text=Copy Local Address")
        page.keyboard.press("Enter")
        page.wait_for_timeout(3000)
        page.keyboard.press("Control+Shift+F")
        page.get_by_placeholder("Search").click()
        page.get_by_placeholder("Search").clear()
        page.keyboard.press("Control+V")
        assert "3071" in page.get_by_placeholder("Search").input_value()

        page.get_by_title("Copy Local Address (Ctrl+C)").click()
        page.get_by_placeholder("Search").click()
        page.get_by_placeholder("Search").clear()
        page.keyboard.press("Control+V")
        assert "3071" in page.get_by_placeholder("Search").input_value()

        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Copy Forwarded Port Address")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.get_by_placeholder("Search").click()
        page.get_by_placeholder("Search").clear()
        page.keyboard.press("Control+V")
        assert "3071" in page.get_by_placeholder("Search").input_value()
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.forwardport
def test_codespace_openports(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        test_opencodespace_runnpm(page)

        page.wait_for_timeout(1000)
        page.get_by_label("Port has running process").nth(0).click()
        page.get_by_label("Port has running process").nth(0).click(button="right")
        # page.click("div[id='list_id_4_0']",button="right")
        page.wait_for_timeout(500)
        page.click("text=Copy Local Address")
        page.keyboard.press("Enter")
        page.keyboard.press("Control+Shift+F")
        page.get_by_placeholder("Search").click()
        page.get_by_placeholder("Search").clear()
        page.keyboard.press("Control+V")
        url1=page.get_by_placeholder("Search").input_value()
        page1=test_newtemplatepage(playwright,url1)
        page.wait_for_timeout(2000)
        assert "Visual Studio Live Share Guestbook" in page1.text_content("h1")
        page1.close()
        page.wait_for_timeout(3000)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Copy Forwarded Port Address")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.get_by_placeholder("Search").click()
        page.get_by_placeholder("Search").clear()
        page.keyboard.press("Control+V")
        url2=page.get_by_placeholder("Search").input_value()
        page2=test_newtemplatepage(playwright,url2)
        page2.close()

        page.wait_for_timeout(3000)
        page.get_by_label("Port has running process").nth(0).click()
        page.get_by_role("listitem", name="Copy Local Address (Ctrl+C)").click()
        page.get_by_placeholder("Search").click()
        page.get_by_placeholder("Search").clear()
        page.keyboard.press("Control+V")
        url3=page.get_by_placeholder("Search").input_value()
        page3=test_newtemplatepage(playwright,url3)
        page.wait_for_timeout(2000)
        assert "Visual Studio Live Share Guestbook" in page3.text_content("h1")
        page3.close()
        page.wait_for_timeout(3000)
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.forwardport   
def test_codespace_openPublicPort(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    browser = playwright.chromium.launch(headless=False)
    try:
        context = browser.new_context(storage_state="cway")
        page = context.new_page()
        page.goto(tempurl)
        test_opencodespace_runnpm(page)
        page.wait_for_timeout(1000)
        page.click("div[id='list_id_4_0']",button="right")
        page.wait_for_timeout(500)
        page.click("text=Preview in Editor")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        assert page.get_by_role("tab").get_by_title("Simple Browser").is_visible()

        page.click("div[id='list_id_4_0']",button="right")
        page.wait_for_timeout(500)
        page.click("text=Port Visibility")
        page.wait_for_timeout(500)
        page.get_by_role("menuitemcheckbox", name="Public").click()
        page.wait_for_timeout(1500)
        page.get_by_label("Port has running process").nth(0).click()
        page.get_by_role("listitem", name="Copy Local Address (Ctrl+C)").click()
        
        page.keyboard.press("Control+Shift+F")
        page.get_by_placeholder("Search").click()
        page.get_by_placeholder("Search").clear()
        page.keyboard.press("Control+V")
        url1=page.get_by_placeholder("Search").input_value()
        page1 = context.new_page()
        page1.goto(url1)
        page.wait_for_timeout(1000)
        assert "Visual Studio Live Share Guestbook" in page1.text_content("h1")
        page1.close()
        #remove a public port
        if "3031" not in page.locator(".monaco-table.table_id_1").inner_text():
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Add Port").click()
            test_addport(page, "3031")
            page.wait_for_timeout(500)
        page.locator(".monaco-icon-label-container", has_text="3031").nth(0).click()
        page.locator(".monaco-icon-label-container", has_text="3031").nth(0).click(button="right")
        page.wait_for_timeout(500)
        page.click("text=Port Visibility")
        page.wait_for_timeout(500)
        page.get_by_role("menuitemcheckbox", name="Public").click()
        page.wait_for_timeout(1500)
        page.get_by_role("button", name="Stop Forwarding Port (Delete)").click()
        page.wait_for_timeout(500)
        page.get_by_role("button", name="Add Port").click()
        test_addport(page, "3031")
        page.wait_for_timeout(500)
        page.locator(".monaco-icon-label-container", has_text="3031").nth(0).click()
        page.locator(".monaco-icon-label-container", has_text="3031").nth(0).click(button="right")
        page.click("text=Port Visibility")
        assert page.get_by_role("menuitemcheckbox", name="Private").is_checked()
        page.wait_for_timeout(500)
        page.get_by_role("menuitemcheckbox", name="Public").click()
        page.wait_for_timeout(2000)
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.forwardport   
def test_codespace_protocol_ports(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(30000)

        page.locator("a", has_text="Ports").click()
        if "3081" not in page.locator(".monaco-table.table_id_1").inner_text():
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Add Port").click()
            test_addport(page, "3081")
            page.wait_for_timeout(500)
        #change port protocol
        page.wait_for_timeout(2000)
        page.locator(".monaco-icon-label-container", has_text="3081").nth(0).click()
        page.locator(".monaco-icon-label-container", has_text="3081").nth(0).click(button="right")
        page.click("text=Change Port Protocol")
        if not page.get_by_role("menuitemcheckbox", name="HTTPS").is_checked():
            page.get_by_role("menuitemcheckbox", name="HTTPS").click()
            page.wait_for_timeout(500)
            page.locator(".monaco-icon-label-container", has_text="3081").nth(0).click()
            page.locator(".monaco-icon-label-container", has_text="3081").nth(0).click(button="right")
            page.click("text=Change Port Protocol")
            page.wait_for_timeout(1500)
            page.get_by_role("menuitemcheckbox",name="HTTP").nth(0).click()
            page.wait_for_timeout(1000)
            page.locator(".monaco-icon-label-container", has_text="3081").nth(0).click()
            page.locator(".monaco-icon-label-container", has_text="3081").nth(0).click(button="right")
            page.click("text=Change Port Protocol")
            # assert page.get_by_role("menuitemcheckbox", name="HTTPS").is_checked()
        if page.get_by_role("menuitemcheckbox", name="HTTPS").is_checked():
            page.get_by_role("menuitemcheckbox",name="HTTP").nth(0).click()
            page.wait_for_timeout(500)
            page.locator(".monaco-icon-label-container", has_text="3081").nth(0).click()
            page.locator(".monaco-icon-label-container", has_text="3081").nth(0).click(button="right")
            page.click("text=Change Port Protocol")
            page.wait_for_timeout(1500)
            page.get_by_role("menuitemcheckbox", name="HTTPS").click()
            # assert page.get_by_role("menuitemcheckbox",name="HTTP", exact=True).is_checked()
        page.wait_for_timeout(800)
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.forwardport   
def test_codespace_forward_set_delete_ports(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(30000)

        page.locator("a", has_text="Ports").click()
        if page.get_by_role("button", name="Forward a Port").is_visible():
            page.get_by_role("button", name="Forward a Port").click()
        else :
            if page.get_by_role("button", name="Add Port").is_visible():
                page.get_by_role("button", name="Add Port").click()
        if "3001" not in page.locator(".monaco-table.table_id_1").inner_text():
            test_addport(page, "3001")
        page.wait_for_timeout(800)
        page.click("div[id='list_id_4_0']",button="right")
        page.locator("text=Forward a Port").click()
        # page.keyboard.press("Enter")
        test_addport(page, "3011")
        
        page.wait_for_timeout(800)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Forward a Port")
        page.keyboard.press("Enter")
        test_addport(page, "3021")
        page.wait_for_timeout(800)
        page.get_by_role("button", name="Add Port").click()
        test_addport(page, "3031")
        page.wait_for_timeout(1000)
        assert "3001" and "3011" and "3021" and "3031" in page.locator(".monaco-table.table_id_1").inner_text()
        page.wait_for_timeout(1000)

        #Set a label for port
        page.locator("#list_id_4_0").click()
        page.click("div[id='list_id_4_0']",button="right")
        page.locator("text=Set Port Label").click()
        # page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        page.keyboard.type("3041")
        page.keyboard.press("Enter")
        page.wait_for_timeout(800)
        page.locator("#list_id_4_1").click()
        page.get_by_role("button", name="Set Port Label (F2)").click()
        page.wait_for_timeout(800)
        page.keyboard.type("3051")
        page.keyboard.press("Enter")
        page.wait_for_timeout(800)
        assert "3041" and "3051" in page.locator(".monaco-table.table_id_1").inner_text()
        #delete port
        page.locator("#list_id_4_0").click()
        page.click("div[id='list_id_4_0']",button="right")
        page.get_by_role("menuitem",name="Stop Forwarding Port").click()
        page.keyboard.press("Enter")
        page.wait_for_timeout(800)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Stop Forwarding Port")
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)
        page.keyboard.type("3021")
        page.keyboard.press("Enter")
        page.wait_for_timeout(800)
        page.locator("#list_id_4_0").click()
        page.get_by_role("button", name="Stop Forwarding Port (Delete)").click()
        page.wait_for_timeout(800)
        assert "3031" in page.locator(".monaco-table.table_id_1").inner_text()
        page.wait_for_timeout(1000)
        page.locator(".monaco-icon-label-container", has_text="3031").nth(0).click()
        page.locator(".monaco-icon-label-container", has_text="3031").nth(0).click(button="right")
        page.get_by_role("menuitem",name="Set Label and Update devcontainer.json").click()
        # page.keyboard.press("Enter")
        page.wait_for_timeout(800)
        page.keyboard.type("3061")
        page.keyboard.press("Enter")
        page.wait_for_timeout(800)
        page.keyboard.press("Control+Shift+E")
        page.locator(".monaco-tl-row", has_text=".devcontainer").click()
        page.wait_for_timeout(800)
        page.locator(".monaco-tl-contents", has_text="devcontainer.json").dblclick()
        devconfigur = '"3031":{"label":"3061"}}'
        assert devconfigur in page.locator(".view-lines.monaco-mouse-cursor-text").inner_text().replace("\xa0","").replace("\n","")
        page.wait_for_timeout(2000)
    finally:
        page.close()

def test_opencodespace_runnpm(page:Page):
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Open in ...").click()
    page.get_by_role("menuitem", name="Open in browser").click()
    page.wait_for_timeout(30000)

    page.locator("a", has_text="Ports").click()
    page.wait_for_timeout(9000)
    if page.locator("p",  has_text="No forwarded ports. Forward a port to access your running services locally.").is_visible() or not page.get_by_label("Port has running process").is_visible():
        page.keyboard.press("Control+Shift+`")
        page.wait_for_timeout(3000)
        page.type("div.xterm-helpers > textarea", "npm start")
        page.keyboard.press("Enter")
        page4=page.wait_for_event('popup')
        page.wait_for_timeout(1000)
        page4.close()
        page.get_by_text("Ports", exact=True).click()

def test_addport(page: Page, port: string):
    page.keyboard.type(port)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2000)
