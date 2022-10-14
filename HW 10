from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class AddressBook(UserDict):

    def find_contact(self):
        name = input('enter name: ')
        if name in self.data:
            record = self.data[name]
            print(record, str(record.name.value), str(record.phones))
        else:
            print('Contact is not found')

    def add_record(self):
        name = Name(input('enter name: '))
        phone = Phone(input('enter phone: '))
        record = Record(name=name)
        if phone.value:
            record.add(phone)
        print(record)
        self.data[record.name.value] = record
        print('New contact added.')

    def show_all(self):
        for name, phone in self.data.items():
            print(name, phone)

    def change(self):
        name = Name(input('enter name: '))
        phone = Phone(input('enter phone to change: '))
        self.data[name] = phone
        print(f'Contact{name} successfully changed.')


class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []

    def add(self, phone):
        self.phones.append(phone)

    def remove(self, phone):
        self.phones.remove(phone)

    def update(self, old_phone, new_phone):
        self.remove(old_phone)
        self.add(new_phone)


def input_error(handler):
    def wrapper(*args):
        try:
            handler(*args)
        except TypeError as e:
            print('Enter user name')
        except Exception as e:
            print('Give me name and phone please')
    return wrapper


@input_error
def hello():
    print('How can I help you?')


def main():
    book = AddressBook()

    commands = {
        'hello': hello,
        'exit': quit,
        'close': quit,
        'good bye': quit,
        'add': book.add_record,
        'phone': book.find_contact,
        'show all': book.show_all,
        'change': book.change
    }

    while True:
        com, *args = input("Enter command:").split()
        if com.lower() == 'show' and args[0].lower() == 'all' or com.lower() == 'good' and args[0].lower() == 'bye':
            com = com.lower() + " " + args[0].lower()
            commands[com]()
            continue
        com = com.lower()
        if com not in commands:
            print('Wrong command')
            continue
        commands[com](*args)


if __name__ == "__main__":
    exit(main())
