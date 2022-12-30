def load_list_from_file(filename):
    if '.txt' not in filename:
        filename += '.txt'
    file_obj = open(filename, 'r')
    data = file_obj.read().split('\n')
    file_obj.close()
    return data
