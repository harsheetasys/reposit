from time import sleep
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
import flightradar24 as fl

api = fl.Api()

def get_airport_iata(country):
    try:
        all_airports = api.get_airports()
        data = []

        for airport in all_airports['rows']:
            if airport["country"].lower() == country.lower():
                data.append({
                    "name": airport["name"],
                    "iata": airport["iata"]
                })
        return data
    except Exception as e:
        print(f"Error fetching airports: {e}")
        return []

def get_airline_code(airline_name):
    try:
        all_airlines = api.get_airlines()
        results = []

        for airline in all_airlines['rows']:
            if airline["Name"].lower() == airline_name.lower():
                return airline['Code']
            elif airline["Name"].lower().find(airline_name.lower()) != -1:
                results.append(airline)

        return results
    except Exception as e:
        print(f"Error fetching airlines: {e}")
        return []

def list_flights(arr_iata, dep_iata, year, month, date, hour):
    try:
        base_url = f'https://www.flightstats.com/v2/flight-tracker/route/{arr_iata}/{dep_iata}/?year={year}&month={month}&date={date}&hour={hour}'
        res = requests.get(base_url)
        soup = BeautifulSoup(res.content, 'html.parser')

        flights = []
        departure_time = []
        arrival_time = []

        flights_data = soup.find_all('h2', class_='flights-list-bold-text flights-list-margined leftText')
        dept_time_data = soup.find_all('h2', class_='flights-list-bold-text flights-list-margined departureTimePadding')
        arr_time_data = soup.find_all('h2', class_='flights-list-light-text flights-list-margined')

        if len(flights_data) and len(dept_time_data) and len(arr_time_data) != 0:
            for flight in flights_data:
                flights.append(flight.text.strip())

            for dep_time in dept_time_data:
                departure_time.append(dep_time.text.strip())

            for arr_time in arr_time_data:
                arrival_time.append(arr_time.text.strip())

            return flights, departure_time, arrival_time, base_url
        else:
            return None
    except Exception as e:
        print(f"Error fetching flight list: {e}")
        return None

