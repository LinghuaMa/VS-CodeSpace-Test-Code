
from lib2to3.pgen2 import pgen
from multiprocessing import context
from pydoc import pager
from re import T
import pytest
from playwright.async_api import Page, expect, Playwright, Browser, BrowserContext

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
def test_login_codespaces(page: Page) -> Page:
    page.goto("https://github.com/codespaces")
    page.locator("id=login_field").fill("v-margema@microsoft.com")
    page.locator("id=password").fill("Extensibility123456")
    page.click("input[name*='commit']")
    assert 'Your codespaces' in page.text_content('h2')

    #Go to docs
    page.click("a[href*='developing-online-with-codespaces']") 
    assert 'GitHub Codespaces' in page.text_content('h1')
    page.wait_for_timeout(3000)

@pytest.mark.alltemplate
def test_showall_codespace_template(page: Page) -> Page:
    page.goto("https://github.com/codespaces")
    page.locator("id=login_field").fill("v-margema@microsoft.com")
    page.locator("id=password").fill("Extensibility123456")
    page.click("input[name*='commit']")
    assert 'Your codespaces' in page.text_content('h2')

    #see all template
    page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-sidebar.p-2 > ul > li:nth-child(1) > nav-list > ul > li > ul > li:nth-child(2)").click()
    assert 'Choose a template' in page.text_content('h1')
    page.wait_for_timeout(3000)

# @pytest.mark.opennewcodespacepage
# def test_open_createcodespace_page(page: Page) -> Page:
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
def test_create_codespace(page: Page) -> Page:
    page.goto("https://github.com/codespaces")
    page.locator("id=login_field").fill("v-margema@microsoft.com")
    page.locator("id=password").fill("Extensibility123456")
    page.click("input[name*='commit']")
    assert 'Your codespaces' in page.text_content('h2')

    #create codespace
    page.goto("https://github.com/codespaces/new")
    locator=page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > new-codespace > div.js-codespaces-completable > div.Box.position-relative.container-md > div.Box-footer.px-3.py-3 > div > button")
    expect(locator).to_be_disabled()

    # page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div.clearfix.mt-3.pb-2 > div.col-md-4.col-sm-12.float-right.position-relative.d-inline-flex.flex-justify-end.mb-1 > a.btn-primary.btn").click()
    # page.goto("https://github.com/codespaces/new")
    # page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > new-codespace > div.js-codespaces-completable > div.Box.position-relative.container-md > div.Box-body.p-0 > form > div:nth-child(2) > div > details > summary > span.text-normal.css-truncate-target").click()
    # page.locator("#repository-menu-list > label:nth-child(1) > div > span").click()
    page.wait_for_timeout(3000)
