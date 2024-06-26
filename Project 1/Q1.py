from math import inf


class LPSolver(object):
    EPS = 1e-9
    NEG_INF = -inf

    def __init__(self, A, b, c):
        self.m = len(b)
        self.n = len(c)
        self.N = [0] * (self.n + 1)
        self.B = [0] * self.m
        self.D = [[0 for i in range(self.n + 2)] for j in range(self.m + 2)]
        for i in range(self.m):
            for j in range(self.n):
                self.D[i][j] = A[i][j]
        for i in range(self.m):
            self.B[i] = self.n + i
            self.D[i][self.n] = -1
            self.D[i][self.n + 1] = b[i]
        for j in range(self.n):
            self.N[j] = j
            self.D[self.m][j] = -c[j]
        self.N[self.n] = -1
        self.D[self.m + 1][self.n] = 1

    def matmul(self, a, b):
        out = [[0 for row in range(len(b[0]))] for col in range(len(a))]
        for i in range(len(a)):
            for j in range(len(b[0])):
                for k in range(len(a[0])):
                    out[i][j] += a[i][k] * b[k][j]
        return out

    def get_by_indice(self, a, start_row, end_row, start_col, end_col):
        out = [[a[col][row] for row in range(
            start_col, end_col)] for col in range(start_row, end_row)]
        return out

    def sub(self, a, b):
        for i in range(len(a)):
            for j in range(len(a[i])):
                a[i][j] -= b[i][j]
        return a

    def pivot(self, r, s):
        D = self.D
        B = self.B
        N = self.N
        inv = 1.0 / D[r][s]
        dec_mat = self.matmul(self.get_by_indice(
            D, 0, len(D), s, s+1), self.get_by_indice(D, r, r+1, 0, len(D[0])))
        for i in range(len(dec_mat)):
            for j in range(len(dec_mat[i])):
                dec_mat[i][j] *= inv
        for i in range(len(dec_mat[r])):
            dec_mat[r][i] = 0
        for i in range(len(dec_mat)):
            dec_mat[i][s] = 0
        self.D = self.sub(self.D, dec_mat)
        for i in range(s):
            self.D[r][i] *= inv
        for i in range(s+1, len(self.D[0])):
            self.D[r][i] *= inv
        for i in range(r):
            self.D[i][s] *= -inv
        for i in range(r+1, len(D)):
            self.D[i][s] *= -inv
        self.D[r][s] = inv
        B[r], N[s] = N[s], B[r]

    def simplex(self, phase):
        m = self.m
        n = self.n
        D = self.D
        B = self.B
        N = self.N
        x = m + 1 if phase == 1 else m
        while True:
            s = -1
            for j in range(n + 1):
                if phase == 2 and N[j] == -1:
                    continue
                if s == -1 or D[x][j] < D[x][s] or D[x][j] == D[x][s] and N[j] < N[s]:
                    s = j
            if D[x][s] > -self.EPS:
                return True
            r = -1
            for i in range(m):
                if D[i][s] < self.EPS:
                    continue
                if r == -1 or D[i][n + 1] / D[i][s] < D[r][n + 1] / D[r][s] or (D[i][n + 1] / D[i][s]) == (D[r][n + 1] / D[r][s]) and B[i] < B[r]:
                    r = i
            if r == -1:
                return False
            self.pivot(r, s)

    def solve(self):
        m = self.m
        n = self.n
        D = self.D
        B = self.B
        N = self.N
        r = 0
        for i in range(1, m):
            if D[i][n + 1] < D[r][n + 1]:
                r = i
        if D[r][n + 1] < -self.EPS:
            self.pivot(r, n)
            if not self.simplex(1) or D[m + 1][n + 1] < -self.EPS:
                return self.NEG_INF, None
            for i in range(m):
                if B[i] == -1:
                    s = -1
                    for j in range(n + 1):
                        if s == -1 or D[i][j] < D[i][s] or D[i][j] == D[i][s] and N[j] < N[s]:
                            s = j
                    self.pivot(i, s)
        if not self.simplex(2):
            return self.NEG_INF, None
        x = [0] * self.n
        for i in range(m):
            if B[i] < n:
                x[B[i]] = round(D[i][n + 1], 9)
        return round(D[m][n + 1], 9), x


# def find_nash_equilibrium_row(matrix1, matrix2, num_rows, num_cols):
#     payoff_matrix1 = [[row[i] for row in matrix1]
#                       for i in range(len(matrix1[0]))]
#     payoff_matrix2 = matrix2
#     # Create the payoff matrix for the linear program
#     A_ub = []
#     b_ub = []

#     A_ub = [[1 for i in range(num_cols)]]
#     A_ub.append([-1 for i in range(num_cols)])

#     for i in range(num_rows):
#         A_ub.append([-1 if i == j else 0 for j in range(num_cols)])
#     b_ub.append(1)
#     b_ub.append(-1)
#     for i in range(num_cols):
#         b_ub.append(0)
#     solved = []
#     for k in range(num_rows):
#         c = [1 * payoff_matrix1[k][i] for i in range(num_cols)]
#         solver = LPSolver(A_ub, b_ub, c)
#         solved.append(solver.solve())
#     min
#     return solved


