from Core_layer import Command_package as cp


class IAction(cp.ABC):

    @cp.abstractmethod
    def fas(cls):
        pass
    @cp.abstractmethod
    def calculate(cls):
        pass
    @cp.abstractmethod
    def find(cls):
        pass
    @cp.abstractmethod
    def translate(cls):
        pass
    @cp.abstractmethod
    def show(cls):
        pass

class CommandActionTelegram(IAction):

    boto = None
    message = None
    Inputstr = None

    __pred = cp.TextPreprocessers.Preprocessing()
    __pr = cp.TextPreprocessers.CommonPreprocessing()


    def __init__(self, boto, message, Inputstr):
        CommandActionTelegram.Inputstr = Inputstr
        CommandActionTelegram.boto = boto
        CommandActionTelegram.message = message

    @classmethod
    def fas(cls):
        Inputstr = cls.__pred.preprocess_text(cls.Inputstr)
        Inputstr = Inputstr.replace('атакуй ', '').replace('пиздани ', '').replace('фас ', '')
        Inputarr = Inputstr.split(' ')
        cls.command_flag = 1
        Inputstr = Inputstr.replace(Inputarr[0] + ' ', '')
        return Inputstr + ' - пидор.'

    @classmethod
    def calculate(cls, Inputstr):
        Inputarr = Inputstr.split(' ')
        c = cp.Calculators.SympyCalculator()
        if cls.__pr.preprocess_text(Inputarr[0]) == 'производная':
            output = c.deravative(Inputarr[1], Inputarr[2])
            return output
        elif cls.__pr.preprocess_text(Inputarr[0]) == 'интеграл':
           output = c.integrate(Inputarr[1], Inputarr[2])
           return output
        Inputstr = cls.Inputstr.replace(Inputarr[1].rstrip(), '')
        Inputstr = Inputstr.replace(Inputarr[2], '').replace(Inputarr[0], '')
        Inputstr = Inputstr.strip(' ')
        cls.command_flag = 1
        return Inputstr

    @classmethod
    def find(cls):
        Inputstr = cls.Inputstr.strip(' ').replace('найди ', '').replace('поссчитай ', '')
        tmp = cls.__pr.preprocess_text(Inputstr)
        if (tmp.count('производная') > 0) or (tmp.count('интеграл') > 0):
            Inputstr = cls.calculate(Inputstr)
            cls.command_flag = 1
            return Inputstr
        else:
            apif = cp.Finders.WikiFinder()
            finded_list = apif.find(tmp)
            try:
                return str(finded_list)
            except:
                return "Не нашла"

    @classmethod
    def translate(cls):
        tmp = cls.Inputstr.count('переведи данные')
        Inputstr = cls.Inputstr.strip(' ').replace('переведи ', '')
        tr = cp.Translators.GoogleTranslator("ru")
        if (tmp > 0):
            Inputstr = Inputstr.split(' ')
            dataselect = 'SELECT * FROM ' + Inputstr[1]
            insertdtname = 'translated'
            return cp.Translators.GoogleTranslator.translate(dataselect, insertdtname)
        else:
            translated = tr.translate(Inputstr)
            return translated
        cls.command_flag = 1

class CommandActionDiscord(IAction):

    def __init__(self, boto, message, Inputstr):
        CommandActionDiscord.Inputstr = Inputstr
        CommandActionDiscord.boto = boto
        CommandActionDiscord.message = message
    @classmethod
    def fas(cls):
        pass
    @classmethod
    def calculate(cls):
        pass
    @classmethod
    def find(cls):
        pass
    @classmethod
    def translate(cls):
        pass
    @classmethod
    def show(cls):
        pass
