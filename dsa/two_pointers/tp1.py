# DSA
# This is a two pointers example -> 
## Two pointers, as names suggests uses 2 pointers to run through a string or list or some kind of iterable
##

# To check whether a string a PALINDROME or not
# Ignore these chars ['!', '/', '@', '#', '$', '%', '^', '&', '*', '(', ')']
# Ignore cases sensitivity
##


#INGORE_CHARS = ['!', '/', '@', '#', '$', '%', '^', '&', '*', '(', ')']

class PalindromeFinder:
    def __init__(self, ignore_chars=None):
        self.INGORE_CHARS = ignore_chars if ignore_chars else None

    def check(self, inp_string=''):
        if not inp_string:
            return False

        l, r = 0, len(inp_string)-1
        while l < r:
            while l < r and  inp_string[l] in self.INGORE_CHARS:
                l+=1
            while l<r and inp_string[r] in self.INGORE_CHARS:
                r-=1
            if inp_string[l].lower() != inp_string[r].lower():
                return False
            l+=1
            r-=1
        return True

ignore_chars = ['!', '/', '@', '#', '$', '%', '^', '&', '*', '(', ')', ' ']

p = PalindromeFinder(ignore_chars=ignore_chars)
print(p.check(inp_string=input('ENter your string - ')))

# NO!MO!MO !N
# 0123456789A