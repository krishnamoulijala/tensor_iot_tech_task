import json


# import boto3


class ParkingArea:
    def __init__(self, total_area, parking_size=(8, 12)):
        self.parking_size = parking_size
        self.num_of_places = total_area // (parking_size[0] * parking_size[1])
        self.parking_list = [None] * self.num_of_places
        self.parking_place_mapping_to_car = {}

    def do_park_car(self, car, place):
        if self.parking_list[place] is None:
            self.parking_list[place] = car
            self.parking_place_mapping_to_car[place] = car.license_number
            return True
        else:
            return False

    def is_parking_full(self):
        return all(each_one is not None for each_one in self.parking_list)

    def parking_details_json(self):
        return json.dumps(self.parking_place_mapping_to_car)


# parki = ParkingArea(2000,(10,12))
# print(parki.num_of_places)
# print(parki.parking_list)

class Car:
    def __init__(self, license_number):
        self.license_number = license_number

    def __str__(self):
        return f"Car with license plate {self.license_number}"

# new_car = Car("1234")
# print(new_car)
