from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record


class Record(Field):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add(self, phone):
        self.phones.append(Phone(phone))

    def remove(self, phone):
        self.phones.remove(Phone(phone))

    def update(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.add(new_phone)
                self.phones.remove(phone)


def input_error(handler):
    def wrapper(*args):
        try:
            handler(*args)
        except TypeError:
            print('Give me name and phone please.')
        except ValueError:
            print('Enter correct type.')
        except IndexError:
            print('Give me name and phone please.')
        except KeyError:
            print('Enter user name.')
    return wrapper


@input_error
def hello():
    print('How can I help you?')


@input_error
def show():
    print(addressbook.data)


@input_error
def add_contact(*args):
    name = args[0]
    phone = args[1]
    record = Record(name)
    record.add(phone)
    addressbook.add_record(record)
    print(f'New contact added.\nName: {name},\nPhone: {phone}')


@input_error
def find_contact(arg):
    name = arg
    print(list(map(lambda x: x.value, addressbook.data[name].phones)))


@input_error
def change(*args):
    name = args[0]
    phone = args[1]
    new_phone = args[2]
    record = addressbook.data[name]
    record.update(old_phone=phone, new_phone=new_phone)
    print(f'Contact {name} successfully changed old phone: {phone} to new: {new_phone}')


def quit_func():
    print('Good bye!')
    quit()


COMMANDS = {
    'hello': hello,
    'exit': quit_func,
    'close': quit_func,
    'good bye': quit_func,
    'add': add_contact,
    'phone': find_contact,
    'show all': show,
    'change': change
}


def main():
    while True:
        com, *args = input("Enter command:").split()
        if com.lower() == 'show' and args[0].lower() == 'all' or com.lower() == 'good' and args[0].lower() == 'bye':
            com = com.lower() + " " + args[0].lower()
            COMMANDS[com]()
            continue
        com = com.lower()
        if com not in COMMANDS:
            print('Wrong command')
            continue
        COMMANDS[com](*args)


if __name__ == "__main__":
    addressbook = AddressBook()
    main()
