import random
import json

class ParkingLot:
    def __init__(self, square_footage, spot_size=(8, 12)):
        self.spot_size = spot_size
        self.num_spots = square_footage // (spot_size[0] * spot_size[1])
        self.spots = [None] * self.num_spots
        self.vehicle_to_spot_mapping = {}

    def is_full(self):
        return all(spot is not None for spot in self.spots)

    def park_car(self, car, spot):
        if self.spots[spot] is None:
            self.spots[spot] = car
            self.vehicle_to_spot_mapping[car.license_plate] = spot
            return True
        else:
            return False

    def map_vehicles_to_spots(self):
        return json.dumps(self.vehicle_to_spot_mapping)

class Car:
    def __init__(self, license_plate):
        self.license_plate = license_plate

    def __str__(self):
        return f"Car with license plate {self.license_plate}"

def main():
    parking_lot_size = 2000  # Change this to the desired parking lot size in square feet
    parking_lot = ParkingLot(parking_lot_size)

    cars = [Car(str(random.randint(1000000, 9999999))) for _ in range(30)]  # 30 cars with random license plates

    for car in cars:
        while not parking_lot.is_full():
            spot = random.randint(0, parking_lot.num_spots - 1)
            if parking_lot.park_car(car, spot):
                print(f"{car} parked successfully in spot {spot}")
                break
            else:
                print(f"Spot {spot} is occupied. {car} is trying another spot.")

    if parking_lot.is_full():
        print("Parking lot is full.")

    # Optional: Map vehicles to spots and save to a JSON file
    vehicle_to_spot_mapping_json = parking_lot.map_vehicles_to_spots()
    with open("vehicle_to_spot_mapping.json", "w") as file:
        file.write(vehicle_to_spot_mapping_json)
    # You can upload the JSON file to an S3 bucket using an AWS SDK or third-party library.

if __name__ == "__main__":
    main()
