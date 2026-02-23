def depth_first_traverse(graph, start):
    # depth first traverse/ search first looks through each node's child node's till no further path exists
    # its is achieved by stach as it provides LIFO ; In python, we can use list and do appen() & pop() or remove(last_item)
    dft_stack = [start]
    while len(dft_stack) > 0:
        current_node = dft_stack.pop() # or could use .remove(last_item) #-1
        print(current_node)
        for n in graph[current_node]:
            dft_stack.append(n)



graph = {
    'a': ['b', 'c'],
    'b': [],
    'c': ['e', 'f'],
    'd': [],
    'e': ['d', 'g'],
    'f': ['h'],
    'g': [],
    'h': ['j'],
    'i': [],
    'j': ['i']
}

depth_first_traverse(graph, 'a')





