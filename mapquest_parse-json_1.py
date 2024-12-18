import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "iVFunQKGKDhFjeLy5alWuBw2kRhlBvDT"

while True:
    orig = input("Starting Location: ")
    if orig.lower() in ["quit", "q"]:
        break
    dest = input("Destination: ")
    if dest.lower() in ["quit", "q"]:
        break

    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})

    print("URL: " + url)

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================")
        print("Directions from " + orig + " to " + dest)
        print("Trip Duration:   " + json_data["route"]["formattedTime"])

        # Extract and convert times
        normal_time = json_data["route"]["time"] / 60  # in minutes
        real_time = json_data["route"].get("realTime", normal_time) / 60  # in minutes
        congestion_time = real_time - normal_time

        print("Normal Duration: {:.2f} minutes".format(normal_time))
        print("Real-Time Duration (with traffic): {:.2f} minutes".format(real_time))
        print("Traffic Delay: {:.2f} minutes".format(congestion_time))

        # Convert distance to kilometers
        distance_km = json_data["route"]["distance"] * 1.61
        print("Kilometers:      " + "{:.2f}".format(distance_km))

        # Fuel consumption calculation
        if "fuelUsed" in json_data["route"]:
            fuel_used_liters = json_data["route"]["fuelUsed"] * 3.78
        else:
            estimated_fuel_gallons = json_data["route"]["distance"] / 25  # 25 miles per gallon
            fuel_used_liters = estimated_fuel_gallons * 3.78

        print("Fuel Used (Ltr): " + "{:.2f}".format(fuel_used_liters))

        # Adjust fuel consumption for traffic congestion
        additional_fuel_due_to_traffic = (congestion_time / 60) * (fuel_used_liters / normal_time)
        total_fuel_liters = fuel_used_liters + additional_fuel_due_to_traffic

        print("Additional Fuel (due to traffic): {:.2f} Ltr".format(additional_fuel_due_to_traffic))
        print("Total Fuel Used (Ltr): {:.2f}".format(total_fuel_liters))

        # Calculate fuel efficiency (km per liter) adjusted for traffic
        adjusted_fuel_efficiency = distance_km / total_fuel_liters
        print("Adjusted Fuel Efficiency: {:.2f} km/L".format(adjusted_fuel_efficiency))

        print("=============================================")

        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print(each["narrative"] + " (" + str("{:.2f}".format(each["distance"] * 1.61)) + " km)")

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