import {useEffect, useState} from "react";
import { ImageDB } from "./ImageDB";

const CachedImage = ({ src, cacheKey, messageContent, messageUser }) => {
    const [imgSrc, setImgSrc] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const loadImage = async () => {
            try {
                // 1. Сначала проверяем кэш в IndexedDB
                const cached = await ImageDB.get(cacheKey);

                if (cached) {
                    setImgSrc(cached);
                    setIsLoading(false);
                    checkForUpdates();
                } else {
                    await fetchAndCacheImage();
                }
            } catch (error) {
                console.error('Ошибка при загрузке из кэша:', error);
                await fetchAndCacheImage();
            }
        };

        const fetchAndCacheImage = async () => {
            try {
                setIsLoading(true);
                const response = await fetch(src + '?t=' + Date.now());

                if (!response.ok) throw new Error('Network response was not ok');

                const blob = await response.blob();

                // Конвертируем в base64 для хранения
                const base64data = await new Promise((resolve) => {
                    const reader = new FileReader();
                    reader.onloadend = () => resolve(reader.result);
                    reader.readAsDataURL(blob);
                });

                // Сохраняем в IndexedDB
                await ImageDB.set(cacheKey, base64data);

                setImgSrc(base64data);
                setIsLoading(false);

            } catch (error) {
                console.error('Ошибка загрузки изображения:', error);
                setIsLoading(false);
            }
        };

        const checkForUpdates = async () => {
            // Фоновая проверка обновлений
            try {
                const response = await fetch(src + '?check=' + Date.now());
                // Можно добавить логику проверки ETag или Last-Modified
            } catch (error) {
                console.log('Не удалось проверить обновления изображения');
            }
        };

        loadImage();
    }, [src, cacheKey]);

    if (isLoading) {
        return <div className="image-loading">Загрузка изображения...</div>;
    }

    return (
        <img
            src={imgSrc}
            alt={`Изображение от ${messageUser}`}
            className="message-image"
            onError={(e) => {
                e.currentTarget.style.display = 'none';
                const textElement = document.createElement('div');
                textElement.className = 'message-text';
                textElement.style.whiteSpace = 'pre-line';
                textElement.textContent = messageContent;
                e.currentTarget.parentNode.appendChild(textElement);
            }}
        />
    );
};

export default CachedImage;