from os import listdir, walk
from os.path import isfile, join
from shutil import copy2

def list_files(filepath):
    """
    Generate a list of filenames within a path.  This is non-recursive.
    """
    resultlist = [ f for f in listdir(filepath) if isfile(join(filepath,f)) ]
    for filename in resultlist:
        print filename
    return resultlist

def find_all(name, path):
    """
    Find paths to all occurances of a file name within a path.
    """
    result = []
    for root, dirs, files in walk(path):
        if name in files:
            result.append(join(root, name))
            print '   Found: ' + ''.join(result)
    return result

def copy_one_file(sourcepathfile, destinationpath):
    """
    Copy one file to a destination directory.
    """
    try:
        copy2(sourcepathfile, destinationpath)
        print '   Copied: ' + sourcepathfile
        print '      to: ' + destinationpath
    except IOError, e:
        print "Unable to copy file. %s" % e

destpath = '/destpath'
backuppath = '/backuppath'

srcpath = raw_input("Modified File Path:")

print 'Files to Copy:'
filesToCopy = list_files(srcpath)
print '   from:'+srcpath

print 'Found Files in Destination to Backup:'
filesToBackup = {}
for file in filesToCopy:
    targetFilesToBackup = find_all(file, destpath)
    print str(len(targetFilesToBackup)) + ' Files Found'
    if len(targetFilesToBackup) > 1:
        print 'WARNING: Multiple files found; using the first file'
    if len(targetFilesToBackup) > 0:
        filesToBackup[file] = targetFilesToBackup.pop(0)

print 'Backing Up Files:'
for file in filesToBackup:
    copy_one_file(filesToBackup[file], backuppath)

print 'Copying in New Files:'
for file in filesToBackup:
    copy_one_file(srcpath+'/'+file, filesToBackup[file])
print 'Dekimashita!'