def flight_status(flight_id, year, month, date):
    try:
        airline = flight_id.split()[0]
        id = flight_id.split()[1]
        base_url = f'https://www.flightstats.com/v2/flight-tracker/{airline}/{id}?year=20{year}&month={month}&date={date}'
        res = requests.get(base_url)
        soup = BeautifulSoup(res.content, 'html.parser')

        status = soup.find("div", class_='text-helper__TextHelper-sc-8bko4a-0 iicbYn').text.strip()
        dep_city = soup.find_all("div", class_='text-helper__TextHelper-sc-8bko4a-0 efwouT')[0].text.strip()
        dep_airport = soup.find_all('div', class_='text-helper__TextHelper-sc-8bko4a-0 cHdMkI')[0].text.strip()
        arr_city = soup.find_all("div", class_='text-helper__TextHelper-sc-8bko4a-0 efwouT')[1].text.strip()
        arr_airport = soup.find_all('div', class_='text-helper__TextHelper-sc-8bko4a-0 cHdMkI')[1].text.strip()
        scheduled_dep_time = soup.find_all("div", class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[0].text.strip()
        actual_dep_time = soup.find_all("div", class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[1].text.strip()
        scheduled_arr_time = soup.find_all("div", class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[2].text.strip()
        actual_arr_time = soup.find_all("div", class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[3].text.strip()
        terminal_dep = soup.find_all("div", class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[0].text.strip()
        gate_dep = soup.find_all("div", class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[1].text.strip()
        terminal_arr = soup.find_all("div", class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[2].text.strip()
        gate_arr = soup.find_all("div", class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[3].text.strip()

        return status, arr_city, arr_airport, dep_city, dep_airport, scheduled_arr_time, actual_arr_time, scheduled_dep_time, actual_dep_time, terminal_arr, gate_arr, terminal_dep, gate_dep
    except Exception as e:
        print(f"Error fetching flight status: {e}")
        return None

def display_flight_details(data):
    if data:
        status, arr_city, arr_airport, dep_city, dep_airport, scheduled_arr_time, actual_arr_time, scheduled_dep_time, actual_dep_time, terminal_arr, gate_arr, terminal_dep, gate_dep = data

        print(Fore.GREEN + "--" * 40 + Fore.RESET)
        print(Fore.GREEN + "                    Flight Status" + Fore.RESET)
        print(Fore.GREEN + f"Status: {status}" + Fore.RESET)
        print(Fore.GREEN + f"Arrival City: {arr_city}" + Fore.RESET)
        print(Fore.GREEN + f"Arrival Airport: {arr_airport}" + Fore.RESET)
        print(Fore.GREEN + f"Departure City: {dep_city}" + Fore.RESET)
        print(Fore.GREEN + f"Departure Airport: {dep_airport}" + Fore.RESET)
        print(Fore.GREEN + f"Scheduled Arrival Time: {scheduled_arr_time}" + Fore.RESET)
        print(Fore.GREEN + f"Actual Arrival Time: {actual_arr_time}" + Fore.RESET)
        print(Fore.GREEN + f"Scheduled Departure Time: {scheduled_dep_time}" + Fore.RESET)
        print(Fore.GREEN + f"Actual Departure Time: {actual_dep_time}" + Fore.RESET)
        print(Fore.GREEN + f"Arrival Terminal: {terminal_arr}" + Fore.RESET)
        print(Fore.GREEN + f"Arrival Gate: {gate_arr}" + Fore.RESET)
        print(Fore.GREEN + f"Departure Terminal: {terminal_dep}" + Fore.RESET)
        print(Fore.GREEN + f"Departure Gate: {gate_dep}" + Fore.RESET)
        print(Fore.GREEN + "--" * 40 + Fore.RESET)
    else:
        print(Fore.RED + "--" * 40 + Fore.RESET)
        print(Fore.RED + "No data available." + Fore.RESET)
        print(Fore.RED + "--" * 40 + Fore.RESET)

def main_menu():
    while True:
        print()
        print(Fore.BLUE + "█████████████████████████████████████████████████████████████████████████████████████████████████████████████████" + Fore.RESET)
        print(Fore.BLUE + "                                 [ 1 ] LIST FLIGHTS                                                        " + Fore.RESET)
        print(Fore.BLUE + "                                 [ 2 ] FLIGHT STATUS                                                       " + Fore.RESET)
        print(Fore.BLUE + "                                 [ 3 ] AIRLINE NAME                                                         " + Fore.RESET)
        print(Fore.BLUE + "                                 [ 4 ] AIRPORT NAME                                                         " + Fore.RESET)
        print(Fore.BLUE + "                                 [ 5 ] EXIT PROGRAM                                                        " + Fore.RESET)
        print(Fore.BLUE + "                                 [ 6 ] Update the System                                                   " + Fore.RESET)
        print(Fore.BLUE + "█████████████████████████████████████████████████████████████████████████████████████████████████████████████████" + Fore.RESET)
        print()

        choice = input(Fore.YELLOW + "Enter your choice (1-5): " + Fore.RESET).strip()

        if choice == '1':
            arr_iata = input("Enter arrival airport IATA code: ").strip().upper()
            dep_iata = input("Enter departure airport IATA code: ").strip().upper()
            year = input("Enter year: ").strip()
            month = input("Enter month: ").strip()
            date = input("Enter date: ").strip()
            hour = input("Enter hour: ").strip()

            flights_data = list_flights(arr_iata, dep_iata, year, month, date, hour)

            if flights_data:
                flights, departure_time, arrival_time, base_url = flights_data
                print(Fore.CYAN + "--" * 40 + Fore.RESET)
                print(Fore.CYAN + f"Flight List for {dep_iata} to {arr_iata} on {date}-{month}-{year} at {hour}:00" + Fore.RESET)
                for i in range(len(flights)):
                    print(Fore.CYAN + f"Flight: {flights[i]}, Departure Time: {departure_time[i]}, Arrival Time: {arrival_time[i]}" + Fore.RESET)
                print(Fore.CYAN + "--" * 40 + Fore.RESET)
            else:
                print(Fore.RED + "No flights found for the given parameters." + Fore.RESET)

        elif choice == '2':
            flight_id = input("Enter airline code and flight number (e.g., DL 123): ").strip().upper()
            year = input("Enter year: ").strip()
            month = input("Enter month: ").strip()
            date = input("Enter date: ").strip()

            flight_data = flight_status(flight_id, year, month, date)

            if flight_data:
                display_flight_details(flight_data)
            else:
                print(Fore.RED + "Flight status not found for the given parameters." + Fore.RESET)

        elif choice == '3':
            airline_name = input("Enter airline name (or part of it): ").strip().upper()
            airline_codes = get_airline_code(airline_name)

            if airline_codes:
                print(Fore.CYAN + "--" * 40 + Fore.RESET)
                print(Fore.CYAN + "Airline Codes:" + Fore.RESET)
                for airline in airline_codes:
                    print(Fore.CYAN + f"Name: {airline['Name']}, Code: {airline['Code']}" + Fore.RESET)
                print(Fore.CYAN + "--" * 40 + Fore.RESET)
            else:
                print(Fore.RED + "No airlines found with the given name." + Fore.RESET)

        elif choice == '4':
            country = input("Enter country name to fetch airport IATA codes: ").strip().capitalize()
            airports = get_airport_iata(country)

            if airports:
                print(Fore.CYAN + "--" * 40 + Fore.RESET)
                print(Fore.CYAN + f"Airports in {country}:" + Fore.RESET)
                for airport in airports:
                    print(Fore.CYAN + f"Name: {airport['name']}, IATA Code: {airport['iata']}" + Fore.RESET)
                print(Fore.CYAN + "--" * 40 + Fore.RESET)
            else:
                print(Fore.RED + "No airports found in the given country." + Fore.RESET)

        elif choice == '5':
            print("Exiting program...")
            break

        elif choice == '6':
            print("Updating the system...")
            sleep(2)  # Simulate update process
            print("System updated successfully!")

        else:
            print(Fore.RED + "Invalid choice! Please enter a number from 1 to 5." + Fore.RESET)

if __name__ == "__main__":
    main_menu()
