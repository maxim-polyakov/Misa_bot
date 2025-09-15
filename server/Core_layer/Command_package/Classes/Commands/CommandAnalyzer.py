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
            return outlist if outlist else ['general_query']

        except Exception as e:
            logging.exception('Exception in commandanalyzer.__action: ' + str(e))

    @classmethod
    def __is_code_message(cls, text):
        """Быстрая проверка на код (CSS, JS, HTML, XML и т.д.)"""
        if len(text) > 2000:  # Длинные сообщения вероятно код
            return True

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
        # Простое логирование в консоль
        def log(message, level='info'):
            print(f"{level.upper()} - {message}")

        try:
            log(f'🚀 Starting analysis of message: "{message_text}"')

            outstr = ''

            dot_count = message_text.count('.')
            if dot_count > 0:
                word_arr = message_text.split('. ')
                log(f'📝 Split by periods. Got {len(word_arr)} parts')
            else:
                word_arr = message_text.split(', ')
                log(f'📝 Split by commas. Got {len(word_arr)} parts')

            processed_count = 0
            for i, word in enumerate(word_arr):
                log(f'🔍 Processing part {i}: "{word}"', 'debug')

                outlist = cls.__action(word)

                if outlist is not None:
                    processed_count += 1
                    for outmes in outlist:
                        outstr += str(outmes) + '\n'
                    log(f'✅ Added output from part {i}')

            log(f'📊 Processed {processed_count}/{len(word_arr)} parts with results')

            empty_patterns = ['\n\n', '', '\n', '\nNone\n', 'none']
            if outstr in empty_patterns:
                log('⚠️ Output' + outstr + ' is empty, falling back to GPT answer', 'warning')
                gpt_response = cls._gpta.answer(message_text)
                log(f'🤖 GPT response received')
                return gpt_response

            log(f'🎯 Returning processed output')
            return outstr

        except Exception as e:
            log(f'❌ Exception: {str(e)}', 'error')
            raise
