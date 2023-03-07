import subprocess
import csv
import datetime
import pysftp

# set the connection parameters for the database
server = 'myserver'
username = 'myusername'
password = 'mypassword'
database = 'mydatabase'

# set the path to the SQL script
sql_script = '/path/to/myscript.sql'

# call the SQL script and capture the output
cmd = f'sqlcmd -E -S {server} -d {database} -i {sql_script}'
output = subprocess.check_output(cmd, shell=True)

# convert the output to a string and split it into lines
output = output.decode('utf-8')
lines = output.strip().split('\n')

# remove any leading or trailing whitespace from each line
lines = [line.strip() for line in lines]

# remove any empty lines
lines = [line for line in lines if line]

# convert the lines to a list of lists (assuming the output is comma-separated)
data = [line.split(',') for line in lines]

# write the data to a CSV file with today's date
filename = datetime.datetime.now().strftime('%Y-%m-%d.csv')

with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)

# set the connection parameters for the SFTP server
sftp_server = 'sftp.server.com'
sftp_username = 'sftp_username'
sftp_password = 'sftp_password'

# upload the CSV file to the SFTP folder
with pysftp.Connection(sftp_server, username=sftp_username, password=sftp_password) as sftp:
    sftp.chdir('/home/user')
    sftp.put(filename)
