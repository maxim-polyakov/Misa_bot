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
                '7': str(ac.fifth()),
                '8': str(ac.seventh()),
                '9': str(ac.tenth())
                }
            # log successful completion of the process
            logging.info('The commandanalyzer.__action_step process has completed successfully')
            # return the corresponding value from the dictionary
            return info_dict[chosen_item]
        except Exception as e:
            # log successful completion of the process
            logging.info('The commandanalyzer.__action_step process has not completed successfully')
            return 'команды нет в списке'

    @classmethod
    def neurocheck(cls, message_text, user):
        message_text = message_text.replace('\n', ' ')
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
            "7 - погода\n"
            "8 - почистить\n"
            "9 - очищать\n"
            "10 - команды нет в списке\n\n"
            "Задача: Найди команду(ы) в списке, строго учитывая контекст. "
            "Если фраза выражает совет, описание, размышление или эмоцию — не учитывай как команду. "
            "Если в тексте есть действие, которого нет в списке команд, включай 10 только если это реальная отдельная команда, "
            "а не объект, дополнение или описание к существующей команде. "
            "Только прямое побуждение к действию считается командой. "
            "Может быть несколько команд одновременно. "
            "Верни все номера через запятую.\n"
            "Может быть код, возвращать код не нужно, нужно проанализировать контекст с кодом \n"
            "Формат ответа: только цифры, без дополнительного текста."
        )
        gpt_response = cls._gpta.answer(input,user, True)
        return gpt_response

    @classmethod
    def __action(cls, message_text, user):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # Обычная обработка только для текстовых сообщений
            outlist = []
            # Берем только первые 10 слов для анализа (оптимизация)
            check = cls.neurocheck(message_text, user)
            array_of_message_text = check.split(',')

            for word in array_of_message_text:
                processed_word = cls.__action_step(word, message_text)
                outlist.append(processed_word)

            outlist = list(set(outlist))
            logging.info('Commandanalyzer.__action process completed successfully')
            return outlist

        except Exception as e:
            logging.exception('Exception in commandanalyzer.__action: ' + str(e))

    @classmethod
    def analyse(cls, message_text, user):
        # analise commands
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outstr = ''
            command_executed = False  # Флаг для отслеживания выполнения команды
            has_unknown_command_response = False  # Флаг для "команды нет в списке"
            known_commands = ['абонируй', 'абонируйся', 'нарисуй', 'атакуй',
                              'фас', 'найди', 'погода', 'почисти', 'очисти']

            # Сначала проверяем весь текст целиком на наличие команд
            outlist = cls.__action(message_text, user)
            if outlist:
                for outmes in outlist:
                    # Проверяем, является ли результат "команды нет в списке"
                    if 'команды нет в списке' in str(outmes):
                        has_unknown_command_response = True
                    else:
                        # Добавляем только валидные команды
                        outstr += str(outmes) + '|command|\n'
                        command_executed = True


            # ДОБАВИМ ОТЛАДОЧНУЮ ИНФОРМАЦИЮ
            logging.info(f'command_executed: {command_executed}')

            logging.info(f'outstr: {outstr}')

            # Логика ответа:
            if command_executed and not has_unknown_command_response:
                # Только известные команды - возвращаем только результат команды
                logging.info('Case 1: Only known commands')
                return outstr
            elif command_executed and (has_unknown_command_response):
                # Есть и известные и неизвестные команды - результат команды + GPT
                logging.info('Case 2: Mixed commands - command + GPT')
                gpt_response = cls._gpta.answer(message_text, user, False)
                return f"{outstr}" + "|command|\n" + f"{gpt_response}"
            elif has_unknown_command_response:
                # Только неизвестные команды или "команды нет в списке" - только GPT
                logging.info('Case 3: Only unknown commands - GPT only')
                return cls._gpta.answer(message_text,user, False)
            else:
                # Нет команд вообще - только GPT
                logging.info('Case 4: No commands - GPT only')
                return cls._gpta.answer(message_text,user, False)

        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in commandanalyzer.analyse: ' + str(e))