# Length of longest sub string in a given substring
# Approach sliding window for O(n) runtime
# My code -> after learning

def lengthMaxSubString(s: str)-> int:
    # abcabdds # ppprpef
    last_item = dict()
    left = 0
    max_length = 0

    for right, char in enumerate(s):
        if char in last_item and last_item[char] >= left:
            left = last_item[char] + 1

        last_item[char] = right
        max_length = max(max_length, right - left + 1)
    print(last_item, max_length)
    return max_length

lengthMaxSubString('abcabdds')