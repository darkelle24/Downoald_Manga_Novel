def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c,'')
    return value