import logging
from duckduckgo_search import DDGS
from Deep_layer.API_package.Interfaces import IFinder
import random
import time
from urllib.parse import urlparse


class DuckduckgoFinder(IFinder.IFinder):
    """
    DuckDuckGo finder class with multiple queries for diversity
    """

    @classmethod
    def find(cls, message_text, max_results=8):
        try:
            time.sleep(random.uniform(2, 5))

            ddgs = DDGS()
            all_links = set()

            # Основной запрос
            main_results = ddgs.text(
                keywords=message_text,
                region='ru-ru',
                max_results=5
            )
            all_links.update(cls._extract_links(main_results))

            # Если нужно больше разнообразия, делаем дополнительные запросы
            if len(all_links) < max_results:
                additional_queries = cls._generate_alternative_queries(message_text)

                for query in additional_queries[:2]:  # Ограничиваем количество доп. запросов
                    time.sleep(random.uniform(1, 3))  # Задержка между запросами

                    try:
                        additional_results = ddgs.text(
                            keywords=query,
                            region='ru-ru',
                            max_results=3
                        )
                        new_links = cls._extract_links(additional_results)
                        all_links.update(new_links)

                        if len(all_links) >= max_results:
                            break
                    except Exception as e:
                        logging.debug(f"Additional query failed for '{query}': {e}")
                        continue

            return set(list(all_links)[:max_results])

        except Exception as e:
            logging.exception(f'Error: {e}')
            return set()

    @staticmethod
    def _extract_links(results):
        """Извлекает ссылки из результатов"""
        links = []
        domains_used = set()

        for result in results:
            url = result.get('href', '')
            if url:
                try:
                    domain = urlparse(url).netloc
                    if domain.startswith('www.'):
                        domain = domain[4:]

                    # Проверяем, не использовали ли уже этот домен
                    if domain not in domains_used:
                        links.append(url)
                        domains_used.add(domain)
                except Exception:
                    links.append(url)  # Добавляем даже если не удалось распарсить

        return links

    @staticmethod
    def _generate_alternative_queries(main_query):
        """Генерирует альтернативные запросы для большего разнообразия"""
        words = main_query.split()
        if len(words) <= 1:
            return [main_query]

        alternatives = [
            main_query + " обзор",
            main_query + " сайт",
            "лучшие " + main_query,
            main_query + " отзывы"
        ]

        # Перемешиваем слова
        if len(words) > 2:
            shuffled = words.copy()
            random.shuffle(shuffled)
            alternatives.append(' '.join(shuffled))

        return alternatives