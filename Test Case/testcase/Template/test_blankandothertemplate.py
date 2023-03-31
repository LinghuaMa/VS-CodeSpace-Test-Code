import string
import json
import uuid
import pytest
from playwright.async_api import Page, Playwright, Browser
from test_commoncode import test_newtemplatepage,test_terminalcommand,test_getgithubuserrepo, test_terminalothertemplatecommand

#region Blank Template
@pytest.mark.blanktemplate
def test_blank_template_create_codespace_(playwright: Playwright) -> None:
    new_page=chooseppeoption(playwright,"Blank")
    commondactionselecter="div.codicon.error.terminal-command-decoration.xterm-decoration.codicon-terminal-decoration-error"
    terminaltextarea="div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-helpers > textarea"
    test_excutecommandandvalidate(new_page,terminaltextarea,commondactionselecter,"git status","fatal: not a git repository")
    test_addnewfileandnavigatetosoucontrol(new_page)
    new_page.get_by_role("button").filter(has_text="Publish to GitHub").click()
    
    oldreponame=new_page.get_by_role("combobox").input_value()
    guid = uuid.uuid4().hex
    new_page.locator(reponameselector).fill(oldreponame+guid)
    new_page.wait_for_timeout(1000)
    new_page.keyboard.press("ArrowDown")
    new_page.keyboard.press("Enter")
    new_page.wait_for_timeout(1000)
    new_page.keyboard.press("Tab")
    new_page.keyboard.press("Enter")
    new_page.wait_for_timeout(3000)

    test_getgithubuserrepo(new_page, oldreponame+guid)
    new_page.wait_for_timeout(3000)
    new_page.close()
#endregion Blank Template

#region Other Templates
@pytest.mark.railstemplate
def test_rubyonrailstemplate(playwright: Playwright):
    test_othertempcodespace("Ruby on Rails", "rails\xa0server", playwright)

@pytest.mark.reacttemplate
def test_reacttemplate(playwright: Playwright):
    test_othertempcodespace("React By github A pop", "npm\xa0start", playwright)

@pytest.mark.jupytertemplate
def test_jupytertemplate(playwright: Playwright):
    test_othertempcodespace("Jupyter Notebook","npm\xa0start", playwright)

@pytest.mark.expresstemplate
def test_expresstemplate(playwright: Playwright):
    test_othertempcodespace("Express","npm\xa0start", playwright)

@pytest.mark.nextjstemplate
def test_nextjstemplate(playwright: Playwright):
    test_othertempcodespace("Next.js By github Next.js","npm\xa0run\xa0dev",playwright)

@pytest.mark.djangotemplate
def test_djangotemplate(playwright: Playwright):
    test_othertempcodespace("Django","python\xa0manage.py\xa0runserver",playwright)

@pytest.mark.flasktemplate
def test_flasktemplate(playwright: Playwright):
    test_othertempcodespace("Flask","flask\xa0--debug\xa0run",playwright)

@pytest.mark.preacttemplate
def test_preacttemplate(playwright: Playwright):
    test_othertempcodespace("Preact By github A fast","npm\xa0run\xa0dev",playwright)

