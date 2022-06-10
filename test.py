# Проверка високосного года
def is_leap(year):
    return year % 400 == 0 or (year % 4 == 0 and not year % 100 == 0)

# Проверка правильности даты рождения
def check_date(day, month, year):
    if not(type(day) is int and type(month) is int and type(year) is int):
        return False
    if year < 1900 or year > 2022:
        return False
    if month < 1 or month > 12:
        return False
    if is_leap(year):
        feb=[31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        feb=[31,28,31,30,31,30,31,31,30,31,30,31]
    
    if day > 0 and day <= feb[month-1]:
        return True
    else:
        return False
        
def register(surname, name, date, middle_name=None, registry=None):
    if registry is None:
        registry = []
    if not check_date(date[0], date[1], date[2]):
        raise ValueError("Invalid Date!")
    kort = (surname, name, middle_name, date[0], date[1], date[2])
    registry.append(kort)
    return registry

def sort_registry(registry):
    registry.sort(key = lambda registry: (registry[5], registry[4], registry[3], \
                  registry[0], registry[1], registry[2]))
    return registry

def get_strings(registry):
    # отбираем годы рождения более 2000
    y_list = filter(lambda x: x[5] >= 2000, registry)
    # Всех отобранных пользователей форматируем с помощью функции
    def format_strings(s_val):
        sname = s_val[0]
        name = s_val[1]
        mname = s_val[2]
        day = str(s_val[3]).zfill(2)
        month = str(s_val[4]).zfill(2)
        year = s_val[5]
        if mname is None:
            return '{} {}., {}.{}.{}'.format(sname, name[:1], day, month, year)
        else:
            return '{} {}.{}., {}.{}.{}'.format(sname, name[:1], mname[:1], day, month, year)
    # и оператора MAP
    result_a = map(lambda x: format_strings(x) , y_list)
    # Переводим объект map в list и возвращаем его
    return list(result_a)

def print_students(students, groups):
    def group_gen(n):
        i = 0
        while True:
            i += 1
            if i > n: i = 1
            yield i
    group_list = group_gen(groups)
    for student, grp in zip(students, group_list):
        print(student, 'studies in group', grp)
        

reg = register('Petrova', 'Maria', (13, 3, 2003), 'Ivanovna')
reg = register('Ivanov', 'Sergej', (24, 9, 1995), registry=reg)
reg = register('Smith', 'John', (13, 2, 2003), registry=reg)
reg = sort_registry(reg)
print(reg)
reg = get_strings(reg)
print(reg)
print_students(reg, 3)