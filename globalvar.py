import os
_global_dict={
    'temp':os.getenv('TEMP'),
    'tmp':os.getenv('TMP'),
    'programData':os.getenv('ProgramData')
}
def get_value(name):
    if _global_dict[name]:
        return _global_dict[name]
    elif name in ['TEMP','TMP']:
        for i in ['TEMP','TMP']:
            if _global_dict[i]:
                return _global_dict[i]
    return _global_dict['programData']

