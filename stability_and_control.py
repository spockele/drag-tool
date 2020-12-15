if __name__ == '__main__':
    f = open('data/stability_and_control_sample_input.csv')
    lines = [line.strip(",\n").split(", ") for line in f.readlines()]
    f.close()

    print(lines)
