def auto_categorize(description: str) -> str:
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
