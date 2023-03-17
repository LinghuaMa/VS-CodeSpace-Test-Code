import string
import json
import uuid
import pytest
from playwright.async_api import Page, Playwright, Browser
from test_commoncode import test_newtemplatepage,test_terminalcommand,test_getgithubuserrepo, test_terminalothertemplatecommand

#region Blank Template
@pytest.mark.blanktemplatecreatecodespace
def test_blank_template_create_codespace_(playwright: Playwright) -> None:
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(1) > div > div:nth-child(3) > form > button"
    new_page=chooseppeoption(playwright,usethistempbuttonselector)
    commondactionselecter="#terminal > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.shell-integration.integrated-terminal.wide > div.monaco-split-view2.horizontal > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-decoration-container > div.codicon.error.terminal-command-decoration.xterm-decoration.codicon-terminal-decoration-error"
    terminaltextarea="#terminal > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.shell-integration.integrated-terminal.wide > div.monaco-split-view2.horizontal > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-helpers > textarea"
    test_excutecommandandvalidate(new_page,commondactionselecter,terminaltextarea,"git status","fatal: not a git repository")
    test_addnewfileandnavigatetosoucontrol(new_page)

    publishtogithubselector="#workbench\.view\.scm > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.welcome > div.welcome-view > div > div.welcome-view-content > div > a"
    new_page.locator(publishtogithubselector).click()
    
    #rename reponame
    reponameselector="#js-vscode-workbench-placeholder > div > div.quick-input-widget.show-file-icons > div.quick-input-header > div.quick-input-and-message > div.quick-input-filter > div.quick-input-box > div > div.monaco-inputbox.idle > div > input"
    oldreponame=new_page.locator(reponameselector).input_value()
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
#endregion Blank Template

#region Other Templates
def test_othertempcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(3) > div > div:nth-child(3) > form > button"
    codespace_page=chooseppeoption(playwright,usethistempbuttonselector)
    codespace_page.wait_for_timeout(6000)
    # open devcontainer.json file
    devcontainerselector="#list_id_2_0 > div > div.monaco-tl-twistie.collapsible.codicon.codicon-tree-item-expanded"
    codespace_page.locator(devcontainerselector).click()
    codespace_page.wait_for_timeout(1000)
    fileselector="#list_id_2_1 > div > div.monaco-tl-contents > div > div > span > a"
    codespace_page.locator(fileselector).click()
    jsonfiletextselector="#workbench\.parts\.editor > div.content > div > div > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.editor-container > div > div > div.overflow-guard > div.monaco-scrollable-element.editor-scrollable.vs > div.lines-content.monaco-editor-background > div.view-lines.monaco-mouse-cursor-text"
    openfilenameselector='#workbench\\.parts\\.editor > div.content > div > div > div > div > div.monaco-scrollable-element > div.split-view-container > div:nth-child(1) > div > div.title.tabs.show-file-icons > div.tabs-and-actions-container > div.monaco-scrollable-element > div.tabs-container > div:nth-child(1) > div.monaco-icon-label.file-icon.src-name-dir-icon.app\\.js-name-file-icon.name-file-icon.js-ext-file-icon.ext-file-icon.javascript-lang-file-icon.tab-label.tab-label-has-badge > div'
    assert codespace_page.locator(openfilenameselector).inner_text() in codespace_page.locator(jsonfiletextselector).inner_text()
    codespace_page.wait_for_timeout(1000)
    assert "npm\xa0start" in codespace_page.locator(jsonfiletextselector).inner_text()
    #open a new terminal and validate git status
    codespace_page.wait_for_timeout(5000)

    bashselector="#list_id_1_0 > div > div > div.monaco-icon-label-container"
    codespace_page.locator(bashselector).click()
    terminalareaselector="#terminal > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.shell-integration.integrated-terminal.wide > div.monaco-split-view2.horizontal > div.monaco-scrollable-element > div.split-view-container > div:nth-child(1) > div > div > div:nth-child(1) > div > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-helpers > textarea"
    commondactionselecter="#terminal > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.shell-integration.integrated-terminal.wide > div.monaco-split-view2.horizontal > div.monaco-scrollable-element > div.split-view-container > div:nth-child(1) > div > div > div:nth-child(1) > div > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-decoration-container > div.terminal-command-decoration.codicon.xterm-decoration.codicon-terminal-decoration-success"
    
    test_excutecommandandvalidate(codespace_page, terminalareaselector, commondactionselecter, "git status","nothing to commit, working tree clean")
    commondactionselecter="#terminal > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.shell-integration.integrated-terminal.wide > div.monaco-split-view2.horizontal > div.monaco-scrollable-element > div.split-view-container > div:nth-child(1) > div > div > div:nth-child(1) > div > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-decoration-container > div:nth-child(2)"
    test_excutecommandandvalidate(codespace_page, terminalareaselector, commondactionselecter, "git log","Initial commit")
    
    test_addnewfileandnavigatetosoucontrol(new_page)
    test_terminalcommand(codespace_page, "npm start")

    test_validatepublishbutton(codespace_page, "react")
    
    # Export/Publish from /Codespaces
    codespace_page.goto("https://github.com/codespaces?unpublished=true")
    spaceconfig='body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(3) > div > div.Box-row > div > div:nth-child(2) > div > div.right-0.top-0.top-lg-auto.right-lg-auto.position-absolute.position-lg-relative > options-popover>details:nth-child(1)'
    summaryselector=spaceconfig+">summary"
    codespace_page.query_selector_all(summaryselector)[0].click()
    publishareposelector=spaceconfig+"> details-menu > button:nth-child(4) > span"
    codespace_page.query_selector_all(publishareposelector)[0].click()
    codespace_page.wait_for_timeout(1000)
    publishreponameselector="#publish-codespace-repo-name"
    guid = uuid.uuid4().hex
    codespace_page.query_selector_all(publishreponameselector)[0].fill(tempname+guid)
    button="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(3) > div > div:nth-child(2) > div > div:nth-child(2) > div > div.right-0.top-0.top-lg-auto.right-lg-auto.position-absolute.position-lg-relative > options-popover > details:nth-child(3) > details-dialog>div:nth-child(3)>export-branch>div>form>button"
    codespace_page.query_selector_all(button)[0].click()
    test_getgithubuserrepo(codespace_page, tempname+guid)
    codespace_page.wait_for_timeout(3000)

