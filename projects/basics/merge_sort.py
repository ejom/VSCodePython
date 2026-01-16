def merge(arr: list, li: int, ri: int, mi):
    #define the left and right lists
    len_l = mi-li+1
    len_r = ri-mi
    l = arr[li:mi+1] 
    r = arr[mi+1:ri+1]

    #merge sort
    i = 0
    j=0
    k=li
    #iterate through all the left or right array items putting the smallest in front
    while i<len_l and j<len_r:
        if l[i]<=r[j]:
            arr[k]=l[i]
            i+=1
        else:
            arr[k]=r[j]
            j+=1
        k+=1
    #fill the rest of the array with whatevers leftover
    while i<len_l:
        arr[k]=l[i]
        i+=1
        k+=1
    while j<len_r:
        arr[k]=r[j]
        j+=1
        k+=1

#First we need to divide up the list into halves
def merge_sort(arr: list, li: int, ri: int):
    #continue dividing subdivisions until the left index equals the right index (cant divide anymore)
    if li<ri:
        #define the middle index between left and right indexes
        mi = li + (ri-li)//2
        #continue dividing the subdivisions
        merge_sort(arr, li, mi)
        merge_sort(arr, mi+1, ri)
        #merge sort the subdivisions
        merge(arr, li, ri, mi)

test_arr = [12, 11, 13, 5, 6, 7]
print(f"Given array is: {[12, 11, 13, 5, 6, 7]}")
merge_sort(test_arr, 0, len(test_arr)-1)
print(f"Sorted array is: {test_arr}")
