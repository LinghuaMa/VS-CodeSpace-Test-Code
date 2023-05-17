import pytest
import string
import getpass
from playwright.sync_api import Page, Playwright
from test_commonmethod import test_open_page_sso,test_create_ppe_codespace,test_createAndinstall,test_upload_install_vsix

def test_valid_devcontainer(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?location=SouthEastAsia"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        test_create_ppe_codespace(page, "Microsoft/vscode-remote-try-cpp")
        test_createAndinstall(page, "4-core")
    finally:
        page.close()