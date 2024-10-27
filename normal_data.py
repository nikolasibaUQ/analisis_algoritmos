class NormalData:
    def __init__(self, author=None, title=None, abstract=None, year=None, volume=None, pages=None):
        self.author = author
        self.title = title
        self.abstract = abstract
        self.year = year
        self.volume = volume
        self.pages = pages

    def get_data(self):
        # Solo devolver los datos que no sean nulos o vacíos, permitir volume=1 y pages=1
        data = {}
        if self.author: data['author'] = self.author
        if self.title: data['title'] = self.title
        if self.abstract: data['abstract'] = self.abstract
        if self.year: data['year'] = self.year
        if self.volume is not None:  # Verificar explícitamente si volume no es None
            data['volume'] = self.volume
        if self.pages is not None:
            data['pages'] = self.pages
        return data
