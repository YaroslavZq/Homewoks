CONTACTS = {}


def input_error(handler):
    def wrapper(*args):
        try:
            handler(*args)
        except TypeError as e:
            arg = input('Enter user name:')
            return wrapper(arg)
        except Exception as e:
            args = input('Give me name and phone please:').split()
            return wrapper(*args)
    return wrapper


@input_error
def hello():
    print('How can I help you?')


def show():
    for name, phone in CONTACTS.items():
        print(f"{name}: {phone}")


@input_error
def add_contact(*args):
    name = args[0]
    phone = args[1]
    CONTACTS[name] = phone
    print('New contact added.')


@input_error
def find_contact(arg):
    name = arg
    print(name, CONTACTS[name])


@input_error
def change(*args):
    name = args[0]
    phone = args[1]
    CONTACTS[name] = phone
    print(f'Contact{name} successfully changed.')


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
    exit(main())
