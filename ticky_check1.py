import re
import csv
import operator

error_messages = {}
per_user = {}
ficherolog = "/home/student-04-cb83367de9a4/syslog.log"
patron = r"(INFO|ERROR) ([\w' ]+|[\w\[\]#' ]+) (\(\w+\)|\(\w+\.\w+\))$"

with open(ficherolog) as f:
	for line in f:
		result = re.search(patron, line)
		if result is None:
			continue
		if result.groups()[0] == "INFO":
			category = result.groups()[0]
			message = result.groups()[1]
			name = str(result.groups()[2])[1:-1]
			if name in per_user:
				user = per_user[name]
				user[category] += 1
			else:
				per_user[name] = {'INFO':1, 'ERROR':0}
		if result.groups()[0] == "ERROR":
			category = result.groups()[0]
			message = result.groups()[1]
			name = str(result.groups()[2])[1:-1]
			error_messages[message] = error_messages.get(message, 0) + 1
			if name in per_user:
				user = per_user[name]
				user[category] += 1
			else:
				per_user[name] = {'INFO':0, 'ERROR':1}

sorted_messages = [("Error", "Count")] + sorted(error_messages.items(), key = operator.itemgetter(1), reverse=True)
#sorted_messages = [("Error", "Count")] + sorted(error_messages.items(), key = lambda x: x[1], reverse=True)
sorted_users = [("Username", "INFO", "ERROR")] + sorted(per_user.items())[0:8]
#sorted_users = [("Username", "INFO", "ERROR")] + sorted(per_user.items())

with open("error_message.csv", "w") as error_file:
	for line in sorted_messages:
		error_file.write("{}, {}\n".format(line[0], line[1]))

with open("user_statistics.csv", "w") as user_file:
	for line in sorted_users:
		if isinstance(line[1], dict):
			user_file.write("{}, {}, {}\n".format(line[0], line[1].get("INFO"), line[1].get("ERROR")))
		else:
			user_file.write("{}, {}, {}\n".format(line[0], line[1], line[2]))
			
#Adding this comment
