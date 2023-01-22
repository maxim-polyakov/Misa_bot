from Deep_layer.NLP_package import TextPreprocessers
from Deep_layer.DB_package import DB_Bridge

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

    def __checkcash(self, ac, PreprocessedInsidestringarr, Insidestringarr, idx):
        if (self.__nothingflg == 0):
            if (DB_Bridge.DB_Communication.checkcommands(Insidestringarr[idx])):
                if(self.__mesentype == 'telegram'):
                    return 'Команда'
                else:
                    return 'Команда'
            else:
                if (self.__cash == 'находить'):
                    return ac.find(PreprocessedInsidestringarr)
                elif (self.__cash == 'атаковать'):
                    return ac.fas(PreprocessedInsidestringarr)
                elif (self.__cash == 'перевести'):
                    return ac.translate(PreprocessedInsidestringarr)

    def commandanalyse(self, Inputstr):

        if(Inputstr.count('.')>0):
            Insidestringarr = Inputstr.split('. ')
        else:
            Insidestringarr = Inputstr.split(', ')

        for idx in range(0,len(Insidestringarr)):
            PreprocessedInputStr = self.__pr.preprocess_text(Insidestringarr[idx])
            PreprocessedInsidestringarr = self.__pred.preprocess_text(Insidestringarr[idx])

            if (self.__mesentype == 'telegram'):
                ac = Second_layer.Command_package.CommandActions.CommandActionTelegram(self.boto, self.message, PreprocessedInsidestringarr)
            else:
                ac = Second_layer.Command_package.CommandActions.CommandActionDiscord(self.boto, self.message, PreprocessedInsidestringarr)

            if (PreprocessedInputStr.count('атаковать') > 0 or
                    PreprocessedInputStr.count('фас') > 0 or
                    PreprocessedInputStr.count('пиздануть') > 0):
                fas = ac.fas()
                return fas
                self.__cash = 'атаковать'
                self.__nothingflg = 1

            if (PreprocessedInputStr.count('находить') > 0) or (PreprocessedInputStr.count('поссчитать') > 0):
                return str(ac.find())
                self.__cash = 'находить'
                self.__nothingflg = 2

            if (PreprocessedInputStr.count('перевести') > 0):
                return ac.translate()
                self.__cash = 'перевести'
                self.__nothingflg = 3

            self.__checkcash(ac, PreprocessedInsidestringarr, Insidestringarr, idx)






