from os import listdir, walk
from os.path import isfile, join
from shutil import copy2

def list_files(filepath):
    resultlist = [ f for f in listdir(filepath) if isfile(join(filepath,f)) ]
    for filename in resultlist:
        print filename
    return resultlist

def find_all(name, path):
    result = []
    for root, dirs, files in walk(path):
        if name in files:
            result.append(join(root, name))
            print '   Found: ' + ''.join(result)
    return result

def copy_one_file(sourcepathfile, destinationpath):
    try:
        copy2(sourcepathfile, destinationpath)
        print '   Copied: ' + sourcepathfile
        print '      to: ' + destinationpath
    except IOError, e:
        print "Unable to copy file. %s" % e

destpath = '/destipath'
backuppath = '/backuppath'

print 'Files to Copy:'
filesToCopy = list_files(backuppath)
print '   from:'+backuppath

print 'Found Files in Destination to Restore:'
filesToRestore = {}
for file in filesToCopy:
    targetFilesToRestore = find_all(file, destpath)
    print str(len(targetFilesToRestore)) + ' Files Found'
    if len(targetFilesToRestore) > 1:
        print 'WARNING: Multiple files found; using the first file'
    if len(targetFilesToRestore) > 0:
        filesToRestore[file] = targetFilesToRestore.pop(0)

print 'Restoring Backup Files:'
for file in filesToRestore:
    copy_one_file(backuppath+'/'+file, filesToRestore[file])
print 'Dekimashita!'
