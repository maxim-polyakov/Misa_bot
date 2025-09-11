from nltk.corpus import stopwords
from string import punctuation
from pymystem3 import Mystem
import re
import logging
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing


class CommonPreprocessing(Preprocessing.Preprocessing):
    """
    It is a common preprocessing of sentences
    """

    @classmethod
    def preprocess_text(cls, text):
        """Оптимизированная предобработка текста"""
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # Если текст слишком длинный, возвращаем как есть
            if len(text) > 100:
                return text.lower().strip()

            tokens = str(text)
            # Используем кэш для лемматизации
            if not hasattr(cls, '_lemmatizer'):
                cls._lemmatizer = Mystem()

            tokens = cls._lemmatizer.lemmatize(text.lower())

            # Кэшируем стоп-слова для производительности
            if not hasattr(cls, '_stopwords'):
                cls._stopwords = set(stopwords.words('russian')) | set(stopwords.words('english')) | set(punctuation)

            tokens = [token for token in tokens if token not in cls._stopwords and token.strip()]

            text = ' '.join(tokens).rstrip('\n')

            # Упрощенные regex паттерны
            text = re.sub(r'[\d.]', '', text)
            text = re.sub(r'\s+', ' ', text).strip()

            logging.info('Text preprocessing completed successfully')
            return text

        except Exception as e:
            logging.exception('Exception in preprocess_text: ' + str(e))

    @classmethod
    def reversepreprocess_text(cls, text):
        pass
