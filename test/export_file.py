import csv

log_arr = [];
log_arr.append([10,10])

with open("plot.csv","w+") as my_csv: # flag was w+
    csvWriter = csv.writer(my_csv,delimiter=',')
