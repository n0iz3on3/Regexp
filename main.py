from sortnparse import *

if __name__ == '__main__':
    pretty_contact_list = get_pretty_contact_list(pure_contact_list)
    write_to_csv_file(file_name, pretty_contact_list, field_names)

    for elements in pretty_contact_list:
        print(elements)