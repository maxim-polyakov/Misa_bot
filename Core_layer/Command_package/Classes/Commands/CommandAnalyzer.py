import logging
from Core_layer.Command_package.Interfaces import IAnalyzer
from Core_layer.Command_package.Classes.CommandActions import CommandAction
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionF
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionS
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionF
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionS
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing, CommonPreprocessing, CommandPreprocessing


class CommandAnalyzer(IAnalyzer.IAnalyzer):
    """
    It is command analyzer
    """
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
#
#
        try:
            fc = AActionF.AActionF(cls.__message, message_text)
            fcs = AActionS.AActionS(cls.__message, message_text)
            sc = BActionF.BActionF(cls.__message, message_text)
            scs = BActionS.BActionS(cls.__message, message_text)
            ac = CommandAction.CommandAction(cls.__message, message_text)
            info_dict = {
                'абонировать': str(fc.first()),
                'абонироваться': str(fc.second()),
                'абсолютизировать': str(fc.third()),
                'абсолютизироваться': str(fc.fourth()),
                'абсолютировать': str(fc.fifth()),
                'абсорбировать': str(fc.sixth()),
                'абсорбироваться': str(fc.seventh()),
                'абстрагировать': str(fc.eighth()),
                'абстрагироваться': str(fc.nineth()),
                'авансировать': str(fc.tenth()),
                'авансироваться': str(fc.eleventh()),
                'авизировать': str(fc.twelth()),
                'авизироваться': str(fc.thirteenth()),
                'автоматизировать': str(fc.fourteenth()),
                'автоматизироваться': str(fc.fifteenth()),
                'авторизовать': str(fc.sixteenth()),
                'авторизоваться': str(fc.seventeenth()),
                'агглютинировать': str(fc.eithneenth()),
                'агглютинироваться': str(fc.nineteenth()),
                'агитировать': str(fc.twenttyth()),
                'агломерировать': str(fc.twentyfirst()),
                'агломерироваться': str(fc.twentysecond()),
                'агонизировать': str(fc.twentythird()),
                'агрегатировать': str(fc.twentyfourth()),
                'агрегатироваться': str(fc.twentyfifth()),
                'агрегировать': str(fc.twentysixth()),
                'агрегироваться': str(fc.twentyseventh()),
                'агукать': str(fc.twentyeighth()),
                'агукнуть': str(fc.twentynineth()),
                'адаптировать': str(fc.thirtyth()),
                'адаптироваться': str(fc.thirtyfirst()),
                'адвербиализироваться': str(fc.thirtysecond()),
                'адвокатствовать': str(fc.thirtythird()),
                'администрировать': str(fc.thirtyfourth()),
                'адоптировать': str(fc.thirtyfifth()),
                'адоптироваться': str(fc.thirtysixth()),
                'адресовать': str(fc.thirtyseventh()),
                'адресоваться': str(fc.thirtyeighth()),
                'адсорбировать': str(fc.thirynineth()),
                'адсорбироваться': str(fc.fourtyth()),
                'адъективироваться': str(fc.fourtyfirst()),
                'ажитировать': str(fc.fourtysecond()),
                'ажитироваться': str(fc.fourythird()),
                'азартничать': str(fc.fourtyfourth()),
                'азотировать': str(fc.fourtyfifth()),
                'азотироваться': str(fc.fourtysixth()),
                'айкай': str(fc.fourtyseventh()),
                'айкать': str(fc.fourtyeight()),
                'айкнуть': str(fc.fourtynineth()),
                'акать': str(fc.fiftyth()),
                'акклиматизировать': str(fc.fiftyfirst()),
                'акклиматизироваться': str(fc.fiftysecond()),
                'аккомодировать': str(fc.fiftythird()),
                'аккомодироваться': str(fc.fiftyfourth()),
                'аккомпанировать': str(fc.fiftyfifth()),
                'аккредитовать': str(fc.fiftysixth()),
                'аккредитоваться': str(fc.fiftyseventh()),
                'аккумулировать': str(fc.fiftyeight()),
                'аккумулироваться': str(fc.fiftynineth()),
                'акробатничать': str(fc.sixtyth()),
                'акробатствовать': str(fc.sixtyfirst()),
                'акселерироваться': str(fc.sixtysecond()),
                'актерствовать': str(fc.sixtythird()),
                'активизировать': str(fc.sixtyfourth()),
                'активизироваться': str(fc.sixtyfifth()),
                'активировать': str(fc.sixtysixth()),
                'активироваться': str(fc.sixsyseventh()),
                'активничать': str(fc.sixtyeighthth()),
                'актировать': str(fc.sixtynineth()),
                'актироваться': str(fc.seventyth()),
                'актуализировать': str(fc.seventyfirst()),
                'актуализироваться': str(fc.seventysecond()),
                'акушерствовать': str(fc.seventythird()),
                'акцентировать': str(fc.seventyfourth()),
                'акцентироваться': str(fc.seventyfifth()),
                'акцептовать': str(fc.seventysixth()),
                'алгоритмизировать': str(fc.seventyseventh()),
                'алгоритмизироваться': str(fc.seventyeigth()),
                'аля': str(fc.seventynineth()),
                'алеть': str(fc.eightyth()),
                'алеться': str(fc.eightyfirst()),
                'алкать': str(fc.eightysecond()),
                'алтынничать': str(fc.eightythird()),
                'амальгамировать': str(fc.eightyfourth()),
                'амальгамироваться': str(fc.eightyfifth()),
                'американизировать': str(fc.eightysixth()),
                'американизироваться': str(fc.eightyseventh()),
                'амикошонствовать': str(fc.eightyeighth()),
                'амнистировать': str(fc.eightynineth()),
                'амнистироваться': str(fc.ninetyth()),
                'амортизировать': str(fc.ninetyfirst()),
                'амортизироваться': str(fc.ninetysecond()),
                'ампутировать': str(fc.ninetythird()),
                'ампутироваться': str(fc.ninetyfourth()),
                'амуриться': str(fc.ninetyfifth()),
                'амурничать': str(fc.ninetysixth()),
                'анализировать': str(fc.ninetyseventh()),
                'анализироваться': str(fc.ninetyeighth()),
                'анатомировать': str(fc.ninetynineth()),
                'ангажировать': str(fc.hundredth()),
                'англизироваться': str(fcs.first()),
                'анестезировать': str(fcs.second()),
                'анкетировать': str(fcs.third()),
                'аннексировать': str(fcs.fourth()),
                'аннексироваться': str(fcs.fifth()),
                'аннигилироваться': str(fcs.sixth()),
                'аннотировать': str(fcs.seventh()),
                'аннотироваться': str(fcs.eighth()),
                'аннулировать': str(fcs.nineth()),
                'аннулироваться': str(fcs.tenth()),
                'анодировать': str(fcs.eleventh()),
                'анодироваться': str(fcs.twelth()),
                'анонсировать': str(fcs.thirteenth()),
                'анонсироваться': str(fcs.fourteenth()),
                'антидатировать': str(fcs.fifteenth()),
                'антидатироваться': str(fcs.sixteenth()),
                'антрепренерствовать': str(fcs.seventeenth()),
                'апеллировать': str(fcs.eithneenth()),
                'аплодировать': str(fcs.nineteenth()),
                'аппретировать': str(fcs.twenttyth()),
                'аппретироваться': str(fcs.twentyfirst()),
                'апробировать': str(fcs.twentysecond()),
                'апробироваться': str(fcs.twentysecond()),
                'аранжировать': str(fcs.twentythird()),
                'аранжироваться': str(fcs.twentyfourth()),
                'аргументировать': str(fcs.twentyfifth()),
                'аргументироваться': str(fcs.twentysixth()),
                'арендовать': str(fcs.twentyseventh()),
                'арендоваться': str(fcs.twentyeighth()),
                'арестовывать': str(fcs.twentynineth()),
                'арестовываться': str(fcs.thirtyth()),
                'аристократничать': str(fcs.thirtyfirst()),
                'арканить': str(fcs.thirtysecond()),
                'аркебузировать': str(fcs.thirtythird()),
                'армировать': str(fcs.thirtyfourth()),
                'армироваться': str(fcs.thirtyfifth()),
                'ароматизировать': str(fcs.thirtysixth()),
                'ароматизироваться': str(fcs.thirtyseventh()),
                'артачиться': str(fcs.thirtyeighth()),
                'артикулировать': str(fcs.thirynineth()),
                'артикулироваться': str(fcs.fourtyth()),
                'архаизировать': str(fcs.fourtyfirst()),
                'архаизироваться': str(fcs.fourtysecond()),
                'аршинничать': str(fcs.fourythird()),
                'ассенизировать': str(fcs.fourtyfourth()),
                'ассигновать': str(fcs.fourtyfifth()),
                'ассигноваться': str(fcs.fourtysixth()),
                'ассигновывать': str(fcs.fourtyseventh()),
                'ассигновываться': str(fcs.fourtyeight()),
                'ассимилировать': str(fcs.fourtynineth()),
                'ассимилироваться': str(fcs.fiftyth()),
                'ассистировать': str(fcs.fiftyfirst()),
                'ассоциировать': str(fcs.fiftysecond()),
                'ассоциироваться': str(fcs.fiftythird()),
                'асфальтировать': str(fcs.fiftyfourth()),
                'асфальтироваться': str(fcs.fiftyfifth()),
                'атаковать': str(fcs.fiftysixth()),
                'атаковаться': str(fcs.fiftyseventh()),
                'атаковывать': str(fcs.fiftyeight()),
                'атаковываться': str(fcs.fiftynineth()),
                'атаманить': str(fcs.sixtyth()),
                'атаманствовать': str(fcs.sixtyfirst()),
                'атрофироваться': str(fcs.sixtysecond()),
                'аттестовать': str(fcs.sixtythird()),
                'аттестоваться': str(fcs.sixtyfourth()),
                'атукать': str(fcs.sixtyfifth()),
                'атукнуть': str(fcs.sixtysixth()),
                'аудитировать': str(fcs.sixsyseventh()),
                'аукать': str(fcs.sixtyeighthth()),
                'аукаться': str(fcs.sixtynineth()),
                'аукнуть': str(fcs.seventyth()),
                'аукнуться': str(fcs.seventyfirst()),
                'афишировать': str(fcs.seventysecond()),
                'афишироваться': str(fcs.seventythird()),
                'ахать': str(fcs.seventyfourth()),
                'ахнуть': str(fcs.seventyfifth()),
                'бабахать': str(sc.first()),
                'бабахаться': str(sc.second()),
                'бабахнуть': str(sc.third()),
                'бабахнуться': str(sc.fourth()),
                'бабиться': str(sc.fifth()),
                'бабничать': str(sc.sixth()),
                'багрить': str(sc.seventh()),
                'багряться': str(sc.eighth()),
                'багруй': str(sc.nineth()),
                'багруйте': str(sc.tenth()),
                'багруиться': str(sc.eleventh()),
                'багровый': str(sc.twelth()),
                'багроветь': str(sc.thirteenth()),
                'багряный': str(sc.fourteenth()),
                'багрянеть': str(sc.fifteenth()),
                'багрянуть': str(sc.sixteenth()),
                'багряниться': str(sc.seventeenth()),
                'базарить': str(sc.eithneenth()),
                'базарничать': str(sc.nineteenth()),
                'базировать': str(sc.twenttyth()),
                'базироваться': str(sc.twentyfirst()),
                'баклушничать': str(sc.twentysecond()),
                'балаболить': str(sc.twentythird()),
                'балабонить': str(sc.twentyfourth()),
                'балаганить': str(sc.twentyfifth()),
                'балаганничать': str(sc.twentysixth()),
                'балагурить': str(sc.twentyseventh()),
                'балакать': str(sc.twentyeighth()),
                'баламутить': str(sc.twentynineth()),
                'баламутиться': str(sc.thirtyth()),
                'балансировать': str(sc.thirtyfirst()),
                'балбесничать': str(sc.thirtysecond()),
                'балдеть': str(sc.thirtythird()),
                'балластировать': str(sc.thirtyfourth()),
                'баллотировать': str(sc.thirtyfifth()),
                'баллотироваться': str(sc.thirtysixth()),
                'баловать': str(sc.thirtyseventh()),
                'баловаться': str(sc.thirtyeighth()),
                'бальзамировать': str(sc.thirynineth()),
                'бальзамироваться': str(sc.fourtyth()),
                'балясничать': str(sc.fourtyfirst()),
                'баня': str(sc.fourtysecond()),
                'банить': str(sc.fourythird()),
                'баниться': str(sc.fourtyfourth()),
                'банковать': str(sc.fourtyfifth()),
                'банкротиться': str(sc.fourtysixth()),
                'барабанить': str(sc.fourtyseventh()),
                'барахлить': str(sc.fourtyeight()),
                'барахтаться': str(sc.fourtynineth()),
                'барражировать': str(sc.fiftyth()),
                'баррикадировать': str(sc.fiftyfirst()),
                'баррикадироваться': str(sc.fiftysecond()),
                'барствовать': str(sc.fiftythird()),
                'бархатись': str(sc.fiftyfourth()),
                'бархатитесь': str(sc.fiftyfifth()),
                'барышничать': str(sc.fiftysixth()),
                'басить': str(sc.fiftyseventh()),
                'бастовать': str(sc.fiftyeight()),
                'батрачить': str(sc.fiftynineth()),
                'бахать': str(sc.sixtyth()),
                'бахаться': str(sc.sixtyfirst()),
                'бахвалиться': str(sc.sixtysecond()),
                'бахнуть': str(sc.sixtythird()),
                'бахнуться': str(sc.sixtyfourth()),
                'бацать': str(sc.sixtyfifth()),
                'бацаться': str(sc.sixtysixth()),
                'бацнуть': str(sc.sixsyseventh()),
                'бацнуться': str(sc.sixtyeighthth()),
                'башливать': str(sc.sixtynineth()),
                'баюкать': str(sc.seventyth()),
                'бай': str(sc.seventyfirst()),
                'байт': str(sc.seventysecond()),
                'бдеть': str(sc.seventythird()),
                'бегать': str(sc.seventyfourth()),
                'бедный': str(sc.seventyfifth()),
                'беднеть': str(sc.seventysixth()),
                'бедовать': str(sc.seventyseventh()),
                'бедокурить': str(sc.seventyeigth()),
                'бедствовать': str(sc.seventynineth()),
                'бежать': str(sc.eightyth()),
                'безбожничать': str(sc.eightyfirst()),
                'бездействовать': str(sc.eightysecond()),
                'бездельничать': str(sc.eightythird()),
                'бездомничать': str(sc.eightyfourth()),
                'беззаконничать': str(sc.eightyfifth()),
                'безлюдеть': str(sc.eightysixth()),
                'безмолвствовать': str(sc.eightyseventh()),
                'безобразить': str(sc.eightyeighth()),
                'безобразничать': str(sc.ninetyth()),
                'безуметь': str(sc.ninetyfirst()),
                'безумствовать': str(sc.ninetysecond()),
                'белый': str(sc.ninetythird()),
                'белеть': str(sc.ninetyfourth()),
                'белеться': str(sc.ninetyfifth()),
                'бель': str(sc.ninetysixth()),
                'белить': str(sc.ninetyseventh()),
                'белиться': str(sc.ninetyeighth()),
                'белковать': str(sc.ninetynineth()),
                'беллетризировать': str(sc.hundredth()),
                #
                'фас': str(ac.fas()),
                'перевести': str(ac.translate()),
                'поссчитать': str(ac.find()),
                'находить': str(ac.find()),
                'сказать': str(ac.say()),
                'погода': str(ac.weather()),
                'поздороваться': str(ac.sayhi()),
                'почистить': str(ac.clean()),
                'очистить': str(ac.clean())
                }
            return info_dict[chosen_item]
        except Exception as e:
            return ''

    @classmethod
    def __action(cls, message_text):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outlist = []
            array_of_message_text = message_text.split(' ')
            for word in array_of_message_text:
                outlist.append(cls.__action_step(cls.__pr.preprocess_text(word), message_text))
            outlist = list(set(outlist))
            logging.info('The commandanalyzer.__action is done')
            return outlist
        except Exception as e:
            logging.exception(str('The exception in commandanalyzer.__action ' + str(e)))

    @classmethod
    def analyse(cls, message_text):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outstr = ''

            if (message_text.count('.') > 0):
                word_arr = message_text.split('. ')
            else:
                word_arr = message_text.split(', ')
            for word in word_arr:
                outlist = cls.__action(word)
                if (outlist != None):
                    for outmes in outlist:
                        outstr += outmes + '\n'
            logging.info('The commandanalyzer.analyse is done')
            return outstr
        except Exception as e:
            logging.exception(str('The exception in commandanalyzer.analyse ' + str(e)))