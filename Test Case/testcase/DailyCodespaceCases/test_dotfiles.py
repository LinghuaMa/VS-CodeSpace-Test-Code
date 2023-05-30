import pytest
import string
import getpass
from playwright.sync_api import Page, Playwright
from test_commonmethod import test_getusenamefromcookiefile,test_create_ppe_codespace,test_createAndinstall,test_newtemplatepage
from test_delete_codespace import test_deleteAllCodespace 

@pytest.mark.dotfiles
def test_delete_all_codespaces(playwright: Playwright):
    test_deleteAllCodespace(playwright)

@pytest.mark.dotfiles
def test_enable_autimaticlly_donot_executable_script(playwright: Playwright):
    pageurl="https://github.com/settings/codespaces"
    page=test_newtemplatepage(playwright,pageurl)
    try:
        if not page.locator("#codespace_dotfiles_enabled").is_checked():
            page.locator("#codespace_dotfiles_enabled").click()
            page.wait_for_timeout(2000)
        assert page.locator("#codespace_dotfiles_enabled").is_checked()
        page.get_by_role("button", name=test_getusenamefromcookiefile()).click()
        page.get_by_role("textbox", name="Search for a repository").fill("dotfile")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        page.goto("https://github.com/codespaces/new?location=EastUs")
        test_create_ppe_codespace(page, "cltest02/publicguestbook")
        page.get_by_role("button", name="Create codespace").click()
        page.wait_for_timeout(150000)
        for i in range(page.get_by_label("Close (Ctrl+F4)").count()):
            page.get_by_label("Close (Ctrl+F4)").nth(0).click()
        page.wait_for_timeout(1000)
        page.keyboard.press("Control+Shift+P")
        page.wait_for_timeout(400)
        page.keyboard.type("codespaces: view creation log")
        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(400)
        page.keyboard.press("Enter")
        page.wait_for_timeout(3500)
        page.keyboard.press("Control+F")
        page.wait_for_timeout(1000)
        page.get_by_placeholder("Find").fill("dotfiles")
        filtertext=page.locator(" div.split-view-container > div:nth-child(1) > div > div > div > div > div > div> div > div.view-lines.monaco-mouse-cursor-text").inner_text().replace("\xa0", " ")
        assert "$ # Clone & install dotfiles" in filtertext
        assert "Cloning into \'/workspaces/.codespaces/.persistedshare/dotfiles\'" in filtertext
        page.wait_for_timeout(3000)
        page.keyboard.press("Control+Shift+`")
        page.wait_for_timeout(2000)
        cdpath="cd /workspaces/.codespaces/.persistedshare/dotfiles"
        labelname="Terminal 3, bash"
        dotfiles= "./.config_dotfiles_default.gitattributes.load.wgetrc../.curlrc.gitconfig.macos.xbindkeysrc.IGNORE.dircolors.gitignore.minttyrc.zprofile.ackrc.dotfilecheck.gitignore_global.osx.zshrc.aliases.editorconfig.gitmessage.redpill/LICENSE-MIT.txt.bash_complete.exports.global_gitignore.screenrcREADME.md.bash_logout.fonts/.gvimrc.shellrcbin/.bash_profile.functions.hgignore.tmux.confexamples/.bashrc.gdbinit.hushlogin.travis.ymlfirstInstallCygwin.sh*.colordiffrc.gemrc.icons.vim/firstInstallDebianBased.sh*.colors.git/.inputrc.vimrc.config/.git-templates/.irbrc.vimrc.bundles"
        test_execute_command(page, labelname, cdpath, dotfiles)

        page.keyboard.press("Control+Shift+`")
        page.wait_for_timeout(2000)
        page.get_by_role("listitem", name="Terminal 3 bash").locator("a", has_text="bash").hover()
        page.get_by_title("Kill (Delete)").nth(1).click()
        cdpath="cd ~"
        labelname="Terminal 4, bash"
        atfiles="./.config/.gemrc@.icons@.oh-my-zsh/.travis.yml@../.config_dotfiles_default@.git-templates@.inputrc@.osx@.vim@.IGNORE@.curlrc@.gitattributes@.irbrc@.php/.vimrc@.ackrc@.dircolors@.gitconfig@.jupyter/.profile.vimrc.bundles@.aliases@.docker@.gitignore@.load@.python/.vscode-remote/.bash_complete@.dotfilecheck@.gitignore_global@.local/.rbenv/.wgetrc@.bash_logout@.dotnet@.gitmessage@.macos@.redpill@.xbindkeysrc@.bash_profile@.editorconfig@.global_gitignore@.maven/.ruby/.yarn/.bashrc@.exports@.gvimrc@.minikube/.rvmrc.zprofile@.cache/.fonts@.hgignore@.minttyrc@.screenrc@.zshrc@.colordiffrc@.functions@.hugo/.npm/.shellrc@java@.colors@.gdbinit@.hushlogin@.nvs/.tmux.conf@nvm@"
        test_execute_command(page,labelname ,cdpath, atfiles) 
    finally:
        page.goto("https://github.com/settings/codespaces")
        if page.locator("#codespace_dotfiles_enabled").is_checked():
            page.wait_for_timeout(600)
            page.locator("#codespace_dotfiles_enabled").click()
        page.close()

