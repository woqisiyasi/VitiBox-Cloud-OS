import requests

import pdb
import uuid


class ApiService:
    
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if ApiService.__instance == None:
            ApiService()
        return ApiService.__instance


    def __init__(self):
        
        self.base_url = 'https://api.vitivisor.com.au/gbvs/'
        if ApiService.__instance != None:
            raise Exception("This class is a ApiService!")
        else:
            ApiService.__instance = self


    
    # def request_verification_code(self, country_code, phone):
    #     url = self.base_url + 'user/phone/verify'
        
    #     data = {'countryCode': country_code, 'phone': phone}
    #     headers = {'Content-type': 'application/json'}
    #     res = requests.post(url, json = data, headers = headers, timeout=10)

    #     json_resp = res.json()
    #     return json_resp

    # def login(self, country_code, phone, verification_code):
    #     url = self.base_url + 'user/login'
    #     if (phone[0] != '0'): 
    #         phone = '0' + phone
    #     phone = country_code + '-' + phone

    #     data = {'username': phone, 'password': verification_code, 'client_id': 1, 'client_secret': '-', 'grant_type': 'password'}
    #     headers = {'Content-type': 'application/x-www-form-urlencoded'}
        
    #     res = requests.post(url, data = data, headers = headers, timeout=10)
    #     json_resp = res.json()
    #     return json_resp

    # def get_me(self, token):
    #     url = self.base_url + 'user/me'
    #     headers = {'Authorization': 'Bearer ' + token}
    #     res = requests.get(url, headers = headers, timeout=10)
    #     json_resp = res.json()
    #     return json_resp
        

    # def get_locations(self, token):
    #     url = self.base_url + 'locations'
    #     headers = {'Authorization': 'Bearer ' + token }
    #     res = requests.get(url, headers = headers, timeout=10)
    #     if res.status_code == 500:
    #         return False
    #     json_resp = res.json()
        
    #     return json_resp


    # # {
    # #     year: pic.timePointId.substr(0, 4),
    # #     month: pic.timePointId.substr(4, 2),
    # #     day: pic.timePointId.substr(6),
    # #     id: pic.timePointId,
    # #   };
    # def save_timepoint(self, token, timepoint):
    #     url = self.base_url + 'timepoint'
    #     headers = {'Authorization': 'Bearer ' + token, 'Content-type': 'application/json'}
    #     res = requests.post(url, json = timepoint, headers = headers, timeout=10)
    #     json_resp = res.json()
    #     return json_resp

    
    def property_list(self, token):
        url = self.base_url + 'property_list'
        headers = {'Authorization': 'Bearer ' + token}
        res = requests.get(url, headers = headers, timeout=30)
       
        json_resp = res.json()
        return json_resp


    def upload_image(self, token, data, file_):
        url = self.base_url + 'upload'
        headers = {'Authorization': 'Bearer ' + token}
        res = requests.post(url, data = data, headers = headers, files = file_, timeout=30)
        
        json_resp = res.json()
        return json_resp



#api_service = ApiService.getInstance()
#api_service.request_verification_code('+61', '0426198809')
#api_service.login('+61', '0426198809', '9076')
#token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Iis2MS0wNDIyNTE3OTM0IiwiaWF0IjoxNjAyNDg0NDA2LCJleHAiOjE2MzQwNDIwMDYsImF1ZCI6Imh0dHA6Ly92aXRpY2Fub3B5LmNvbS5hdSIsImlzcyI6IlZpdGljYW5vcHkgc29mdCIsInN1YiI6ImluZm9Adml0aWNhbm9weS5jb20uYXUifQ.olIKwzmwkHANFq8kF0m1O9cYSjXA9b34zwme8QBR9sxGFnY8tYLUPprvCdaVuIGYHPdFByJzv7zGf7i2CxeiEw'
#print( api_service.get_me(token) )

#print( api_service.get_locations(token))

#timepoint = {
#     'year': '2020',
#     'month': '09',
#     'day': '22',
#     'id': '20201022'
# }
#print( api_service.save_timepoint(token, timepoint) )


# location_id = 'dc2709f4-aac6-4cf4-9a33-1c4f9797fb56'
 
# picture = {
#       'picId': str(uuid.uuid4()),
#       'locationId': location_id,
#       'latitude': '-34.884017',
#       'longitude': '138.645432',
#       'timePointId': '20200922'
#     }
# file_ = {
#     'picture': open('/Users/Yan/Desktop/IMG_9751.jpg', 'rb')
# }
# print( api_service.upload_image(token, picture, file_) )

