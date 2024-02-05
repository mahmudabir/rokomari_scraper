from models.book_category import BookCategory


class Book:
    def __init__(
        self,
        title: str,
        author: str,
        isAvailable: bool,
        originalPrice: float,
        currentPrice: float,
        imageUrl: str,
        bookUrl: str,
        category: BookCategory = None,
    ):
        self.title = title.strip()
        self.author = author.strip()
        self.isAvailable = isAvailable
        self.originalPrice = originalPrice
        self.currentPrice = currentPrice
        self.imageUrl = imageUrl.strip()
        self.bookUrl = bookUrl.strip()
        self.category = category

    def __str__(self):
        return f"{self.title} By {self.author}"
