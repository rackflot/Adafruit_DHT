


date_time_str = "2024-03-07 16:39:00"
format_str = "%Y-%m-%d %H:%M:%S"
epoch_time = text_to_epoch(date_time_str, format_str)
print(f"The epoch time for {date_time_str} is: {epoch_time}")

date_time_str2 = "03/07/2024 16:39"
format_str2 = "%m/%d/%Y %H:%M"
epoch_time2 = text_to_epoch(date_time_str2, format_str2)
print(f"The epoch time for {date_time_str2} is: {epoch_time2}")

date_time_str3 = "Sun 03Mar24 04:39:00 PM"
format_str3 = "%a %d%b%y %I:%M:%S %p"
epoch_time3 = text_to_epoch(date_time_str3, format_str3)
print(f"The epoch time for {date_time_str3} is: {epoch_time3}")

# ------------------------------------------------------------------------------
# Get sample frequency in minutes
def freqSample():
	times, temps, hums = dbh.getHistData (2)
	# timediff = time[1] - time[0]
#	fmt = '%Y-%m-%d %H:%M:%S'
#	fmt = '%d%m%y %H:%M:%S %p'
	fmt = "%a %d%b%y %I:%M:%S %p"
	tstamp0 = datetime.strptime(times[0], fmt)
	tstamp1 = datetime.strptime(times[1], fmt)
	freq = tstamp1-tstamp0
	freq = int(round(freq.total_seconds()/60))
	return (freq)
