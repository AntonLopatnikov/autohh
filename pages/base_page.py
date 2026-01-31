import random
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def wait_random(self, min_ms=1500, max_ms=3500):
        self.page.wait_for_timeout(random.randint(min_ms, max_ms))

    def human_scroll(self):
        """Плавная прокрутка страницы для имитации чтения (анти-фрод)"""
        for _ in range(random.randint(2, 4)):
            #Прокручиваем на случайную величину
            self.page.mouse.wheel(0, random.randint(400, 900))
            #Ждем как человек
            self.wait_random(600, 1300)

    def scroll_to_pagination(self, page_bar_selector):
        print("Ищу панель навигации страниц...")
        for i in range(15):
            pagination_bar = self.page.locator(page_bar_selector)
            if pagination_bar.is_visible():
                self.page.mouse.wheel(0, 450) # Прокрутка чуть ниже бара
                print(f"Пагинация найдена на шаге {i}")
                return True
            self.page.mouse.wheel(0, random.randint(700, 1000))
            self.wait_random(500, 800)
        return False

    def scroll_to_element(self, selector):
        """Плавно скроллит страницу до тех пор, пока элемент не станет видимым"""
        max_attempts = 10
        for _ in range(max_attempts):
            if self.page.locator(selector).is_visible():
                # Немного прокручиваем, чтобы кнопка не была на самом краю экрана
                self.page.mouse.wheel(0, random.randint(100, 200))
                break

            # Имитируем рывок прокрутки
            self.page.mouse.wheel(0, random.randint(400, 700))
            self.wait_random(400, 800)

    def handle_relocation_warning(self):
        """Улучшенная обработка окна 'Все равно откликнуться'"""
        selector = '[data-qa="relocation-warning-confirm"]'
        try:
            button = self.page.wait_for_selector(selector, state="visible", timeout=2500)
            if button:
                self.wait_random(800, 1200)  # Имитируем чтение текста окна
                try:
                    button.click(timeout=2000)
                except:
                    button.dispatch_event("click")
                print("(!) Нажато 'Все равно откликнуться' (через принудительное событие).")
                self.wait_random(1000, 1500)  # Ждем закрытия анимации окна
                return True
        except:
            return False

    def apply_to_vacancy(self):
        """Основной процесс: найти кнопку отклика, доскроллить, нажать и обработать окна"""
        apply_button_selector = '[data-qa="vacancy-response-link-top"]'

        print("Поиск кнопки отклика...")
        self.scroll_to_element(apply_button_selector)

        apply_button = self.page.locator(apply_button_selector).first

        if apply_button.is_visible():
            self.wait_random(800, 1500)
            apply_button.click()

            # Сразу после клика проверяем, не вылезло ли окно о релокации
            self.wait_random(1000, 2000)
            self.handle_relocation_warning()
        else:
            print("Кнопка отклика не найдена.")

    def is_element_visible(self, selector, timeout=5000):
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except:
            return False