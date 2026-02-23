

TOTAL_HOURS = 40

print('''This program will help you convert your daily hours worked to time percent.
Total hours is by default considered as 8x5= 40 hours.
Enter your work hours space separated values.
''')

daily_work_hours = list(map(int, input('Enter space separated values\n=>').strip().split(' ')))


def percent_calc(daily_work_hours):
   obj = {}
   for hour in daily_work_hours:
      obj[str(hour)] = (100/TOTAL_HOURS)*hour
   return obj

print("Your values sum up to ", sum(daily_work_hours))
percent_hours = percent_calc(daily_work_hours)

print(percent_hours, '\nPercent hours sum up to ', sum( list( percent_hours.values() ) ), '%')