def test_othertempcodespace(hastext: string, assertserver:string, playwright: Playwright):
    codespace_page=chooseppeoption(playwright,hastext)
    codespace_page.wait_for_load_state()
    codespace_page.wait_for_timeout(10000)
    # open devcontainer.json file
    devcontainerselector="#list_id_2_0 > div > div.monaco-tl-twistie.collapsible.codicon.codicon-tree-item-expanded"
    codespace_page.locator(devcontainerselector).click()
    codespace_page.wait_for_timeout(1000)
    fileselector="#list_id_2_1 > div > div.monaco-tl-contents > div > div > span > a"
    codespace_page.locator(fileselector).click()
    jsonfiletextselector="div:nth-child(3) > div > div > div > div > div:nth-child(3) > div > div > div > div.split-view-container > div:nth-child(1)"
    openfilenameselector=".tab.tab-actions-right.sizing-fit.has-icon"
    codespace_page.wait_for_timeout(1000)
    jsonfiletext=codespace_page.locator(jsonfiletextselector).inner_text()
    if "jupyter" not in jsonfiletext:
        assert codespace_page.query_selector_all(openfilenameselector)[0].inner_text() in jsonfiletext
        codespace_page.wait_for_timeout(1000)
        assert assertserver in jsonfiletext
        #open a new terminal and validate git status
        codespace_page.wait_for_timeout(10000)

        bashselector="#list_id_1_0 > div > div > div.monaco-icon-label-container"
        codespace_page.locator(bashselector).click()
    codespace_page.wait_for_timeout(10000)
    #validate git-status
    terminalareaselector="div:nth-child(1) > div > div > div > div > div > div > div > div > div.xterm-screen > div.xterm-helpers > textarea"
    commondactionselecter="div.terminal-command-decoration.codicon.xterm-decoration.codicon-terminal-decoration-success"
    test_excutecommandandvalidate(codespace_page, terminalareaselector, commondactionselecter, "git status","nothing to commit, working tree clean")
    #validate git-log       div.xterm-decoration-container > div:nth-child(2)
    commondactionselecter="div.xterm-decoration-container > div:nth-child(2)"
    test_excutecommandandvalidate(codespace_page, terminalareaselector, commondactionselecter, "git log","Initial commit")
    
    test_addnewfileandnavigatetosoucontrol(codespace_page)
    codespace_page.keyboard.type("add a test html file")
    codespace_page.wait_for_timeout(1000)
    changelistid="#list_id_6_2"
    commitlistid="#list_id_6_1"
    if "jupyter" in jsonfiletext:
        changelistid="#list_id_7_2"
        commitlistid="#list_id_7_1"
    changesselector=changelistid+" > div > div.monaco-tl-contents > div > div.name"
    codespace_page.locator(changesselector).hover()
    sageallselector=changelistid+" > div > div.monaco-tl-contents > div > div.actions > div > ul > li:nth-child(2) > a"
    codespace_page.locator(sageallselector).click()
    codespace_page.wait_for_timeout(1000)
    commitbuttonselector=commitlistid+" > div > div.monaco-tl-contents > div > div > a.monaco-button.monaco-text-button"
    codespace_page.locator(commitbuttonselector).click()
    codespace_page.wait_for_timeout(1000)
    portsselector="#workbench\.parts\.panel > div.composite.title > div.composite-bar.panel-switcher-container > div > ul>li:nth-child(5)"
    
    if "jupyter" not in jsonfiletext:
        if codespace_page.locator(portsselector).get_attribute('aria-selected')=="false":
            codespace_page.locator(portsselector).click()
        runningprocessselector="#list_id_8_0 > div > div:nth-child(4) > div > div.monaco-icon-label > div"
        for i in range(50):
            if codespace_page.locator(runningprocessselector).inner_text()=="":
                codespace_page.wait_for_timeout(5000)
            else:
                break
        codespace_page.wait_for_timeout(5000)
        simplebrowserselector="#workbench\.parts\.editor > div.content > div > div > div > div > div.monaco-scrollable-element > div.split-view-container > div:nth-child(2) > div > div.title.tabs.show-file-icons > div.tabs-and-actions-container > div.monaco-scrollable-element > div.tabs-container > div:nth-child(1) >div:nth-child(2)"

        assert 'Simple Browser' in codespace_page.locator(simplebrowserselector).inner_text()
    
    codespace_page.wait_for_timeout(1000)
    publishselector=commitlistid+" > div > div.monaco-tl-contents > div > a"
    codespace_page.locator(publishselector).click()
    reponame="#js-vscode-workbench-placeholder > div > div.quick-input-widget.show-file-icons > div.quick-input-header > div.quick-input-and-message > div.quick-input-filter > div.quick-input-box > div > div.monaco-inputbox.idle > div > input"
    oldreponame=codespace_page.locator(reponame).input_value()
    guid = uuid.uuid4().hex
    codespace_page.locator(reponame).fill(oldreponame+guid)
    codespace_page.wait_for_timeout(2000)
    codespace_page.keyboard.press("ArrowDown")
    codespace_page.keyboard.press("Enter")
    codespace_page.wait_for_timeout(2000)
    test_getgithubuserrepo(codespace_page, oldreponame+guid)
    codespace_page.wait_for_timeout(3000)
    codespace_page.close()    

def chooseppeoption(playwright:Playwright,hastext: string)->Page:
    tempurl="https://github.com/codespaces/templates"
    page=test_newtemplatepage(playwright, tempurl)
    assert "Choose a template" in page.text_content('h1')

    page.locator(".form-select.mt-1.color-bg-subtle").nth(0).click()
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    assert page.locator(".form-select.mt-1.color-bg-subtle").nth(0).input_value()=="ppe"
    page.locator("li",has_text=hastext).locator("button").click()
    new_page=page.wait_for_event('popup')
    return new_page

#create a new file named htmltest.html and Navigate to the Source Control panel
def test_addnewfileandnavigatetosoucontrol(new_page:Page)->Page:
    new_page.keyboard.press("Control+Shift+E")
    new_page.get_by_role("button",name="New File...").click()
    new_page.keyboard.type("htmltest.html")
    new_page.keyboard.press("Enter")
    new_page.wait_for_timeout(1500)
    new_page.keyboard.press("Enter")
    new_page.keyboard.type("<html>htmltest</html>")
    new_page.keyboard.press("Control+Shift+G")
    new_page.wait_for_timeout(1000)
    return new_page

def test_excutecommandandvalidate(codespace_page:Page, terminaltextarea:string, commondactionselecter:string,  terminalcommand:string, assertstr:string):
    if "fatal: not a git repository"!=assertstr:
        bashselector="#list_id_1_0 > div > div > div.monaco-icon-label-container"
        codespace_page.locator(bashselector).click()
    test_terminalothertemplatecommand(codespace_page, terminalcommand,terminaltextarea,assertstr)
    codespace_page.wait_for_timeout(2000)
    codespace_page.locator(commondactionselecter).click()
    for i in range(3):
        codespace_page.keyboard.press("ArrowDown")
    codespace_page.keyboard.press("Enter")
    if terminalcommand!="git log":
        searchselector="#workbench\.parts\.activitybar > div > div.composite-bar > div > ul > li:nth-child(2) > a"
        codespace_page.locator(searchselector).click()
    codespace_page.get_by_placeholder("Search").click()
    codespace_page.get_by_placeholder("Search").clear()
    codespace_page.keyboard.press("Control+V")
    codespace_page.wait_for_timeout(500)
    if "fatal: not a git repository"!=assertstr:
        if codespace_page.locator('#list_id_1_0').get_attribute('aria-selected')=="false":
            bashselector="#list_id_1_0 > div > div > div.monaco-icon-label-container"
            codespace_page.locator(bashselector).click()
    assert assertstr in codespace_page.get_by_placeholder("Search").input_value()
#endregion Other Templates