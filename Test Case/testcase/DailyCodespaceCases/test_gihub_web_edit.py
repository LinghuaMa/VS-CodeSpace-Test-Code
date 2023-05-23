import pytest
import string
import getpass
from playwright.sync_api import Page, Playwright
from test_commonmethod import test_create_ppe_codespace,test_createAndinstall,test_newtemplatepage

@pytest.mark.githubedit
def test_bare_repo(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(60000)
        assert "main" in page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - cd878bf").inner_text()
    finally:
        page.close()

@pytest.mark.githubedit
def test_tree_at_root_with_branch(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/tree/cti-testing"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(60000)
        assert "cti-testing" in page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - 1477d74").inner_text()
    finally:
        page.close()

@pytest.mark.githubedit
def test_tree_at_root_with_branch_with_slash(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/tree/cti/testing/branch"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert "cti/testing/branch" in page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - 4dd8028").inner_text()
    finally:
        page.close()

@pytest.mark.githubedit
def test_blob_on_ref(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/blob/main/README.md"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert "main" in page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - cd878bf").inner_text()
        assert 'README.md' in page.get_by_role("listitem").filter(has_text="README.md").locator("span").inner_text()
    finally:
        page.close()

@pytest.mark.githubedit
def test_blob_on_ref_with_slash(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/blob/cti/testing/branch/README.md"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert "cti/testing/branch" in page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - 4dd8028").inner_text()
        assert 'README.md' in page.get_by_role("listitem").filter(has_text="README.md").locator("span").inner_text()
    finally:
        page.close()

@pytest.mark.githubedit
def test_commit(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/commit/1477d7454f1e2ea1a64595cdd8f2e94e5bf51e8c"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - 1477d74").is_visible()
    finally:
        page.close()

@pytest.mark.githubedit
def test_pull_request(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/pull/4953"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert page.get_by_role("button", name="git-pull-request  Pull Request #4953").is_visible()
    finally:
        page.close()

@pytest.mark.githubedit #https://ppe.github.dev/JoannaWu-wd/testRepository/pull/2  need joannawu help
def test_pull_request_from_a_fork(playwright: Playwright):
    pageurl="https://ppe.github.dev/JoannaWu-wd/testRepository/pull/2"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert page.get_by_role("button", name="git-pull-request  Pull Request #4953").is_visible()
    finally:
        page.close()

@pytest.mark.githubedit 
def test_tree_at_path_with_branch(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/tree/main/github"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert "main" in page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - cd878bf").inner_text()
        assert page.get_by_role("treeitem", name="github", exact=True, selected=True).is_visible()
    finally:
        page.close()

@pytest.mark.githubedit 
def test_tree_at_path_with_branch_with_slash(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/tree/cti/testing/branch/github"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert "cti/testing/branch" in page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - 4dd8028").inner_text()
        assert page.get_by_role("treeitem", name="github", exact=True, selected=True).is_visible()
    finally:
        page.close()

@pytest.mark.githubedit 
def test_blob_on_sha(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/blob/1477d7454f1e2ea1a64595cdd8f2e94e5bf51e8c/README.md"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - 1477d74").is_visible()
        assert 'README.md' in page.get_by_role("listitem").filter(has_text="README.md").locator("span").inner_text()
    finally:
        page.close()

@pytest.mark.githubedit 
def test_tree_at_root_with_sha(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/tree/1477d7454f1e2ea1a64595cdd8f2e94e5bf51e8c"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - 1477d74").is_visible()
    finally:
        page.close()

@pytest.mark.githubedit 
def test_blob_on_sha_or_ref_with_line_number(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/blob/main/README.md#L1"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert "main" in page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - cd878bf").inner_text()
        assert 'README.md' in page.get_by_role("listitem").filter(has_text="README.md").locator("span").inner_text()
    finally:
        page.close()

@pytest.mark.githubedit 
def test_blob_on_sha_or_ref_with_range(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/blob/main/README.md#L1-L2"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert "main" in page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - cd878bf").inner_text()
        assert 'README.md' in page.get_by_role("listitem").filter(has_text="README.md").locator("span").inner_text()
    finally:    
        page.close()

@pytest.mark.githubedit 
def test_tree_at_path_with_sha(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/tree/1477d7454f1e2ea1a64595cdd8f2e94e5bf51e8c/github"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert page.get_by_role("button", name="vssaas-planning (microsoft/vssaas-planning) - 1477d74").is_visible()
        assert page.get_by_role("treeitem", name="github", exact=True, selected=True).is_visible()
    finally:
        page.close()

@pytest.mark.githubedit 
def test_full_request_files_view(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/vssaas-planning/pull/4953/files"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert page.get_by_role("button", name="git-pull-request  Pull Request #4953").is_visible()
    finally:
        page.close()

@pytest.mark.githubedit 
def test_no_existing_repo(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft/not-a-real-repo"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert page.get_by_alt_text("404 “This is not the web page you are looking for”").is_visible()
    finally:
        page.close()

@pytest.mark.githubedit 
def test_pointing_to_a_user(playwright: Playwright):
    pageurl="https://ppe.github.dev/microsoft"
    page=test_sso_login(playwright, pageurl)
    try:
        page.context.pages[-2].close()
        page.wait_for_timeout(30000)
        assert page.get_by_role("heading", name="Microsoft").is_visible()
    finally:
        page.close()

def test_sso_login(playwright: Playwright, pageurl: string)-> Page:
    context = playwright.chromium.launch_persistent_context(user_data_dir=f"c:\\User\\{getpass.getuser()}\\AppData\\Local\\Microsoft\\Edge\\User Data",
                                                accept_downloads=True,
                                                headless=False,
                                                bypass_csp=False,
                                                slow_mo=1000,
                                                channel="msedge")    
    page = context.new_page()
    page.storage_state="cway"
    page.goto(pageurl)
    if page.locator("button", has_text="Continue").is_visible():
        page.locator("button", has_text="Continue").click()
        page.wait_for_timeout(5000)
    return page