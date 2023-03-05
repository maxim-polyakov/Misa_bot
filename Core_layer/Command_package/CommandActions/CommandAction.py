from Deep_layer.NLP_package.TextPreprocessers import CommonPreprocessing, Preprocessing
from Deep_layer.API_package.Calculators import SympyCalculator
from Deep_layer.API_package.Finders import WikiFinder
from Deep_layer.API_package.Translators import GoogleTranslator
from Deep_layer.NLP_package.DataShowers import SnsShower
from Core_layer.Command_package.CommandActions import IAction
from Deep_layer.DB_package.DB_Bridge import DB_Communication

class CommandAction(IAction.IAction):

    boto = None
    message = None
    message_text = None
    
    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, boto, message, message_text):
        CommandAction.message_text = message_text
        CommandAction.boto = boto
        CommandAction.message = message

    @classmethod
    def fas(cls):
        Inputstr = cls.__pred.preprocess_text(cls.message_text)
        Inputstr = Inputstr.replace('атакуй ', '').replace('пиздани ', '').replace('фас ', '')
        Inputarr = Inputstr.split(' ')
        cls.command_flag = 1
        Inputstr = Inputstr.replace(Inputarr[0] + ' ', '')
        return Inputstr + ' - пидор.'

    @classmethod
    def __calculate(cls, message_text):
        Inputarr = message_text.split(' ')
        c = SympyCalculator.SympyCalculator()
        if cls.__pr.preprocess_text(Inputarr[0]) == 'производная':
            output = c.deravative(Inputarr[1], Inputarr[2])
            return output
        elif cls.__pr.preprocess_text(Inputarr[0]) == 'интеграл':
           output = c.integrate(Inputarr[1], Inputarr[2])
           return output

        message_text = cls.message_text.replace(Inputarr[1].rstrip(), '')
        message_text = message_text.replace(Inputarr[2], '').replace(Inputarr[0], '')
        message_text = message_text.strip(' ')
        cls.command_flag = 1
        return message_text

    @classmethod
    def find(cls):
        message_text = cls.message_text.strip(' ').replace('находить ', '').replace('поссчитать ', '')
        if (message_text.count('производная') > 0) or (message_text.count('интеграл') > 0):
            message_text = cls.__calculate(message_text)
            cls.command_flag = 1
            return message_text
        else:
            apif = WikiFinder.WikiFinder()
            finded_list = apif.find(message_text)
            try:
                return str(finded_list)
            except:
                return "Не нашла"

    @classmethod
    def translate(cls):
        message_text = cls.message_text.strip(' ').replace('перевести ', '')
        tr = GoogleTranslator.GoogleTranslator("ru")
        translated = tr.translate(message_text)
        return translated

    @classmethod
    def show(cls):
        dbc = DB_Communication.DB_Communication()
        message_text = cls.message_text.split(' ')
        target = str(message_text[2])
        ALL_SELECT = str('SELECT text, ' + str(target) + ' FROM train_sets.all_set_none ' +
                         'UNION ALL select text, ' + str(target) + ' FROM train_sets.all_set_thanks ' +
                         'UNION ALL select text, ' + str(target) + ' FROM train_sets.all_set_hi ' +
                         'UNION ALL select text, ' + str(target) + ' FROM train_sets.all_set_business ' +
                         'UNION ALL select text, ' + str(target) + ' FROM train_sets.all_set_trash ')
        train = dbc.get_data(ALL_SELECT)
        shower = SnsShower.SnsShower()
        outpath = shower.showdata(train, target)
        return outpath
