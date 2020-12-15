if __name__ == '__main__':
    index = int(input('Enter the index of the input file: '))
    f = open(f'data/s_and_c-input_{index}.csv')
    lines = [line.strip(",\n").split(", ") for line in f.readlines()]
    f.close()

    print(lines)
