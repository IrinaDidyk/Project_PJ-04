import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Инициализация драйвера
        cls.driver = webdriver.Chrome()
        cls.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")

    def test_load_login_page(self):
        """Тест 1: Проверка загрузки страницы входа"""
        WebDriverWait(self.driver, 10).until(EC.title_contains("Ростелеком ID"))
        self.assertIn("Ростелеком ID", self.driver.title)

    def test_elements_on_login_page(self):
        """Тест 2: Проверка наличия элементов на странице"""
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        self.assertTrue(self.driver.find_element(By.ID, "username"))  # Поле для логина
        self.assertTrue(self.driver.find_element(By.ID, "password"))  # Поле для пароля
        self.assertTrue(self.driver.find_element(By.XPATH, "//button[text()='Войти']"))  # Кнопка "Войти"
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, "Забыли пароль?"))  # Ссылка на восстановление пароля

    def test_successful_login(self):
        """Тест 3: Успешный вход в систему"""
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        self.driver.find_element(By.ID, "username").send_keys("89089638189")
        self.driver.find_element(By.NAME, "password").send_keys("Chto&kto")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Ростелеком ID"))
        self.assertIn("Ростелеком ID", self.driver.title)

    def test_incorrect_username(self):
        """Тест 4: Неправильный логин"""
        self.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")  # Вернуться на страницу входа
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        self.driver.find_element(By.ID, "username").send_keys("89999999999")
        self.driver.find_element(By.NAME, "password").send_keys("Chto&kto")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Неверный логин или пароль')]")))
        self.assertTrue(self.driver.find_element(By.XPATH, "//div[contains(text(), 'Неверный логин или пароль')]"))

    def test_incorrect_password(self):
        """Тест 5: Неправильный пароль"""
        self.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        self.driver.find_element(By.ID, "username").send_keys("89089638189")
        self.driver.find_element(By.NAME, "password").send_keys("111")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Неверный логин или пароль')]")))
        self.assertTrue(self.driver.find_element(By.XPATH, "//div[contains(text(), 'Неверный логин или пароль')]"))

    def test_recovery_page(self):
        """Тест 6: Переход на страницу восстановления пароля"""
        self.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Забыли пароль?")))
        self.driver.find_element(By.LINK_TEXT, "Забыли пароль?").click()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Ростелеком ID"))
        self.assertIn("Ростелеком ID", self.driver.title)

    def test_empty_username_and_password(self):
        """Тест 7: Пустые поля логина и пароля"""
        self.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Введите номер телефона')]")))

    def test_empty_username(self):
        """Тест 8: Пустое поле логина"""
        self.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")
        self.driver.find_element(By.NAME, "password").send_keys("Chto&kto")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Введите номер телефона')]")))

    def test_empty_password(self):
        """Тест 9: Пустое поле пароля"""
        self.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")
        self.driver.find_element(By.ID, "username").send_keys("89089638189")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Забыл пароль')]")))

    def test_login_with_special_characters(self):
        """Тест 10: Вход с использованием специальных символов в логине и пароле"""
        self.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")
        self.driver.find_element(By.ID, "username").send_keys("!@#$%^&*()")
        self.driver.find_element(By.NAME, "password").send_keys("!@#$%^&*()")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Неверный логин или пароль')]")))

    def test_login_with_long_username_and_password(self):
        """Тест 11: Вход с длинным логином и паролем"""
        long_username = "a" * 256
        long_password = "b" * 256
        self.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")
        self.driver.find_element(By.ID, "username").send_keys(long_username)
        self.driver.find_element(By.NAME, "password").send_keys(long_password)
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Неверный логин или пароль')]")))

    def test_successful_logout(self):
        """Тест 12: Успешный выход из системы"""
        # Предполагается успешный вход перед выходом
        self.test_successful_login()

        # Находим кнопку выхода и кликаем по ней
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Выйти']")))
        self.driver.find_element(By.XPATH, "//button[text()='Выйти']").click()

        # Проверяем, что пользователь вернулся на страницу входа
        WebDriverWait(self.driver, 10).until(EC.title_contains("Ростелеком ID"))
        self.assertIn("Ростелеком ID", self.driver.title)

    def test_profile_page_access_after_login(self):
        """Тест 13: Доступ к странице профиля после входа"""
        self.test_successful_login()  # Выполняем успешный вход

        # Переходим на страницу профиля
        self.driver.get("https://lk.rt.ru/#")

        # Проверяем заголовок страницы профиля
        WebDriverWait(self.driver, 10).until(EC.title_contains("Главная - Единый Личный Кабинет"))
        self.assertIn("Главная - Единый Личный Кабинет", self.driver.title)

    def test_no_access_to_profile_without_login(self):
        """Тест 14: Отказ в доступе к странице профиля без входа"""

        # Пытаемся перейти на страницу профиля без входа
        self.driver.get("https://lk.rt.ru/#")

        # Проверяем перенаправление на страницу входа
        WebDriverWait(self.driver, 10).until(EC.title_contains("Ростелеком ID"))
        self.assertIn("Ростелеком ID", self.driver.title)

    def test_account_settings_access_after_login(self):
        """Тест 15: Доступ к заявкам аккаунта после входа"""

        self.test_successful_login()  # Выполняем успешный вход

        # Переходим на страницу заявок аккаунта
        self.driver.get("https://lk.rt.ru/#orders")

        # Проверяем заголовок страницы заявок
        WebDriverWait(self.driver, 10).until( EC.title_contains("Мои заявки - Единый Личный Кабинет"))
        self.assertIn("Мои заявки - Единый Личный Кабинет", self.driver.title)

    def test_login_attempts_limit_exceeded(self):
        """Тест 16: Превышение лимита попыток входа"""

        for _ in range(5):  # Пробуем войти с неправильными данными несколько раз
            self.test_incorrect_password()

            # Проверяем сообщение о блокировке или превышении лимита попыток
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Введите символы с картинки')]")))

    def test_login_with_email_instead_of_username(self):
        """Тест 17: Вход с использованием email вместо логина"""

        self.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")

        # Вводим email вместо логина
        self.driver.find_element(By.NAME, "username").send_keys("iradidyk1@gmail.com")
        self.driver.find_element(By.NAME, "password").send_keys("Chto&kto")

        # Пытаемся войти
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()

        WebDriverWait(self.driver, 10).until(EC.title_contains("Неверный логин или пароль"))

    def test_remember_me_functionality(self):
        """Тест 18: Проверка функции 'Запомнить меня'"""

        self.test_successful_login()

        # Выходим из системы
        self.test_successful_logout()

        # Снова открываем страницу входа и проверяем наличие сохраненных данных
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

        username_field = self.driver.find_element(By.ID, "username")

        # Проверяем заполнено ли поле логина
        saved_username = username_field.get_attribute('value')

        self.assertEqual(saved_username, "89089638189")

    def test_password_visibility_toggle(self):
        """Тест 19: Проверка переключателя видимости пароля"""

        self.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")

        password_field = self.driver.find_element(By.NAME, "password")

        # Проверяем начальное состояние видимости пароля (должно быть скрыто)
        initial_type = password_field.get_attribute('type')

        toggle_button = self.driver.find_element(By.XPATH,
                                                 "//button[@class='rt-base-icon rt-base-icon--fill-path rt-eye-icon rt-input__eye']")

        toggle_button.click()

        # Проверяем изменилось ли состояние видимости пароля
        new_type = password_field.get_attribute('type')

        self.assertNotEqual(initial_type, new_type)

    def test_invalid_credentials_message_displayed(self):
        """Тест 20: Проверка отображения сообщения об ошибке при неверных данных для входа"""

        self.test_incorrect_username()

        # Проверяем сообщение об ошибке при неверных данных для входа

        error_message = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Неверный логин или пароль')]")))
        self.assertIsNotNone(error_message)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()