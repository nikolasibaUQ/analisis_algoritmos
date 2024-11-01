class NormalData:
    def __init__(self, author=None, title=None, abstract=None, year=None, volume=None, pages=None, entry_type='article', journal=None, database=None):
        self.author = author
        self.title = title
        self.abstract = abstract
        self.year = year
        self.volume = volume
        self.pages = pages
        self.entry_type = entry_type
        self.journal = journal
        self.database = database

    def get_data(self):
        # Solo devolver los datos que no sean nulos o vacíos, permitir volume=1 y pages=1
        data = {}

        if self.author:
            data['author'] = self.author
        if self.title:
            data['title'] = self.title
        if self.abstract:
            data['abstract'] = self.abstract
        if self.year:
            data['year'] = self.year
        if self.volume is not None:  # Verificar explícitamente si volume no es None
            data['volume'] = self.volume
        if self.pages is not None:
            data['pages'] = self.pages
        if self.entry_type:
            data['ENTRYTYPE'] = self.entry_type
        if self.journal:
            data['journal'] = self.journal
        if self.database:
            data['database'] = self.database
        return data
