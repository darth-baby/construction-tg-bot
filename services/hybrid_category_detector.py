import re
from fuzzywuzzy import fuzz
import fasttext
import os
from utils import resource_path
import logging  # Хорошая практика - добавить логирование


TECH_BUTTONS_DATA = [
    ("Автовышка", "tech:aerial_platform"),
    ("Автогрейдер", "tech:autograder"),
    ("Автокран", "tech:truck_crane"),
    ("Бетоновоз", "tech:concrete_mixer_truck"),
    ("Бульдозер", "tech:bulldozer"),
    ("Каток", "tech:road_roller"),
    ("Контейнер (ПУХТО)", "tech:container_pukhto"),
    ("Манипулятор", "tech:manipulator"),
    ("Мини-погрузчик", "tech:mini_loader"),
    ("Мини-экскаватор", "tech:mini_excavator"),
    ("Поливомоечная(коммунальная) техника", "tech:watering_communal"),
    ("Самосвал", "tech:dump_truck"),
    ("Тонар", "tech:tonar"),
    ("Трактор", "tech:tractor"),
    ("Трал", "tech:trawl"),
    ("Фронтальный погрузчик", "tech:front_loader"),
    ("Шаланда(длинномер)", "tech:flatbed_truck"),
    ("Эвакуатор", "tech:tow_truck"),
    ("Экскаватор гусеничный", "tech:crawler_excavator"),
    ("Экскаватор колесный", "tech:wheeled_excavator"),
    ("Экскаватор-погрузчик", "tech:loader_excavator"),
    ("Ямобур", "tech:auger_drill"),
]

# --- Синонимы и сокращения ---
CATEGORY_SYNONYMS = {
    "tech:truck_crane": ["автокран", "а/к", "кран"],
    "tech:loader_excavator": ["экскаватор погрузчик", "экскаватор-погрузчик", "эп"],
    "tech:crawler_excavator": ["экскаватор гусеничный", "гусянка", "эг"],
    "tech:wheeled_excavator": ["экскаватор колесный", "колесник", "эк"],
    "tech:manipulator": ["манипулятор"],
    "tech:dump_truck": ["самосвал", "камаз"],
    "tech:watering_communal": [
        "поливомоечная",
        "поливомоечка",
        "поливомоечная машина",
        "коммунальная",
    ],
}


# --- Быстрый словарный детектор ---
def detect_category_simple(text: str):
    text = text.lower()

    for name, code in TECH_BUTTONS_DATA:
        if name.lower() in text:
            return code

    for code, synonyms in CATEGORY_SYNONYMS.items():
        for word in synonyms:
            if word in text:
                return code
            if fuzz.partial_ratio(word, text) > 85:
                return code
    return None


# --- ML часть (fastText) ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), "tech_category.bin")
_model = None


def load_model():
    """Загружает модель fastText, если она еще не загружена."""
    global _model
    if _model is None:
        # --- ИСПОЛЬЗУЕМ НОВЫЙ ПОДХОД ---
        model_path = resource_path("services/tech_category.bin")
        if os.path.exists(model_path):
            try:
                _model = fasttext.load_model(model_path)
                logging.info(f"Модель fastText успешно загружена из {model_path}")
            except Exception as e:
                logging.error(f"Не удалось загрузить модель fastText: {e}")
        else:
            logging.warning(
                f"Файл модели 'tech_category.bin' не найден по пути {model_path}. ML-детектор будет отключен."
            )
    return _model


def detect_category_ml(text: str):
    model = load_model()
    if not model:
        return None
    text = re.sub(r"[^а-яa-z0-9\s]", " ", text.lower())
    label, prob = model.predict(text)
    if prob[0] > 0.6:
        return label[0]
    return None


# --- Гибрид ---
def detect_category(text: str):
    """Основная функция: ищет словарь → ML → None"""
    cat = detect_category_simple(text)
    if cat:
        return cat
    cat_ml = detect_category_ml(text)
    return cat_ml


# --- Тренировка модели (разово) ---
def train_model(dataset_path="train.txt"):
    # Для функции обучения тоже используем resource_path, чтобы она сохраняла модель рядом с .exe
    model_save_path = resource_path("tech_category.bin")

    # ... остальная логика обучения ...
    model = fasttext.train_supervised(
        input=dataset_path,
        lr=0.5,
        epoch=25,
        wordNgrams=2,
        dim=100,
    )
    model.save_model(model_save_path)
    print(f"✅ Модель обучена и сохранена в {model_save_path}")
