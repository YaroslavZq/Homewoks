from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        self._value = self.validate_phone(value)

    @staticmethod
    def validate_phone(phone):
        if not phone[0].isdigit():
            if len(phone[0]) < 10 or len(phone[0]) > 12:
                print('Phone must be 10-12 characters without letters')
                return False

        return phone


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        self._value = self.validate_day(value)

    @staticmethod
    def validate_day(person_birthday):

        today = datetime.now()

        if person_birthday > datetime.date(today):
            return False
        return person_birthday


class Record:

    def __init__(self, name: Name, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def replace_phone(self, old_phone: Phone, new_phone: Phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.add_phone(new_phone)
                self.phones.remove(phone)

    def remove_phone(self, name, count):
        self.phones.pop(count)
        print(f'Phone number for contact {name.value.capitalize()} '
              f'is deleted')

    def add_birthday(self, birth: datetime):
        if self.birthday is None:
            birth = Birthday(birth)
            self.birthday = birth
        else:
            while True:
                question = input('Change birthday for contact?\n(y/n)')
                if question.lower() == 'y':
                    birth = Birthday(birth)
                    self.birthday = birth
                    break
                if question.lower() == 'n':
                    break

    def days_to_birthday(self, original_date, now):
        self.original_date = self.birthday
        self.now = datetime.now()
        delta1 = datetime(now.year, original_date.month, original_date.day)
        delta2 = datetime(now.year+1, original_date.month, original_date.day)
        self.days = ((delta1 if delta1 > now else delta2) - now).days
        return self.days

    def __repr__(self):
        if not self.birthday:
            return str(f'{self.name.value.capitalize()}, {self.phones}')
        else:
            return str(f'{self.name.value.capitalize()}, {self.phones}, '
                       f'Birthday: {self.birthday.value}')


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self):
        for record in self.data.values():
            yield record


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


def hello_message():
    print("How can I help you?")


@input_error
def add_person(user_message):
    name = Name(user_message.split(' ')[1])
    phone = Phone(user_message.split(' ')[2])
    record = Record(name)
    record.add_phone(Phone(phone))
    if len(user_message.split(' ')) != 3:
        print('Enter correct name and phone')
        return False
    if name.value in addressbook:
        print(f'{name.value.capitalize()} is already in the phone book')
        return False
    if Phone.validate_phone(phone.value):
        addressbook.add_record(record)
        print(f'A contact {name.value.capitalize()} has been added '
              f'to the phone book. Phone(s) {phone.value}')


@input_error
def change_phone(user_message):
    name = Name(user_message.split(' ')[1])
    phone = Phone(user_message.split(' ')[2])
    new_phone = Phone(user_message.split(' ')[3])
    record = Record(name)
    if len(user_message.split(' ')) != 4:
        print('use command like this "change /contact name/ /old contact phone/ /new contact phone/"')
        return False
    if name.value in addressbook and Phone.validate_phone(phone.value):
        record.replace_phone(phone, new_phone)
        print(f'{name.value.capitalize()} phone has been '
              f'changed to {phone.value}')
    if name.value not in addressbook:
        print(f'{name.value.capitalize()} is not in the phone book. '
              f'You cannot change its number')


@input_error
def append_phone(user_message):
    name = Name(user_message.split(' ')[1])
    phone = Phone(user_message.split(' ')[2])
    record = Record(name)
    if len(user_message.split(' ')) != 3:
        print('Enter correct name and phone')
        return False
    if name.value not in addressbook:
        print(
            f'{name.value.capitalize()} is not in the phone book. '
            f'You cannot added number for it')
        return False
    if Phone.validate_phone(phone.value):
        record.add_phone(phone)
        print(f'For {name.value.capitalize()} added phone {phone.value}')


@input_error
def show_phone(user_message):
    name = Name(user_message.split(' ')[1])
    if len(user_message.split(' ')) != 2:
        print('when searching for a number, use the template "phone" "name"')
        return False
    if name.value in addressbook:
        for users in addressbook.values():
            if name.value == users.name.value:
                print(
                    f'Name: {users.name.value.capitalize()}, '
                    f'Phone: {users.phones.value}')
    else:
        print(f'Name {name.value.capitalize()} is not in the phone book')


@input_error
def delete_phone(user_message):
    name = Name(user_message.split(' ')[1])
    if len(user_message.split(' ')) != 2:
        print('when delete phone for contact, use the "delete name"')
        return False
    if name.value in addressbook:
        for users in addressbook.values():
            count = 0
            for phone in users.phones.value:
                print(f'{count} - {phone}')
                count += 1
            order = int(input('What of phones do you want to delete by order: '))
            users.remove_phone(name, order)


def show_all():
    print('Your contact list:')
    for users in addressbook.values():
        print(users)


@input_error
def show_part(user_message):
    count = user_message.split(' ')[1]
    page = addressbook.iterator()
    while True:
        try:
            show_next = input(f'\nShow {count} contacts? (y/n)\n')
            if show_next == 'y':
                for _ in range(int(count)):
                    print(next(page))
            if show_next == 'n':
                break
        except StopIteration:
            print('Book is over')
            break


@input_error
def select_birthday_date(user_message):
    name = Name(user_message.split(' ')[1])
    if len(user_message.split(' ')) != 2:
        print('Error. Enter "birthday" "name"')
        return False
    if name.value in addressbook:
        birthday = input('Enter YYYY/MM/DD''\n').split('/')
        person_birthday = datetime(year=int(birthday[0]), month=int(
            birthday[1]), day=int(birthday[2]))
        person_birthday = datetime.date(person_birthday)
        for users in addressbook.values():
            if (users.name.value == name.value
                    and Birthday.validate_day(person_birthday)):
                users.add_birthday(person_birthday)
                print(f'For contact {users.name.value.capitalize()} '
                      f'added birthday {users.birthday.value}')
        if not Birthday.validate_day(person_birthday):
            print('Incorrect date, try again')
    else:
        print(f'{name.value} birthday not in address book')


@input_error
def when_birthday(user_message):
    name = Name(user_message.split(' ')[1])
    if len(user_message.split(' ')) != 2:
        print('when searching for a number, use the template "party" "name"')
        return False
    if name.value in addressbook:
        for users in addressbook.values():
            if name.value == users.name.value and users.birthday is not None:
                days = users.days_to_birthday(
                    users.birthday.value, datetime.now())
                print(
                    f'Name: {users.name.value.capitalize()}, '
                    f'Birthday: {users.birthday.value}, after {days} days')
            if name.value == users.name.value and users.birthday is None:
                print('This contact does not have a date of birth')
    else:
        print(f'Name {name.value.capitalize()} is not in the phone book')


commands = '''
Add a new contact: "add" /contact name/ /contact phone/
Change phone for a contact: "change" /contact name/ /old contact phone/ /new contact phone/
Add new phone for contact: "append" /contact name/ /new contact phone/
Delete the phone for contact: "delete" /contact name/
See the contact's phone number: "phone" /contact name/
Set a birthday for a contact: "birthday" /contact name/
Get information about the contact's birthday: "party" /contact name/
View all contacts: "show all"
View N elements of the notebook: "part" /N/
See this message again: "help"
'''


def get_help():
    print(commands)


COMMANDS = {
    'hello': hello_message,
    'add': add_person,
    'change': change_phone,
    'phone': show_phone,
    'delete': delete_phone,
    'append': append_phone,
    "show all": show_all,
    "part": show_part,
    'birthday': select_birthday_date,
    'help': get_help,
    'party': when_birthday,
}


def main():
    print(commands)
    while True:
        user_message = input('Enter command: ').lower()
        if user_message.endswith(' '):
            user_message = user_message.rstrip()
        if not user_message or user_message.startswith(' '):
            continue
        if user_message in ("good bye", "close", "exit"):
            print("Good bye!")
            break
        if user_message in COMMANDS:
            COMMANDS[user_message]()
        elif user_message.split()[0] in COMMANDS:
            COMMANDS[user_message.split()[0]](user_message)


if __name__ == '__main__':
    addressbook = AddressBook()
    main()
