class NormalData:
    def __init__(self, author=None, title=None, abstract=None, year=None, volume=None):
        self.author = author
        self.title = title
        self.abstract = abstract
        self.year = year
        self.volume = volume

    def get_data(self):
        # Solo devolver los datos que no sean nulos o vacíos
        data = {}
        if self.author: data['author'] = self.author
        if self.title: data['title'] = self.title
        if self.abstract: data['abstract'] = self.abstract
        if self.year: data['year'] = self.year
        if self.volume: data['volume'] = self.volume
        return data
