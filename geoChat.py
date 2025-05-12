import phonenumbers
from phonenumbers import geocoder


class GeoInformationProvider:
    
    def __init__(self , number):
      self.number = number
    
    def provide_location(self):
      try:
        num = phonenumbers.parse(self.number)
        location = geocoder.description_for_number(num, 'en')
        if location == '':
          return f'The number [ {self.number} ] you entered is not a valid phonenumber'
        else:
          return f'The number {self.number} is from {location}'
      except NumberParseException as e:
        return e

