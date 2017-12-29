# Split the CSV file into a separate file for each time series
csvfile = open('synthetic_control_data.csv', 'r').readlines()
filename = 1
for i in range(len(csvfile)):
    open(str(filename) + '.csv', 'w+').writelines(csvfile[i])
    filename += 1
