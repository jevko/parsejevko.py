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