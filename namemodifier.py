#!/usr/bin/python3

import sys, os, argparse, re

def change_name(filename, filetype, location):
    filetype = filetype.strip('.\n\t\r')
    print(filetype)
    if (location == None):
        location = '.'
    else:
        #path = os.path.abspath(location)
        if(os.path.isdir(location) != True):
            print('The location you input is not exist, please check it')
            exit()
    find_pattern = re.compile(r'(\d+)')
    for filenames in os.listdir(location):
        if(filetype != None) and (filenames.endswith(filetype)):
            pass
        else:
            continue
        m = re.search(find_pattern, filenames)
        if(m == None):
            continue
        num = m.group(0)
        new_name = ""
        if(filename != None):
            new_name = "%s_%s.%s"%(filename,num,filetype)
        else:
            new_name = "%s.%s"%(num,filetype)
        os.rename(filenames,new_name)
    return

if __name__ == '__main__':
    progname = 'namemodifier.py'
    usage_content = "%s [-h] [-n filename] [-t file_type] [-l file_location]"%(progname)
    parser = argparse.ArgumentParser(prog=progname, usage=usage_content, add_help = False)
    parser.add_argument('-h', help='print help', action='store_true')
    parser.add_argument('-n', type=str, help='filename')
    parser.add_argument('-l', type=str, help='file_location')
    parser.add_argument('-t', type=str, help='file_type')
    args = parser.parse_args()
    if (args.h == True):
        parser.print_help()
        exit()
    if (args.t == None):
        print('you must specify the file type')
        exit()
    change_name(args.n, args.t, args.l)
    
