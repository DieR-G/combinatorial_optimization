from functools import reduce

def gcd(a,b):
    if(b == 0):
        return abs(a)
    else:
        return gcd(b, a % b)

def validate(c):
    if c[0] < 0 and c[1] < 0:
        c = (abs(c[0]), abs(c[1]))
    g = gcd(abs(c[0]), abs(c[1]))
    d = (c[0]//g,c[1]//g)
    return d

def fraction(a,b):
    if a == 0:
        return (0,1)
    c = (a,b)
    return validate(c)

def identity(n):
    mat = [[(0,1)]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if(i == j):
                mat[i][j] = (1,1)
    return mat

def div(a, b):
    c = (a[0]*b[1], a[1]*b[0])
    return validate(c)
    
def mult(a,b):
    c = (a[0]*b[0], a[1]*b[1])
    return validate(c)

def sub(a,b):
    c = (a[0]*b[1]-b[0]*a[1], a[1]*b[1])
    return validate(c)

def sum_f(a,b):
    c = (a[0]*b[1]+b[0]*a[1], a[1]*b[1])
    return validate(c)

#A - B
def sub_mat(A, B):
    m = len(A)
    n = len(A[0])
    c = [[(0,1)] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            c[i][j] = sub(A[i][j], B[i][j])
    return c

#A is mxn and B is nxm
def mult_mat(A, B):
    m = len(A)
    n = len(B[0])
    c = [[(0,1)] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(m):
                c[i][j] = sum_f(c[i][j], mult(A[i][k],B[k][j]))
    return c

def eliminate(r1, r2, col, target=(0,1)):
    fac = div(sub(r2[col],target), r1[col])
    for i in range(len(r2)):
        r2[i] = sub(r2[i], mult(fac, r1[i]))

def gauss(a):
    for i in range(len(a)):
        if a[i][i] == (0,1):
            for j in range(i+1, len(a)):
                if a[i][j] != (0,1):
                    a[i], a[j] = a[j], a[i]
                    break
            else:
                raise ValueError("Matrix is not invertible")
        for j in range(i+1, len(a)):
            eliminate(a[i], a[j], i)
    for i in range(len(a)-1, -1, -1):
        for j in range(i-1, -1, -1):
            eliminate(a[i], a[j], i)
    for i in range(len(a)):
        eliminate(a[i], a[i], i, target=(1,1))
    return a

def inverse(a):
    tmp = [[] for _ in a]
    for i,row in enumerate(a):
        assert len(row) == len(a)
        tmp[i].extend(row + [(0,1)]*i + [(1,1)] + [(0,1)]*(len(a)-i-1))
    gauss(tmp)
    return [tmp[i][len(tmp[i])//2:] for i in range(len(tmp))]

def is_final(r):
    for x in r:
        if x != (0,1):
            return False
    return True

def fraction_list(p):
    numerators = []
    denominators = []
    for x in p:
        numerators.append(x[0])
        denominators.append(x[1])
    list_lcm = reduce(lambda x,y: x*y//gcd(x,y), denominators)
    for i in range(len(numerators)):
        numerators[i] = numerators[i]*list_lcm // denominators[i]
    numerators.append(list_lcm)
    return numerators

def solution(m):
    n = len(m)
    if n==1:
        if len(m[0]) == 1 and m[0][0] == 0:
            return [1, 1]
    transient = []
    final = []
    for i in range(n):
        denom = sum(m[i])
        for j in range(n):
            m[i][j] = fraction(m[i][j], denom)
    for i in range(n):
        if is_final(m[i]):
            final.append(i)
        else:
            transient.append(i)
    r = len(transient)
    s = len(final)
    Q = [[(0,1)]*r for _ in range(r)]
    R = [[(0,1)]*s for _ in range(r)]
    for i in range(r):
        for j in range(r):
            Q[i][j] = m[transient[i]][transient[j]]
        for j in range(s):
            R[i][j] = m[transient[i]][final[j]]
    F = mult_mat(inverse(sub_mat(identity(r), Q)), R)
    return fraction_list(F[0])

print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))