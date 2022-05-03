# Проект «Склад оргтехники».

# Создайте класс, описывающий склад.
# А также класс «Оргтехника», который будет базовым для классов конкретных типов оргтехники (принтер, сканер, копир).
# В базовом классе определите параметры, общие для приведённых типов.
# В классах-наследниках реализуйте параметры, уникальные для каждого типа оргтехники.

# Разработайте методы, которые отвечают за приём оргтехники на склад и передачу в определённое подразделение компании.
# Для хранения данных (наименование, количество и др.) можно использовать подходящую структуру (например, словарь).

# Реализуйте механизм валидации вводимых пользователем данных.
# Например, для указания количества принтеров, отправленных на склад, нельзя использовать строковый тип данных.

# Подсказка: постарайтесь реализовать в проекте максимум возможностей, изученных на уроках по ООП.


from random import randint


class EquipmentError(Exception):                                            # перехват ошибок при работе с оборудованием

    def __init__(self, _):
        pass


class Warehouse:                                                            # склад

    def __init__(self, name, max_storage):
        self.storage = {}                                                   # складское хранилище
        self.name = name
        self.max_storage = max_storage

    def accept_equipment(self, equipment, number=1):                        # приемка оборудования на склад
        # проверка корректности указанного количества
        if not isinstance(number, int) or number <= 0:
            raise EquipmentError('ошибка: количество оборудования должно быть целым положительным числом')
        # проверка наличия свободного места
        if sum([self.storage[i][0] for i in self.storage.keys()]) + number > self.max_storage:
            raise EquipmentError(f'ошибка: {self.name} - нет свободного места')
        # проверка соответствия типа и стоимости добавляемого оборудования уже имеющемуся
        if equipment.model in self.storage.keys():
            if self.storage[equipment.model][2]['name'] != equipment.parameters['name']:
                raise EquipmentError(f'ошибка: модель у оборудования разного типа не может совпадать')
            if self.storage[equipment.model][1] != equipment.price:
                raise EquipmentError(f'ошибка: стоимости добавляемого и уже имеющегося оборудования должны совпадать')
        # добавление оборудования на склад
        try:
            self.storage[equipment.model][0] += number
        except KeyError:
            self.storage[equipment.model] = [number, equipment.price, equipment.parameters]

    @staticmethod
    def transfer_equipment(wh_from, wh_where, equipment, number=1):         # перемещение оборудования между складами
        # проверка корректности указанного количества
        if not isinstance(number, int) or number <= 0:
            raise EquipmentError('ошибка: количество оборудования должно быть целым положительным числом')
        # проверка наличия оборудования
        try:
            if wh_from.storage[equipment.model][0] < number:
                raise EquipmentError(f'ошибка: {wh_from.name} - нет нужного количества оборудования')
        except KeyError:
            raise EquipmentError(f'ошибка: {wh_from.name} - нет такого оборудования')
        # приемка оборудования на второй склад
        wh_where.accept_equipment(equipment, number)
        # списание оборудования с первого склада
        wh_from.storage[equipment.model][0] -= number
        # удаление позиции с нулевым количеством, если такая появилась при списании оборудования
        if wh_from.storage[equipment.model][0] == 0:
            del wh_from.storage[equipment.model]


class OfficeEquipment:                                                      # оборудование

    def __init__(self, name, model, price, parameters):
        self.model = model
        self.price = price
        self.parameters = {'name': name, **parameters}   # (!) name сразу же может быть перезаписан из parameters


class Printer(OfficeEquipment):                                             # оборудование - принтер

    def __init__(self, model, price, **kwargs):
        super().__init__('принтер', model, price, kwargs)


class Scanner(OfficeEquipment):                                             # оборудование - сканер

    def __init__(self, model, price, **kwargs):
        super().__init__('сканер', model, price, kwargs)


class Copier(OfficeEquipment):                                              # оборудование - копир

    def __init__(self, model, price, **kwargs):
        super().__init__('копир', model, price, kwargs)


# создание складов
w0 = Warehouse('основной склад', randint(150, 250))
print(f'> {w0.name}: свободно {w0.max_storage} мест')
w1 = Warehouse('склад it-отдела', randint(30, 60))
print(f'> {w1.name}: свободно {w1.max_storage} мест')

# создание списка оборудования
op1 = Printer('HP LaserJet M111a', 16000, print_speed=20, max_format='A4', connect='USB 2.0')
op2 = Printer('HP LaserJet M111w', 17000, print_speed=20, max_format='A4', connect='USB 2.0', WiFi=True)
os1 = Scanner('HP ScanJet PRO 4500', 103000, scan_speed=30, type='планшетный', connect='USB 3.0', WiFi=True)
oc1 = Copier('CANON imageRUNNER 2206N', 98000, copy_speed=22, max_format='A4', type='B/W')
elst = [op1, os1, oc1, op2]

# заполнение первого склада
for i in elst:
    n = randint(40, 80)
    print(f'добавляем {i.parameters["name"]} {i.model} в количестве {n} шт')
    try:
        w0.accept_equipment(i, n)
    except EquipmentError as error:
        print(error)
print('> насобирали на первом складе:')
for i in w0.storage.keys():
    print(f'* {w0.storage[i][2]["name"]} {i} - {w0.storage[i][0]} шт')

# перемещение части оборудования на второй склад
for i in range(10):
    n1 = randint(0, len(elst)-1)
    n2 = randint(1, 20)
    print(f'перемещаем {elst[n1].parameters["name"]} {elst[n1].model} в количестве {n2} шт')
    try:
        Warehouse.transfer_equipment(w0, w1, elst[n1], n2)
    except EquipmentError as error:
        print(error)
print('> теперь на первом складе:')
for i in w0.storage.keys():
    print(f'* {w0.storage[i][2]["name"]} {i} - {w0.storage[i][0]} шт')
print('> теперь на втором складе:')
for i in w1.storage.keys():
    print(f'* {w1.storage[i][2]["name"]} {i} - {w1.storage[i][0]} шт')
