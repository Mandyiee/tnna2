import csv, json
data = []
with open('news.csv', 'r', newline='') as csv_input:
    csv_reader = csv.DictReader(csv_input)
    for row in csv_reader:
        print(row)
        data.append(row)

print(data)
with open('news.json', 'w') as json_output:
    json.dump(data, json_output, indent=4)