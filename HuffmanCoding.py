from collections import Counter

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.right = right
        self.left = left


def get_code(root: Node, code_dict=None, code=""):
    if code_dict is None:
        code_dict = dict()
    if root is None:
        return

    if isinstance(root.value, str):
        code_dict[root.value] = code
        return code_dict

    get_code(root.left, code_dict, code + "0")
    get_code(root.right, code_dict, code + "1")

    return code_dict


def get_tree(string: str) -> Node:
    string_count = Counter(string)

    if len(string_count) <= 1:
        node = Node(None)

        if len(string_count) == 1:
            node.left = Node([key for key in string_count][0])
            node.right = Node(None)

        string_count = {node: 1}

    while len(string_count) != 1:
        node = Node(None)
        spam = string_count.most_common()[:-3:-1]

        if isinstance(spam[0][0], str):
            node.left = Node(spam[0][0])

        else:
            node.left = spam[0][0]

        if isinstance(spam[1][0], str):
            node.right = Node(spam[1][0])

        else:
            node.right = spam[1][0]

        del string_count[spam[0][0]]
        del string_count[spam[1][0]]
        string_count[node] = spam[0][1] + spam[1][1]

    return [key for key in string_count][0]


def encoder(string: str, code_dict: dict) -> str:
    result = ""

    for symbol in string:
        result += code_dict[symbol]

    return result


def decode(string: str, code_dict: dict) -> str:
    res = ""
    i = 0

    while i < len(string):
        for code in code_dict:
            if string[i:].find(code_dict[code]) == 0:
                res += code
                i += len(code_dict[code])

    return res

if __name__ == '__main__':

    with open("input_file.txt", "r") as file:
        my_string = "".join(file)
    tree = get_tree(my_string)

    # with open("output_file.bin", "wb") as file:
    #     file.write("abc".encode())
        # s = "abc".encode()
    # print(s)

    codes = get_code(tree)
    print(f"Шифр: {codes}")

    coding_str = encoder(my_string, codes)
    with open("output_file.bin", "wb") as file:
        coding_str_bin = struct.pack('!l', int(coding_str, 2))
        # file.write(coding_str.encode())
        file.write(coding_str_bin)
        # file.write(bytes(coding_str, encoding='utf-8'))
    print("Сжатая строка: ", coding_str)


    decoding_str = decode(coding_str, codes)
    print("Исходная строка: ", decoding_str)

