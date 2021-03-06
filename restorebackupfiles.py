from os import listdir, walk, remove, chmod
from os.path import isfile, join
from shutil import copy2
import stat, os
import cPickle as pickle

def listdir_nohiddenfiles(path):
    """
    do listdir, but don't include files starting with '.'
    """
    for file in listdir(path):
        if not file.startswith('.'):
            yield file

def get_file_list_from_dict_file(filename):
    """
    To speed file path search, retrieve previous searches from dictionary file.
    """
    previousSearchDictionary = {}
    try:
        with open(filename,'rb') as fp:
            previousSearchDictionary = pickle.load(fp)
    except IOError, e:
        print "Failed to find previous file search backup. %s" % e
    return previousSearchDictionary

def list_files(filepath):
    """
    Generate a list of filenames within a path.  This is non-recursive.
    """
    resultlist = [ f for f in listdir_nohiddenfiles(filepath) if isfile(join(filepath,f)) ]
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
previoussearchfilename = 'prevsearches'

print 'Retrieving Previous Directory Search Results:'
prevFoundFiles = get_file_list_from_dict_file(backuppath+'/'+previoussearchfilename)

print 'Files to Copy:'
filesToCopy = list_files(backuppath)
print '   from:'+backuppath

if previoussearchfilename in filesToCopy:
    filesToCopy.remove(previoussearchfilename)
    print 'Removed ' + previoussearchfilename + ' From File Recovery List.'
    

print 'Found Files in Destination to Restore:'
filesToRestore = {}
for file in filesToCopy:
    #first search the previous searches backup
    if file in prevFoundFiles:
        filesToRestore[file] = prevFoundFiles[file]
        print 'Found file from previous search: '
        print '   '+ file + ' in: ' + prevFoundFiles[file]
    #then search through the directories
    else:
        #this code should never execute since the search results are cached
        targetFilesToRestore = find_all(file, destpath)
        print str(len(targetFilesToRestore)) + ' Files Found'
        if len(targetFilesToRestore) > 1:
            print 'WARNING: Multiple files found; using the first file'
        if len(targetFilesToRestore) > 0:
            filesToRestore[file] = targetFilesToRestore.pop(0)

print 'Removing Files from Destination:'
for file in filesToRestore:
    fileAttributes = os.stat(filesToRestore[file])[0]
    if (not fileAttributes & stat.S_IWRITE):
        # File is read-only, so make it writeable
        chmod(filesToRestore[file], stat.S_IWRITE)
    remove(filesToRestore[file])
    print filesToRestore[file]

print 'Restoring Backup Files:'
for file in filesToRestore:
    copy_one_file(backuppath+'/'+file, filesToRestore[file])

print 'Removing Files from Backup:'
for file in filesToCopy:
    fileAttributes = os.stat(backuppath+'/'+file)[0]
    if (not fileAttributes & stat.S_IWRITE):
        # File is read-only, so make it writeable
        chmod(backuppath+'/'+file, stat.S_IWRITE)
    remove(backuppath+'/'+file)
    print 'Removed: ' + backuppath+'/'+file

print 'Dekimashita!'
