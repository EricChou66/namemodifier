import re
import os
import shutil


# Covert file_ext string to list
def gen_ext_list(file_ext):
    return file_ext.split(',')


# Validate if folder is exist
def folder_exist(path):
    return os.path.isdir(path)


# Validate if file is exist
def file_exist(path):
    return os.path.isfile(path)


# Split the original_filename by "{" and "}"
# And escape regex character . ^ $ * + ? { } [ ] \ | ( )
def split_escape(filename):
    # deal with mulitple '{' '}'
    try:
        tmp = filename.rpartition("{")
        left = tmp[0]
        right = tmp[2].split("}", 1)[1]
        return re.compile(re.escape(left)+r'(\d+)'+re.escape(right))
    except:
        return re.compile(r'(\d+)\D*$')

# Change files name upder specific folder
def change_files_in_folder(original_folder, original_filename, new_folder,
                           new_filename, removeflag, samefolderflag,
                           skipdupflag, file_ext):
    # Duplicate file name counter
    dup_cnt = 1
    # Complex new filename(including "{}" to indicate the number's position)
    comp_newname = False
    # In normal mode, find the last occurance number
    find_pattern = re.compile(r'{.*}')
    if(find_pattern.search(new_filename)):
        comp_newname = True
    # If the original filename is empty
    if(original_filename == ""):
        find_pattern = re.compile(r'(\d+)\D*$')
    # else if the original filename containing "{}" to indicate the number's
    # position
    else:
        find_pattern = split_escape(original_filename)
        print(find_pattern)

    # loop all files under original folder
    for filename in os.listdir(original_folder):
        if(filename.startswith('.')):
            continue
        # check if file type in file_ext list
        filetype = filename.split('.')[-1]
        ext_list = gen_ext_list(file_ext)
        if(filetype not in ext_list):
            continue
        m = re.search(find_pattern, filename)
        if(m == None):
            continue
        try:
            num = m.group(1).strip('{}')
        except IndexError:
            continue
        folder_path = original_folder
        old_name = os.path.join(folder_path, filename)
        # if the output in same folder is checked
        if not samefolderflag:
            folder_path = new_folder
        # extract the number from "{}"
        if(comp_newname):
            tmp_name = re.sub(r'{.*}', (num), new_filename)
        else:
            tmp_name = "%s%s"%(new_filename, num)
        new_name = os.path.join(folder_path, "%s.%s"%(tmp_name, filetype))

        # if file is duplicate, force to add 1 after the new name
        isdup = False
        while(True):
            if(file_exist(new_name)):
                isdup = True
                if(skipdupflag):
                    break
                new_name = os.path.join(folder_path,  tmp_name + "(%s).%s"%(dup_cnt, filetype))
                dup_cnt += 1
            else:
                break
        dup_cnt = 1
        if(isdup and skipdupflag):
            continue
        else:
            # keep the original file
            if not removeflag:
                shutil.copy2(old_name, new_name)
            # rename file
            else:
                os.rename(old_name, new_name)
