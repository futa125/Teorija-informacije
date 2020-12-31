import numpy as np
import math


def input_larger_than(message, lower_limit):
    while True:
        try:
            data = int(input(message))
            if data >= lower_limit:
                return data
            else:
                print("Incorrect input!")
        except ValueError:
            print("Incorrect input!")
            continue


def input_one_or_zero():
    while True:
        try:
            data = int(input("Enter 0 or 1: "))
            if data == 0 or data == 1:
                return data
            else:
                print("Incorrect input!")
        except ValueError:
            print("Incorrect input!")
            continue


def input_matrix(rows, columns):
    print("Input the elements of your generator matrix (left to right, top to bottom):")
    return np.array([[int(input_one_or_zero()) for _x in range(columns)] for _y in range(rows)])


def has_identity_matrix(k, generator_matrix):
    for i in range(k):
        for j in range(k):
            if (i != j and generator_matrix[i][j] != 0) or (i == j and generator_matrix[i][j] != 1):
                return False

    return True


def has_standard_form(generator_matrix):
    rows = generator_matrix.shape[0]
    for i in range(rows):
        if all(x == 0 for x in generator_matrix[i]):
            return False

    for i in range(rows):
        for j in range(rows):
            if i != j and np.array_equal(generator_matrix[i], generator_matrix[j]):
                return False

    return True


def get_standard_form(generator_matrix):
    matrix = np.array(generator_matrix)
    rows, cols = matrix.shape
    raw_rows = list(np.arange(rows))

    while raw_rows:
        position = raw_rows[0]

        if matrix[position, position] == 0:

            row_swap = check_col(matrix, position)
            if row_swap != -1:
                matrix[[position, row_swap]] = matrix[[row_swap, position]]

            else:
                col_swap = get_col_swap(matrix, position)
                matrix[:, [position, col_swap]] = matrix[:, [col_swap, position]]

        for i in range(rows):
            if matrix[i, position] == 1 and i != position:
                matrix[i, :] = matrix[i, :] - matrix[position, :]
        matrix = np.where(matrix == -1, 1, matrix)
        raw_rows.pop(0)

    return matrix


def check_col(matrix, col):
    rows = matrix.shape[0]
    for i in range(col, rows):
        if matrix[i][col] == 1:
            return i
    return -1


def get_col_swap(matrix, row):
    cols = matrix.shape[1]
    for i in range(row, cols):
        if matrix[row][i] == 1:
            return i


def get_codes(matrix, k, n):
    output = []
    matrix = ["".join(item) for item in matrix.astype(str)]

    for i in range(2 ** k):
        tmp = i - 2 ** k
        code = 0
        for j in range(k):
            code = code ^ (((tmp & (1 << j)) >> j) * int(matrix[j], 2))
        output.append([format(code, "0" + str(n) + "b")])

    return np.array(output)


def is_linear(codes, n):
    if ("0" * n) not in codes:
        return False

    for i in range(len(codes)):
        for j in range(len(codes)):
            if format((int(codes[i][0], base=2) ^ int(codes[j][0], base=2)), "0" + str(n) + "b") not in codes:
                return False

    return True


def hamming_distance(x, y, n):
    ans = 0
    for i in range(n - 1, -1, -1):
        ans += not (x >> i & 1 == y >> i & 1)
    return ans


def is_perfect(codes, k, n):
    _min = n

    for i in range(len(codes)):
        for j in range(len(codes)):
            if i != j and hamming_distance(int(codes[i][0], base=2), int(codes[j][0], base=2), n) < _min:
                _min = hamming_distance(int(codes[i][0], base=2), int(codes[j][0], base=2), n)

    t = math.floor((_min - 1) / 2)
    tmp_sum = 0

    for i in range(t + 1):
        tmp_sum += math.factorial(n) / (math.factorial(i) * math.factorial(n - i))

    return 2 ** k == 2 ** n / tmp_sum


def code_efficiency(k, n):
    return k / n


def encode_message(k, n, generator_matrix):
    message = []
    print("Enter your message: ")

    for _ in range(k):
        message.append(input_one_or_zero())

    message = np.dot(np.array(message), generator_matrix)
    for i in range(n):
        message[i] %= 2

    return message


def main():
    rows = input_larger_than("Enter number of rows: ", 1)
    print()
    columns = input_larger_than("Enter number of columns: ", rows + 1)
    print()

    print("For this code k is {} and n is {}!".format(rows, columns))
    print()

    generator_matrix = input_matrix(rows, columns)
    print()
    print("Here is the generator matrix: ")
    print(generator_matrix)
    print()

    if has_identity_matrix(rows, generator_matrix):
        print("This generator matrix is already in standard form!")
    else:
        print("This generator matrix is not in standard form, lets try to fix that!")
        print()
        if not has_standard_form(generator_matrix):
            raise Exception("The matrix you have entered is not valid!")
        else:
            print(get_standard_form(generator_matrix))
    print()

    codes = get_codes(generator_matrix, rows, columns)
    print("Here are all the codes: ")
    print(codes)
    print()

    print("This code is linear!") if is_linear(codes, columns) else print("This code is not linear!")
    print()

    print("This code is perfect!") if is_perfect(codes, rows, columns) else print("This code is not perfect!")
    print()

    print("The efficiency of this code is: {:.2f}%".format(code_efficiency(rows, columns) * 100))
    print()

    encoded_message = encode_message(rows, columns, generator_matrix)
    print()
    print("Your message was encoded as: {}".format(encoded_message))


if __name__ == "__main__":
    main()
