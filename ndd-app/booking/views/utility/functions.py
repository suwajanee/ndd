def check_key_detail(obj, data, key, pop):
    if key in data:
        if data[key]:
            obj[key] = data[key]
        else: 
            try:
                if pop:
                    obj.pop(key)
                else:
                    obj[key] = ''
            except:
                pass
    else:
        try:
            if pop:
                obj.pop(key)
            else:
                obj[key] = ''
        except:
            pass
    return obj

def set_if_not_none(mapping, key, value):
    if value is not None and value:
        mapping[key] = value