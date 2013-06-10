from os import listdir, walk, remove, chmod
from os.path import isfile, join
from shutil import copy2
import stat, os
import cPickle as pickle

def listdir_nohiddenfiles(path):
    """
    Do listdir, but don't include files starting with '.'.
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

def store_file_list_to_dict_file(filename, filelist):
    """
    To speed file path search, store previous searches to a dictionary file.
    """
    try:
        with open(filename,'wb') as fp:
            pickle.dump(filelist,fp)
            print "Previous Search Save Succeeded."
    except IOError, e:
        print "Failed to find previous file search backup. %s" % e

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

srcpath = raw_input("Modified File Path:")
#copy/paste path by drag folder into bash term, results in ' ' at end of path; remove
srcpath = srcpath.rstrip()

print 'Retrieving Previous Directory Search Results:'
prevFoundFiles = get_file_list_from_dict_file(backuppath+'/'+previoussearchfilename)

print 'Files to Copy:'
filesToCopy = list_files(srcpath)
print '   from:'+srcpath

print 'Found Files in Destination to Backup:'
filesToBackup = {}
for file in filesToCopy:
    #first search the previous searches backup
    if file in prevFoundFiles:
        filesToBackup[file] = prevFoundFiles[file]
        print 'Found file from previous search: '
        print '   '+ file + ' in: ' + prevFoundFiles[file]
    #then search through the directories
    else:
        print 'Searching directories for file: ' + file
        targetFilesToBackup = find_all(file, destpath)
        print str(len(targetFilesToBackup)) + ' File(s) Found'
        if len(targetFilesToBackup) > 1:
            print 'WARNING: Multiple files found; using the first file'
        if len(targetFilesToBackup) > 0:
            filesToBackup[file] = targetFilesToBackup.pop(0)
            prevFoundFiles[file] = filesToBackup[file]
            print 'Added '+prevFoundFiles[file]
            print '   to previous search results, to speed future searches.'

print 'Saving Updates to Previous Search Results File:'
store_file_list_to_dict_file(backuppath+'/'+previoussearchfilename,
                             prevFoundFiles)

print 'Backing Up Files:'
for file in filesToBackup:
    copy_one_file(filesToBackup[file], backuppath)

print 'Removing Files from Destination:'
for file in filesToBackup:
    fileAttributes = os.stat(filesToBackup[file])[0]
    if (not fileAttributes & stat.S_IWRITE):
        # File is read-only, so make it writeable
        chmod(filesToBackup[file], stat.S_IWRITE)
    remove(filesToBackup[file])
    print filesToBackup[file]

print 'Copying in New Files:'
for file in filesToBackup:
    copy_one_file(srcpath+'/'+file, filesToBackup[file])
print 'Dekimashita!'
