def cap2(s):
    #print(s)
    if s!='' and s[0].isalpha() and ord(s[0])>96  and ord(s[0])<123:
        ns = list(s)
        ns[0] = chr( ord(s[0]) - 32)
        #print(s, ns)
        return ''.join(ns)
    else:
        return s

def solve(s):

    #return ' '.join(list(map(cap1, s.split(' '))))
    print( ' '.join(list(map(cap2, s.strip().split(' ')))) )
  
solve('132 456 Wq  m e')