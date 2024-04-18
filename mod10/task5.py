def find_insert_position(arr, x):
    start = 0
    end = len(arr) - 1

    while start <= end:
        mid = (start + end) // 2

        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            start = mid + 1
        else:
            end = mid - 1

    return end + 1


A = [1, 2, 3, 3, 3, 5]
x = 4
print(find_insert_position(A, x))