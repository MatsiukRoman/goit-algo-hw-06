from collections import UserDict

class CheckPhoneNumber(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit():
           raise CheckPhoneNumber(f'Phone {value} is not digit') 
        elif len(value) > 10:
            raise CheckPhoneNumber(f'Phone {value} > 10 digits')
        super().__init__(value)

    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def add_phone(self,phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        if phone in [p.value for p in self.phones]:
            self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        try:
            Phone(new_phone)  
        except ValueError as e:
            return str(e)
        
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self,phone):
        try:
            found_phone = next(item for item in self.phones if item.value == phone)
            return found_phone
        except Exception as e:
            return str(e)


class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.value] = record
   
    def find(self,record):
        return self.data.get(record)
    
    def delete(self,record):
        for key in list(self.keys()):
            if key == record:
                del self[key]  

book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.delete("Jane")