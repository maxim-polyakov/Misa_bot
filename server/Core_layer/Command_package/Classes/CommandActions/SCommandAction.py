import logging
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing
from Core_layer.Answer_package.Classes import GptAnswer

class SCommandAction(IAction.IAction):
    """
    It is class for comand's actions started on symbol a
    """
    boto = None
    message = None
    message_text = None
    user = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text, user):
        SCommandAction.message = message
        SCommandAction.message_text = message_text
        SCommandAction.user = user

    @classmethod
    def first(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.first ' + str(e)))

    @classmethod
    def second(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.second ' + str(e)))

    @classmethod
    def third(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.third ' + str(e)))

    @classmethod
    def fourth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.fourth ' + str(e)))

    @classmethod
    def fifth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.fifth ' + str(e)))

    @classmethod
    def sixth(cls):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.sixth ' + str(e)))

    @classmethod
    def seventh(cls):
#
#       атаковать
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
                return name + ' - пидор.'
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.seventh ' + str(e)))

    @classmethod
    def eighth(cls):
#
#       атаковаться
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
            logging.exception(str('The exception in scommandaction.eighth ' + str(e)))

    @classmethod
    def nineth(cls):
#
#       атаковывать
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.nineth ' + str(e)))

    @classmethod
    def tenth(cls):
#
#       атаковываться
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception in aactionsixteen.tenth ' + str(e)))