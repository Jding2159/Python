import paramiko
import datetime

def get_ssh_connection(hostname, username, private_key_path):
    """Establishes an SSH connection"""
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, username=username, pkey=private_key)
    return client

def get_sftp_connection(ssh_client):
    """Establishes an SFTP connection using an existing SSH connection"""
    return ssh_client.open_sftp()

def get_files_in_directory(sftp, directory):
    """Returns a list of filenames in the specified directory"""
    return sftp.listdir(directory)

def get_yesterday_and_today_filenames():
    """Returns the filenames for yesterday and today in the format 'yyyymmdd'"""
    today = datetime.date.today().strftime('%Y%m%d')
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    return yesterday, today

def compare_files(source_files, destination_files):
    """Compares the files between the source and destination directories"""
    missing_files_source = set(source_files) - set(destination_files)
    missing_files_destination = set(destination_files) - set(source_files)

    return missing_files_source, missing_files_destination

def main():
    # Source and destination directory paths
    source_directory = '/path/to/source_directory'
    destination_directory = '/path/to/destination_directory'

    # Source SSH credentials
    source_hostname = 'source_ssh_hostname'
    source_username = 'source_ssh_username'
    source_private_key_path = '/path/to/source_private_key'

    # Destination SSH credentials
    destination_hostname = 'destination_ssh_hostname'
    destination_username = 'destination_ssh_username'
    destination_private_key_path = '/path/to/destination_private_key'

    # Get SSH connections for source and destination
    with get_ssh_connection(source_hostname, source_username, source_private_key_path) as source_ssh, \
            get_ssh_connection(destination_hostname, destination_username, destination_private_key_path) as destination_ssh:
        # Get SFTP connections for source and destination
        source_sftp = get_sftp_connection(source_ssh)
        destination_sftp = get_sftp_connection(destination_ssh)

        # Get filenames for yesterday and today
        yesterday, today = get_yesterday_and_today_filenames()

        # Get files in source and destination directories
        source_files = get_files_in_directory(source_sftp, source_directory)
        destination_files = get_files_in_directory(destination_sftp, destination_directory)

        # Filter files for yesterday and today
        source_files = [file for file in source_files if file.startswith((yesterday, today))]
        destination_files = [file for file in destination_files if file.startswith((yesterday, today))]

        # Compare files
        missing_files_source, missing_files_destination = compare_files(source_files, destination_files)

        # Print the results
        if missing_files_source or missing_files_destination:
            print("Files missing:")
            if missing_files_source:
                print("Missing in source directory:", missing_files_source)
            if missing_files_destination:
                print("Missing in destination directory:", missing_files_destination)
        else:
            print("All files match in source and destination directories.")

if __name__ == '__main__':
    main()
