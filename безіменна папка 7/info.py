import telebot
import logging
from telebot import types
import time


bot = telebot.TeleBot("")


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


restaurants = {
    "Країна мрій": {
        "Київ": {
            "графік": "Пн-Пт: 10:00-22:00, Сб-Нд: 11:00-23:00",
            "місце": "Адреса в Києві",
            "телефон": "+380123456789",
            "меню_файл": "menu_kyiv.pdf",
            "сезонне_меню": "Країна Мрій_Осіннє меню 2023_A4--.pdf",
            "виїзати_анімації": "https://www.krainamriy.fun/ua/kyiv/animatory/",
            "святкові_послуги": "Замовлення свята Київ_2023_new.pdf",
            "акції": ["1.png"],
            "безкоштовні_програми": ["2.png"]
        },
        
    },
    "FunPlanet": {
        "ресторан1": {
            "графік": "Графік ресторану FunPlanet",
            "місце": "Адреса ресторану FunPlanet",
            "телефон": "+380987654321",
            "меню_файл": "menu_funplanet.pdf"
        },
        
    },
    "Questopia": {
        "ресторан2": {
            "графік": "Графік ресторану Questopia",
            "місце": "Адреса ресторану Questopia",
            "телефон": "+380555555555",
            "меню_файл": "menu_questopia.pdf"
        },
        
    }
}


категории = list(restaurants.keys())

TELEPHONE = "+380123456789"

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for category in категории:
        markup.add(types.KeyboardButton(category))
    bot.send_message(message.chat.id, f"Привіт, {user.first_name}! Виберіть категорію:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_category_choice)
    logger.info(f"Пользователь {user.first_name} начал работу с ботом.")

def handle_category_choice(message):
    user_choice = message.text
    chat_id = message.chat.id
    logger.info(f"Пользователь выбрал категорию: {user_choice}")

    if user_choice in категории:
        category = user_choice
        if category == "Країна мрій":
            city = "Київ"
            city_info = f"Місто: {city}\n"
            city_info += f"Графік: {restaurants[category][city]['графік']}\n"
            city_info += f"Місце розташування: {restaurants[category][city]['місце']}\n"
            city_info += f"Телефон: {TELEPHONE}\n"
            bot.send_message(chat_id, city_info)
            logger.info(f"Отправлена информация о ресторане в Киеве")

            # Добавьте кнопки "Сезонне меню" и "Виїздні анімації"
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            download_menu_button = types.KeyboardButton("Скачати меню")
            seasonal_menu_button = types.KeyboardButton("Сезонне меню")
            exit_animations_button = types.KeyboardButton("Виїздні анімації")
            holiday_services_button = types.KeyboardButton("Святкові послуги")
            promotions_button = types.KeyboardButton("Акції")
            free_programs_button = types.KeyboardButton("Безкоштовні програми")
            markup.row(download_menu_button, seasonal_menu_button, exit_animations_button)
            markup.row(holiday_services_button, promotions_button, free_programs_button)
            bot.send_message(chat_id, "Оберіть дію:", reply_markup=markup)
            bot.register_next_step_handler(message, handle_menu_actions, category=category, restaurant=city)
        elif category == "FunPlanet":
            
            pass
        else:
            category_info = f"Категорія: {category}\n"
            bot.send_message(chat_id, category_info)
    else:
        bot.send_message(chat_id, "Категорію не знайдено. Виберіть іншу категорію:")
        bot.register_next_step_handler(message, handle_category_choice)

def handle_menu_actions(message, category, restaurant):
    user_choice = message.text
    chat_id = message.chat.id
    logger.info(f"Пользователь выбрал действие: {user_choice}")

    if user_choice == "Скачати меню":
        menu_file = restaurants[category][restaurant]["меню_файл"]
        send_document(chat_id, menu_file)
    elif user_choice == "Сезонне меню":
        seasonal_menu_file = restaurants[category][restaurant]["сезонне_меню"]
        send_document(chat_id, seasonal_menu_file)
    elif user_choice == "Виїздні анімації":
        if "виїзати_анімації" in restaurants[category][restaurant]:
            animation_url = restaurants[category][restaurant]["виїзати_анімації"]
            bot.send_message(chat_id, f"Вас перенаправлено на сайт виїздних анімацій: {animation_url}")
            logger.info(f"Пользователь перенаправлен на сайт виїздних анімацій.")
        else:
            bot.send_message(chat_id, "Ця послуга недоступна для даного ресторану.")
            logger.info("Пользователь получил сообщение о недоступности услуги.")
    elif user_choice == "Святкові послуги":
        holiday_services_file = restaurants[category][restaurant]["святкові_послуги"]
        send_document(chat_id, holiday_services_file)
    elif user_choice == "Акції":
        send_all_images(chat_id, restaurants[category][restaurant]["акції"])
    elif user_choice == "Безкоштовні програми":
        send_all_images(chat_id, restaurants[category][restaurant]["безкоштовні_програми"])

def send_document(chat_id, file_path):
    with open(file_path, 'rb') as file:
        bot.send_document(chat_id, file, caption="Завантаження документу...")
        logger.info(f"Отправлен документ: {file_path}")

def send_all_images(chat_id, images):
    for image in images:
        with open(image, 'rb') as img:
            bot.send_photo(chat_id, img)
            logger.info(f"Отправлена картинка: {image}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
