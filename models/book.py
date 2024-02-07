from models.book_category import BookCategory


class Book:
    def __init__(
        self,
        title: str=None,
        author: str=None,
        isAvailable: bool=None,
        originalPrice: float=None,
        currentPrice: float=None,
        imageUrl: str=None,
        bookUrl: str=None,
        category: BookCategory = None,
    ):
        self.title = title.strip()
        self.author = author.strip()
        self.isAvailable = isAvailable
        self.originalPrice = originalPrice
        self.currentPrice = currentPrice
        self.imageUrl = imageUrl.strip()
        self.bookUrl = bookUrl.strip()
        self.category = category.name

    def __str__(self):
        return f"{self.title} By {self.author}"

    def __keys__(self):
        dict_keys = Book().__dict__.keys()
        key_list = list(dict_keys)
        return key_list
