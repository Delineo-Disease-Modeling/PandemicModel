import sys
import requests
from Delineo_Simulation import master as sim
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from threading import current_thread


class Covid_UI:
    def format_input_data(self, inputJSON):
        length = int(inputJSON['tspan'][1])
        return length

    def format_output_data(self, inputJSON, totalInfectedInFacilities, facilities, infectionInFacilitiesHourly, peopleInFacilitiesHourly, facilityinfections, houseinfections, infectionInFacilities, Pop, length):

        data = {
            "t": [
            ],
            "u": [

            ],
            "outputs": [
            ],
            "metadata": {
                "p": inputJSON['p'],
                "u0": inputJSON['u0'],
                "tspan": inputJSON['tspan'],
            },
            "model": {
                "name": "Delineo Modeling Project",
                "modelVersion": "1.0.0",
                "connectorVersion": "1.0.0"
            }

        }

        for i in range(length + 1):
            data["t"].append(float(i))
            countTemp = 0
            for j in range(len(facilities)):
                countTemp += infectionInFacilitiesHourly[j][i]
        tempu0 = inputJSON['u0']
        for i in range(len(tempu0)):
            tempU = []
            for j in range(len(data["t"])):
                tempU.append(
                    float(inputJSON['u0'][i] - inputJSON['u0'][i]/(length * (j+1))))
            data["u"].append(tempU)

        return data

    def http_requests(self):
        mc = sim()
        inputJSON = {"p": [0.25, 0.25], "u0": [
            0.99, 0.01, 0.0], "tspan": [0.0, 2]}
        length = self.format_input_data(inputJSON)
        intervention_list = {"maskWearing": 100, "stayAtHome": False, "contactTracing": 100,
                             "dailyTesting": 100, "roomCapacity": 100, "vaccinatedPercent": 50}
        totalInfectedInFacilities, facilities, infectionInFacilitiesHourly, peopleInFacilitiesHourly, facilityinfections, houseinfections, infectionInFacilities, Pop = mc.Run_Covid_UI(print_infection_breakdown=False, num_days=length,
                                                                                                                                                                                        intervention_list=intervention_list)
        return self.format_output_data(inputJSON, totalInfectedInFacilities, facilities, infectionInFacilitiesHourly, peopleInFacilitiesHourly, facilityinfections, houseinfections, infectionInFacilities, Pop, length)

        while False:
            try:
                future = requests.get('https://covidmod.isi.jhu.edu/covid_ui')
                valueSet = self.format_input_data(future.json())
                values = ValueController(valueSet)
                mc = MasterController(values)
                mc.runFacilityTests('facilities_info.txt')
                data = mc.Run_Covid_UI(print_infection_breakdown=False, num_days=10,
                                       intervention_list=valueSet['interventions'])
                data = self.format_output_data(data)
                r = requests.post(
                    'https://reqbin.com/echo/post/json', json=data)
            except Exception as e:
                return 0

    def main(self):
        try:
            futures = []
            with ThreadPoolExecutor(max_workers=1) as executor:
               # while True:
                futures.append(executor.submit(self.http_requests))
                for future in as_completed(futures):
                    print(future.result())
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    Covid_UI().main()
