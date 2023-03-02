
from asyncio import sleep
from lib2to3.pgen2 import pgen
from multiprocessing import context
from pydoc import pager
from re import T
import pytest
from playwright.async_api import Page, expect, Playwright, Browser, BrowserContext

# def test_test01():
#      with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False,slow_mo=100) #打开浏览器
#         context1 = browser.new_context() #创建浏览器上下文，支持创建多个上下文
#         page1 = context1.new_page()#新打开一个浏览器标签页
#         page1.goto("https://github.com/codespaces")
#         page1.locator("id=login_field").fill("v-margema@microsoft.com")
#         page1.locator("id=password").fill("Extensibility123456")
#         page1.click("input[name*='commit']")
#         assert 'Your codespaces' in page1.text_content('h2')

#         page1.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div.clearfix.mt-3.pb-2 > div.col-md-4.col-sm-12.float-right.position-relative.d-inline-flex.flex-justify-end.mb-1 > a.btn-primary.btn").click()
#         assert 
#         page.wait_for_url("https://github.com/codespaces/new")
#         context2 = browser.new_context()  # 创建浏览器上下文，支持创建多个上下文
#         page2 = context2.new_page()#新打开一个浏览器标签页
#         page2.goto("https://www.bilibili.com")

@pytest.mark.forgotpassword
def test_open_forgotpassword(page: Page) -> Page:
      page.goto("https://github.com/codespaces")
      # //a[contains(@href, "/password_reset")]
      # a[href*="/password_reset"]
      page.click("a[href*='/password_reset']")
      assert 'Reset your password' in page.text_content('h1')
    #   assert 'Reset your password' in page.inner_text('h1')
    #   page.wait_for_timeout(300)
    #   page.get_attribute("login_field").fill("v-margema@microsoft.com")
    #   page.get("password").fill("Extensibility123456")
      
      page.wait_for_timeout(3000)

