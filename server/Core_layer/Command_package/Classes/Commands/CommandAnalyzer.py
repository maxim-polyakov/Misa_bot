import logging
from Core_layer.Command_package.Interfaces import IAnalyzer
from Core_layer.Command_package.Classes.CommandActions import CommandAction
from Core_layer.Command_package.Classes.CommandActions import FCommandAction
from Core_layer.Command_package.Classes.CommandActions import SCommandAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing, CommonPreprocessing, CommandPreprocessing
from Core_layer.Answer_package.Classes import GptAnswer
import re

class CommandAnalyzer(IAnalyzer.IAnalyzer):
    """
    It is command analyzer
    """
    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()
    __cpr = CommandPreprocessing.CommandPreprocessing()
    __nothingflg = 0
    __cash = ''
    __boto = None
    __message = None
    __mesentype = None
    _gpta = GptAnswer.GptAnswer()

    def __init__(self, boto, message, mesentype):
        CommandAnalyzer.__boto = boto
        CommandAnalyzer.__message = message
        CommandAnalyzer.__mesentype = mesentype

    @classmethod
    def __action_step(cls, chosen_item, message_text):
        # step of action
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # create instances of different command action classes
            aone = FCommandAction.FCommandAction(cls.__message, message_text)
            asixteen = SCommandAction.SCommandAction(cls.__message, message_text)
            ac = CommandAction.CommandAction(cls.__message, message_text)
            # create a dictionary mapping command words to their corresponding method results
            info_dict = {
                '1': str(aone.first()),
                '2': str(aone.second()),
                '3': str(aone.third()),
                '4': str(asixteen.seventh()),
                '5': str(ac.first()),
                '6': str(ac.third()),
                '7': str(ac.fourth()),
                '8': str(ac.fifth()),
                '9': str(ac.seventh()),
                '10': str(ac.tenth())
                }
            # log successful completion of the process
            logging.info('The commandanalyzer.__action_step process has completed successfully')
            # return the corresponding value from the dictionary
            return info_dict[chosen_item]
        except Exception as e:
            # log successful completion of the process
            logging.info('The commandanalyzer.__action_step process has not completed successfully')
            return ''

    @classmethod
    def neurocheck(cls, message_text):
        input = (
            "Новый запрос. Не учитывай предыдущие сообщения.\n\n"
            f"Команда: {message_text}\n"
            "Список команд:\n"
            "1 - абонировать\n"
            "2 - абонироваться\n"
            "3 - нарисовать\n"
            "4 - атаковать\n"
            "5 - фас\n"
            "6 - находить\n"
            "7 - сказать\n"
            "8 - погода\n"
            "9 - почистить\n"
            "10 - очищать\n"
            "11 - команды нет в списке\n\n"
            "Задача: Найди команду(ы) в списке. Учитывай контекст высказывания: "
            "если фраза выражает совет, описание, мысль или эмоциональное высказывание, "
            "а не прямую команду, верни 11. Если это прямая команда на действие, "
            "найди соответствующий номер(а) в списке и верни их через запятую.\n"
            "Формат ответа: только цифры, без дополнительного текста."
        )
        gpt_response = cls._gpta.answer(input)
        return gpt_response

    @classmethod
    def __action(cls, message_text):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # Проверяем, является ли сообщение кодом (CSS, JS, HTML и т.д.)
            if cls.__is_code_message(message_text):
                # Для кода возвращаем специальный маркер, пропускаем NLP обработку
                return ''

            # Обычная обработка только для текстовых сообщений
            outlist = []
            # Берем только первые 10 слов для анализа (оптимизация)
            check = cls.neurocheck(message_text)
            array_of_message_text = check.split(',')

            for word in array_of_message_text:
                processed_word = cls.__action_step(word, message_text)
                if processed_word:
                    outlist.append(processed_word)

            outlist = list(set(outlist))
            logging.info('Commandanalyzer.__action process completed successfully')
            return outlist

        except Exception as e:
            logging.exception('Exception in commandanalyzer.__action: ' + str(e))

    @classmethod
    def __is_code_message(cls, text):
        """Быстрая проверка на код (CSS, JS, HTML, XML и т.д.)"""

        code_indicators = [
            '{', '}', ':', ';', '=', '<', '>', '/',
            'function', 'var', 'const', 'let', 'class', 'import',
            'margin', 'padding', 'font', 'color', 'background',
            '<?php', '<html', '<div', '<script', '<style'
        ]

        # Быстрая проверка по первым 200 символам
        preview = text[:200]
        indicator_count = sum(1 for indicator in code_indicators if indicator in preview)
        return indicator_count >= 2

    @classmethod
    def __has_unknown_commands(cls, message_text, known_commands):
        """Проверяет, есть ли в сообщении неизвестные команды (без #)"""
        # Ищем все хештеги в сообщении (без решетки)
        all_hashtags = re.findall(r'#(\w+)', message_text.lower())

        # Проверяем, есть ли хештеги, которых нет в known_commands
        known_commands_set = set(known_commands)
        unknown_commands = [tag for tag in all_hashtags if tag not in known_commands_set]

        return len(unknown_commands) > 0

    @classmethod
    def analyse(cls, message_text):
        # analise commands
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outstr = ''
            command_executed = False  # Флаг для отслеживания выполнения команды
            known_commands = ['абонируй', 'абонируйся', 'нарисуй', 'атакуй',
                              'фас', 'найди', 'скажи', 'погода', 'почисти', 'очисти']

            # Сначала проверяем весь текст целиком на наличие команд
            outlist = cls.__action(message_text)
            if outlist:
                for outmes in outlist:
                    outstr += str(outmes) + '|\n'
                command_executed = True

            # Если в целом тексте не найдено команд, пробуем разбить на предложения
            if not outstr:
                # check if the message contains periods (.) to determine sentence splitting
                if (message_text.count('.') > 0):
                    word_arr = message_text.split('. ')
                else:
                    word_arr = message_text.split(', ')

                # process each word or phrase in the array
                for word in word_arr:
                    outlist = cls.__action(word)
                    if outlist:
                        for outmes in outlist:
                            outstr += str(outmes) + '|\n'
                        command_executed = True

            # log successful completion of the analysis process
            logging.info('The commandanalyzer.analyse process has completed successfully')

            # Проверяем, есть ли неизвестные команды
            has_unknown_commands = cls.__has_unknown_commands(message_text, known_commands)

            # Логика ответа:
            if command_executed and not has_unknown_commands:
                # Только известные команды - возвращаем только результат команды
                return outstr
            elif command_executed and has_unknown_commands:
                # Есть и известные и неизвестные команды - результат команды + GPT
                gpt_response = cls._gpta.answer(message_text)
                return f"{outstr}" + "|\n" + f"{gpt_response}"
            elif not command_executed and has_unknown_commands:
                # Только неизвестные команды - только GPT
                return cls._gpta.answer(message_text)
            else:
                # Нет команд вообще - только GPT
                return cls._gpta.answer(message_text)

        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in commandanalyzer.analyse: ' + str(e))
