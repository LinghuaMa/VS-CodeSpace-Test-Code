import string
import json
import uuid
import pytest
from playwright.async_api import Page, Playwright, Browser
from test_commoncode import test_newtemplatepage

#region Vanity URLs
@pytest.mark.blanktemplatecreatecodespace
def test_new_blanktemplatepage(playwright: Playwright):
    blanktempurl="https://github.com/codespaces/new?template=blank"
    page=test_newtemplatepage(playwright,blanktempurl)
    assert 'Blank' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.reacttemplatecreatecodespace
def test_new_reacttemplatepage(playwright: Playwright):
    reacttempurl="https://github.com/codespaces/new?template=react"
    page=test_newtemplatepage(playwright,reacttempurl)
    assert 'React' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.railstemplatecreatecodespace
def test_new_railstemplatepage(playwright: Playwright):
    railstempurl="https://github.com/codespaces/new?template=rails"
    page=test_newtemplatepage(playwright,railstempurl)
    assert 'Ruby on Rails' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.jupytertemplatecreatecodespace
def test_new_jupytertemplatepage(playwright: Playwright):
    jupytertempurl="https://github.com/codespaces/new?template=jupyter"
    page=test_newtemplatepage(playwright,jupytertempurl)
    assert 'Jupyter Notebook' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.expresstemplatecreatecodespace
def test_new_expresstemplatepage(playwright: Playwright):
    expresstempurl="https://github.com/codespaces/new?template=express"
    page=test_newtemplatepage(playwright,expresstempurl)
    assert 'Express' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.nextjstemplatecreatecodespace
def test_new_nextjstemplatepage(playwright: Playwright):
    nextjstempurl="https://github.com/codespaces/new?template=nextjs"
    page=test_newtemplatepage(playwright,nextjstempurl)
    assert 'Next.js' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.djangotemplatecreatecodespace
def test_new_djangotemplatepage(playwright: Playwright):
    djangotempurl="https://github.com/codespaces/new?template=django"
    page=test_newtemplatepage(playwright,djangotempurl)
    assert 'Django' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.flasktemplatecreatecodespace
def test_new_flasktemplatepage(playwright: Playwright):
    flasktempurl="https://github.com/codespaces/new?template=flask"
    page=test_newtemplatepage(playwright,flasktempurl)
    assert 'Flask' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.preacttemplatecreatecodespace
def test_new_preacttemplatepage(playwright: Playwright):
    preacttempurl="https://github.com/codespaces/new?template=preact"
    page=test_newtemplatepage(playwright,preacttempurl)
    assert 'Preact' in page.text_content('h5')
    page.wait_for_timeout(2000)
#endregion Vanity URLs

#region Slightly-less-vanity URLs 
@pytest.mark.blankcodespacesopenpage
def test_blnkcodespacespage(playwright: Playwright):
    blankcodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-blank"
    page=test_newtemplatepage(playwright,blankcodespacesurl)
    assert 'Blank' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.railscodespacesopenpage
def test_railscodespacespage(playwright: Playwright):
    railscodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-rails"
    page=test_newtemplatepage(playwright,railscodespacesurl)
    assert 'Ruby on Rails' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.reactcodespacesopenpage
def test_reactcodespacespage(playwright: Playwright):
    reactcodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-react"
    page=test_newtemplatepage(playwright,reactcodespacesurl)
    assert 'React' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.jupytercodespacesopenpage
def test_jupytercodespacespage(playwright: Playwright):
    jupytercodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-jupyter"
    page=test_newtemplatepage(playwright,jupytercodespacesurl)
    assert 'Jupyter Notebook' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.expresscodespacesopenpage
def test_expresscodespacespage(playwright: Playwright):
    expresscodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-express"
    page=test_newtemplatepage(playwright,expresscodespacesurl)
    assert 'Express' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.nextjscodespacesopenpage
def test_nextjscodespacespage(playwright: Playwright):
    nextjscodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-nextjs"
    page=test_newtemplatepage(playwright,nextjscodespacesurl)
    assert 'Next.js' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.djangocodespacesopenpage
def test_djangocodespacespage(playwright: Playwright):
    djangocodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-django"
    page=test_newtemplatepage(playwright,djangocodespacesurl)
    assert 'Django' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.flaskcodespacesopenpage
def test_flaskcodespacespage(playwright: Playwright):
    flaskcodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-flask"
    page=test_newtemplatepage(playwright,flaskcodespacesurl)
    assert 'Flask' in page.text_content('h5')
    page.wait_for_timeout(2000)  

@pytest.mark.preactcodespacesopenpage
def test_preactcodespacespage(playwright: Playwright):
    preactcodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-preact"
    page=test_newtemplatepage(playwright,preactcodespacesurl)
    assert 'Preact' in page.text_content('h5')
    page.wait_for_timeout(2000)  
#endregion Slightly-less-vanity URLs 