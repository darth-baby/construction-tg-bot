# Файл: services/database.py
import sqlite3
import logging


class Database:
    def __init__(self, db_file="bot_database.db"):
        """Инициализация соединения с БД."""
        try:
            self.connection = sqlite3.connect(db_file)
            self.cursor = self.connection.cursor()
            logging.info(f"Успешное подключение к базе данных: {db_file}")
        except sqlite3.Error as e:
            logging.error(f"Ошибка подключения к БД: {e}")
            raise

    def setup(self):
        """Создает таблицы, если они не существуют."""
        with self.connection:
            # 1. Таблица пользователей
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 2. Справочник категорий техники
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tech_categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    callback_data TEXT NOT NULL UNIQUE
                )
            """)

            # 3. Таблица подписок (связывает users и tech_categories)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    user_id INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    radius_km INTEGER DEFAULT 50, -- Радиус по умолчанию
                    is_active BOOLEAN DEFAULT 1,
                    
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES tech_categories (category_id) ON DELETE CASCADE,
                    PRIMARY KEY (user_id, category_id)
                )
            """)
        logging.info("Структура таблиц базы данных проверена/создана.")

    def add_user(self, user_id: int, username: str, first_name: str):
        """Добавляет нового пользователя, если он не существует."""
        with self.connection:
            self.cursor.execute(
                "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                (user_id, username, first_name),
            )

    def populate_tech_categories(self, tech_buttons: list):
        """Заполняет справочник техники (выполняется один раз при старте)."""
        try:
            with self.connection:
                self.cursor.executemany(
                    "INSERT OR IGNORE INTO tech_categories (name, callback_data) VALUES (?, ?)",
                    tech_buttons,
                )
        except sqlite3.Error as e:
            logging.error(f"Ошибка при заполнении категорий техники: {e}")

    def add_or_update_subscription(self, user_id: int, category_callback: str):
        """Добавляет или обновляет подписку. Возвращает True/False."""
        try:
            with self.connection:
                category_id_result = self.cursor.execute(
                    "SELECT category_id FROM tech_categories WHERE callback_data = ?",
                    (category_callback,),
                ).fetchone()

                if not category_id_result:
                    logging.warning(f"Категория {category_callback} не найдена в БД!")
                    return False

                category_id = category_id_result[0]

                # INSERT OR REPLACE обновит запись, если она существует (по PRIMARY KEY), или создаст новую.
                self.cursor.execute(
                    "INSERT OR REPLACE INTO subscriptions (user_id, category_id) VALUES (?, ?)",
                    (user_id, category_id),
                )
                return True
        except sqlite3.Error as e:
            logging.error(f"Ошибка при добавлении подписки для user_id={user_id}: {e}")
            return False


# Создаем единый экземпляр класса для всего приложения
db = Database()
