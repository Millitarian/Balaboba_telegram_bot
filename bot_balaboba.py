import telebot
from telebot import types
from balaboba import Balaboba

bb = Balaboba()
text_types = bb.get_text_types(language="ru")
bot = telebot.TeleBot('6140575940:AAGKdGypAgdqrPkjgrqoTWRFSK2EryPqjQ4')


button_generate = types.KeyboardButton("Набалабобить")
button_type = types.KeyboardButton("Выбор стиля балабобы")
button_continue = types.KeyboardButton("Добалабобить")
button_menu = types.KeyboardButton("Выход в меню")
button_generate_again = types.KeyboardButton("Перебалабобить")

# Создание кнопок настроек
button_model = types.KeyboardButton("Стиль")
style_button_a = types.KeyboardButton("Стандарт")
style_button_c = types.KeyboardButton("Рецепт")
style_button_d = types.KeyboardButton("Народные мудрости")
style_button_e = types.KeyboardButton("Короткие истории")
style_button_f = types.KeyboardButton("Определение для слов")
style_button_g = types.KeyboardButton("Сюжет фильма по названию")
style_button_h = types.KeyboardButton("Предсказание по имени или знаку зодиака")

# Создание переменных под настройки
balaboba_style = 0
text_after_generation = "Продолженный текст"
text_for_generation = "Начальный текст"
overflow_text = "Напишите что-нибудь и получите продолжение от балабобы"
num_of_symbols = 0

# Создание шаблонов клавиатур
keyboard_type = types.ReplyKeyboardMarkup(row_width=1)
keyboard_type.add(style_button_a, style_button_c, style_button_d,
                  style_button_e, style_button_f, style_button_g, style_button_h)

keyboard_main = types.ReplyKeyboardMarkup(row_width=2)
keyboard_main.add(button_type, button_generate)

keyboard_vibor = types.ReplyKeyboardMarkup(row_width= 2)
keyboard_vibor.add(button_menu, button_continue, button_generate, button_generate_again)

# Нужные флажки
generation_flag = False

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Бот активирован', reply_markup= keyboard_main)
    bot.send_message(message.chat.id, "*DISCLAIMER!!!*\n"
                                      "Генератор может выдавать очень странные тексты. Пожалуйста, будьте разумны, "
                                      "распространяя их. Подумайте, не будет ли текст обидным для кого-то и не станет "
                                      "ли его публикация нарушением закона.", parse_mode='Markdown')
    bot.register_next_step_handler(message, main_handler)

@bot.message_handler(commands=['choice'])
def main_handler(message):
    global generation_flag
    generation_flag = False
    if message.text == button_generate.text:
        bot.send_message(message.chat.id, overflow_text, reply_markup= types.ReplyKeyboardRemove())
        generation_flag = True
    elif message.text == button_type.text:
        bot.send_message(message.chat.id, "Выберите стиль", reply_markup= keyboard_type)
        bot.register_next_step_handler(message, types_handler)

@bot.message_handler(commands= ["type_settings"])
def types_handler(message):
    global balaboba_style,style_button_a, style_button_c, style_button_d, \
        style_button_e, style_button_f, style_button_g, style_button_h, overflow_text
    if message.text == style_button_a.text:
        balaboba_style = 0
        overflow_text = "Напишите что-нибудь и получите продолжение от балабобы"
    elif message.text == style_button_c.text:
        balaboba_style = 3
        overflow_text = "Перечислите съедобные ингредиенты, а Балабоба придумает рецепт с ними"
    elif message.text == style_button_d.text:
        balaboba_style = 4
        overflow_text = "Напишите что-нибудь и получите народную мудрость"
    elif message.text == style_button_e.text:
        balaboba_style = 5
        overflow_text = "Начните писать историю, а Балабоба продолжит"
    elif message.text == style_button_f.text:
        balaboba_style = 6
        overflow_text = "Напишите какое-нибудь слово, а Балабоба даст этому определение"
    elif message.text == style_button_g.text:
        balaboba_style = 7
        overflow_text = "Напишите название фильма (существующего или нет), а Балабоба расскажет вам, о чем он"
    elif message.text == style_button_h.text:
        balaboba_style = 8
        overflow_text = "Введите имя или знак зодиака, чтобы получить шуточное предсказание"

    bot.send_message(message.chat.id, 'Возврат в главное меню', reply_markup=keyboard_main)
    bot.register_next_step_handler(message, main_handler)

@bot.message_handler(commands= ['vibor'])
def vibor(message):
    global text_for_generation, text_after_generation, num_of_symbols
    if message.text == button_menu.text:
        bot.send_message(message.chat.id, "Переход в главное меню", reply_markup = keyboard_main)
        bot.register_next_step_handler(message, main_handler)
    elif message.text == button_generate.text:
        bot.send_message(message.chat.id, "Введите новый текст для генерации",
                         reply_markup= types.ReplyKeyboardRemove())
    elif message.text == button_continue.text:
        num_of_symbols = len(text_after_generation)-len(text_for_generation)
        text_after_generation = text_after_generation[-num_of_symbols:]
        text_after_generation = bb.balaboba(text_after_generation, text_type=text_types[balaboba_style])
        bot.send_message(message.chat.id, f"Набалабоблено:\n\n{text_after_generation[-(len(text_after_generation)-num_of_symbols-1):]}",
                         reply_markup= keyboard_vibor)
        bot.register_next_step_handler(message, vibor)
    elif message.text == button_generate_again.text:
        text_after_generation = bb.balaboba(text_for_generation, text_type=text_types[balaboba_style])
        bot.send_message(message.chat.id, f"Перебалабоблено:\n\n{text_after_generation}",
                         reply_markup= keyboard_vibor)
        bot.register_next_step_handler(message, vibor)

@bot.message_handler(func= lambda message: True)
def messages_handler(message):
    global generation_flag, text_for_generation, text_after_generation
    if generation_flag:
        text_for_generation = message.text
        text_after_generation = bb.balaboba(text_for_generation, text_type=text_types[balaboba_style])
        bot.send_message(message.chat.id, f"Набалабоблено:\n\n{text_after_generation}",
                         reply_markup = keyboard_vibor)
        bot.register_next_step_handler(message, vibor)
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так, возврат в главное меню", reply_markup= keyboard_main)
        bot.register_next_step_handler(message, main_handler)

bot.polling(non_stop=True)