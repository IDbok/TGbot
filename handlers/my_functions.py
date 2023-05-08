from dict import currency_dict
from dict import category_list

# Функция по поиску разделителя
def find_separator(text):
    # Определяем возможные разделители
    separators = ['/', '\\', '|', ' ']

    # Ищем разделитель в сообщении
    for sep in separators:
        if sep in text:
            return sep
    return None

# Функция по вычленению валюты из сообщения. Возвращает первое встречающееся упоминание валюты
def find_currency(text_as_list, default_currency: str = "лар" ):
    currencies = []
    for currency, aliases in currency_dict.items():
        for alias in aliases:
            if alias in text_as_list and currency not in currencies:
                currencies.append(currency)
                # Записываем индекс первого вхождения валюты в списке words
                currencies[-1] = (currency, text_as_list.index(alias))
    # Сортируем список валют по индексу их первого вхождения в сообщении
    currencies.sort(key=lambda x: x[1])
    if currencies == []:
        currencies = [(default_currency, 0)]
    # Удаляем индексы из списка валют
    return currencies[0] #[currency for currency, index in currencies][0]

# Функция по поиску числа в сообщении. Возвращает первое встречающееся упоминание валюты
def find_amount(text_as_list):
    digits = []
    for digit in text_as_list:
        if digit.isdigit():
            digits.append(digit)
            # Записываем индекс
            digits[-1] = (digit, text_as_list.index(digit))
    # Сортируем список по индексу их первого вхождения в сообщении
    digits.sort(key=lambda x: x[1])
    return digits[0]

# Функция по поиску категории затрат
def find_category(text_as_list, default_category: str = 'Прочее'):
    categorys = []
    for word in text_as_list:
        if word.capitalize() in category_list:
            categorys.append(word.capitalize())
            # Записываем индекс
            categorys[-1] = (word.capitalize(), text_as_list.index(word))
    # Сортируем список по индексу их первого вхождения в сообщении
    categorys.sort(key=lambda x: x[1])
    if categorys == []:
        categorys = [(default_category, 0)]
    return categorys[0]

# Функция по обработки входного сообщения и формирования ответа
def text_message(message_info, text_spliter="/"):


    # Создаём используемые переменные [amount, currency, category, note]
    # message_info = [message.chat.id, message.chat.username, message.chat.first_name, message.text, message.date]
    amount = ''
    currency = ''
    category = ''
    note = ''

    text_in_list = message_info[3].split(text_spliter, 3)

    # Проверяю налиние необходимых параметров в сообщении и заполняем переменные для БД

    # Сначала проверю есть ли вторым значение в списке валюта

    if len(text_in_list) >= 2:

        # Проверяем, что первое значение это число
        if text_in_list[0].isdigit():
            amount = text_in_list[0]

            # Проверяем на наличие обозначения валюты, если нет, то присваиваем лар
            if text_in_list[1].lower() in currency_list:
                currency = text_in_list[1].lower()

                # Проверяем категорию, если это послений элемент списка и не удовлетворяет ни одной категории, то
                # вставляем в категорию прочее и устанавличаем его как примечание
                if text_in_list[2].title() in category_list:
                    category = text_in_list[2].title()
                else:
                    if category == '':
                        category = "Прочее"
                        note = text_in_list[2]
                    pass

            else:
                currency = "лар"
                if text_in_list[1].title() in category_list:
                    category = text_in_list[1].title()
                    if len(text_in_list) == 3:
                        note = text_in_list[2]
                    else:
                        pass  # return "Что-то не так, проверь порядок ввода данных (сумма/(валюта)/Категория/(примечание)"

                else:
                    if len(text_in_list) == 2:
                        category = "Прочее"
                        note = text_in_list[1]
                    else:
                        return f"Категория {text_in_list[1]} не определена"
        else:
            return "Поставь первым число"

        return [amount, currency, category, note]
    else:
        return "Недостаточно данных. \n" \
               "Проверь порядок ввода данных: сумма/(валюта)/Категория/(примечание)\n" \
               "То что в скобках вводить необязательно.\n" \
               "Валюта по умолчанию лар.\n" \
               "Валюту пиши как руб,лар или дол"


def bd_list_from_message(message_text, text_spliter="/", currency_defolt = 'лари'):
    # Создаём список для загрузки в БД [amount, currency, category, note]
    # Разбиваем сообщение на строки по разделителю
    text_as_list = message_text.split(text_spliter)
    # Ищем есть ли указание валюты в сообщении и выводим его. Если валюты нет, выводим валюту по умолчанию
    currency = find_currency(text_as_list)
    if currency[0] == None:
        currency = currency_defolt
    # Поиск числа и вывод первого числа в списке
    amount = find_amount(text_as_list)
    # Поиск категории. В случае если категории нет, возвращаю "Прочее"
    category = find_category(text_as_list)
    # Поиск наличия примечания
    note_list_index = max([amount[1], currency[1], category[1]])+1
    note = ''
    if note_list_index+1 <= len(text_as_list):
        note_index = message_text.find(text_as_list[note_list_index])
        note = message_text[note_index:]

    return [amount[0], currency[0], category[0], note ]

def message_processing(message_info):
    # message_info = [message.chat.id, message.chat.username, message.chat.first_name, message.text, message.date]
    Error_message = ''
    bd_list = []
    results = [bd_list , Error_message]
    message_text = message_info[3]

    # Определение разделителя в тексте
    if find_separator(message_text) !=None:
        text_spliter = find_separator(message_text)
    else:
        Error_message = 'Не был найдень разделитель в тексте'
        return [bd_list , Error_message]
    # print(f'Разделитель "{text_spliter}"')

    text_as_list = message_text.split(text_spliter)
    # Проверка, есть ли число в сообщении
    check_digit = False
    for digit in text_as_list:
        if digit.isdigit():
            check_digit = True

    # Применяем функцию создания данный вносимых в БД
    if check_digit:
        bd_list = bd_list_from_message(message_text, text_spliter)
    else:
        Error_message = 'Не увидел числа. Проверь сообщение!'
        print(Error_message)
        return [bd_list , Error_message]


    return [bd_list , Error_message]