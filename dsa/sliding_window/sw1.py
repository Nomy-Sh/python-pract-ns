# Length of longest sub string in a given substring
# Approach sliding window for O(n) runtime
# AI code -> for learning

def lengthOfLongestSubstring(s: str) -> int:
    last_seen = {}
    left = 0
    max_length = 0

    print(s)
    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        max_length = max(max_length, right - left + 1)

        #print(f"char {char}, left {left}, right {right}, max_length {max_length} max(max_length, right-left+1), last_item_hash {last_seen}")

    return max_length

print('\n', '*'*20, '\n')
lengthOfLongestSubstring(s = 'abba')

print('\n', '*'*20, '\n')

lengthOfLongestSubstring(s = 'abcbac')
print('\n', '*'*20, '\n')