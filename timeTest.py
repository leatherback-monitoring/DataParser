import pandas as pd
import timeSync

csvpath ="cr-sensor3-test"
data = pd.read_csv(csvpath + ".csv", names = ['rawTime','temp','humidity'])

if len(data) > 0:
	#multiply to get time in seconds
	data['rawTime'] = data['rawTime']*8

	timeSeries = list(data['rawTime'])

	data['rawTime'] = timeSync.checkResetOverflow(timeSeries)

	timeSync.singleSync(data, 'rawTime')

	pd.DataFrame.to_csv(data,path_or_buf=csvpath+"-clean.csv")
