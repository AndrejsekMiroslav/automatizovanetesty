import pytest
from playwright.sync_api import Page

BASE_URL = "https://www.psmf.cz/"

def ensure_desktop(page: Page):
    """Nastaví větší viewport, aby se zobrazilo plné menu."""
    page.set_viewport_size({"width": 1280, "height": 800})

def test_vyhledani_tymu(page: Page):
    """Ověření, že lze vyhledat a otevřít stránku týmu 'Pornolištičky'."""
    ensure_desktop(page)
    page.goto(BASE_URL)

    # Zadání dotazu do vyhledávacího pole
    page.locator("#SearchInput").fill("Pornolištičky")

    # Kliknutí na tlačítko hledání
    page.locator("#SearchForm > div > button").click()

    # Počkáme na výsledky a klikneme na první odkaz obsahující 'Pornolištičky'
    first_result = page.locator("a", has_text="Pornolištičky").first
    first_result.wait_for(state="visible", timeout=5000)
    first_result.click()

    # Ověření titulku stránky
    page.wait_for_load_state("domcontentloaded")
    assert page.title().strip() == "Pornolištičky"

def test_hlavni_navigace(page: Page):
    """Kontrola viditelnosti hlavních odkazů v navigaci."""
    ensure_desktop(page)
    page.goto(BASE_URL)
    page.wait_for_selector("header, nav", timeout=3000)
    assert page.locator("a:has-text('Soutěže')").count() > 0
    assert page.locator("a:has-text('Vývěska')").count() > 0
    assert page.locator("a:has-text('Hřiště')").count() > 0

def test_odkazz_na_dokumenty(page: Page):
    """Ověření, že odkaz 'Dokumenty' vede na správnou stránku."""
    ensure_desktop(page)
    page.goto(BASE_URL)
    page.click("a:has-text('Dokumenty')")
    page.wait_for_url("**/dokumenty/**", timeout=5000)
    assert "/dokumenty" in page.url
    page.wait_for_selector("text=Pravidla malého fotbalu", timeout=5000)
    assert page.locator("text=Pravidla malého fotbalu").count() > 0