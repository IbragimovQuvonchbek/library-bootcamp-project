from hashlib import blake2b

from scriptsLibrary.hjson import read_data, write_data


def user_exists(username, gmail):
    clients_data = read_data('../databases/clients.json')
    for client in clients_data:
        if client['username'] == username or client['gmail'] == gmail:
            return True
    return False


class Client:
    id = -1

    def __init__(self, name, surname, username, gmail, password):
        self.name = name
        self.surname = surname
        self.username = username
        self.gmail = gmail
        self.books = []
        self.__password = blake2b(password.encode('utf-8')).hexdigest()

    def add_new_client(self):
        if not user_exists(username=self.username, gmail=self.gmail):
            clients_data = read_data('../databases/clients.json')
            self.id = clients_data[-1]['id'] + 1 if clients_data else 1
            new = {
                'id': self.id,
                'name': self.name,
                'surname': self.surname,
                'username': self.username,
                'gmail': self.gmail,
                'books': self.books,
                'superuser': False if clients_data else True,
                'password': self.__password
            }
            clients_data.append(new)
            write_data('../databases/clients.json', clients_data)
        return self.id


class Books:
    id = -1

    def __init__(self, name, description, category, author, unit):
        self.name = name
        self.description = description
        self.category = category
        self.author = author
        self.unit = unit

    def add_new_book(self):
        data = read_data('../databases/books.json')
        self.id = data[-1]['id'] + 1 if data else 1
        new_book = {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'category': self.category,
            'description': self.description,
            'unit': self.unit,
            'owners': []
        }
        data.append(new_book)
        write_data('../databases/books.json', data)

        return self.id
