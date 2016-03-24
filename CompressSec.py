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
            print 'Unzipping: %s' % self.args.file
        folder_name = self.args.file.split('/')
        folder_name = folder_name[len(folder_name) - 1]
        folder_name = folder_name.split('.')[0]
        if not self.args.password and self.args.command_line_ran:
            print 'we should prompt for a password'
            # @todo
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
            else:
                zip_file_name = fp
        zip_file_name += '.zip'
        if os.path.exists(zip_file_name):
            zip_file_name += '.2'

        to_zip_is_dir = os.path.isdir(self.args.file)
        if to_zip_is_dir:
            files = os.walk(self.args.file)
            paths = []
            for root, dirs, files in os.walk(self.args.file):
                for file in files:
                    paths.append(root + '/' + file)

            path_string = ''
            for path in paths:
                path_string = path_string + path + ' '
            path_string = path_string[0: len(path_string) - 1]
        else:
            path_string = self.args.file

        try:
            command = 'zip -e -P%s %s %s ' % (
                self.args.password,
                zip_file_name,
                path_string)
            print command
            subprocess.call(command, shell=True)
        except Exception, e:
            print e
            sys.exit()

        if self.args.verbosity:
            print 'Wrote Zipfile: %s' % zip_file_name

        # Remove files and folder we zipped
        if os.path.exists(zip_file_name):
            if self.args.verbosity:
                print 'Removing unencrypted originals'
            if to_zip_is_dir:
                os.rmdir(self.args.file)
            else:
                os.remove(self.args.file)


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
    parser.add_argument(
        '-v',
        '--verbosity',
        action='store_true',
        default=False,
        help='Sets Verbosity')
    parser.add_argument('-p', '--password', default=False, help='Password for zip')
    parser.add_argument('-n', '--name', default=False, help='Tables to pulldown')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args(sys.argv)
    args.command_line_ran = True
    Compress(args).run()

# End File: compress.py
