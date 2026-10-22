
# print(groupedData[2024]['VIRGINIA']['DEMOCRAT']['total'])
# print(len(groupedData[2024]['VIRGINIA']['DEMOCRAT']))

for year in groupedData:
    for state in groupedData[year]:
        total = groupedData[year][state]['DEMOCRAT']['total'] + groupedData[year][state]['REPUBLICAN']['total']
        print(state, total)
