
from time import sleep, strftime
import requests
import webbrowser
from colorama import Fore
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
        html_content = res.text

        flights = []
        departure_time = []
        arrival_time = []

        # Extract flight data using string manipulation or regex
        # Example:
        # flights_data = re.findall(r'<h2 class="flights-list-bold-text flights-list-margined leftText">(.*?)</h2>', html_content)
        # departure_time_data = re.findall(r'<h2 class="flights-list-bold-text flights-list-margined departureTimePadding">(.*?)</h2>', html_content)
        # arrival_time_data = re.findall(r'<h2 class="flights-list-light-text flights-list-margined">(.*?)</h2>', html_content)

        # Sample logic, actual implementation may vary based on HTML structure
        # for flight_data, dep_time, arr_time in zip(flights_data, departure_time_data, arrival_time_data):
        #     flights.append(flight_data.strip())
        #     departure_time.append(dep_time.strip())
        #     arrival_time.append(arr_time.strip())

        return flights, departure_time, arrival_time, base_url
    except Exception as e:
        print(f"Error fetching flight list: {e}")
        return None

def flight_status(flight_id, year, month, date):
    try:
        airline = flight_id.split()[0]
        id = flight_id.split()[1]
        base_url = f'https://www.flightstats.com/v2/flight-tracker/{airline}/{id}?year=20{year}&month={month}&date={date}'
        res = requests.get(base_url)
        html_content = res.text

        # Extract necessary details using string manipulation or regex
        # Example:
        # status = re.search(r'<div class="text-helper__TextHelper-sc-8bko4a-0 iicbYn">(.*?)</div>', html_content).group(1).strip()
        # dep_city = re.search(r'<div class="text-helper__TextHelper-sc-8bko4a-0 efwouT">(.*?)</div>', html_content).group(1).strip()
        # dep_airport = re.search(r'<div class="text-helper__TextHelper-sc-8bko4a-0 cHdMkI">(.*?)</div>', html_content).group(1).strip()
        # arr_city = re.search(r'<div class="text-helper__TextHelper-sc-8bko4a-0 efwouT">(.*?)</div>', html_content).group(1).strip()
        # arr_airport = re.search(r'<div class="text-helper__TextHelper-sc-8bko4a-0 cHdMkI">(.*?)</div>', html_content).group(1).strip()
        # scheduled_dep_time = re.search(r'<div class="text-helper__TextHelper-sc-8bko4a-0 kbHzdx">(.*?)</div>', html_content).group(1).strip()
        # actual_dep_time = re.search(r'<div class="text-helper__TextHelper-sc-8bko4a-0 kbHzdx">(.*?)</div>', html_content).group(1).strip()
        # scheduled_arr_time = re.search(r'<div class="text-helper__TextHelper-sc-8bko4a-0 kbHzdx">(.*?)</div>', html_content).group(1).strip()
        # actual_arr_time = re.search(r'<div class="text-helper__TextHelper-sc-8bko4a-0 kbHzdx">(.*?)</div>', html_content).group(1).strip()
        # terminal_dep = re.search(r'<div class="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx">(.*?)</div>', html_content).group(1).strip()
        # gate_dep = re.search(r'<div class="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx">(.*?)</div>', html_content).group(1).strip()
        # terminal_arr = re.search(r'<div class="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx">(.*?)</div>', html_content).group(1).strip()
        # gate_arr = re.search(r'<div class="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx">(.*?)</div>', html_content).group(1).strip()

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
    print()
    print('''███████╗██╗     ██╗ ██████╗ ██╗  ██╗████████╗    ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗     
██╔════╝██║     ██║██╔════╝ ██║  ██║╚══██╔══╝    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗    
█████╗  ██║     ██║██║  ███╗███████║   ██║          ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝    
██╔══╝  ██║     ██║██║   ██║██╔══██║   ██║          ██║   ██
          ''')