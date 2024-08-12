from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing, CommonPreprocessing, CommandPreprocessing
from Core_layer.Command_package.Classes.CommandActions import CommandAction
from Core_layer.Command_package.Interfaces import IAnalyzer


class CommandAnalyzer(IAnalyzer.IAnalyzer):

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()
    __cpr = CommandPreprocessing.CommandPreprocessing()
    __nothingflg = 0
    __cash = ''

    def __init__(self, message, mesentype):
        CommandAnalyzer.__message = message
        CommandAnalyzer.__mesentype = mesentype

    @classmethod
    def __action_step(cls, chosen_item, message_text):
        ac = CommandAction.CommandAction(cls.__message, message_text)

        try:
            info_dict = {
                'погода': str(ac.weather()),
                'атаковать': str(ac.fas()),
                'фас': str(ac.fas()),
                'перевести': str(ac.translate()),
                'поссчитать': str(ac.find()),
                'находить': str(ac.find())
                }
            return info_dict[chosen_item]
        except:
            return ''

    @classmethod
    def __action(cls, message_text):
        outlist = []
        array_of_message_text = message_text.split(' ')
        for word in array_of_message_text:
            outlist.append(cls.__action_step(cls.__pr.preprocess_text(word), cls.__pr.preprocess_text(message_text)))
        outlist = list(set(outlist))
        return outlist

    @classmethod
    def analyse(cls, message_text):
        outstr = ''

        if (message_text.count('.') > 0):
            word_arr = message_text.split('. ')
        else:
            word_arr = message_text.split(', ')

        for word in word_arr:
            outlist = cls.__action(word)
            if (outlist != None):
                for outmes in outlist:
                    outstr += outmes
        return outstr