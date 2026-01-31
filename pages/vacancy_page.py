import random
from .base_page import BasePage
from data.data import get_random_cover_letter

import random
from .base_page import BasePage
from data.data import get_random_cover_letter

import random
from .base_page import BasePage
from data.data import get_random_cover_letter


class HHVacancyHandler(BasePage):
    def __init__(self, page, search_url):
        super().__init__(page)
        self.search_url = search_url
        self.skipped_employers = set()
        self.btn_selector = 'a[data-qa="vacancy-serp__vacancy_response"]'
        self.vacancy_card_selector = '[data-qa="vacancy-serp__vacancy"]'
        self.next_page_selector = '[data-qa="pager-next"]'
        self.page_bar = '[data-qa="pager-block"]'

    def run_auto_apply_flow(self, max_pages=40):
        for current_page in range(1, max_pages + 1):
            print(f"\n=== РАБОТАЕМ НА СТРАНИЦЕ №{current_page} ===")
            self.page.wait_for_load_state("domcontentloaded")
            self.process_all_vacancies_on_page()
            if not self.go_to_next_page(current_page):
                break

    def process_all_vacancies_on_page(self):
        # 1. Что ДОЛЖНО быть (White-list)
        target_titles = ["qa", "тестировании", "тестировщик", "test",
                         "automation", "engineer", "автотест", "автоматизации"]

        # 2. Что ЗАПРЕЩЕНО (Black-list)
        black_list_titles = ["lead", "лид", "senior", "сеньор", "руководитель",
                             "ведущий", "java", "Senior", "старший"]

        try:
            self.page.wait_for_selector(self.btn_selector, timeout=5000)
        except:
            print("Кнопки отклика не обнаружены.")
            return

        i = 0
        while i < self.page.locator(self.btn_selector).count():
            try:
                card = self.page.locator(self.vacancy_card_selector).nth(i)
                title_locator = card.locator('[data-qa="serp-item__title"]')

                if title_locator.count() == 0:
                    i += 1
                    continue

                # Гарантированное приведение к нижнему регистру для сравнения
                raw_title = title_locator.inner_text().lower().strip()

                # ГАРАНТИРОВАННЫЙ ФИЛЬТР (ЧЕРНЫЙ СПИСОК)
                black_word_found = None
                for black_word in black_list_titles:
                    if black_word in raw_title:
                        black_word_found = black_word
                        break

                if black_word_found:
                    print(f"[-] СКИП (Black-list): В '{raw_title}' найдено запрещенное '{black_word_found}'")
                    i += 1
                    continue  # ГАРАНТИРОВАННО ПЕРЕХОДИМ К СЛЕДУЮЩЕЙ ВАКАНСИИ

                # --- ФИЛЬТР ПО БЕЛОМУ СПИСКУ ---
                if not any(word in raw_title for word in target_titles):
                    print(f"[?] ПРОПУСК (Нецелевая): '{raw_title}'")
                    i += 1
                    continue

                # Если прошли все фильтры
                print(f"[+] ПОДХОДИТ: '{raw_title}'")

                # Остальная логика (проверка работодателя, клик, письмо)
                employer_element = card.locator('[data-qa="vacancy-serp__vacancy-employer"]')
                employer = employer_element.inner_text().strip() if employer_element.count() > 0 else "Неизвестный"

                if employer in self.skipped_employers:
                    i += 1
                    continue

                current_btn = self.page.locator(self.btn_selector).nth(i)
                if "Откликнулись" in current_btn.inner_text():
                    i += 1
                    continue

                current_btn.scroll_into_view_if_needed()
                self.wait_random(800, 1500)
                current_btn.click()
                self.wait_random(2500, 3500)

                # Блок теста
                if "vacancy_questions" in self.page.url or \
                        self.page.get_by_text("необходимо ответить на несколько вопросов").is_visible():
                    print(f"(!) Скип теста у '{employer}'")
                    self.skipped_employers.add(employer)
                    self.page.goto(self.search_url)
                    self.page.wait_for_load_state("domcontentloaded")
                    i = 0  # Сброс индекса при перегрузке страницы
                    continue

                self.handle_relocation_warning()

                # Повторная проверка на тест после модалки
                if "vacancy_questions" in self.page.url:
                    self.page.goto(self.search_url)
                    i = 0
                    continue

                self._fill_cover_letter()
                i += 1

            except Exception as e:
                print(f"Ошибка на вакансии {i}: {e}")
                i += 1

    def _fill_cover_letter(self):
        letter_input = self.page.locator('[data-qa="vacancy-response-popup-form-letter-input"]')
        if letter_input.is_visible():
            letter_input.fill(get_random_cover_letter())
            self.page.locator('[data-qa="vacancy-response-submit-popup"]').click()
            self.wait_random(1500, 2500)

    def go_to_next_page(self, current_page_num):
        found = self.scroll_to_pagination(self.page_bar)
        if found:
            next_btn = self.page.locator(self.next_page_selector)
            if next_btn.is_visible():
                next_btn.hover()
                self.wait_random(500, 1000)
                next_btn.click(force=True)
            else:
                next_page_val = current_page_num + 1
                digit_selector = f'{self.page_bar} a:has-text("{next_page_val}"), {self.page_bar} button:has-text("{next_page_val}")'
                digit_btn = self.page.locator(digit_selector).first
                if digit_btn.is_visible():
                    digit_btn.click(force=True)
                else:
                    return False
            try:
                self.page.wait_for_load_state("load", timeout=10000)
            except:
                pass
            self.search_url = self.page.url
            return True
        return False