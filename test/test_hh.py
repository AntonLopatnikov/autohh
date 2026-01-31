from pages.search_page import HHSearchPage
from pages.vacancy_page import HHVacancyHandler


def test_hh_auto_apply_flow(page):
    search = HHSearchPage(page)
    search_url = search.setup_filters('QA engineer')
    handler = HHVacancyHandler(page, search_url)
    handler.run_auto_apply_flow(max_pages=40)