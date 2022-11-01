import csv
import re

file_name_dirty = 'phonebook_raw.csv'
file_name_pretty = 'phonebook_simple.csv'


def read_csv_file(filename, dialect='excel'):
    with open(filename, encoding='utf-8', newline='') as file:
        return list(csv.reader(file, dialect))


file_data = read_csv_file(file_name_dirty)

# поиск номера телефона
pattern = r"(\+7|8)\s?(\()?(\d{3})(\))?\-?\s?(\d{3})(\-)?(\d{2})(\-)?(\d{2})(\W|)?((\(|)(доб......)(\)|)|)"
sub_pattern = r"+7(\3)\5-\7-\9 \13"
# поиск email'a
pattern2 = r"(\w+)(([_.-])(\w+))?@\w+\S\w+"

field_names = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']

# пересобираем список с ФИО по местам и стилизацией номера
def get_new_list(data):
    result = list()
    for line in data:
        record = list()
        full_name = line[0].split(' ')
        full_name = re.findall(r'(\w+)', ' '.join(line[:3]))
        if len(full_name) < 3:
            full_name.append('')
        record += full_name
        record.append(line[3])
        record.append(line[4])
        record.append(re.sub(pattern, sub_pattern, line[5]).strip())
        record.append(line[6])
        result.append(record)
    return result

# сортируем список, соединяем дубли
def get_sort_contact_list(data):
    result = dict()
    for elem in data:
        result[elem[0]] = merge_doubles(elem, result[elem[0]]) if elem[0] in result else elem
    return result.values()

# объединение дублей
def merge_doubles(result_one, result_two):
    result = list()
    for i in range(len(result_one)):
        result.append(result_one[i]) if result_one[i] else result.append(result_two[i])
    return result


dirty_contact_list = get_new_list(file_data)
pure_contact_list = get_sort_contact_list(dirty_contact_list)

# список словаерей для записи в .csv и вывода в консоль(если надо)
def get_pretty_contact_list(data):
    source = []
    result = []
    for element in data:
        source.append(element)

    keys = source[0]
    values = source[1:]
    for i in range(len(values)):
        result.append(dict(zip(keys, values[i])))
    return result

# запись в файл
def write_to_csv_file(filename, rows, field_names):
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(rows)