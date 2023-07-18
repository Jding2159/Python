import pysftp
import datetime

def get_sftp_connection(hostname, username, private_key_path):
    """Establishes an SFTP connection"""
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.load('/etc/ssh/ssh_known_hosts')
    private_key = private_key_path

    return pysftp.Connection(host=hostname, username=username, private_key=private_key, cnopts=cnopts)

def get_files_in_directory(sftp, directory):
    """Returns a list of filenames in the specified directory"""
    sftp.cwd(directory)
    return sftp.listdir()

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

    # SFTP credentials
    hostname = 'sftp_hostname'
    username = 'sftp_username'
    private_key_path = '/path/to/private_key'

    # Get SFTP connections
    with get_sftp_connection(hostname, username, private_key_path) as sftp:
        # Get filenames for yesterday and today
        yesterday, today = get_yesterday_and_today_filenames()

        # Get files in source and destination directories
        source_files = get_files_in_directory(sftp, source_directory)
        destination_files = get_files_in_directory(sftp, destination_directory)

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
