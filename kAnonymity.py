#!c:/Python34/python.exe
import math
import random
from retrying import retry
import time

class kAnonymity:
    x = []
    y = []
    val = []
    count = 0


    def __init__(self, latitude, longitude, kValue, radius):
        self.latitude = latitude
        self.longitude = longitude
        self.kValue = kValue
        self.radius = radius



    def generate_hilbert(self, x0, y0, xi, xj, yi, yj, n):
        if n <= 0:
            X = x0 + (xi + yi) / 2
            Y = y0 + (xj + yj) / 2
            self.count = self.count + 1
            self.x.append(X)
            self.y.append(Y)
            self.val.append(self.count)
            # Output the coordinates of the cv
            #print('%s %s %s' % (X, Y, count))
        else:
            self.generate_hilbert(x0, y0, yi / 2, yj / 2, xi / 2, xj / 2, n - 1)
            self.generate_hilbert(x0 + xi / 2, y0 + xj / 2, xi / 2, xj / 2, yi / 2, yj / 2, n - 1)
            self.generate_hilbert(x0 + xi / 2 + yi / 2, y0 + xj / 2 + yj / 2, xi / 2, xj / 2, yi / 2, yj / 2, n - 1)
            self.generate_hilbert(x0 + xi / 2 + yi, y0 + xj / 2 + yj, -yi / 2, -yj / 2, -xi / 2, -xj / 2, n - 1)

        


    def map_range(self, a, b, s, square):
        (a1, a2), (b1, b2) = a, b
        #print("count",self.count)
        return math.floor( (random.randint(999,9999) + b1 + ((s - a1) * (b2 - b1) / (a2 - a1))) % math.pow(4, square))

    def generate_location_block(self, k):
        square = 4
        self.generate_hilbert(0.0, 0.0, 1.0, 0.0, 0.0, 1.0, square)
        mini_x = min(self.x)
        mini_y = min(self.y)
        """for i in range(0, len(x)):
            print("%s %s %s" % ((x[i] - mini_x) / (mini_x * 2), (y[i] - mini_y) / (mini_y * 2), val[i]))"""
        key1 = 1345267
        key2 = random.randint(999999, 9999999)
        key_final = (key1 * key2) % random.randint(999, 9999)
        #print(key_final)
        # for i in range(0,len(key)):
        mapped_val = []
        for s in range(1, k + 1):
            # print("%2g maps to %g" % (s, map_range((1, k+1), (0,math.pow(4,square)), s, square)))
            self.val = self.map_range((1, k + 1), (0, math.pow(4, square)), s, square)
            #print("self.val",self.val)
            if self.val not in mapped_val:
                mapped_val.append(self.val)
            else:
                while self.val not in mapped_val:
                    self.val = (self.val + 1) % math.pow(4, square)
                mapped_val.append(self.val)
        mapped_val.sort()
        #print(mapped_val)
        return mapped_val, mini_x, mini_y

    def generate_dummy_locations(self):
        mapped_val, min_x, mini_y = self.generate_location_block(self.kValue)
        user_index = random.randint(0,len(mapped_val))
        user_block = mapped_val[user_index]
        user_x = self.x[user_index]
        user_y = self.y[user_index]
        #print(user_block)
        lat_lng = [[self.latitude, self.longitude]]
        lat = [self.latitude]
        lng = [self.longitude]
        for a in mapped_val:
            if a != user_block:
                dummy_x = self.x[a]
                dummy_y = self.y[a]
                dist_x = (dummy_x - user_x) * 0.01 * self.radius
                dist_y = (dummy_y - user_y) * 0.01 * self.radius
                lat_lng.append([self.latitude + dist_y, self.longitude + dist_x])
                lat.append(self.latitude + dist_y)
                lng.append(self.longitude + dist_x)
                #print(str(dist_x)+"   "+str(dist_y))
        #print(lat_lng)
        random.shuffle(lat_lng)
        #print(lat_lng)
        response = self.get_all_addresses(lat_lng, [self.latitude, self.longitude])
        #print("Final response", response)
        return response
        #print(json.loads(response)["results"][0]["formatted_address"])

    def get_all_addresses(self, lat_lng,user_lat_lng):
        finalList = []
        for latlng in lat_lng:
            #print(latlng)
            latitude = latlng[0]
            longitude = latlng[1]
            response = self.fetch_dummy_address_from_coordinates(latitude,longitude)
            if [latitude, longitude] == user_lat_lng:
                response = response
                import json
                #print("get_correct_response",response)
                #print(json.loads(response)["results"][0]["formatted_address"]+"<br/>\r\n")
            finalList.append(response)
        return finalList

    @retry(stop_max_attempt_number=3)
    def fetch_user_address_from_coordinates(self):
        import requests, json
        request_string = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" \
                        + str(self.latitude) + "," + str(self.longitude) + "&sensor=true&key=AIzaSyDou720GbkIU_-G4d7ilis6eAzVvltsJJg"
        response = requests.get(request_string)
        locat = response.text
        locat = json.loads(locat)
        location_info = locat["results"][0]["formatted_address"]
        #print(location_info+"<br/>\r\n")
        return response
    
    @retry(stop_max_attempt_number=3)
    def fetch_dummy_address_from_coordinates(self, latitude, longitude):
        import requests, json
        request_string = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" \
                        + str(latitude) + "," + str(longitude) + "&sensor=true&key=AIzaSyDou720GbkIU_-G4d7ilis6eAzVvltsJJg"
        response = requests.get(request_string)
        locat = response.text
        locat = json.loads(locat)
        location_info = locat["results"][0]["formatted_address"]
        #print(location_info+"<br/>\r\n")
        return location_info




