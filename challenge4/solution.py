# Absorbing Markov Chain
# Absorbing Probabilities: B = (I - Q)^-1 * R
# I is identity matrix (zero matrix here)
# Q is t by t matrix of probabilities between transient states
# R is t by r matrix of probabilities from transient to absorbing states

# need sort, normalize, decompose, identity, subtract, getmatrixinverse, multiply

from fractions import Fraction
#uncomment functools for python 2.7.13
# from functools import reduce


def get_lcm(a, b):
    if a > b:
        greater = a
    else:
        greater = b
    while True:
        if greater % a == 0 and greater % b == 0:
            lcm = greater
            break
        greater += 1
    return lcm


def get_lcm_list(l):
    return reduce(lambda x, y: get_lcm(x, y), l)


#number of absorbing states (full zeros)
def num_abs(m):
    for row in range(len(m)):
        for col in range(len(m[row])):
            if m[row][col] != 0:
                break
        else:
            return row
    return 0

# returns Q and R matrices
def get_q_r(m):
    t = num_abs(m)
    Q = []
    R = []

    for row in range(t):
        r = []
        for col in range(t):
            r.append(m[row][col])
        Q.append(r)

    for row in range(t):
        r = []
        for col in range(t, len(m[row])):
            r.append(m[row][col])
        R.append(r)
    return Q, R

# returns identity matrix of size t by t
def identity(t):
    m = []
    for i in range(t):
        r = []
        for j in range(t):
            r.append(int(j == i))
        m.append(r)
    return m

# swaps rows in the matrix
def swap(m, i, j):
    n = []
    size = len(m)

    if i == j:
        return m

    for row in range(size):
        r = []
        temp_r = m[row]

        if row == i:
            temp_r = m[j]
        if row == j:
            temp_r = m[i]
        for col in range(size):
            temp_c = temp_r[col]
            if col == i:
                temp_c = temp_r[j]
            if col == j:
                temp_c = temp_r[i]
            r.append(temp_c)
        n.append(r)
    return n

# sorts the matrix so all absorbing states are at the end
def sort(m):
    size = len(m)
    abs_row = -1

    for row in range(size):
        s = sum(m[row])
        if s == 0:
            abs_row = row
        if s != 0 and abs_row > -1:
            n = swap(m, row, abs_row)
            return sort(n)
    return m


def subtract(i, q):
    s = []
    for row in range(len(i)):
        s_r = []
        for col in range(len(i[row])):
            s_r.append(i[row][col] - q[row][col])
        s.append(s_r)
    return s


def multiply(a, b):
    m = []
    lens = [len(a), len(b[0]), len(a[0])]
    for row in range(lens[0]):
        m_r = []
        for col in range(lens[1]):
            sum = 0
            for i in range(lens[2]):
                sum += (a[row][i] * b[i][col])
            m_r.append(sum)
        m.append(m_r)
    return m


def normalize(m):
    n = []
    for row in range(len(m)):
        sum = 0
        cols = len(m[row])
        for col in range(cols):
            sum += m[row][col]

        n_r = []

        if sum == 0:
            n_r = m[row]
        else:
            for col in range(cols):
                n_r.append(Fraction(m[row][col], sum))
        n.append(n_r)
    return n


def transpose(m):
    t = []
    for row in range(len(m)):
        t_r = []
        for col in range(len(m[row])):
            if col == row:
                t_r.append(m[row][col])
            else:
                t_r.append(m[col][row])
        t.append(t_r)
    return t


def minor(m, x, y):
    return [row[:y] + row[y+1:] for row in (m[:x]+m[x+1:])]


def determinant(m):
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    d = 0
    for col in range(len(m)):
        d += ((-1) ** col) * m[0][col] * determinant(minor(m, 0, col))
    return d


def inverse(m):
    d = determinant(m)

    if len(m) == 2:
        return [[m[1][1]/d, -1*m[0][1]/d], [-1*m[1][0]/d, m[0][0]/d]]

    cof = []

    for row in range(len(m)):
        cof_r = []
        for col in range(len(m)):
            min = minor(m, row, col)
            cof_r.append(((-1) ** (row+col)) * determinant(min))
        cof.append(cof_r)
    cof = transpose(cof)
    for row in range(len(cof)):
        for col in range(len(cof)):
            cof[row][col] = cof[row][col]/d
    return cof

# Absorbing Probabilities: B = (I - Q)^-1 * R


def calc_probabilities(m):
    m = sort(m)
    n = normalize(m)
    (q, r) = get_q_r(n)
    i = identity(len(q))
    s = subtract(i, q)
    v = inverse(s)
    b = multiply(v, r)
    return b


def solution(m):
    #if first state is also an absorbing state
    if num_abs(m) == 0:
        return [1] + [0]*(num_abs(m)-1) + [1]
    probabilities = calc_probabilities(m)[0]
    lcm = get_lcm_list([p.denominator for p in probabilities])
    sol = []
    for p in probabilities:
        if p.numerator == 0:
            sol.append(0)
        elif p.denominator == lcm:
            sol.append(p.numerator)
        else:
            sol.append(int((lcm / float(p.denominator))*p.numerator))
    sol.append(lcm)
    return sol


print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [
      0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]))
# returns [7, 6, 8, 21]

print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [
      0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
# returns [0, 3, 2, 9, 14]