@pytest.mark.dotfiles
def test_enable_autimaticlly_have_executable_script(playwright: Playwright):
    pageurl="https://github.com/settings/codespaces"
    page=test_newtemplatepage(playwright,pageurl)
    try:
        if not page.locator("#codespace_dotfiles_enabled").is_checked():
            page.locator("#codespace_dotfiles_enabled").click()
            page.wait_for_timeout(2000)  
        assert page.locator("#codespace_dotfiles_enabled").is_checked()
        page.get_by_role("button", name=test_getusenamefromcookiefile()).click()
        page.wait_for_timeout(999)
        page.get_by_role("textbox", name="Search for a repository").fill("dotfile-2")
        page.wait_for_timeout(1200)
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        assert page.locator("p", has_text="Changes saved").is_visible()

        page.goto("https://github.com/codespaces/new?location=EastUs")
        test_create_ppe_codespace(page, "cltest02/publicguestbook")
        page.get_by_role("button", name="Create codespace").click()
        page.wait_for_timeout(150000)
        for i in range(page.get_by_label("Close (Ctrl+F4)").count()):
            page.get_by_label("Close (Ctrl+F4)").nth(0).click()
        page.wait_for_timeout(1000)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("codespaces: view creation log")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(3500)
        page.keyboard.press("Control+F")
        page.wait_for_timeout(1000)
        page.get_by_placeholder("Find").fill("dotfiles")
        filtertext=page.locator(" div.split-view-container > div:nth-child(1) > div > div > div > div > div > div> div > div.view-lines.monaco-mouse-cursor-text").inner_text().replace("\xa0", " ")
        assert "$ # Clone & install dotfiles" in filtertext
        assert "Cloning into \'/workspaces/.codespaces/.persistedshare/dotfiles\'" in filtertext
        page.wait_for_timeout(3000)
        page.keyboard.press("Control+Shift+`")
        page.wait_for_timeout(2000)
        cdpath="cd /workspaces/.codespaces/.persistedshare/dotfiles"
        labelname="Terminal 3, bash"
        dotfiles= "..gitignoreNewfolder123docspackagestests...travis.yml.disableREADME.mddotdroprequirements.txttests-ng.coveragercCONTRIBUTING.mdbootstrap.shdotdrop.shscriptstests-requirements.txt.gitLICENSEcompletiondotfilessetup.cfgtests.sh.githubMANIFEST.inconfig.yamlmkdocs.ymlsetup.py"
        test_execute_command(page, labelname, cdpath, dotfiles)
    finally:
        page.goto("https://github.com/settings/codespaces")
        if page.locator("#codespace_dotfiles_enabled").is_checked():
            page.wait_for_timeout(600)
            page.locator("#codespace_dotfiles_enabled").click()
        page.close()

@pytest.mark.dotfiles
def test_verify_dotfiles_disable_autimaticlly_install(playwright: Playwright):
    pageurl="https://github.com/settings/codespaces"
    page=test_newtemplatepage(playwright,pageurl)
    try:
        if page.locator("#codespace_dotfiles_enabled").is_checked():
            page.locator("#codespace_dotfiles_enabled").click()
            page.wait_for_timeout(2000)
        assert not page.locator("#codespace_dotfiles_enabled").is_checked() 
        page.goto("https://github.com/codespaces/new?location=EastUs")
        test_create_ppe_codespace(page, "cltest02/publicguestbook")
        page.get_by_role("button", name="Create codespace").click()
        page.wait_for_timeout(150000)
        for i in range(page.get_by_label("Close (Ctrl+F4)").count()):
            page.get_by_label("Close (Ctrl+F4)").nth(0).click()
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("codespaces: view creation log")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(3500)
        page.keyboard.press("Control+F")
        page.wait_for_timeout(1000)
        page.get_by_placeholder("Find").fill("dotfiles")
        assert "$ # Clone & install dotfiles" not in page.locator(" div.split-view-container > div:nth-child(1) > div > div > div > div > div > div> div > div.view-lines.monaco-mouse-cursor-text").inner_text().replace("\xa0", " ")
    finally:
        page.close()

def test_execute_command(page:Page, labelname: string, cdpath: string, verifytext: string):
    page.get_by_label(labelname).fill(cdpath)
    page.keyboard.press("Enter")
    page.wait_for_timeout(999)
    page.get_by_label(labelname).fill("ls -a")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)
    page.locator(".xterm-decoration-container > div:nth-child(2)").click()
    page.wait_for_timeout(500)
    for i in range(3):
        page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    if not page.get_by_placeholder("Search").is_visible():
        page.keyboard.press("Control+Shift+F")
    page.get_by_placeholder("Search").click()
    page.get_by_placeholder("Search").clear()
    page.keyboard.press("Control+V")
    page.wait_for_timeout(1000)
    assert verifytext in page.get_by_placeholder("Search").input_value().replace(" ","").replace("\n","")