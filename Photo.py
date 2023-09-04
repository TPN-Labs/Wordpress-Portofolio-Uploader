class PhotoDetails:
    def __init__(self, title, category, file_name):
        self.title = title
        self.category = category
        self.file_name = file_name

    def __str__(self):
        return '> Title: (' + self.title + ')\n> Category: (' + self.category + ')\n> File name: ' + self.file_name + '\n'