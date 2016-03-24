import os
import sys
import subprocess
import zipfile
from argparse import ArgumentParser


class Compress(object):

    def __init__(self, args):
        self.args = args
        if self.args.command_line_ran:
            self.args.verbosity = True

    def run(self):
        operation = self.set_operation_type(self.args.file)
        if operation == 'unzip':
            self.unzip()
        else:
            self.zip()
            print 'go'

    def set_operation_type(self, file):
        if file[-4:] == '.zip':
            return 'unzip'
        else:
            return 'zip'

    def unzip(self):
        if self.args.verbosity:
            print 'Unzipping: %s' % zip_file
        folder_name = zip_file.split('/')
        folder_name = folder_name[len(folder_name) - 1]
        folder_name = folder_name.split('.')[0]
        try:
            os.mkdir(folder_name)
            zipfile.ZipFile(self.args.file).extractall(pwd=self.args.password)
        except Exception, e:
            print 'Error unzipping: %s' % e
            sys.exit()
        print 'Successfully Unzipped File!'

    def zip(self):
        if self.args.verbosity:
            print 'Zipping..'

        if self.args.name:
            zip_file_name = self.args.name
        else:
            fp = self.args.file
            if '/' in fp:
                zip_file_name = fp[fp.rfind('/'):]
                if zip_file_name == '/':
                    zip_file_name = fp.replace('/', '')
                zip_file_name += '.zip'
            print zip_file_name

        files = os.walk(self.args.file)

        paths = []
        for root, dirs, files in os.walk(self.args.file):
            for file in files:
                paths.append(root + '/' + file)

        path_string = ''
        for path in paths:
            path_string = path_string + path + ' '
        path_string = path_string[0: len(path_string) - 1]

        try:
            command = 'zip -e -P%s %s %s ' % (
                self.args.password,
                self.args.file,
                path_string)
            print command
            subprocess.call(command, shell=True)
        except Exception, e:
            print e
            sys.exit()

        print 'Wrote Zipfile: %s' % zip_file_name
        print ''
        sys.exit()

    # Remove files and folder we zipped
    # check to make sure a zip has been made that is bigger then 0k
    # print 'Removing unencrypted originals'
    # for f in paths:
    #   os.remove( f )
    #   print '  Removed: %s' % f
    # os.rmdir( file_path )


def main(argv):
    # Get the options
    try:
        opts, args = getopt.getopt(argv, "hzucn:v", ["help", "zip=", "unzip=", "password=", "name="])
    except getopt.GetoptError:
        usage()
        sys.exit()
    print args
    password = False
    for opt, arg in opts:
        if opt in ("-p", "--password"):
            password = arg
            continue

    if not password:
        password = 'password'

    # Main Routing Loop
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()

        # Zip Operation
        elif opt in ("-z", "--zip"):
            folder_to_zip = arg
            for opt, arg in opts:
                if opt in ("-n", "--name"):
                    zip(folder_to_zip, password, arg)
            zip(folder_to_zip, password, arg)

        # Unzip Operation
        elif opt in ("-u", "--unzip"):
            folder_to_unzip = arg
            unzip(folder_to_unzip, password)

        else:
            usage()


def usage():
    print ''
    print 'Compression Sec'
    print '   [file/folder/zip]'
    print '   Options'
    print '     --password, -p  = password default "password"'
    print '     --help,     -h  = this screen'
    # print '     --name,     -n  = zip file name to create'
    # print '     --keeporiginals = wont remove original files after zipping'
    print ' '


def parse_args(args):
    parser = ArgumentParser(description='')
    parser.add_argument('file', default=False, help='File/Folder or zip file to zip or unzip.')
    parser.add_argument('-v', '--verbosity', action='store_true', default=False, help='Sets Verbosity')
    parser.add_argument('-p', '--password', default=False, help='Password for zip')
    parser.add_argument('-n', '--name', default=False, help='Tables to pulldown')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args(sys.argv)
    args.command_line_ran = True
    Compress(args).run()

# End File: compress.py