# def find_nash_equilibrium(matrix1, matrix2, num_rows, num_cols):
#     solved = find_nash_equilibrium_row(matrix1, matrix2, num_rows, num_cols)
#     print(solved)


def find_nash_equilibrium(matrix1, matrix2, num_rows, num_cols, row_start, col_start, tuple):
    # Create the payoff matrix for the linear program
    flag = 1
    i = row_start
    m = col_start
    A_ub = []
    b_ub = []
    c = [1 for i in range(num_rows+num_cols)]
    A_ub = [
        [1 if i < num_rows else 0 for i in range(num_rows+num_cols)]]
    b_ub.append(1)
    A_ub.append(
        [1 if i >= num_rows else 0 for i in range(num_rows+num_cols)])
    b_ub.append(1)
    A_ub.append(
        [-1 if i < num_rows else 0 for i in range(num_rows+num_cols)])
    b_ub.append(-1)
    A_ub.append(
        [-1 if i >= num_rows else 0 for i in range(num_rows+num_cols)])
    b_ub.append(-1)
    for k in range(num_rows+num_cols):
        A_ub.append(
            [-1 if k == j else 0 for j in range(num_rows+num_cols)])
        b_ub.append(0)

    for j in range(num_cols):
        if j != i:
            if tuple[j+num_rows] == 1:
                A_ub.append([-matrix2[k][i] + matrix2[k][j] if k <
                            num_rows else 0 for k in range(num_rows+num_cols)])
                A_ub.append([matrix2[k][i] - matrix2[k][j] if k <
                            num_rows else 0 for k in range(num_rows+num_cols)])
                b_ub.append(0)
                b_ub.append(0)
            else:
                A_ub.append([-matrix2[k][i] + matrix2[k][j] if k <
                            num_rows else 0 for k in range(num_rows+num_cols)])
                b_ub.append(0)
                A_ub.append(
                    [1 if k == j+num_rows else 0 for k in range(num_rows+num_cols)])
                b_ub.append(0)

    for j in range(num_rows):
        if m != j:
            # print("j = {}".format(j))
            if tuple[j] == 1:
                A_ub.append([-matrix1[m][k-num_rows] + matrix1[j][k-num_rows] if k >= num_rows else 0
                            for k in range(num_cols+num_rows)])
                A_ub.append([matrix1[m][k-num_rows] - matrix1[j][k-num_rows] if k >= num_rows else 0
                            for k in range(num_cols+num_rows)])
                b_ub.append(0)
                b_ub.append(0)
            else:
                A_ub.append([-matrix1[m][k-num_rows] + matrix1[j][k-num_rows] if k >= num_rows else 0
                            for k in range(num_cols+num_rows)])
                b_ub.append(0)
                A_ub.append(
                    [1 if k == j else 0 for k in range(num_cols+num_rows)])
                b_ub.append(0)
    # print("A_ub:")
    # print(A_ub)
    # print("b_ub:")
    # print(b_ub)
    solver = LPSolver(A_ub, b_ub, c)
    solved = solver.solve()
    # print("solved: ", solved)
    return solved


def find_nash_equilibrium_all(matrix1, matrix2, num_rows, num_cols):
    for i in range(0, 2**num_rows, 1):
        # print("i: ", i)
        # print(num_cols)
        for j in range(0, 2**num_cols, 1):
            # print("j: ", j)
            # cast i to binary
            binary_i = bin(i)[2:]
            binary_j = bin(j)[2:]
            # fill the binary number with 0s
            binary_i = "0" * (num_rows - len(binary_i)) + binary_i
            binary_j = "0" * (num_cols - len(binary_j)) + binary_j
            # find first 1 in the binary number
            my_j = binary_i.find("1")
            my_k = binary_j.find("1")
            tuple = [int(i) for i in binary_i] + [int(i) for i in binary_j]
            # print("tuple: ", tuple)
            # print("tuple: ", tuple)
            solved = find_nash_equilibrium(
                matrix1, matrix2, num_rows, num_cols, my_k, my_j, tuple)
            if solved[0] != -inf:
                # print("j = {}, k = {}".format(my_j, my_k))
                # print("tuple: ", tuple)
                # print("solved: ", solved[1])
                x = solved[1]
                # take absolute value of the output
                x = [abs(i) for i in x]
                # make the output to 6 decimal places
                for i in range(num_rows):
                    print("{:.6f}".format(x[i]), end=" ")
                print()
                for i in range(num_cols):
                    print("{:.6f}".format(x[num_rows+i]), end=" ")

                # Exit the program
                return
                # print()
                # print()

                # Read the reward matrices siza from the console
num_rows, num_cols = map(int, input().split())

# Read payoff matrix 1 from the console
matrix1 = []
for i in range(num_rows):
    matrix1.append(list(map(int, input().split())))

# Read payoff matrix 2 from the console
matrix2 = []
for i in range(num_rows):
    matrix2.append(list(map(int, input().split())))


# Find the Nash equilibrium
find_nash_equilibrium_all(matrix1, matrix2, num_rows, num_cols)
# find_nash_equilibrium(matrix1, matrix2, num_rows,
#                       num_cols, 0, 0, [1, 1, 0, 1, 1])
