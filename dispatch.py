def re_response(value):
  return value

def command_dispatch(response):
  
  if response == '@geoversion':
    re_response(True)
  elif response == '@aiversion':
    re_response(False)
