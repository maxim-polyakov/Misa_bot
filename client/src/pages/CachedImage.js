import {useEffect, useState} from "react";
import { imageDB } from "./ImageDB";

const CachedImage = ({ src, cacheKey, messageContent, messageUser }) => {
    const [imgSrc, setImgSrc] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const loadImage = async () => {
            try {
                // 1. Сначала проверяем кэш в IndexedDB
                const cached = await imageDB.get(cacheKey);

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
                if (!src || typeof src !== 'string') {
                    setImgSrc(src);
                    setIsLoading(false);
                    return;
                }
                setIsLoading(true);
                const response = await fetch(src + '?t=' + Date.now(), {
                    mode: 'cors',
                    credentials: 'omit',
                });

                if (!response.ok) throw new Error('Network response was not ok');

                const blob = await response.blob();

                // Конвертируем в base64 для хранения
                const base64data = await new Promise((resolve) => {
                    const reader = new FileReader();
                    reader.onloadend = () => resolve(reader.result);
                    reader.readAsDataURL(blob);
                });

                // Сохраняем в IndexedDB
                await imageDB.set(cacheKey, base64data);

                setImgSrc(base64data);
                setIsLoading(false);

            } catch (error) {
                // Failed to fetch — обычно CORS на S3/внешних доменах; img src загрузит напрямую
                if (error?.name === 'TypeError' && error?.message?.includes('fetch')) {
                    setImgSrc(src);
                } else {
                    console.error('Ошибка загрузки изображения:', error);
                    setImgSrc(src);
                }
                setIsLoading(false);
            }
        };

        const checkForUpdates = async () => {
            // Фоновая проверка обновлений (игнорируем ошибки CORS)
            try {
                if (src && typeof src === 'string') {
                    await fetch(src + '?check=' + Date.now(), { mode: 'cors', credentials: 'omit' });
                }
            } catch {
                // CORS или сеть — не критично
            }
        };

        loadImage();
    }, [src, cacheKey]);

    if (isLoading) {
        return <div className="image-loading">Загрузка изображения...</div>;
    }

    // imgSrc может быть null при ошибке до fetch — используем src напрямую
    const displaySrc = imgSrc || src;
    if (!displaySrc) {
        return <div className="message-text">{messageContent}</div>;
    }

    return (
        <img
            src={displaySrc}
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