def chooseppeoption(playwright:Playwright,usethistempbuttonselector:string)->Page:
    tempurl="https://github.com/codespaces/templates"
    page=test_newtemplatepage(playwright, tempurl)
    assert "Choose a template" in page.text_content('h1')

    ppeselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > div > div:nth-child(2) > div > select"
    page.locator(ppeselector).click()
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    assert page.locator(ppeselector).input_value()=="ppe"
    page.locator(usethistempbuttonselector).click()
    new_page=page.wait_for_event('popup')
    return new_page

#create a new file named htmltest.html and Navigate to the Source Control panel
def test_addnewfileandnavigatetosoucontrol(new_page:Page):
    new_page.keyboard.press("Control+Shift+E")
    newfileactionselector="#workbench\.view\.explorer > div > div > div.monaco-scrollable-element > div.split-view-container > div:nth-child(1) > div > div.pane-header.expanded > div.actions > div > div > ul > li:nth-child(1)"
    new_page.locator(newfileactionselector).click()
    new_page.keyboard.type("htmltest.html")
    new_page.keyboard.press("Enter")
    new_page.wait_for_timeout(1500)
    new_page.keyboard.press("Enter")
    new_page.keyboard.type("<html>htmltest</html>")
    sourcecontrolselector="#workbench\.parts\.activitybar > div > div.composite-bar > div > ul > li:nth-child(3) > a"
    new_page.locator(sourcecontrolselector).click()

def test_excutecommandandvalidate(codespace_page:Page, terminaltextarea:string, commondactionselecter:string,  terminalcommand:string, assertstr:string):
    test_terminalothertemplatecommand(codespace_page, terminalcommand,terminaltextarea)
    codespace_page.locator(commondactionselecter).click()
    for i in range(3):
        codespace_page.keyboard.press("ArrowDown")
    codespace_page.keyboard.press("Enter")
    searchselector="#workbench\.parts\.activitybar > div > div.composite-bar > div > ul > li:nth-child(2) > a"
    codespace_page.locator(searchselector).click()
    searchtextarea="#workbench\.view\.search > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body > div.search-view.actions-right > div.search-widgets-container > div.search-widget > div.search-container.input-box > div > div.monaco-scrollable-element > div.monaco-inputbox.idle > div > textarea"
    codespace_page.locator(searchtextarea).click()
    codespace_page.keyboard.press("Control+V")
    assert assertstr in codespace_page.locator(searchtextarea).input_value()
#endregion Other Templates