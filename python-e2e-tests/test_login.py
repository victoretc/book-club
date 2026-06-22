from playwright.sync_api import Page 
from allure import title
import pytest 

@pytest.fixture
def base_url():
    # TODO: В зависимости от окружения может быть разным.  
    return "http://localhost:5173"
    

@title("Login")
def test_login(page: Page):
    page.goto(base_url + "/signin")
