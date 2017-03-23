import string


def get_password_strength(password):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    symbols = "!@#$%^&*()_+-=[]\;',./{}|:\"<>? "
    numbers = "0123456789"
    strength = 0
    if len(password) > 5:
        strength += 1
    else:
        strength -= 3
    for x in [uppercase, symbols, numbers]:
        done = 0
        for char in password:
            if char in x and (not done > 1):
                done += 1
                strength += 1
    strength += 1
    if strength <= 0:
        return "Very Weak"
    elif strength == 1:
        return "Weak"
    elif strength == 2:
        return "Kind of Weak"
    elif strength == 3:
        return "Average"
    elif strength == 4:
        return "Sort of Strong"
    elif strength == 5:
        return "Strong"
    elif strength == 6:
        return "Pretty Strong"
    else:
        return "Very Strong"
