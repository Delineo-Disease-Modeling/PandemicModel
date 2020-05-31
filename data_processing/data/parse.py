import json as js
import datetime
with open('infections_timeseries.json') as json_file:
    infection_ts = js.load(json_file)

with open('deaths_timeseries.json') as json_file:
    death_ts = js.load(json_file)

with open('interventions.json') as json_file:
    interventions = js.load(json_file)

# print(type(infection_ts))
# print(type(death_ts))
# print(type(interventions))

'''
    format of output:
    output = [
        {   date: xxx
            #FIP: {
                combined_key: xx
                infected: xx
                death: xx  
                policies: xxx
            },
            #FIP : {
                xxx
            }
        },
        {
            another_date: xxx
            #FIP: {
                xxx
            }
        }
    ]
'''


def convert_boolean(cur_date, ordinan_date):
    # print(cur_date)
    # print(ordinan_date)
    if ordinan_date:
        start_date = datetime.date.fromordinal(ordinan_date)
        cur_date =  datetime.datetime.strptime(cur_date, '%m/%d/%y'.lstrip("0").replace(" 0","")).date()
        if start_date < cur_date or cur_date == start_date:
            #print("reach true")
            return True
        #print('reach false')
        return False
    else:
        return ""


if __name__ == "__main__":
    output = []
    dates = []
    for k, v in infection_ts[0].items():
        if k != "FIPS" and k != "Combined_Key":
            dates.append(k)
    for date in dates:
        output.append({"date":date})
    print(len(output))

    pass

    # now append FIPS with information about death, infection, and policies inside:
    for i in range(len(output)):
        cur = output[i]
        date = cur['date']
        for item in infection_ts:
            FIPS = item['FIPS']
            cur[FIPS] = dict()
            cur[FIPS]['infected'] = item[date]
            cur[FIPS]['CKey'] = item['Combined_Key']

    for i in range(len(output)):
        cur = output[i]
        date = cur['date']
        for k, v in cur.items():
            if k != "date":
                # updating info in different FIPS:
                for item in death_ts:
                    if item['FIPS'] == k:
                        v['death'] = item[date]
                        break
                
            

                    
    for i in range(len(output)):
        cur = output[i]
        date = cur['date']
        for k, v in cur.items():
            if k != "date":
                # updating info in different FIPS:
                for item in interventions:
                    if item['FIPS'] == k:

                        v["stay at home"] = convert_boolean(date, item["stay at home"])
                        v[">50 gatherings"] = convert_boolean(date, item[">50 gatherings"])
                        v[">500 gatherings"] = convert_boolean(date, item[">500 gatherings"])
                        v["public schools"] = convert_boolean(date, item["public schools"])
                        v["restaurant dine-in"] = convert_boolean(date,item["restaurant dine-in"])
                        v["entertainment/gym"] = convert_boolean(date,item["entertainment/gym"])
                        v["federal guidelines"] = convert_boolean(date, item["federal guidelines"])
                        v["foreign travel ban"] = convert_boolean(date, item["foreign travel ban"])
                        break
                
            
    #print(output[0][1001])


    with open('data.json', 'w') as out_file:
        js.dump(output, out_file)








# for date in dates:
#     output[date] = []
#     #print(output)
#     for item in infection_ts:
#         # each item is a dictionary with fip, combined key, and all dates
#         FIPS = item['FIPS']
#         Ckey = item['Combined_Key']
#         number_infected = item[date]
#         temp = dict()
#         temp['FIPS'] = FIPS
#         temp['CKey'] = Ckey
#         temp['infected'] = number_infected
#         output[date].append(temp)

# for date in output.keys():
#     for v in output[date]:
#         for item in death_ts:
#             if item['FIPS'] == v['FIPS']:
#                 v['death'] = item[date]
#                 break

# for date in output.keys():
#     for v in output[date]:
#         for item in interventions:
#             if item['FIPS'] == v['FIPS']:
#                 v["stay at home"] = item["stay at home"]
#                 v[">50 gatherings"] = item[">50 gatherings"]
#                 v[">500 gatherings"] = item[">500 gatherings"]
#                 v["public schools"] = item["public schools"]
#                 v["restaurant dine-in"] = item["restaurant dine-in"]
#                 v["entertainment/gym"] = item["entertainment/gym"]
#                 v["federal guidelines"] = item["federal guidelines"]
#                 v["foreign travel ban"] = item["foreign travel ban"]
#                 break

