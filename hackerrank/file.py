def octal(dec_n):
   #return (str(dec_n // 8)+str(dec_n % 8)).lstrip('0')
   q = 1
   dd = dec_n
   ds = 8
   rem = []
   while q != 0:
      q = dd // ds
      rem.append(dd % ds)
      dd = q
   #print(rem)
   return ''.join((map(str, rem[::-1]))) 


def hexa(dec_n):
   hex_arr = [i for i in range(10)]
   hex_arr += ['A', 'B', 'C', 'D', 'E', 'F']
   #print("hex_arr: ", hex_arr)
   return (str(hex_arr[dec_n // 16])+str(hex_arr[dec_n % 16])).lstrip('0')

def binary(dec_n):
   return bin(dec_n).replace('0b', '').lstrip('0')

def print_formatted(number):
   # your code goes here
   for i in range(1, number+1):
      space = len(binary(number))
      print(str(i).rjust(space) + ' ' + octal(i).rjust(space) + ' ' + hexa(i).rjust(space) + ' ' + binary(i).rjust(space))


if __name__ == '__main__':
   number = int(input("Enter decimal number:- "))
   print_formatted(number)
   # print(octal(int(dec_n)))
   # print(hexa(int(dec_n)))


#octal(int(input("octal - ")))
