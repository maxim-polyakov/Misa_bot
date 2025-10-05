import logging
from Core_layer.Command_package.Interfaces import IAnalyzer
from Core_layer.Command_package.Classes.CommandActions import CommandAction
from Core_layer.Command_package.Classes.CommandActions import FCommandAction
from Core_layer.Command_package.Classes.CommandActions import SCommandAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing, CommonPreprocessing, CommandPreprocessing
from Core_layer.Answer_package.Classes import GptAnswer

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
                'абонировать': str(aone.first()),
                'абонироваться': str(aone.second()),
                'нарисовать': str(aone.third()),
                'атаковать': str(asixteen.seventh()),
                'фас': str(ac.first()),
                'находить': str(ac.third()),
                'сказать': str(ac.fourth()),
                'погода': str(ac.fifth()),
                'почистить': str(ac.seventh()),
                'очищать': str(ac.tenth())
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
            array_of_message_text = message_text.split(' ')[:10]

            for word in array_of_message_text:
                processed_word = cls.__action_step(cls.__pr.preprocess_text(word), message_text)
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
    def analyse(cls, message_text):
        # analise commands
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outstr = ''
            command_executed = False  # Флаг для отслеживания выполнения команды

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

            # Если команда выполнена, возвращаем результат команды + GPT-ответ
            if command_executed:
                gpt_response = cls._gpta.answer(message_text)
                # Комбинируем результат команды и GPT-ответ
                combined_response = f"{outstr}\n|\n{gpt_response}"
                return combined_response

            # Если команд не найдено, возвращаем только GPT-ответ
            logging.debug('outstr ' + outstr)
            if outstr == '\n\n' or outstr == '' or outstr == '\n' or outstr == '\nNone\n' or outstr == 'none':
                return cls._gpta.answer(message_text)
            return outstr

        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in commandanalyzer.analyse: ' + str(e))
