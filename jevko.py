opener = '['
closer = ']'
escaper = '`'

def parseJevko(st):
  parents = []
  parent = {'subjevkos': []}
  buffer = ''
  isEscaped = False
  line = 1
  column = 1
  for c in st:
    if (isEscaped):
      if (c == escaper or c == opener or c == closer):
        buffer += c
        isEscaped = False
      else:
        raise SyntaxError(f"Invalid digraph ({escaper}{c}) at {line}:{column}!")
    elif (c == escaper):
      isEscaped = True
    elif (c == opener):
      jevko = {'subjevkos': []}
      parent['subjevkos'].append({'prefix': buffer, 'jevko': jevko})
      parents.append(parent)
      parent = jevko
      buffer = ''
    elif (c == closer):
      parent['suffix'] = buffer
      buffer = ''
      if (len(parents) < 1):
        raise SyntaxError(f"Unexpected closer ({closer}) at {line}:{column}!")
      parent = parents.pop()
    else:
      buffer += c
    
    if (c == '\n'):
      line += 1
      column = 1
    else:
      column += 1

  if (isEscaped):
    raise SyntaxError(f"Unexpected end after escaper ({escaper})!")
  if (len(parents) > 0):
    raise SyntaxError(f"Unexpected end: missing {parents.length} closer(s) ({closer})!")
  parent['suffix'] = buffer
  return parent

def escape(st):
  ret = ''
  for c in st:
    if (c == escaper or c == opener or c == closer): 
      ret += escaper
    ret += c
  return ret

def jevkoToString(jevko):
  ret = ''
  for sub in jevko['subjevkos']:
    ret += f"{escape(sub['prefix'])}[{jevkoToString(sub['jevko'])}]"
  return ret + escape(jevko['suffix'])

def argsToJevko(*args):
  subjevkos = []
  subjevko = {'prefix': ''}
  for arg in args:
    if (isinstance(arg, list)):
      subjevko['jevko'] = argsToJevko(*arg)
      subjevkos.append(subjevko)
      subjevko = {'prefix': ''}
    elif (isinstance(arg, str)):
      subjevko['prefix'] += arg
    else:
      raise Exception(f"Argument #{i} has unrecognized type ({type(arg)})! Only strings and arrays are allowed. The argument's value is: {arg}")
  return {'subjevkos': subjevkos, 'suffix': subjevko['prefix']}

import math 
def interjevkoToSchema(jevko):
  subjevkos = jevko['subjevkos']
  suffix = jevko['suffix']

  trimmed = suffix.strip()
  if (len(jevko['subjevkos']) == 0):
    if (trimmed == 'true' or trimmed == 'false'):
      return {'type': 'boolean'}
    if (trimmed == 'null' or suffix == ''):
      return {'type': 'null'}

    if (trimmed == 'NaN'):
      return {'type': 'float64'}
    try:
      num = float(trimmed)
      return {'type': 'float64'}
    except ValueError:
      return {'type': 'string'}
    
  if (trimmed != ''):
    raise Exception('suffix must be blank')

  prefix = subjevkos[0]['prefix']
  if (prefix.strip() == ''):
    itemSchemas = []
    for sub in subjevkos:
      if (sub['prefix'].strip() != ''):
        raise Exception('bad tuple/array')
      itemSchemas.append(interjevkoToSchema(sub['jevko']))
    return {'type': 'tuple', 'itemSchemas': itemSchemas}

  props = {}
  for sub in subjevkos:
    key = sub['prefix'].strip()
    if (key in props):
      raise Exception(f"duplicate key ({key})")
    props[key] = interjevkoToSchema(sub['jevko'])
  return {'type': 'object', 'props': props}