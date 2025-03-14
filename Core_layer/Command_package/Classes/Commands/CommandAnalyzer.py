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
            logging.info('The commandanalyzer.__action_step process has completed successfully')
            return ''

    @classmethod
    def __action(cls, message_text):
        # action of command
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # initialize an empty list to store processed words
            outlist = []
            # split the input text into words
            array_of_message_text = message_text.split(' ')
            # process each word in the message text
            for word in array_of_message_text:
                outlist.append(cls.__action_step(cls.__pr.preprocess_text(word), message_text))
            # remove duplicate elements from the list
            outlist = list(set(outlist))
            # log successful completion of the method
            logging.info('The commandanalyzer.__action process has completed successfully')
            # return the processed list
            return outlist
        except Exception as e:
            # log the exception if an error occurs
            logging.exception('The exception occurred in commandanalyzer.__action: ' + str(e))

    @classmethod
    def analyse(cls, message_text):
        # analise commands
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outstr = ''
            # check if the message contains periods (.) to determine sentence splitting
            if (message_text.count('.') > 0):
                word_arr = message_text.split('. ')
            else:
                word_arr = message_text.split(', ')
            # process each word or phrase in the array
            for word in word_arr:
                outlist = cls.__action(word)
                if (outlist != None):
                    for outmes in outlist:
                        outstr += str(outmes) + '\n'
            # log successful completion of the analysis process
            logging.info('The commandanalyzer.analyse process has completed successfully')
            # check if the output string is empty or contains only "none"
            if outstr == '\n\n' or outstr == '' or outstr == '\n' or outstr == '\nNone\n' or outstr == 'none':
                return cls._gpta.answer(message_text)
            return outstr.capitalize()
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in commandanalyzer.analyse: ' + str(e))
