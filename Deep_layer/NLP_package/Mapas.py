class Mapa:
    """

    Summary

    """
    HIMAPA = {0: 'Не приветствие', 1: 'Приветствие'}
    QUMAPA = {0: 'Не вопрос', 1: 'Вопрос'}
    THMAPA = {0: 'Не благодарность', 1: 'Благодарность'}
    TRMAPA = {0: 'Не треш', 1: 'Треш'}
    COMMANDMAPA = {0: 'Не команда', 1: 'Команда'}
    BUSINESSMAPA = {0: 'Не дело', 1: 'Дело'}
    WEATHERMAPA = {0: 'Не погода', 1: 'Погода'}
    MULTYMAPA = {0: 'Нет темы', 1: 'Погода', 2: 'Дело'}
    EMOTIONSMAPA = {0: '😞', 1: '🤬', 2: '😨', 3: '😊', 4: '❤', 5: '😳', 6: ''}
    HI_TH_COMMANDMAPA = {0: 'Утверждение', 1: 'Команда', 2: 'Приветствие', 3: 'Благодарность'}

class ListMapas(Mapa):
    """

    Summary

    """
    def getlistmapas(self):
#
#
        listmaps = []
        listmaps.append(super().HIMAPA)
        listmaps.append(super().THMAPA)
        listmaps.append(super().BUSINESSMAPA)
        listmaps.append(super().WEATHERMAPA)
        listmaps.append(super().TRMAPA)
        return listmaps

