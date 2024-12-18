import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "iVFunQKGKDhFjeLy5alWuBw2kRhlBvDT"

# Average speed adjustment factors and fuel efficiency (km/L)
VEHICLE_DATA = {
    "motorcycle": {"speed_factor": 1.2, "efficiency": 35},  # 35 km/L
    "car": {"speed_factor": 1.0, "efficiency": 15},        # 15 km/L
    "bus": {"speed_factor": 0.7, "efficiency": 5}          # 5 km/L
}

while True:
    orig = input("Starting Location: ")
    if orig.lower() in ["quit", "q"]:
        break
    dest = input("Destination: ")
    if dest.lower() in ["quit", "q"]:
        break

    # Vehicle choice
    print("\nChoose your vehicle: [motorcycle, car, bus]")
    vehicle = input("Vehicle: ").lower()
    if vehicle not in VEHICLE_DATA:
        print("Invalid vehicle choice! Defaulting to 'car'.")
        vehicle = "car"

    # API call
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    print("\nURL: " + url)

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================")
        print(f"Directions from {orig} to {dest}")
        
        # Extract travel times
        normal_time = json_data["route"]["time"] / 60  # in minutes
        real_time = json_data["route"].get("realTime", normal_time) / 60  # in minutes
        congestion_time = real_time - normal_time

        # Adjust ETA based on vehicle
        adjusted_eta = normal_time / VEHICLE_DATA[vehicle]["speed_factor"]
        print(f"Normal Duration: {normal_time:.2f} minutes")
        print(f"Adjusted Duration ({vehicle.title()}): {adjusted_eta:.2f} minutes")
        print(f"Traffic Delay: {congestion_time:.2f} minutes")

        # Distance in kilometers
        distance_km = json_data["route"]["distance"] * 1.61
        print(f"Distance: {distance_km:.2f} km")

        # Fuel consumption
        vehicle_efficiency = VEHICLE_DATA[vehicle]["efficiency"]
        fuel_used_liters = distance_km / vehicle_efficiency

        print(f"Fuel Used ({vehicle.title()}): {fuel_used_liters:.2f} L")
        print(f"Fuel Efficiency: {vehicle_efficiency} km/L")

        # Adjust fuel for traffic congestion
        additional_fuel_due_to_traffic = (congestion_time / 60) * (fuel_used_liters / adjusted_eta)
        total_fuel_liters = fuel_used_liters + additional_fuel_due_to_traffic

        print(f"Additional Fuel (Traffic): {additional_fuel_due_to_traffic:.2f} L")
        print(f"Total Fuel Used: {total_fuel_liters:.2f} L")

        print("=============================================")
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print(each["narrative"] + f" ({each['distance'] * 1.61:.2f} km)")
        print("=============================================\n")

    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")

    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")

    else:
        print("************************************************************************")
        print("For Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")