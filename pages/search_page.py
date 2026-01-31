import pytest
from .base_page import BasePage

class HHSearchPage(BasePage): # Наследуем методы
    def setup_filters(self, role_name):
        self.page.goto("https://hh.ru")
        self.human_scroll()
        self.page.click('a[data-qa="advanced-search"]')
        self.page.fill('input[name="text"]', 'QA engineer')
        self.page.click('[data-qa="suggest-item-cell"]')

        # Регион и удаленка
        self.page.click('[data-qa="advanced-search-region-selectFromList"]')
        self.page.locator('[data-qa="tree-selector-input tree-selector-input-113"]').click()
        self.page.click('[data-qa="composite-selection-tree-selector-modal-submit"]')

        self.page.locator('input[data-qa="advanced-search__work_format-item_REMOTE"]').dispatch_event("click")
        self.page.click('button[data-qa="advanced-search-submit-button"]')

        self.page.wait_for_url("**/search/vacancy**", timeout=15000)
        return self.page.url