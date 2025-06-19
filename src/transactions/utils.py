import logging

logger = logging.getLogger(__name__)

def auto_categorize(description: str) -> str:
    """
    Автоматически определяет категорию транзакции по описанию.
    :param description: Описание транзакции
    :return: Категория (строка)
    """
    logger.info(f"Автокатегоризация для описания: '{description}'")
    description = description.lower()
    if any(word in description for word in ["bus", "taxi", "uber", "yandex go"]):
        return "Transport"
    elif any(word in description for word in ["pizza", "burger", "restaurant", "cafe"]):
        return "Food"
    elif any(word in description for word in ["netflix", "cinema", "spotify", "music"]):
        return "Entertainment"
    elif any(word in description for word in ["electricity", "water", "gas", "rent"]):
        return "Utilities"
    else:
        return "Other"
