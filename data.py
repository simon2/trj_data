import pandas as pd
from datetime import datetime

df = pd.read_csv("tour.csv")
#df.set_index('No')
#df.sort_values("Description")
print(df)

name_list = []
json_data = []

min_time = 99999999999
max_time = 0
time_list = []

data_list = []
for index, row in df.iterrows():
    if row["Name"].isnumeric():
        data = []
        data.append(row["Name"])
        data.append(row["Longitude"])
        data.append(row["Latitude"])
        data.append(row["Description"])
        data_list.append(data)

df2 = pd.DataFrame(data_list,columns=["Name","Longitude","Latitude","Description"])
print(df2)
print(len(df2))

for i in range(0,len(df2),1):
    des = df2["Description"][i]
    date_time = des.split("T")
    t_date = date_time[0].split(": ")
    if len(t_date) == 2:
        date = t_date[1]
    time = date_time[1].split("+")[0]
    dt_string = date + " " + time
    datetimet = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
    res_time = datetime.timestamp(datetimet.replace(year=2020,month=1,day=1))
    #res_time = datetime.timestamp(datetimet)
    if int(res_time) < int(min_time):
        min_time = res_time
    if int(res_time) > int(max_time):
        max_time = res_time
    time_list.append(int(res_time))

df2["timestamps"] = time_list
#df2.sort_values(by="timestamps",inplace=True)
print(df2)

count = 0

for index, row in df2.iterrows():
    number = int(row["Description"].split(":")[0])
    path = []
    path.append(row["Longitude"])
    path.append(row["Latitude"])

    if number == 1:
        t_dict = {}
        t_dict["vendor"] = count % 2
        t_dict["path"] = []
        t_dict["path"].append(path)
        t_dict["timestamps"] = []
        t_dict["timestamps"].append((float(row["timestamps"])-1577804409)/10)
        json_data.append(t_dict)
        count = count + 1
        #print("1: count=" + str(count))
    else:
        #print("2: count=" + str(count))
        json_data[count-1]["path"].append(path)
        json_data[count-1]["timestamps"].append((float(row["timestamps"])-1577804409)/10)

print("mintime:"+str(min_time))
print("maxtime:"+str(max_time))
print(int(max_time)-int(min_time))

jason_file = open("kyoto2020.json","w")
jason_file.write("[\n")
for group in json_data:
    jason_file.write("  {\n")
    jason_file.write("    \"vendor\": " + str(group["vendor"]) + ",\n")
    jason_file.write("    \"path\": [\n")
    for i in range(0,len(group["path"])):
    #min = 50
    #if len(group["path"]) < 50:
    #    min = len(group["path"])
    #for i in range(0,min):
        jason_file.write("      " + str(group["path"][i]))
        if i == len(group["path"])-1:
            jason_file.write("],\n")
        else:
            jason_file.write(",\n")
    jason_file.write("    \"timestamps\": " + str(group["timestamps"]) + "\n")
    jason_file.write("  }")
    if json_data.index(group) == len(json_data)-1:
        jason_file.write("\n")
    else:
        jason_file.write(",\n")
jason_file.write("]\n")
jason_file.close()