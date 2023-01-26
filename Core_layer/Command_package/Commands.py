from Deep_layer.NLP_package import TextPreprocessers
from Deep_layer.DB_package import DB_Bridge
from Core_layer.Command_package.CommandActions import CommandAction


class CommandAnalyzer:

    command_flag = 0
    __pred = TextPreprocessers.Preprocessing()
    __pr = TextPreprocessers.CommonPreprocessing()
    __cpr = TextPreprocessers.CommandPreprocessing()
    __nothingflg = 0
    __cash = ''
    __mesentype = 'telegram'

    def __init__(self, boto, message, mesentype):
        self.boto = boto
        self.message = message
        self.__mesentype = mesentype

    def __action_step(self, chosen_item, message_text):
        ac = CommandAction(self.boto, self.message, message_text)

        try:
            info_dict = {
                'атаковать': ac.fas,
                'фас': ac.fas,
                'пиздануть': ac.fas,
                'поссчитать': ac.find,
                'перевести': ac.translate,
                'находить': ac.find
            }
            return info_dict[chosen_item]()
        except:
            return ''

    def __action(self, message_text):
        outlist =[]

        array_of_message_text = message_text.split(' ')

        for word in array_of_message_text:
            outlist.append((self.__action_step(self.__pr.preprocess_text(word), self.__pr.preprocess_text(message_text))))
        outlist = list(set(outlist))
        return outlist

    def commandanalyse(self, message_text):
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










