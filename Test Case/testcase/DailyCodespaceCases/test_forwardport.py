import pytest
from asyncio import sleep
from playwright.sync_api import Page, Playwright, expect
import re
import string
from test_commonmethod import test_newtemplatepage,test_create_ppe_codespace,test_upload_install_vsix

# 8-core SouthEastAsia
@pytest.mark.forwardport   
def test_codespace_copyports(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?location=SouthEastAsia"
    page=test_newtemplatepage(playwright, tempurl)
    test_create_ppe_codespace(page, "cltest02/publicguestbook")
    
    test_createAndinstall(page, "8-core")
    page.locator("a", has_text="Ports").click()
    page.get_by_role("button", name="Forward a Port").click()
    test_addport(page, "3001")
    page.click("div[id='list_id_4_0']",button="right")
    page.click("text=Copy Local Address")
    page.wait_for_timeout(3000)
    page.keyboard.press("Control+Shift+F")
    page.get_by_placeholder("Search").click()
    page.get_by_placeholder("Search").clear()
    page.keyboard.press("Control+V")
    assert "3001" in page.get_by_placeholder("Search").input_value()

    page.get_by_title("Copy Local Address (Ctrl+C)").click()
    page.get_by_placeholder("Search").click()
    page.get_by_placeholder("Search").clear()
    page.keyboard.press("Control+V")
    assert "3001" in page.get_by_placeholder("Search").input_value()

    page.keyboard.press("Control+Shift+P")
    page.keyboard.type("Copy Forwarded Port Address")
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    page.get_by_placeholder("Search").click()
    page.get_by_placeholder("Search").clear()
    page.keyboard.press("Control+V")
    assert "3001" in page.get_by_placeholder("Search").input_value()

# 16-core WestEurope
@pytest.mark.forwardport   
def test_codespace_openports(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Open in ...").click()
    page.get_by_role("menuitem", name="Open in browser").click()
    page.wait_for_timeout(30000)

    page.locator("a", has_text="Ports").click()
    if "3000" not in page.locator("div[id='list_id_4_0']").inner_text():
        page.locator("a", has_text="Terminal").click()
        page.wait_for_timeout(3000)
        page.type("div.xterm-helpers > textarea", "npm start")
        page.keyboard.press("Enter")
        page.wait_for_timeout(3000)
        page4=page.wait_for_event('popup')
        page4.close()
        page.locator("a", has_text="Ports").click()

    page.wait_for_timeout(1000)
    page.click("div[id='list_id_4_0']",button="right")
    page.wait_for_timeout(500)
    page.click("text=Copy Local Address")
    page.keyboard.press("Control+Shift+F")
    page.get_by_placeholder("Search").click()
    page.get_by_placeholder("Search").clear()
    page.keyboard.press("Control+V")
    url1=page.get_by_placeholder("Search").input_value()
    page1=test_newtemplatepage(playwright,url1)
    assert "Visual Studio Live Share Guestbook" in page1.text_content("h1")
    page1.close()

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
    page.get_by_title("Copy Local Address (Ctrl+C)").click()
    page.get_by_placeholder("Search").click()
    page.get_by_placeholder("Search").clear()
    page.keyboard.press("Control+V")
    url1=page.get_by_placeholder("Search").input_value()
    page2=test_newtemplatepage(playwright,url1)
    assert "Visual Studio Live Share Guestbook" in page2.text_content("h1")
    page2.close()
    page.wait_for_timeout(3000)

    

    

    

# 16-core WestEurope
@pytest.mark.forwardport   
def test_codespace_forward_set_delete_ports(playwright: Playwright):
    # tempurl="https://github.com/codespaces/new?location=WestEurope"
    # page=test_newtemplatepage(playwright, tempurl)
    # test_create_ppe_codespace(page, "cltest02/publicguestbook")
    
    # test_createAndinstall(page, "16-core")
    
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    page.get_by_role("button", name="Codespace configuration").nth(1).click()
    page.get_by_role("menuitem", name="Open in ...").click()
    page.get_by_role("menuitem", name="Open in browser").click()
    page.wait_for_timeout(30000)

    page.locator("a", has_text="Ports").click()
    page.get_by_role("button", name="Forward a Port").click()
    test_addport(page, "3001")
    page.wait_for_timeout(800)
    page.click("div[id='list_id_4_0']",button="right")
    page.locator("text=Forward a Port").click()
    page.keyboard.press("Enter")
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
    page.keyboard.press("Enter")
    page.wait_for_timeout(800)
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
    page.locator("#list_id_4_0").click()
    page.click("div[id='list_id_4_0']",button="right")
    page.get_by_role("menuitem",name="Set Label and Update devcontainer.json").click()
    page.keyboard.press("Enter")
    page.wait_for_timeout(800)
    page.keyboard.type("3061")
    page.keyboard.press("Enter")
    page.wait_for_timeout(800)
    page.locator(".monaco-tl-row", has_text=".devcontainer").click()
    page.wait_for_timeout(800)
    page.locator(".monaco-tl-contents", has_text="devcontainer.json").dblclick()
    devconfigur = '"portsAttributes":{"3031":{"label":"3061"}}'
    assert devconfigur in page.locator(".view-lines.monaco-mouse-cursor-text").inner_text().replace("\xa0","").replace("\n","")
    page.wait_for_timeout(2000)

def test_createAndinstall(page:Page, machinetype: string):
    page.wait_for_timeout(1000)
    #8-core
    page.get_by_role("button", name="2-core").click()
    page.wait_for_timeout(500)
    page.locator(".d-flex.flex-justify-between.mb-1", has_text=machinetype).click()
    page.wait_for_timeout(1000)
    assert page.get_by_role("button", name=machinetype).count()==1

    page.get_by_role("button", name="Create codespace").click()
    page.wait_for_timeout(60000)
    test_upload_install_vsix(page)
    page.wait_for_timeout(3000)


def test_addport(page: Page, port: string):
    page.keyboard.type(port)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2000)
