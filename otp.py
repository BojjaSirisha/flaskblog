import random
def genotp():
    upper_case=[chr(i) for i in range(ord('A'),ord('Z')+1)]
    lower_case=[chr(i) for i in range(ord('a'),ord('z')+1)]
    otp=''
    for i in range(2):
        otp+=random.choice(upper_case)
        otp+=str(random.randint(0,9))
        otp+=random.choice(lower_case)
    return otp