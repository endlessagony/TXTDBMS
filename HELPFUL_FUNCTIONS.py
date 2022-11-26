def initialize_dictionary_from_txt(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        result_dict = {}
        for index, line in enumerate(f):
            if index == 0 or line == '\n':
                continue
            else:
                val, key = line.split(',')
                result_dict[key.split('\n')[0]] = val
    return result_dict


def get_ends_of_lines(file_path) -> list:
    new_line_indices = [0]
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            last_index = new_line_indices[i]
            if '\n' in line:
                _index = len(line) + 1
                new_line_indices.append(_index + last_index)

    return new_line_indices


def get_line(file_path: str, index: int):
    with open(file_path, 'r') as file:
        indices = get_ends_of_lines(file_path)
        if index + 1 >= indices.__len__():
            return ''
        else:
            file.seek(indices[index+1])
            result_line = file.readline()
    return result_line


def hash_helper(file_path: str, hash_key: str):
    hash_table = {}
    with open(file_path, 'r') as file:
        headers = file.readline().splitlines()[0].split(',')
        column_number = headers.index(hash_key)
        for iteration, line in enumerate(file):
            iteration += 1
            key = line.split(',')[column_number]
            if key in hash_table:
                hash_table[key] += ":" + str(iteration)
            else:
                hash_table[key] = str(iteration)
    return hash_table


def counting_sort_for_radix(input_array, place_value):
    count_array = [0] * 10
    input_size = len(input_array)

    for i in range(input_size):
        place_element = (input_array[i] // place_value) % 10
        count_array[place_element] += 1

    for i in range(1, 10):
        count_array[i] += count_array[i - 1]

    output_array = [0] * input_size
    i = input_size - 1
    while i >= 0:
        current_element = input_array[i]
        place_element = (input_array[i] // place_value) % 10
        count_array[place_element] -= 1
        new_position = count_array[place_element]
        output_array[new_position] = current_element
        i -= 1

    return output_array


def radix_sort(input_array):
    maximum = max(input_array)
    d = 1

    while maximum > 0:
        maximum /= 10
        d += 1

    place_value = 1
    output_array = input_array

    while d > 0:
        output_array = counting_sort_for_radix(output_array, place_value)
        place_value *= 10
        d -= 1

    return output_array