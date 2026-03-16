import logging
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Core_layer.Bot_package.Classes.Weather import Weather
from Core_layer.Bot_package.Classes.Finder import DuckduckgoFinder
from Core_layer.Bot_package.Classes.Finder import WikiFinder
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing
from Core_layer.Answer_package.Classes import GptAnswer
import re

class CommandAction(IAction.IAction):
    """
    It is class for comand's actions
    """
    boto = None
    message = None
    message_text = None
    user = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()
    _gpta = GptAnswer.GptAnswer()

    def __init__(self, message, message_text, user):
        CommandAction.message = message
        CommandAction.message_text = message_text
        CommandAction.user = user

    @classmethod
    def first(cls):
        # attack
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            prompt_is_attack = (
                "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
                f"Текст: {cls.message_text}\n\n"
                "Задача: Определи, является ли текст командой атаки на кого-то. "
                "Команда атаки содержит слова вроде: «фас», «атакуй», «пиздани», «нападай», «кусай», «цапни» и им подобные. "
                "Пользователь просит «атаковать» или «напасть» на человека по имени.\n\n"
                "Формат ответа: только True или False."
            )
            gpt_is_attack = cls._gpta.answer(prompt_is_attack, cls.user, True)
            is_attack = (not isinstance(gpt_is_attack, dict) and gpt_is_attack and gpt_is_attack.count("True") > 0)

            if is_attack:
                prompt_name = (
                    "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
                    f"Текст: {cls.message_text}\n\n"
                    "Задача: Извлеки из текста имя человека, на которого направлена команда атаки. "
                    "Убери служебные слова: «фас», «атакуй», «пиздани» и т.п. "
                    "Верни только имя в именительном падеже.\n"
                    "Примеры: «фас атакуй Петра» → Петр; «пиздани Ваню» → Ваня; "
                    "«атакуй Максима» → Максим; «фас Ивана» → Иван.\n\n"
                    "Формат ответа: только имя, без пояснений."
                )
                gpt_name = cls._gpta.answer(prompt_name, cls.user, True)
                name = str(gpt_name).strip() if (not isinstance(gpt_name, dict) and gpt_name) else cls.message_text
                if not name:
                    name = cls.message_text
                cls.command_flag = 1
                logging.info('The commandaction.first process is completed successfully')
                return name + ' - нехороший человек.'
        except Exception as e:
            logging.exception('The exception occurred in aaction.first: ' + str(e))

    @classmethod
    def second(cls):
        # translate
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception('The exception occurred in commandaction.second: ' + str(e))

    @classmethod
    def third(cls):
        # find
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # Промпт 1: определить, где искать (Википедия или интернет) — по полному тексту с «в википедии» и т.п.
            prompt_cmd = (
                "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
                f"Сообщение пользователя: {cls.message_text}\n\n"
                "Задача: По контексту определи, где пользователь просит искать.\n"
                "True — Википедия (явно «в википедии» или энциклопедические темы, биографии, история, наука, определения).\n"
                "False — общий интернет (новости, погода, отзывы, рецепты, инструкции, товары).\n\n"
                "Формат ответа: только True или False."
            )
            gpt_cmd = cls._gpta.answer(prompt_cmd, cls.user, True)
            use_wikipedia = (not isinstance(gpt_cmd, dict) and gpt_cmd and gpt_cmd.count("True") > 0)

            # Промпт 2: извлечь объект поиска из текста (после определения команды)
            prompt_object = (
                "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
                f"Текст: {cls.message_text}\n\n"
                "Задача: Извлеки из текста объект, который нужно искать. "
                "Убери служебные слова: «найди», «поищи», «в википедии», «в интернете» и т.п. "
                "Верни только суть запроса — ключевые слова, фразу или имя для поиска.\n"
                "Примеры: «найди Наполеона» → Наполеон; «поищи погоду в Москве» → погода в Москве; "
                "«найди в википедии кто такой Эйнштейн» → Эйнштейн.\n\n"
                "Формат ответа: только извлечённый объект поиска, без пояснений."
            )
            gpt_object = cls._gpta.answer(prompt_object, cls.user, True)
            search_object = str(gpt_object).strip() if (not isinstance(gpt_object, dict) and gpt_object) else cls.message_text
            if not search_object:
                search_object = cls.message_text

            if use_wikipedia:
                try:
                    apif = WikiFinder.WikiFinder(cls.__pr.preprocess_text(search_object))
                    finded_list = apif.find()
                    logging.info('The commandaction.find process has completed successfully (Wikipedia)')
                    return str(finded_list)
                except Exception as e:
                    logging.exception('The exception occurred in commandaction.third: ' + str(e))
                    return 'Не нашла'
            else:
                try:
                    gpif = DuckduckgoFinder.DuckduckgoFinder(search_object)
                    outstr = gpif.find()
                    logging.info('The commandaction.third process has completed successfully (Internet)')
                    return outstr
                except Exception as e:
                    logging.exception('The exception occurred in commandaction.third: ' + str(e))
                    return 'Не нашла'
        except Exception as e:
            logging.exception('The exception occurred in commandaction.third: ' + str(e))

    @classmethod
    def fourth(cls):
        # say
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # check if the message contains the word "скажи" (which means "say" in russian)
            # remove "скажи " from the message text
            message_text = (cls.message_text.replace('скажи ', '').replace(' скажи', '').replace('говори ', '')
                            .replace(' говори', ''))
            # log successful execution of the method
            logging.info('The commandaction.fourth process has completed successfully')
            # return the modified message text
            return message_text
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception in commandaction.fourth ' + str(e))

    @classmethod
    def fifth(cls):
        # weather
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            input = (
                "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
                "Анализируй текст и извлекай названия географических объектов (городов, населенных пунктов). \n\n"
                f"Сообщение: {cls.message_text}\n"
                "Правила:\n"
                "1. Извлекай ТОЛЬКО названия городов/населенных пунктов\n"
                "2. Возвращай название в исходной форме (именительный падеж, единственное число)\n"
                "3. Если в тексте несколько городов - возвращай все через запятую\n"
                "4. Если городов нет - возвращай город не найден\n"
                "5. Игнорируй другие типы географических объектов (реки, страны, регионы)\n"
                "6. Не добавляй пояснения, только результат\n"
                "Примеры:\n"
                "Сообщение: Мне нравится Париж и Берлин \n"
                "Результат: Париж, Берлин \n"
                "Сообщение: предскажи погоду в Нижнем Новгороде\n"
                "Результат: Нижний Новгород\n"
                "Сообщение: какая погода в Москве?\n"
                "Результат: Москва\n"
                "Сообщение: Здесь нет упоминаний населенных пунктов\n"
                "Результат: город не найден\n"
            )
            gpt_response = cls._gpta.answer(input, cls.user, True)

            if (gpt_response =='город не найден'):
                return "Город не найден"

            # get weather information for the specified location
            w = Weather.Weather(gpt_response)
            out = w.predict()
            # log successful execution
            logging.info('The commandaction.fifth process has completed successfully')
            if (out == "п. р"):
                return "Город не найден"
            return out
        except Exception as e:
            # log any exceptions that occur
            logging.exception('The exception occurred in commandaction.fifth: ' + str(e))
            return 'Проблемы с сервисом'

    @classmethod
    def sixth(cls):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception occurred in commandaction.sixth: ' + str(e)))

    @classmethod
    def seventh(cls):
        # clean
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            prompt_clean = (
                "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
                f"Текст: {cls.message_text}\n\n"
                "Задача: Удали из текста все служебные и ключевые слова команды очистки. "
                "Убери слова вроде: «почисти», «очисти», «очисть», «убери лишнее», «удали стоп-слова», "
                "«очисти текст», «почисти текст» и им подобные. "
                "Верни только оставшийся текст — суть, контент без команд.\n"
                "Примеры: «почисти этот текст» → этот текст; «очисти привет мир» → привет мир; "
                "«убери лишнее из: Мама мыла раму» → Мама мыла раму.\n\n"
                "Формат ответа: только очищенный текст, без пояснений."
            )
            gpt_clean = cls._gpta.answer(prompt_clean, cls.user, True)
            message_text = str(gpt_clean).strip() if (not isinstance(gpt_clean, dict) and gpt_clean) else cls.message_text
            if not message_text:
                message_text = cls.message_text
            pr = CommonPreprocessing.CommonPreprocessing()
            logging.info('The commandaction.tenth process has completed successfully')
            return pr.preprocess_text(message_text)
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception(str('The exception in commandaction.seventh ' + str(e)))


    @classmethod
    def eighth(cls):
        pass

    @classmethod
    def nineth(cls):
        # calculate
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
           pass
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in commandaction.nineth: ' + str(e))

    @classmethod
    def tenth(cls):
        # clean
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            prompt_clean = (
                "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
                f"Текст: {cls.message_text}\n\n"
                "Задача: Удали из текста все служебные и ключевые слова команды очистки. "
                "Убери слова вроде: «почисти», «очисти», «очисть», «убери лишнее», «удали стоп-слова», "
                "«очисти текст», «почисти текст» и им подобные. "
                "Верни только оставшийся текст — суть, контент без команд.\n"
                "Примеры: «почисти этот текст» → этот текст; «очисти привет мир» → привет мир; "
                "«убери лишнее из: Мама мыла раму» → Мама мыла раму.\n\n"
                "Формат ответа: только очищенный текст, без пояснений."
            )
            gpt_clean = cls._gpta.answer(prompt_clean, cls.user, True)
            message_text = str(gpt_clean).strip() if (not isinstance(gpt_clean, dict) and gpt_clean) else cls.message_text
            if not message_text:
                message_text = cls.message_text
            pr = CommonPreprocessing.CommonPreprocessing()
            logging.info('The commandaction.tenth process has completed successfully')
            return pr.preprocess_text(message_text)
        except Exception as e:
            logging.exception(str('The exception occurred in commandaction.tenth: ' + str(e)))
