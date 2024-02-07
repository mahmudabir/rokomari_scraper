class Book:
    def __init__(
        self,
        title: str = None,
        author: str = None,
        isAvailable: bool = False,
        originalPrice: float = None,
        currentPrice: float = None,
        imageUrl: str = None,
        bookUrl: str = None,
        category: str = None,
    ):
        self.title = title
        self.author = author
        self.isAvailable = isAvailable
        self.originalPrice = originalPrice
        self.currentPrice = currentPrice
        self.imageUrl = imageUrl
        self.bookUrl = bookUrl
        self.category = category

    def __str__(self):
        return f"{self.title} By {self.author}"

    def __keys__(self):
        dict_keys = Book().__dict__.keys()
        key_list = list(dict_keys)
        return key_list
