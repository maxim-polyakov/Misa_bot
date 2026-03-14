/**
 * Заглушка для Node http — в React Native модуль недоступен.
 * При вызове createServer выбрасывает ошибку (fallback на misa://).
 */
module.exports = {
  createServer: () => {
    throw new Error("http module not available");
  },
};
