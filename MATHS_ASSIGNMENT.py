
with open("matrix.txt","r") as f:
    a = f.read().splitlines()

for i in range(len(a)):
    l = []
    for j in a[i].split():
        l.append(float(j))
    a[i] = l


rows = len(a)
columns = len(a[0])


def scale(matrix,m,k):
    temp_matrix = matrix.copy()
    temp_matrix[m] = [round(a*k, 3) for a in matrix[m]]

    return temp_matrix


def first_non_zero(matrix):
    non_zero = []
    for sub_lst in matrix:
        for i, j in enumerate(sub_lst):
            if j != 0:
                non_zero.append(i)
                break

    return non_zero


def sort_matrix(matrix):
    temp_matrix = matrix.copy()
    non_zero = first_non_zero(matrix)

    for i, j in enumerate(non_zero):
        if temp_matrix[i][j] < 0:
            temp_matrix = scale(temp_matrix, i, -1)

    temp_matrix.sort(reverse = True)

    return temp_matrix


def add(matrix,i,j,scale):
    temp_matrix = matrix.copy()
    temp_matrix[j] = [round(y + (x * scale), 3) for (x,y) in zip(temp_matrix[i],temp_matrix[j])]
    return temp_matrix


def echelon_check(matrix):
    index = []
    for i in matrix:
        for j in i:
            if j != 0:
                index.append(i.index(j))
                break

    index.sort()
    new = []
    for i in index:
        if i not in new:
            new.append(i)
        
    if len(new) != len(index):
        return False
    else:
        return True


while not echelon_check(a):
    a = sort_matrix(a)
    non_zero = first_non_zero(a)
    for i,j in enumerate(non_zero):
        if i+1 < len(non_zero):
            k = non_zero[i+1]
            if j == k:
                a = add(a, i, i+1, -a[i+1][j]/a[i][k])
                break


non_zero = first_non_zero(a)
for i,j in enumerate(non_zero):
    a = scale(a, i, 1/a[i][j])


for i in range(len(a) - 1, -1, -1):
    for j in range(i):
        try:
            k = non_zero[i]
            a = add(a, i, j, -a[j][k])
        except IndexError:
            pass


print("\nRREF :\n")
for i in range(len(a)):
    for j in range(len(a[i])):
        if a[i][j] == -0.0:
            a[i][j] = 0.0
        print(a[i][j], end="  ")

    print("\n")


def get_parametric(matrix,non_zero):
    column_list = []
    
    for i in range(len(matrix[0])):
        l1 = []
        for j in range(len(matrix)):
            l1.append(matrix[j][i])
        column_list.append(l1)
    
    non_pivot_list = column_list[:]
    for i in column_list:
        c = 0
        for j in i:
            if j != 0 and j != 1:
                c+=1
        if c == 0:
            non_pivot_list.pop(non_pivot_list.index(i))

    pivot_index = non_zero

    main_parametric_list = []
    for i in range(len(non_pivot_list)):
        zero_list = []
        for m in range(len(matrix[0])):
            zero_list.append(0)
        try:
            for j,k in enumerate(non_pivot_list[i]):
                zero_list[pivot_index[j]] = -k
        except:
            pass
        main_parametric_list.append(zero_list)
    
    for i in range(len(main_parametric_list)):
        for j in range(len(main_parametric_list[i])):
            if main_parametric_list[i][j] == -0.0:
                main_parametric_list[i][j] = 0.0
                
    indexes = []
    for i in non_pivot_list:
        indexes.append(column_list.index(i))

    for i,j in zip(main_parametric_list,indexes):
            i[j] = 1

    return main_parametric_list,indexes


def beauty(matrix,index):
    ans = ''
    for i,j in enumerate(matrix):
        ans += "X_"+str(index[i])+"*"+str(j)+' + '
    return ans[:-2]

main,indexes = get_parametric(a,first_non_zero(a))
print("SOLUTION:")
print(beauty(main,indexes))