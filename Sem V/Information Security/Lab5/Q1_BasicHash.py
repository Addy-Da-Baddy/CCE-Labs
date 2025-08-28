
input_string = input("Enter string to be hashed: ")

def hash(input_string):
    hash_value = 5381
    mask = 0xFFFFFFFF
    shift1,shift2,shift3 = 16,4,3
    
    for char in input_string:
        hash_value = (hash_value*33) + ord(char)

        hash_value ^= (hash_value << shift1)
        hash_value ^= (hash_value >> shift2)
        hash_value ^= (hash_value << shift3)
        
        hash_value &= mask
        
        
    return hash_value
    
print("Hashed Value: ", hash(input_string))


        