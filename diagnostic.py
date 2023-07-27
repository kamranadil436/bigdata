from itertools import groupby

message = input("Enter a message: ")
mod_string = message + ''
length = len(mod_string)

for char, group in groupby(mod_string):
    group_list = list(group)
    group_length = len(group_list)
    print(char)
    if group_length > 1:
        print(group_length)