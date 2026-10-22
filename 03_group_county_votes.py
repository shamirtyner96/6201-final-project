groupedData = {}

for index, row in voter_data.iterrows():
    party = row['party']
    state = row['state']
    county = row['county_name']
    year = row['year']
    votes = row['candidatevotes']

    if year not in groupedData:
        groupedData[year] = {}

    if state not in groupedData[year]:
        groupedData[year][state] = {}

    if party not in groupedData[year][state]:
        total_votes = 0
        groupedData[year][state][party] = {
                'total': total_votes,
                'counties': {}
                }
        
    if county not in groupedData[year][state][party]['counties']:
        groupedData[year][state][party]['counties'][county] = votes
        groupedData[year][state][party]['total'] += votes
