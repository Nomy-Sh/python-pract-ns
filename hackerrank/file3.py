#hackerrank
#
# Something wrong woth problem statement, does not work

def dynamicArray(n, queries):
    # Write your code here
    last_answer = 0
    arr = [ [] for i in range(n)]
    answer_arr = []

    for query in queries:
        q, x, y = query

        idx = (x^last_answer)%2
        
        if q == 1:
            #query 1
            arr[idx].append(y)
            print(idx, y)
        elif q == 2:
            #query 2
            last_answer = arr[idx][y%n]
            print(idx, arr[idx], last_answer)
            answer_arr.append(last_answer)

    return answer_arr

# first_multiple_input = input().rstrip().split()

# n = int(first_multiple_input[0])

# q = int(first_multiple_input[1])

# queries = []

# for _ in range(q):
#     queries.append(list(map(int, input().rstrip().split())))

n = 2
queries = [[1,0,5],[1,1,7],[1,0,3],[2,1,0],[2,1,1]]

result = dynamicArray(n, queries)
print(result)
