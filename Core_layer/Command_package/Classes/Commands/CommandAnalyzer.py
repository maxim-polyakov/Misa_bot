from Deep_layer.NLP_package.TextPreprocessers import Preprocessing, CommonPreprocessing, CommandPreprocessing
from Core_layer.Command_package.Classes.CommandActions import CommandAction
from Core_layer.Command_package.Interfaces import IAnalyzer


class CommandAnalyzer(IAnalyzer.IAnalyzer):

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()
    __cpr = CommandPreprocessing.CommandPreprocessing()
    __nothingflg = 0
    __cash = ''
    __mesentype = 'telegram'

    def __init__(self, boto, message, mesentype):
        self.boto = boto
        self.message = message
        self.__mesentype = mesentype

    def __action_step(self, chosen_item, message_text):
        ac = CommandAction.CommandAction(self.boto, self.message, message_text)
        try:
            info_dict = {
                'атаковать': ac.fas,
                'фас': ac.fas,
                'поссчитать': ac.find,
                'перевести': ac.translate,
                'находить': ac.find,
                'показывать данные': ac.show
            }
            return info_dict[chosen_item]
        except:
            return ''

    def __action(self, message_text):
        outlist = []
        array_of_message_text = message_text.split(' ')
        for word in array_of_message_text:
            outlist.append((self.__action_step(self.__pr.preprocess_text(word), self.__pr.preprocess_text(message_text))))
        outlist = list(set(outlist))
        return outlist

    def analyse(self, message_text):
        outstr = ''

        if (message_text.count('.') > 0):
            word_arr = message_text.split('. ')
        else:
            word_arr = message_text.split(', ')

        for word in word_arr:
            outlist = self.__action(word)
            if (outlist != None):
                for outmes in outlist:
                    outstr += outmes
        return outstr










