import json
import pandas as pd
import matplotlib.pyplot as plt
from . import person as Person


class displayData():
    '''This class is used to display data from the population.

        It takes in the following parameters:
        self
        population: The population of people
        from_json: The data can be in the form of a json
        file: The json file with the data
        '''

    # constructor
    def __init__(self, population, from_json, file):
        self.population = population
        self.from_json = from_json
        self.file = file

        # sets the dataFrame as none
        self.df = None

        # Populates the dataFrame
        self.parse()


    # The parser to put data in datFrame
    def parse(self):
        if self.from_json == True: # Parse the json
            if self.file != None:  # Parse the json with given file
                pass
            else:                  # Parse the peopleArray json
                people_dict = {}
                try:
                    file = open('./peopleArray.json', 'r')
                    unformated_peopleArray = json.loads(file.read())
                    #print(unformated_peopleArray)
                    for i in range(len(unformated_peopleArray)):
                        people_dict[i] = Person(unformated_peopleArray[str(i)])
                        people_dict[i].setAllParameters(ID=unformated_peopleArray[str(i)]['ID'], age=unformated_peopleArray[str(i)]['age'],
                                            sex=unformated_peopleArray[str(i)]['sex'],
                                            householdLocation=unformated_peopleArray[str(i)]['householdLocation'],
                                            householdContacts=unformated_peopleArray[str(i)]['householdContacts'],
                                            comorbidities=unformated_peopleArray[str(i)]['comorbidities'],
                                            demographicInfo=unformated_peopleArray[str(i)]['demographicInfo'],
                                            severityRisk=unformated_peopleArray[str(i)]['severityRisk'],
                                            currentLocation=unformated_peopleArray[str(i)]['currentLocation'],
                                            vaccinated=unformated_peopleArray[str(i)]['vaccinated'],
                                            extendedhousehold=unformated_peopleArray[str(i)]['extendedHousehold'],
                                            COVID_type=unformated_peopleArray[str(i)]['COVID_type'],
                                            vaccineName=unformated_peopleArray[str(i)]['vaccineName'],
                                            shotNumber=unformated_peopleArray[str(i)]['shotNumber'],
                                            daysAfterShot=unformated_peopleArray[str(i)]['daysAfterShot'],
                                            essentialWorker=unformated_peopleArray[str(i)]['essentialWorker'],
                                            madeVaccAppt=unformated_peopleArray[str(i)]['madeVaccAppt'],
                                            vaccApptDate=unformated_peopleArray[str(i)]['vaccApptDate'],
                                            infectionState=unformated_peopleArray[str(i)]['infectionState'],
                                            incubation=unformated_peopleArray[str(i)]['incubation'],
                                            disease=unformated_peopleArray[str(i)]['disease'],
                                            infectionTimer=unformated_peopleArray[str(i)]['infectionTimer'],
                                            infectionTrack=unformated_peopleArray[str(i)]['infectionTrack'])

                    people = [person.to_dict() for person in list(people_dict.values())]
                    df = pd.DataFrame(people)
                    self.df = df
                except:
                    print('File error occured. Check file configuration')
                finally:
                    file.close()
        else:                      # Parse the peopleArray dict
            people_dict = [person.to_dict() for person in list(self.population.values())]
            df = pd.DataFrame(people_dict)
            self.df = df

    # Plots just age distribution
    def plot_age(self):
        self.df['age'].plot(kind='hist', bins=20)
        plt.title("Age Distribution of Population")
        plt.xlabel("Age")
        plt.show()


    # Plots just sex distribution
    def plot_sex(self):
        sex = self.df['sex'].value_counts()

        ax = sex.plot(kind='bar')
        ax.set_title("Sex distribution", y=1)
        ax.set_xlabel('Sex')
        ax.set_ylabel('Number of People')

        ax.set_xticklabels(('Male', 'Female'))

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')
        plt.show()

    # Plots sex and age distribution
    def plot_sex_and_age(self):
        pd.crosstab(self.df['age'], self.df['sex']).plot.bar()
        plt.show()

    # Plots comorbidities distribution
    def plot_comorbidities(self):
        comorbidities = self.df['comorbidities'].value_counts()

        ax = comorbidities.plot(kind='bar')
        ax.set_title("Comorbidities plot", y=1)
        ax.set_xlabel('Number of comorbidities')
        ax.set_ylabel('Frequency')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')
        plt.show()

    # Plots household location distribution
    def plot_householdlocation(self):
        hl = self.df['household location'].value_counts()

        ax = hl.plot(kind='bar')
        ax.set_title("Household location", y=1)
        ax.set_xlabel('Location')
        ax.set_ylabel('Frequency')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots Demographic Information Distribution
    def plot_demographicInfo(self):
        dI = self.df['demographic Info'].value_counts()

        ax = dI.plot(kind='bar')
        ax.set_title("Demographic Information Distribution", y=1)
        ax.set_xlabel('Information')
        ax.set_ylabel('Frequency')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots severity risk distribution
    def plot_severityRisk(self):
        sr = self.df['severity risk'].value_counts()

        ax = sr.plot(kind='bar')
        ax.set_title("Severity risk", y=1)
        ax.set_xlabel('Risk')
        ax.set_ylabel('Frequency')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots current location distribution
    def plot_currentLocation(self):
        cl = self.df['current location'].value_counts()

        ax = cl.plot(kind='bar')
        ax.set_title("Current Location Distribution", y=1)
        ax.set_xlabel('Current Location')
        ax.set_ylabel('Frequency')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots the distribution of the population which is vaccinated
    def plot_vaccinated(self):
        v = self.df['vaccinated'].value_counts()

        ax = v.plot(kind='bar')
        ax.set_title("Vaccinated Distribution", y=1)
        ax.set_ylabel('Frequency')
        ax.set_xlabel('Vaccinated Status')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots the covid type distribution
    def plot_covidType(self):
        ct = self.df['COVID type'].value_counts()

        ax = ct.plot(kind='bar')
        ax.set_title("Vaccinated", y=1)
        ax.set_xlabel('Type')
        ax.set_ylabel('Frequency')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots the distribution of vaccine name
    def plot_vaccineName(self):
        vn = self.df['vaccine name'].value_counts()

        ax = vn.plot(kind='bar')
        ax.set_title("Vaccine Name", y=1)
        ax.set_xlabel('Name')
        ax.set_ylabel('Frequency')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots the days after shot distribution
    def plot_daysAfterShot(self):
        das = self.df['days after shot'].value_counts()

        ax = das.plot(kind='bar')
        ax.set_title("Days After Shot", y=1)
        ax.set_xlabel('Number of Days')
        ax.set_ylabel('Frequency')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots the distribution of essential worker from population
    def plot_essentialWorker(self):
        ew = self.df['essential worker'].value_counts()

        ax = ew.plot(kind='bar')
        ax.set_title("Essential Worker Distribution", y=1)
        ax.set_xlabel('Essential Worker')
        ax.set_ylabel('Frequency')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots the distribution of those who made vaccine appointments
    def plot_madeVaccAppt(self):
        mva = self.df['made vaccine appt'].value_counts()

        ax = mva.plot(kind='bar')
        ax.set_title("Made Vaccine Appointment", y=1)
        ax.set_ylabel('Frequency')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots the distribution of the infection state of the population
    def plot_infectionState(self):
        iS = self.df['infection state'].value_counts()

        ax = iS.plot(kind='bar')
        ax.set_title("Infection State Distribution", y=1)
        ax.set_ylabel('Frequency')
        ax.set_xlabel('Infection State')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots the incubation state distribution of the population
    def plot_incubation(self):
        incu = self.df['incubation'].value_counts()

        ax = incu.plot(kind='bar')
        ax.set_title("Incubation Distribution", y=1)
        ax.set_ylabel('Frequency')
        ax.set_xlabel('Incubation State')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Plots infection timer distribution
    def plot_infectionTimer(self):
        inTi = self.df['infection timer'].value_counts()

        ax = inTi.plot(kind='bar')
        ax.set_title("Infection Timer Distribution", y=1)
        ax.set_ylabel('Frequency')
        ax.set_xlabel('Infection Timer')

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = 1
            label = format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center',
                        va='bottom')

        plt.show()

    # Calls all other plotting methods
    def plot_all(self):
        self.plot_age()
        self.plot_sex()
        self.plot_infectionState()
        self.plot_incubation()
        self.plot_vaccinated()
        self.plot_comorbidities()
        self.plot_covidType()
        self.plot_currentLocation()
        self.plot_daysAfterShot()
        self.plot_demographicInfo()
        self.plot_essentialWorker()
        self.plot_vaccineName()
        self.plot_sex_and_age()
        self.plot_severityRisk()
        self.plot_madeVaccAppt()
        self.plot_infectionTimer()
        self.plot_householdlocation()