@pytest.mark.loginpage
def test_login_codespaces(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://github.com/codespaces")
    page.locator("id=login_field").fill("Chaoyun8888")
    page.locator("id=password").fill("Dcy200819921028")
    page.click("input[name*='commit']")
    storage = context.storage_state(path="auth/state.json")
    assert 'Your codespaces' in page.text_content('h2')

    #Go to docs
    page.click("a[href*='developing-online-with-codespaces']") 
    assert 'GitHub Codespaces' in page.text_content('h1')
    page.wait_for_timeout(3000)

@pytest.mark.alltemplate
def test_showall_codespace_template(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="cway")
    page = context.new_page()
    page.goto("https://github.com/codespaces")
    # page.locator("id=login_field").fill("v-margema@microsoft.com")
    # page.locator("id=password").fill("Extensibility123456")
    # page.click("input[name*='commit']")
    assert 'Your codespaces' in page.text_content('h2')

    #see all template
    page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-sidebar.p-2 > ul > li:nth-child(1) > nav-list > ul > li > ul > li:nth-child(2)").click()
    assert 'Choose a template' in page.text_content('h1')
    page.wait_for_timeout(3000)

@pytest.mark.opennewcodespacepage
def test_open_createcodespace_page(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="auth/state.json")
    page = context.new_page()
    page.goto("https://github.com/codespaces")
    # page.locator("id=login_field").fill("v-margema@microsoft.com")
    # page.locator("id=password").fill("Extensibility123456")
    # page.click("input[name*='commit']")
    assert 'Your codespaces' in page.text_content('h2')

    #create codespace page can be opened successfully
    page.goto("https://github.com/codespaces/new")
    assert page.title()=="Create new codespace"
    page.wait_for_timeout(3000)

# @pytest.mark.opennewcodespacepage01
# def test_open_createcodespace_page01(page: Page) -> Page:
#     # with sync_playwright() as p:
#     #     browser = p.chromium.launch(headless=False,slow_mo=100) #打开浏览器
#     #     context1 = browser.new_context() #创建浏览器上下文，支持创建多个上下文
#     #     page1 = context1.new_page()#新打开一个浏览器标签页
#     #     page1.goto("https://www.baidu.com")
#     #     context2 = browser.new_context()  # 创建浏览器上下文，支持创建多个上下文
#     #     page2 = context2.new_page()#新打开一个浏览器标签页
#     #     page2.goto("https://www.bilibili.com")
#     #     browser.close()

#     page.goto("https://github.com/codespaces")
#     page.locator("id=login_field").fill("v-margema@microsoft.com")
#     page.locator("id=password").fill("Extensibility123456")
#     page.click("input[name*='commit']")
#     assert 'Your codespaces' in page.text_content('h2')

#     #create codespace
#     page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div.clearfix.mt-3.pb-2 > div.col-md-4.col-sm-12.float-right.position-relative.d-inline-flex.flex-justify-end.mb-1 > a.btn-primary.btn").click()
#     # assertRest=page.inner_text('h2')
#     # assert page.inner_text('h2')== 'Create a new codespace'
#     page.wait_for_url("https://github.com/codespaces/new")
#     page.wait_for_timeout(3000)

@pytest.mark.newcodespacepage
def test_create_codespace(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="cway")
    page = context.new_page()
    page.goto("https://github.com/codespaces")
    assert 'Your codespaces' in page.text_content('h2')

    #create codespace
    page.goto("https://github.com/codespaces/new")
    assert page.title()=="Create new codespace"
                          
    dropdown_selectarepo="body > div.logged-in.env-production.page-responsive > div.application-main > main > new-codespace > div.js-codespaces-completable > div.Box.position-relative.container-md > div.Box-body.p-0 > form > div:nth-child(2) > div > details > summary"
    page.locator(dropdown_selectarepo).click()

    sleep(100000)
    page.locator("#repository-menu-list > label:nth-child(1)").click()
    sleep(2000)
    page.locator("#new_codespace > button").click()
    page.wait_for_timeout(20000)
    #
    # page.mouse.down()
    # page.keyboard.press("Enter")

    # 给下拉框赋值
    # page.select_option(dropdown_selectarepo,"LinghuaMa/WebApplication-2023-0206-13")
    
    # selex="body > div.logged-in.env-production.page-responsive > div.application-main > main > new-codespace > div.js-codespaces-completable > div.Box.position-relative.container-md > div.Box-body.p-0 > form > div:nth-child(2) > div > details > summary > span.text-normal.css-truncate-target"
    # page.select_option(selex,1)
    # page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > new-codespace > div.js-codespaces-completable > div.Box.position-relative.container-md > div.Box-body.p-0 > form > div:nth-child(2) > div > details > summary > span.text-normal.css-truncate-target").click()
    # page.wait_for_timeout(3000)

    # page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div.clearfix.mt-3.pb-2 > div.col-md-4.col-sm-12.float-right.position-relative.d-inline-flex.flex-justify-end.mb-1 > a.btn-primary.btn").click()
    # page.goto("https://github.com/codespaces/new")
    # page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > new-codespace > div.js-codespaces-completable > div.Box.position-relative.container-md > div.Box-body.p-0 > form > div:nth-child(2) > div > details > summary > span.text-normal.css-truncate-target").click()
    # page.locator("#repository-menu-list > label:nth-child(1) > div > span").click()

@pytest.mark.renamecodespace
def test_rename_codespace(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="cway")
    page = context.new_page()
    page.goto("https://github.com/codespaces")
    assert 'Your codespaces' in page.text_content('h2')

    #
    page.locator("a[href*='repository_id=292158748']").click()
    sleep(1000)
    spaceconfig="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(2) > div > div.Box-row > div > div:nth-child(2) > div > div:nth-child(7) > options-popover > details:nth-child(1)"
    page.locator(spaceconfig).click()
    sleep(2000)
    renamebutton=spaceconfig+" > details-menu > button:nth-child(5)"
    page.locator(renamebutton).click()
    sleep(2000)
    machinetype="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(2) > div > div.Box-row > div > div:nth-child(2) > div > p.f6.mb-0.mr-2.text-small.color-fg-muted.tooltipped.tooltipped-nw"
    machinetypevalue=page.locator(machinetype).text_content()
    # if machinetypevalue.
    page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(2) > div > div.Box-row > div > div:nth-child(2) > div > div:nth-child(7) > options-popover > details.ml-2.details-overlay.details-overlay-dark.details-reset.position-relative.d-inline-block > details-dialog > div > div.Box-body.p-0 > form > div > div.Box.radio-group.d-flex.flex-wrap.flex-content-start.my-3 > label:nth-child(2)").click()
    
    # page.keyboard.press("ArrowDown")

    page.keyboard.press("Enter")
    # page.click("button[type*='commit']")
    sleep(2000)
    page.wait_for_timeout(3000)




# @pytest.mark.usereacttemplatecreatecodespace
# def test_use_react_template_create_codespace(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context(storage_state="cway")
#     page = context.new_page()
#     page.goto("https://github.com/codespaces")
#     assert 'Your codespaces' in page.text_content('h2')
    
