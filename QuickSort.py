from random import randrange, sample
import cProfile

numbers = list()

# 10 mil
for i in range(0, 10000):
    int = randrange(0,100000)
    numbers.append(int)


def partition(lst, start, end, pivot):
    lst[pivot], lst[end] = lst[end], lst[pivot]
    store_index = start
    for i in range(start, end):
        if lst[i] > lst[end]:
            lst[i], lst[store_index] = lst[store_index], lst[i]
            store_index += 1
    lst[store_index], lst[end] = lst[end], lst[store_index]
    return store_index


def quick_sort(lst, start, end):
    if start >= end:
        return lst
    pivot = randrange(start, end + 1)
    new_pivot = partition(lst, start, end, pivot)
    quick_sort(lst, start, new_pivot - 1)
    quick_sort(lst, new_pivot + 1, end)

def sort(lst):
    quick_sort(lst, 0, len(lst) - 1)
    return lst

pr = cProfile.Profile()
pr.enable()
    

sort(numbers)
# sorted(numbers)

pr.disable()
pr.print_stats()