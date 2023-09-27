import json
import random

import boto3


class ParkingArea:
    def __init__(self, total_area, wide=8, long=12):
        self.wide = wide
        self.long = long
        self.num_of_places = total_area // (self.wide * self.long)
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


# temp = ParkingArea(2000,10,12)
# print(temp.num_of_places)
# print(temp.parking_list)

class Car:
    def __init__(self, license_number):
        self.license_number = license_number

    def __str__(self):
        return f"Car with license plate {self.license_number}"

    def park(self, parking_lot, spot_num):
        if parking_lot.do_park_car(self, spot_num):
            print(f"The car with license plate {self.license_number} parked successfully in spot {spot_num}")
            return True
        else:
            print(f"The car with license plate {self.license_number} was not parked successfully in spot {spot_num}")
            return False


# new_car = Car("1234")
# print(new_car)

def upload_file_to_s3(file, path):
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id="AWS_S3_KEY",
            aws_secret_access_key="AWS_S3_SECRET"
        )
        key = path + str(random.choice("abcedfghijklmnopqrstuvwxyz0123456789"))
        s3.upload_fileobj(
            file,
            "AWS_S3_TEST_BUCKET",
            key
        )
        return path + key
    except Exception as e:
        print("Something Happened: ", e)
        return e


def generate_cars(number_of_cars=20):
    cars_list = {}
    while len(cars_list) <= number_of_cars:
        rand_number = str(random.randint(1000000, 9999999))
        if rand_number not in cars_list:
            cars_list[rand_number] = Car(rand_number)

    return list(cars_list.values())


def main(cars):
    parking_lot_size = 2000
    parking_lot = ParkingArea(parking_lot_size)

    for car in cars:
        while not parking_lot.is_parking_full():
            spot = random.randint(0, parking_lot.num_of_places - 1)
            if car.park(parking_lot, spot):
                break
        if parking_lot.is_parking_full():
            print("Parking lot is full.")
            break

    vehicle_to_spot_mapping_json = parking_lot.parking_details_json()
    with open("vehicle_to_spot_mapping.json", "w") as file:
        file.write(vehicle_to_spot_mapping_json)


if __name__ == "__main__":
    main(generate_cars(20))
    upload_file_to_s3("vehicle_to_spot_mapping.json", "assets/parking_lot")

# Parking Lot Challenge:
#
# Create a parking lot class that takes in a square footage size as input and creates an array of empty values based on the input square footage size.
# Assume every parking spot is 8x12 (96 ft2) for this program, but have the algorithm that calculates the array size be able to account for different parking spot sizes.
#
# For example, a parking lot of size 2000ft2 can fit 20 cars, but if the parking spots were 10x12 (120 ft2), it could only fit 16 cars.
# The size of the array will determine how many cars can fit in the parking lot.
#
#
# Create a car class that takes in a 7 digit license plate and sets it as a property. The car will have 2 methods:
#
# 1.  A magic method to output the license plate when converting the class instance to a string.
#
# 2.  A "park" method that will take a parking lot and spot # as input and fill in the selected spot in the parking lot.
# If another car is parked in that spot, return a status indicating the car was not parked successfully.
# If no car is parked in that spot, return a status indicating the car was successfully parked.
#
# Have a main method take an array of cars with random license plates and have them park in a random spot in the parking lot
# array until the input array is empty or the parking lot is full. If a car tries to park in an occupied spot, have it try to
# park in a different spot instead until it successfully parks. Once the parking lot is full, exit the program.
#
# Output when a car does or does not park successfully to the terminal (Ex. "Car with license plate [LICENSE_PLATE] parked
# successfully in spot [SPOT #]").
#
# OPTIONAL/BONUS - Create a method for the parking lot class that maps vehicles to parked spots in a JSON object.
# Call this method at the end of the program, save the object to a file, and upload the file to an input S3 bucket.
