import logging
from Core_layer.Command_package.Interfaces import IAnalyzer
from Core_layer.Command_package.Classes.CommandActions import CommandAction
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionOne
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionTwo
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionThree
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionFour
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionFive
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionSix
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionSeven
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionEight
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionNine
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionTen
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionEleven
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionTwelve
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionThirteen
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionFourteen
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionFifteen
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionSixteen
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionSeventeen
from Core_layer.Command_package.Classes.CommandActions.AActions import AActionEighteen
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionOne
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionTwo
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionThree
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionFour
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionFive
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionSix
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionSeven
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionEight
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionNine
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionTen
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionEleven
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionTwelve
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionThirteen
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionFourteen
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionFifteen
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionSixteen
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionSeventeen
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionEighteen
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionNineteen
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionTwenty
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionTwentyOne
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionTwentyTwo
from Core_layer.Command_package.Classes.CommandActions.BActions import BActionTwentyThree
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
    __message = None
    __mesentype = None

    def __init__(self, message, mesentype):
        CommandAnalyzer.__message = message
        CommandAnalyzer.__mesentype = mesentype

    @classmethod
    def __action_step(cls, chosen_item, message_text):
#
#
        try:
            aone = AActionOne.AActionOne(cls.__message, message_text)
            atwo = AActionTwo.AActionTwo(cls.__message, message_text)
            athree = AActionThree.AActionThree(cls.__message, message_text)
            afour = AActionFour.AActionFour(cls.__message, message_text)
            afive = AActionFive.AActionFive(cls.__message, message_text)
            asix = AActionSix.AActionSix(cls.__message, message_text)
            aseven = AActionSeven.AActionSeven(cls.__message, message_text)
            aeight = AActionEight.AActionEight(cls.__message, message_text)
            anine = AActionNine.AActionNine(cls.__message, message_text)
            aten = AActionTen.AActionTen(cls.__message, message_text)
            aeleven = AActionEleven.AActionEleven(cls.__message, message_text)
            atwelve = AActionTwelve.AActionTwelve(cls.__message, message_text)
            athirteen = AActionThirteen.AActionThirteen(cls.__message, message_text)
            afourteen = AActionFourteen.AActionFourteen(cls.__message, message_text)
            afifteen = AActionFifteen.AActionFifteen(cls.__message, message_text)
            asixteen = AActionSixteen.AActionSixteen(cls.__message, message_text)
            aseventeen = AActionSeventeen.AActionSeventeen(cls.__message, message_text)
            aeighteen = AActionEighteen.AActionEighteen(cls.__message, message_text)

            bone = BActionOne.BActionOne(cls.__message, message_text)
            btwo = BActionTwo.BActionTwo(cls.__message, message_text)
            bthree = BActionThree.BActionThree(cls.__message, message_text)
            bfour = BActionFour.BActionFour(cls.__message, message_text)
            bfive = BActionFive.BActionFive(cls.__message, message_text)
            bsix = BActionSix.BActionSix(cls.__message, message_text)
            bseven = BActionSeven.BActionSeven(cls.__message, message_text)
            beight = BActionEight.BActionEight(cls.__message, message_text)
            bnine = BActionNine.BActionNine(cls.__message, message_text)
            bten = BActionTen.BActionTen(cls.__message, message_text)
            beleven = BActionEleven.BActionEleven(cls.__message, message_text)
            btwelve = BActionTwelve.BActionTwelve(cls.__message, message_text)
            bthirteen = BActionThirteen.BActionThirteen(cls.__message, message_text)
            bfourteen = BActionFourteen.BActionFourteen(cls.__message, message_text)
            bfifteen = BActionFifteen.BActionFifteen(cls.__message, message_text)
            bsixteen = BActionSixteen.BActionSixteen(cls.__message, message_text)
            bseventeen = BActionSeventeen.BActionSeventeen(cls.__message, message_text)
            beighteen = BActionEighteen.BActionEighteen(cls.__message, message_text)
            bnineteen = BActionNineteen.BActionNineteen(cls.__message, message_text)
            btwenty = BActionTwenty.BActionTwenty(cls.__message, message_text)
            btwentyone = BActionTwentyOne.BActionTwentyOne(cls.__message, message_text)
            btwentytwo = BActionTwentyTwo.BActionTwentyTwo(cls.__message, message_text)
            btwentythree = BActionTwentyThree.BActionTwentyThree(cls.__message, message_text)

            ac = CommandAction.CommandAction(cls.__message, message_text)
            info_dict = {
                'абонировать': str(aone.first()),
                'абонироваться': str(aone.second()),
                'абсолютизировать': str(aone.third()),
                'абсолютизироваться': str(aone.fourth()),
                'абсолютировать': str(aone.fifth()),
                'абсорбировать': str(aone.sixth()),
                'абсорбироваться': str(aone.seventh()),
                'абстрагировать': str(aone.eighth()),
                'абстрагироваться': str(aone.nineth()),
                'авансировать': str(aone.tenth()),
                'авансироваться': str(atwo.first()),
                'авизировать': str(atwo.second()),
                'авизироваться': str(atwo.third()),
                'автоматизировать': str(atwo.fourth()),
                'автоматизироваться': str(atwo.fifth()),
                'авторизовать': str(atwo.sixth()),
                'авторизоваться': str(atwo.seventh()),
                'агглютинировать': str(atwo.eighth()),
                'агглютинироваться': str(atwo.nineth()),
                'агитировать': str(atwo.tenth()),
                'агломерировать': str(athree.first()),
                'агломерироваться': str(athree.second()),
                'агонизировать': str(athree.third()),
                'агрегатировать': str(athree.fourth()),
                'агрегатироваться': str(athree.fifth()),
                'агрегировать': str(athree.sixth()),
                'агрегироваться': str(athree.seventh()),
                'агукать': str(athree.eighth()),
                'агукнуть': str(athree.nineth()),
                'адаптировать': str(athree.tenth()),
                'адаптироваться': str(afour.first()),
                'адвербиализироваться': str(afour.second()),
                'адвокатствовать': str(afour.third()),
                'администрировать': str(afour.fourth()),
                'адоптировать': str(afour.fifth()),
                'адоптироваться': str(afour.sixth()),
                'адресовать': str(afour.seventh()),
                'адресоваться': str(afour.eighth()),
                'адсорбировать': str(afour.nineth()),
                'адсорбироваться': str(afour.tenth()),
                'адъективироваться': str(afive.first()),
                'ажитировать': str(afive.second()),
                'ажитироваться': str(afive.third()),
                'азартничать': str(afive.fourth()),
                'азотировать': str(afive.fifth()),
                'азотироваться': str(afive.sixth()),
                'айкай': str(afive.seventh()),
                'айкать': str(afive.eighth()),
                'айкнуть': str(afive.nineth()),
                'акать': str(afive.tenth()),
                'акклиматизировать': str(asix.first()),
                'акклиматизироваться': str(asix.second()),
                'аккомодировать': str(asix.third()),
                'аккомодироваться': str(asix.fourth()),
                'аккомпанировать': str(asix.fifth()),
                'аккредитовать': str(asix.sixth()),
                'аккредитоваться': str(asix.seventh()),
                'аккумулировать': str(asix.eighth()),
                'аккумулироваться': str(asix.nineth()),
                'акробатничать': str(asix.tenth()),
                'акробатствовать': str(aseven.first()),
                'акселерироваться': str(aseven.second()),
                'актерствовать': str(aseven.third()),
                'активизировать': str(aseven.fourth()),
                'активизироваться': str(aseven.fifth()),
                'активировать': str(aseven.sixth()),
                'активироваться': str(aseven.seventh()),
                'активничать': str(aseven.eighth()),
                'актировать': str(aseven.nineth()),
                'актироваться': str(aseven.tenth()),
                'актуализировать': str(aeight.first()),
                'актуализироваться': str(aeight.second()),
                'акушерствовать': str(aeight.third()),
                'акцентировать': str(aeight.fourth()),
                'акцентироваться': str(aeight.fifth()),
                'акцептовать': str(aeight.sixth()),
                'алгоритмизировать': str(aeight.seventh()),
                'алгоритмизироваться': str(aeight.eighth()),
                'аля': str(aeight.nineth()),
                'алеть': str(aeight.tenth()),
                'алеться': str(anine.first()),
                'алкать': str(anine.second()),
                'алтынничать': str(anine.third()),
                'амальгамировать': str(anine.fourth()),
                'амальгамироваться': str(anine.fifth()),
                'американизировать': str(anine.sixth()),
                'американизироваться': str(anine.seventh()),
                'амикошонствовать': str(anine.eighth()),
                'амнистировать': str(anine.nineth()),
                'амнистироваться': str(anine.tenth()),
                'амортизировать': str(aten.first()),
                'амортизироваться': str(aten.second()),
                'ампутировать': str(aten.third()),
                'ампутироваться': str(aten.fourth()),
                'амуриться': str(aten.fifth()),
                'амурничать': str(aten.sixth()),
                'анализировать': str(aten.seventh()),
                'анализироваться': str(aten.eighth()),
                'анатомировать': str(aten.nineth()),
                'ангажировать': str(aten.tenth()),
                'англизироваться': str(aeleven.first()),
                'анестезировать': str(aeleven.second()),
                'анкетировать': str(aeleven.third()),
                'аннексировать': str(aeleven.fourth()),
                'аннексироваться': str(aeleven.fifth()),
                'аннигилироваться': str(aeleven.sixth()),
                'аннотировать': str(aeleven.seventh()),
                'аннотироваться': str(aeleven.eighth()),
                'аннулировать': str(aeleven.nineth()),
                'аннулироваться': str(aeleven.tenth()),
                'анодировать': str(atwelve.first()),
                'анодироваться': str(atwelve.second()),
                'анонсировать': str(atwelve.third()),
                'анонсироваться': str(atwelve.fourth()),
                'антидатировать': str(atwelve.fifth()),
                'антидатироваться': str(atwelve.sixth()),
                'антрепренерствовать': str(atwelve.seventh()),
                'апеллировать': str(atwelve.eighth()),
                'аплодировать': str(atwelve.nineth()),
                'аппретировать': str(atwelve.tenth()),
                'аппретироваться': str(athirteen.first()),
                'апробировать': str(athirteen.second()),
                'апробироваться': str(athirteen.third()),
                'аранжировать': str(athirteen.fourth()),
                'аранжироваться': str(athirteen.fifth()),
                'аргументировать': str(athirteen.sixth()),
                'аргументироваться': str(athirteen.seventh()),
                'арендовать': str(athirteen.eighth()),
                'арендоваться': str(athirteen.nineth()),
                'арестовывать': str(athirteen.tenth()),
                'арестовываться': str(afourteen.first()),
                'аристократничать': str(afourteen.second()),
                'арканить': str(afourteen.third()),
                'аркебузировать': str(afourteen.fourth()),
                'армировать': str(afourteen.fifth()),
                'армироваться': str(afourteen.sixth()),
                'ароматизировать': str(afourteen.seventh()),
                'ароматизироваться': str(afourteen.eighth()),
                'артачиться': str(afourteen.nineth()),
                'артикулировать': str(afourteen.tenth()),
                'артикулироваться': str(afifteen.first()),
                'архаизировать': str(afifteen.second()),
                'архаизироваться': str(afifteen.third()),
                'аршинничать': str(afifteen.fourth()),
                'ассенизировать': str(afifteen.fifth()),
                'ассигновать': str(afifteen.sixth()),
                'ассигноваться': str(afifteen.seventh()),
                'ассигновывать': str(afifteen.eighth()),
                'ассигновываться': str(afifteen.nineth()),
                'ассимилировать': str(afifteen.tenth()),
                'ассимилироваться': str(asixteen.first()),
                'ассистировать': str(asixteen.second()),
                'ассоциировать': str(asixteen.third()),
                'ассоциироваться': str(asixteen.fourth()),
                'асфальтировать': str(asixteen.fifth()),
                'асфальтироваться': str(asixteen.sixth()),
                'атаковать': str(asixteen.seventh()),
                'атаковаться': str(asixteen.eighth()),
                'атаковывать': str(asixteen.nineth()),
                'атаковываться': str(asixteen.tenth()),
                'атаманить': str(aseventeen.first()),
                'атаманствовать': str(aseventeen.second()),
                'атрофироваться': str(aseventeen.third()),
                'аттестовать': str(aseventeen.fourth()),
                'аттестоваться': str(aseventeen.fifth()),
                'атукать': str(aseventeen.sixth()),
                'атукнуть': str(aseventeen.seventh()),
                'аудитировать': str(aseventeen.eighth()),
                'аукать': str(aseventeen.nineth()),
                'аукаться': str(aseventeen.tenth()),
                'аукнуть': str(aeighteen.first()),
                'аукнуться': str(aeighteen.second()),
                'афишировать': str(aeighteen.third()),
                'афишироваться': str(aeighteen.fourth()),
                'ахать': str(aeighteen.fifth()),
                'ахнуть': str(aeighteen.sixth()),
                'бабахать': str(bone.first()),
                'бабахаться': str(bone.second()),
                'бабахнуть': str(bone.third()),
                'бабахнуться': str(bone.fourth()),
                'бабиться': str(bone.fifth()),
                'бабничать': str(bone.sixth()),
                'багрить': str(bone.seventh()),
                'багряться': str(bone.eighth()),
                'багруй': str(bone.nineth()),
                'багруйте': str(bone.tenth()),
                'багруиться': str(btwo.first()),
                'багровый': str(btwo.second()),
                'багроветь': str(btwo.third()),
                'багряный': str(btwo.fourth()),
                'багрянеть': str(btwo.fifth()),
                'багрянуть': str(btwo.sixth()),
                'багряниться': str(btwo.seventh()),
                'базарить': str(btwo.eighth()),
                'базарничать': str(btwo.nineth()),
                'базировать': str(btwo.tenth()),
                'базироваться': str(bthree.first()),
                'баклушничать': str(bthree.second()),
                'балаболить': str(bthree.third()),
                'балабонить': str(bthree.fourth()),
                'балаганить': str(bthree.fifth()),
                'балаганничать': str(bthree.sixth()),
                'балагурить': str(bthree.seventh()),
                'балакать': str(bthree.eighth()),
                'баламутить': str(bthree.nineth()),
                'баламутиться': str(bthree.tenth()),
                'балансировать': str(bfour.first()),
                'балбесничать': str(bfour.second()),
                'балдеть': str(bfour.third()),
                'балластировать': str(bfour.fourth()),
                'баллотировать': str(bfour.fifth()),
                'баллотироваться': str(bfour.sixth()),
                'баловать': str(bfour.seventh()),
                'баловаться': str(bfour.eighth()),
                'бальзамировать': str(bfour.nineth()),
                'бальзамироваться': str(bfour.tenth()),
                'балясничать': str(bfive.first()),
                'баня': str(bfive.second()),
                'банить': str(bfive.third()),
                'баниться': str(bfive.fourth()),
                'банковать': str(bfive.fifth()),
                'банкротиться': str(bfive.sixth()),
                'барабанить': str(bfive.seventh()),
                'барахлить': str(bfive.eighth()),
                'барахтаться': str(bfive.nineth()),
                'барражировать': str(bfive.tenth()),
                'баррикадировать': str(bsix.first()),
                'баррикадироваться': str(bsix.second()),
                'барствовать': str(bsix.third()),
                'бархатись': str(bsix.fourth()),
                'бархатитесь': str(bsix.fifth()),
                'барышничать': str(bsix.sixth()),
                'басить': str(bsix.seventh()),
                'бастовать': str(bsix.eighth()),
                'батрачить': str(bsix.nineth()),
                'бахать': str(bsix.tenth()),
                'бахаться': str(bseven.first()),
                'бахвалиться': str(bseven.second()),
                'бахнуть': str(bseven.third()),
                'бахнуться': str(bseven.fourth()),
                'бацать': str(bseven.fifth()),
                'бацаться': str(bseven.sixth()),
                'бацнуть': str(bseven.seventh()),
                'бацнуться': str(bseven.eighth()),
                'башливать': str(bseven.nineth()),
                'баюкать': str(bseven.tenth()),
                'бай': str(beight.first()),
                'байт': str(beight.second()),
                'бдеть': str(beight.third()),
                'бегать': str(beight.fourth()),
                'бедный': str(beight.fifth()),
                'беднеть': str(beight.sixth()),
                'бедовать': str(beight.seventh()),
                'бедокурить': str(beight.eighth()),
                'бедствовать': str(beight.nineth()),
                'бежать': str(beight.tenth()),
                'безбожничать': str(bnine.first()),
                'бездействовать': str(bnine.second()),
                'бездельничать': str(bnine.third()),
                'бездомничать': str(bnine.fourth()),
                'беззаконничать': str(bnine.fifth()),
                'безлюдеть': str(bnine.sixth()),
                'безмолвствовать': str(bnine.seventh()),
                'безобразить': str(bnine.eighth()),
                'безобразничать': str(bnine.tenth()),
                'безуметь': str(bten.first()),
                'безумствовать': str(bten.second()),
                'белый': str(bten.third()),
                'белеть': str(bten.fourth()),
                'белеться': str(bten.fifth()),
                'бель': str(bten.sixth()),
                'белить': str(bten.seventh()),
                'белиться': str(bten.eighth()),
                'белковать': str(bten.nineth()),
                'беллетризировать': str(bten.tenth()),
                'бередить': str(beleven.first()),
                'беременеть': str(beleven.second()),
                'беречь': str(beleven.third()),
                'беречься': str(beleven.fourth()),
                'беседовать': str(beleven.fifth()),
                'бесить': str(beleven.sixth()),
                'беситься': str(beleven.seventh()),
                'бесноваться': str(beleven.eighth()),
                'беспокоить': str(beleven.nineth()),
                'беспокоиться': str(beleven.tenth()),
                'беспризорничать': str(btwelve.first()),
                'беспутничать': str(btwelve.second()),
                'беспутствовать': str(btwelve.third()),
                'бессиливать': str(btwelve.fourth()),
                'бесславить': str(btwelve.fifth()),
                'бесстыдничать': str(btwelve.sixth()),
                'бесстыдствовать': str(btwelve.seventh()),
                'бесчестить': str(btwelve.eighth()),
                'бесчестись': str(btwelve.nineth()),
                'бесчеститесь': str(btwelve.tenth()),
                'бесчинничать': str(bthirteen.first()),
                'бесчинствовать': str(bthirteen.second()),
                'бетонировать': str(bthirteen.third()),
                'бетонироваться': str(bthirteen.fourth()),
                'бешенствовать': str(bthirteen.fifth()),
                'бибикать': str(bthirteen.sixth()),
                'библиографировать': str(bthirteen.seventh()),
                'бивать': str(bthirteen.eighth()),
                'бинтовать': str(bthirteen.nineth()),
                'бинтоваться': str(bthirteen.tenth()),
                'бисировать': str(bfourteen.first()),
                'бисироваться': str(bfourteen.second()),
                'бить': str(bfourteen.third()),
                'биться': str(bfourteen.fourth()),
                'бичевать': str(bfourteen.fifth()),
                'бичуяться': str(bfourteen.sixth()),
                'благовестить': str(bfourteen.seventh()),
                'благоволить': str(bfourteen.eighth()),
                'благоговеть': str(bfourteen.nineth()),
                'благодарить': str(bfourteen.tenth()),
                'благодарствовать': str(bfifteen.first()),
                'благоденствовать': str(bfifteen.second()),
                'благодетельствовать': str(bfifteen.third()),
                'благодушествовать': str(bfifteen.fourth()),
                'благожелательствовать': str(bfifteen.fifth()),
                'благоприобретать': str(bfifteen.sixth()),
                'благоприятствовать': str(bfifteen.seventh()),
                'благоразумничать': str(bfifteen.eighth()),
                'благородить': str(bfifteen.nineth()),
                'благословлять': str(bfifteen.tenth()),
                'благословляться': str(bsixteen.first()),
                'благотворительствовать': str(bsixteen.second()),
                'благотворить': str(bsixteen.third()),
                'благоустраивать': str(bsixteen.fourth()),
                'благоустраиваться': str(bsixteen.fifth()),
                'благоухать': str(bsixteen.sixth()),
                'блаженствовать': str(bsixteen.seventh()),
                'блажь': str(bsixteen.eighth()),
                'блажить': str(bsixteen.nineth()),
                'бланшировать': str(bsixteen.tenth()),
                'бланшироваться': str(bseventeen.first()),
                'блевать': str(bseventeen.second()),
                'бледный': str(bseventeen.third()),
                'бледнеть': str(bseventeen.fourth()),
                'бледнить': str(bseventeen.fifth()),
                'блекнуть': str(bseventeen.sixth()),
                'блеснуть': str(bseventeen.seventh()),
                'блестеть': str(bseventeen.eighth()),
                'блефовать': str(bseventeen.nineth()),
                'блеять': str(bseventeen.tenth()),
                'близиться': str(beighteen.first()),
                'бликовать': str(beighteen.second()),
                'блиндировать': str(beighteen.third()),
                'блиндироваться': str(beighteen.fourth()),
                'блистать': str(beighteen.fifth()),
                'блокировать': str(beighteen.fifth()),
                'блокироваться': str(beighteen.sixth()),
                'блудить': str(beighteen.seventh()),
                'блуждать': str(beighteen.eighth()),
                'блюсти': str(beighteen.tenth()),
                'блюдись': str(bnineteen.first()),
                'блюдитесь': str(bnineteen.second()),
                'богатей': str(bnineteen.third()),
                'богатеть': str(bnineteen.fourth()),
                'богатить': str(bnineteen.fifth()),
                'богословствовать': str(bnineteen.sixth()),
                'боготворить': str(bnineteen.seventh()),
                'богохульничать': str(bnineteen.eighth()),
                'богохульствовать': str(bnineteen.nineth()),
                'бодать': str(bnineteen.tenth()),
                #
                'фас': str(ac.first()),
                'перевести': str(ac.second()),
                'поссчитать': str(ac.nineth()),
                'находить': str(ac.third()),
                'сказать': str(ac.fourth()),
                'погода': str(ac.fifth()),
                'поздороваться': str(ac.sixth()),
                'почистить': str(ac.seventh()),
                'очистить': str(ac.seventh())
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