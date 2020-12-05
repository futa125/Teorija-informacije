import numpy as np
import math
import sympy


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
    return np.array([[int(input_one_or_zero()) for x in range(columns)] for y in range(rows)])

def has_identity_matrix(k, generator_matrix):
    for i in range(k):
        for j in range(k):
            if (i != j and generator_matrix[i][j] != 0) or (i == j and generator_matrix[i][j] != 1):
                return False

    return True

def has_standard_form(generator_matrix, k):
    output_matrix = sympy.Matrix(generator_matrix)
    output_matrix = output_matrix.rref()
    return len(output_matrix[1]) == k

def get_standard_form(generator_matrix):
    output_matrix = sympy.Matrix(generator_matrix)
    output_matrix = output_matrix.rref()
    output_matrix = np.array(output_matrix[0])

    return np.where(output_matrix == -1, 1, output_matrix)

def get_codes(matrix, k, n):
    output = []
    matrix = ["".join(item) for item in matrix.astype(str)]
    
    for i in range(2**k):
        tmp = i - 2**k
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
        ans += not(x>>i&1 == y>>i&1)
    return ans

def is_perfect(codes, k, n):   
    min = n
    
    for i in range(len(codes)):
        for j in range(len(codes)):
            if i != j and hamming_distance(int(codes[i][0], base=2), int(codes[j][0], base=2), n) < min:
                min = hamming_distance(int(codes[i][0], base=2), int(codes[j][0], base=2), n)
    
    t = math.floor((min - 1) / 2)
    tmp_sum = 0

    for i in range(t + 1):
        tmp_sum += math.factorial(n) / (math.factorial(i) * math.factorial(n - i))

    return 2**k == 2**n / tmp_sum

def code_efficiency(k, n):
    return k/n

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
        if has_standard_form(generator_matrix, rows):
            print(get_standard_form(generator_matrix))
        else:
            raise Exception("The matrix you have entered is not valid!")
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