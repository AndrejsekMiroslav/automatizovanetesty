import re
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.psmf.cz/"

@pytest.fixture
def set_desktop_viewport(page: Page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    return page

def test_hlavni_navigace(set_desktop_viewport):
    page = set_desktop_viewport
    page.goto(BASE_URL)

    # Kontrola, že odkazy hlavní navigace jsou viditelné
    expect(page.get_by_role("link", name="Soutěže")).to_be_visible()
    expect(page.get_by_role("link", name="Vývěska")).to_be_visible()
    expect(page.get_by_role("link", name="Hřiště")).to_be_visible()

def test_vyhledani_tymu(set_desktop_viewport):
    page = set_desktop_viewport
    page.goto(BASE_URL)

    search_input = page.locator("#SearchInput")
    expect(search_input).to_be_visible()
    search_input.fill("Pornolištičky")

    search_button = page.locator("#SearchForm > div > button")
    expect(search_button).to_be_visible()
    search_button.click()

    # Klik na první odkaz v seznamu výsledků
    first_result = page.get_by_role("link", name="Pornolištičky").first
    expect(first_result).to_be_visible()
    first_result.click()

    # Ověření titulku stránky týmu
    expect(page).to_have_title(re.compile("Pornolištičky"))

def test_odkazz_na_dokumenty(set_desktop_viewport):
    page = set_desktop_viewport
    page.goto(BASE_URL)

    documents_link = page.get_by_role("link", name="Dokumenty")
    expect(documents_link).to_be_visible()
    documents_link.click()

    # Ověření URL stránky
    expect(page).to_have_url(re.compile("dokumenty"))
