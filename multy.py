#!/usr/bin/python3

import random
import os
import sys
import time

from operator import itemgetter

LONG_TIME = 8

def stat_info(total_errors, errors, long_time_results):
   errors_text = ''
   for a, b in sorted(errors, key=itemgetter(0,1)):
      if errors_text:
         errors_text += ', '
      errors_text += f'{a}x{b}'
   if errors_text:
      errors_text = f' ({errors_text})'
   print(f'Число примеров с ошибками: ' + str(total_errors) + errors_text)
   if not long_time_results:
      return
   print(f'Ответы с задержкой более {LONG_TIME} секунд:')
   for a, b, seconds in sorted(long_time_results, key=itemgetter(0,1,2)):
      print(f'{a}x{b}: {seconds} сек')


if len(sys.argv) > 1:
   check = sys.argv[1:]
else:
   check = input('На какие числа проверяем умножение (через пробел): ').split(' ')

all_variants = []
for value in check:
   if not value.isdigit():
      print('Не поддерживаемое значение: ' + value)
      exit(1)
   value = int(value)
   for n in range(2,10):
      if (n, value) not in all_variants:
         all_variants.append((value, n))


random.shuffle(all_variants)

total_errors = 0
errors = set()
long_time_results = []
while all_variants:
   a, b = all_variants.pop(0)
   bad_found = False
   os.system('cls' if os.name == 'nt' else 'clear')
   start_time = time.time()
   while True:
      try:
         result = input(f'{a} x {b} = ')
      except KeyboardInterrupt:
         print()
         stat_info(total_errors, errors, long_time_results)
         exit()
      if result.isdigit() and int(result) == a * b:
         if bad_found:
            total_errors += 1
            all_variants.append((a, b))
            errors.add((a, b))
         elif time.time() - start_time > LONG_TIME:
            long_time_results.append((a, b, round(time.time() - start_time)))
         break
      print(f'Не правильно. Попробуй еще раз!')
      bad_found = True

stat_info(total_errors, errors, long_time_results)


