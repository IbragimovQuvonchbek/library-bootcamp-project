from hashlib import blake2b

from scriptsLibrary.hjson import read_data, write_data
from scriptsLibrary.models import Client, Books


def signup(name, surname, username, gmail, password):
    new_client = Client(name=name, surname=surname, username=username, gmail=gmail, password=password)
    return new_client.add_new_client()


def login(username, password):
    clients_data = read_data('../databases/clients.json')
    for client in clients_data:
        if client['username'] == username and client['password'] == blake2b(password.encode('utf-8')).hexdigest():
            return client['id']
    return -1


def is_superuser(username):
    clients_data = read_data('../databases/clients.json')
    for client in clients_data:
        if client['username'] == username:
            return client['superuser']
    return False


def show_all_books():
    books_data = read_data('../databases/books.json')
    raw_data = []
    for book in books_data:
        if book['unit'] != 0:
            raw_data.append([book['id'], book['name']])
    return raw_data


def search_books(keyword):
    books_data = read_data('../databases/books.json')
    raw_data = []
    for book in books_data:
        if keyword.lower() in book['name'].lower():
            raw_data.append([book['id'], book['name']])
    return raw_data


def search_registered_books(keyword, user_books):
    books_data = read_data('../databases/books.json')
    raw_data = []
    for book in books_data:
        if keyword.lower() in book['name'].lower() and book['id'] in user_books:
            raw_data.append([book['id'], book['name']])
    return raw_data


def get_book_by_id(id_book):
    books_data = read_data('../databases/books.json')
    raw_data = None
    for book in books_data:
        if id_book == book["id"]:
            raw_data = book
            break
    return raw_data


def is_book_registered(book_id, user_id):
    clients_data = read_data('../databases/clients.json')
    for client in clients_data:
        if client['id'] == user_id and book_id in client['books']:
            return True
    return False


def register_book(book_id, user_id):
    clients_data = read_data("../databases/clients.json")
    books_data = read_data("../databases/books.json")

    for client in clients_data:
        if client['id'] == user_id:
            client['books'].append(book_id)
            write_data('../databases/clients.json', clients_data)
            break

    for book in books_data:
        if book['id'] == book_id:
            book['unit'] -= 1
            book['owners'].append(user_id)
            write_data('../databases/books.json', books_data)
            break


def unregister_book(book_id, user_id):
    clients_data = read_data("../databases/clients.json")
    books_data = read_data("../databases/books.json")

    for client in clients_data:
        if client['id'] == user_id:
            client['books'].remove(book_id)
            write_data('../databases/clients.json', clients_data)
            break

    for book in books_data:
        if book['id'] == book_id:
            book['owners'].remove(user_id)
            book['unit'] += 1
            write_data('../databases/books.json', books_data)
            break


def get_registered_books(user_id):
    clients_data = read_data('../databases/clients.json')
    books_data = read_data('../databases/books.json')
    user_books = []
    for client in clients_data:
        if client['id'] == user_id:
            user_books = client['books']
            break
    raw_data = []
    for book in books_data:
        if book['id'] in user_books:
            raw_data.append([book['id'], book['name']])
    return [raw_data, user_books]


def delete_book(book_id):
    books_data = read_data('../databases/books.json')
    clients_data = read_data('../databases/clients.json')

    for book in books_data:
        if book['id'] == book_id:
            books_data.remove(book)
            write_data('../databases/books.json', books_data)
            break

    for client in clients_data:
        if book_id in client['books']:
            client['books'].remove(book_id)
    write_data('../databases/clients.json', clients_data)


def add_book(name, author, category, description, unit):
    new_book = Books(name=name, author=author, category=category, description=description, unit=unit)
    return new_book.add_new_book()


def edit_book(name, author, category, description, book_id, unit):
    books_data = read_data('../databases/books.json')

    for book in books_data:
        if book['id'] == book_id:
            if name and name.strip() != "leave it for unchanged":
                book['name'] = name
            if author and author.strip() != "leave it for unchanged":
                book['author'] = author
            if category and category.strip() != "leave it for unchanged":
                book['category'] = category
            if description and description.strip() != "leave it for unchanged":
                book['description'] = description
            if unit and unit.strip() != "leave it for unchanged":
                book['unit'] = unit
            write_data('../databases/books.json', books_data)
            break


def is_book_available(book_id):
    books_data = read_data("../databases/books.json")

    for book in books_data:
        if book['id'] == book_id:
            return book['unit'] != 0
    return False


def show_users():
    clients_data = read_data('../databases/clients.json')
    raw_data = []
    for client in clients_data:
        if not client['superuser']:
            raw_data.append([client['id'], client['username']])

    return raw_data


def search_users(keyword):
    clients_data = read_data('../databases/clients.json')
    raw_data = []
    for client in clients_data:
        if keyword.lower() in client['username'].lower():
            raw_data.append([client['id'], client['username']])
    return raw_data


def get_user_by_id(user_id):
    clients_data = read_data('../databases/clients.json')
    for client in clients_data:
        if client['id'] == user_id:
            return client
    return None


def get_user_books_info(user_books):
    books_data = read_data('../databases/books.json')
    raw_data = []
    for book in books_data:
        if book['id'] in user_books:
            raw_data.append([book['id'], book['name']])
    return raw_data
