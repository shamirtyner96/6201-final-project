
# filter rows
filter = (raw_data['party'].isin(['REPUBLICAN', 'DEMOCRAT'])) & (raw_data['mode'].isin(['TOTAL']))
voter_data = raw_data[filter]

