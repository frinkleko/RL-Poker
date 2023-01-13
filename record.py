def load_dict():
    with open('record.dat', 'r') as f:
        dict = {}
        for i in f.readlines():
            info = i.replace('\n', '').split('\t')
            label = '\t'.join(info[:3])
            dict[label] = int(info[-1])
        return dict


def write_file(dict):
    with open('record.dat', 'w') as f:
        for k in dict.keys():
            f.write(k)
            f.write('\t')
            f.write(str(dict[k]))
            f.write('\n')


def print_info():
    with open('record.dat', 'r') as f:
        print("Matchups:")
        print("----------------------")
        for i, info in enumerate(f.readlines()):
            info = info.replace('\n', '').split('\t')
            print("Round" + str(i) + ":", "Computer: " + info[0], "Player: " + info[1], "Game result: " + info[2],
                  "times: " + info[3])


if __name__ == 'main':
    test_dict = {
        'F\tF\t1': 3,
        'W\tW\t0': 1
    }
    write_file(test_dict)
    print_info()
    dict = load_dict()
    print(dict)
