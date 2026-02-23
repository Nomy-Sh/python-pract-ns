


def breadth_first_traverse(graph, start):
    # breadth first traverse/search travels on each breadth/ neighbours first
    # It uses queue to achieve this , as queue provides FIFO
    bft_queue = [start]

    while len(bft_queue) > 0:
        current_node = bft_queue[0]
        bft_queue.remove(current_node)
        print(current_node)
        for n in graph[current_node]:
            bft_queue.append(n)


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

breadth_first_traverse(graph, 'a')





