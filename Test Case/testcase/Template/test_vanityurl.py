import string
import json
import uuid
import pytest
from playwright.async_api import Page, Playwright, Browser
from test_commoncode import test_newtemplatepage

#region Vanity URLs
@pytest.mark.blanktemplate
def test_new_blankVanityURLs(playwright: Playwright):
    blanktempurl="https://github.com/codespaces/new?template=blank"
    page=test_newtemplatepage(playwright,blanktempurl)
    assert 'Blank' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.reacttemplate
def test_new_reactVanityURLs(playwright: Playwright):
    reacttempurl="https://github.com/codespaces/new?template=react"
    page=test_newtemplatepage(playwright,reacttempurl)
    assert 'React' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.railstemplate
def test_new_railsVanityURLs(playwright: Playwright):
    railstempurl="https://github.com/codespaces/new?template=rails"
    page=test_newtemplatepage(playwright,railstempurl)
    assert 'Ruby on Rails' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.jupytertemplate
def test_new_jupyterVanityURLs(playwright: Playwright):
    jupytertempurl="https://github.com/codespaces/new?template=jupyter"
    page=test_newtemplatepage(playwright,jupytertempurl)
    assert 'Jupyter Notebook' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.expresstemplate
def test_new_expressVanityURLs(playwright: Playwright):
    expresstempurl="https://github.com/codespaces/new?template=express"
    page=test_newtemplatepage(playwright,expresstempurl)
    assert 'Express' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.nextjstemplate
def test_new_nextjsVanityURLs(playwright: Playwright):
    nextjstempurl="https://github.com/codespaces/new?template=nextjs"
    page=test_newtemplatepage(playwright,nextjstempurl)
    assert 'Next.js' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.djangotemplate
def test_new_djangoVanityURLs(playwright: Playwright):
    djangotempurl="https://github.com/codespaces/new?template=django"
    page=test_newtemplatepage(playwright,djangotempurl)
    assert 'Django' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.flasktemplate
def test_new_flaskVanityURLs(playwright: Playwright):
    flasktempurl="https://github.com/codespaces/new?template=flask"
    page=test_newtemplatepage(playwright,flasktempurl)
    assert 'Flask' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.preacttemplate
def test_new_preactVanityURLs(playwright: Playwright):
    preacttempurl="https://github.com/codespaces/new?template=preact"
    page=test_newtemplatepage(playwright,preacttempurl)
    assert 'Preact' in page.text_content('h5')
    page.wait_for_timeout(2000)
#endregion Vanity URLs

#region Slightly-less-vanity URLs 
@pytest.mark.blanktemplate
def test_blnkSlightlylessvanityURLs(playwright: Playwright):
    blankcodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-blank"
    page=test_newtemplatepage(playwright,blankcodespacesurl)
    assert 'Blank' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.railstemplate
def test_railsSlightlylessvanityURLs(playwright: Playwright):
    railscodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-rails"
    page=test_newtemplatepage(playwright,railscodespacesurl)
    assert 'Ruby on Rails' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.reacttemplate
def test_reactSlightlylessvanityURLs(playwright: Playwright):
    reactcodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-react"
    page=test_newtemplatepage(playwright,reactcodespacesurl)
    assert 'React' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.jupytertemplate
def test_jupyterSlightlylessvanityURLs(playwright: Playwright):
    jupytercodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-jupyter"
    page=test_newtemplatepage(playwright,jupytercodespacesurl)
    assert 'Jupyter Notebook' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.expresstemplate
def test_expressSlightlylessvanityURLs(playwright: Playwright):
    expresscodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-express"
    page=test_newtemplatepage(playwright,expresscodespacesurl)
    assert 'Express' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.nextjstemplate
def test_nextjsSlightlylessvanityURLs(playwright: Playwright):
    nextjscodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-nextjs"
    page=test_newtemplatepage(playwright,nextjscodespacesurl)
    assert 'Next.js' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.djangotemplate
def test_djangoSlightlylessvanityURLs(playwright: Playwright):
    djangocodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-django"
    page=test_newtemplatepage(playwright,djangocodespacesurl)
    assert 'Django' in page.text_content('h5')
    page.wait_for_timeout(2000)

@pytest.mark.flasktemplate
def test_flaskSlightlylessvanityURLs(playwright: Playwright):
    flaskcodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-flask"
    page=test_newtemplatepage(playwright,flaskcodespacesurl)
    assert 'Flask' in page.text_content('h5')
    page.wait_for_timeout(2000)  

@pytest.mark.preacttemplate
def test_preactSlightlylessvanityURLs(playwright: Playwright):
    preactcodespacesurl="https://github.com/codespaces/new?template_repository=github/codespaces-preact"
    page=test_newtemplatepage(playwright,preactcodespacesurl)
    assert 'Preact' in page.text_content('h5')
    page.wait_for_timeout(2000)  
#endregion Slightly-less-vanity URLs 