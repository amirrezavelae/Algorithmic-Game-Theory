from math import inf
from math import floor


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


def find_correlated_nash_equilibrium(matrix1, matrix2, num_rows, num_cols, eshg1, eshg2):
    payoff_matrix1 = [[eshg1 * cell for cell in row] for row in matrix1]
    payoff_matrix2 = [[eshg2 * cell for cell in row] for row in matrix2]
    C = []
    b_ub = []
    for i in range(num_rows):
        for j in range(num_cols):
            C.append(payoff_matrix1[i][j]+payoff_matrix2[i][j])
    A_ub = [[1 for i in range(num_rows * num_cols)]]
    b_ub.append(1)
    A_ub.append([-1 for i in range(num_rows * num_cols)])
    b_ub.append(-1)
    for i in range(num_cols):
        for j in range(num_rows):
            A_ub.append([-1 if i*num_rows + j ==
                        k else 0 for k in range(num_rows * num_cols)])
            b_ub.append(0)
    for i in range(num_rows):
        for j in range(num_rows):
            if i == j:
                continue
            # print("i: ", i)
            JJJJ = [matrix1[j][k % num_cols] if floor(k / num_cols) <= i and floor(k / num_cols) >
                    i - 1 else 0 for k in range(num_rows * num_cols)]
            KKKK = [matrix1[i][k % num_cols] if floor(k / num_cols) <= i and floor(k / num_cols) >
                    i - 1 else 0 for k in range(num_rows * num_cols)]
            # print("JJJJ: ", JJJJ)
            # print("KKKK: ", KKKK)ً

            A_ub.append(subtract_lists(JJJJ, KKKK))
            b_ub.append(0)
    for i in range(num_cols):
        for j in range(num_cols):
            if i == j:
                continue
            JJJJ = [matrix2[floor(k / num_cols)][j] if k % num_cols <= i and k %
                    num_cols > i - 1 else 0 for k in range(num_rows * num_cols)]
            KKKK = [matrix2[floor(k / num_cols)][i] if k % num_cols <= i and k %
                    num_cols > i - 1 else 0 for k in range(num_rows * num_cols)]

            # print("JJJJ: ", JJJJ)
            # print("KKKK: ", KKKK)
            A_ub.append(subtract_lists(JJJJ, KKKK))
            b_ub.append(0)
    # print("C: ", C)
    # print("A_ub: ", A_ub)
    # print("b_ub: ", b_ub)

    solved = LPSolver(A_ub, b_ub, C)
    print("{:.6f}".format(solved.solve()[0]))
    x = solved.solve()[1]
    for i in range(num_rows):
        for j in range(num_cols):
            print("{:.6f}".format(x[i*num_cols + j]), end=" ")
        print()


def slice_even_odd_columns(matrix):
    even_columns = [row[::2] for row in matrix]
    odd_columns = [row[1::2] for row in matrix]
    return even_columns, odd_columns


def subtract_lists(list1, list2):
    return [a - b for a, b in zip(list1, list2)]


# Read 2 floating point numbers
eshg1, eshg2 = map(float, input().split())
num_rows, num_cols = map(int, input().split())

# print(eshg1)
total_matrix = []
for i in range(num_rows):
    total_matrix.append(list(map(int, input().split())))

matrix1, matrix2 = slice_even_odd_columns(total_matrix)
# print("matrix1: ", matrix1)
# print("matrix2: ", matrix2)


# Find the Nash equilibrium
find_correlated_nash_equilibrium(
    matrix1, matrix2, num_rows, num_cols, eshg1, eshg2)
