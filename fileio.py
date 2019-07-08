import re
import os
import shutil

video_filetype = ['avi', 'mp4', 'wmv', 'flv', 'm4a']

sub_filetype = ['srt', 'ass', 'ssa']

# Validate if folder is exist
def folder_exist(path):
    return os.path.isdir(path)

# Validate if file is exist
def file_exist(path):
    return os.path.isfile(path)

# Change files name upder specific folder
def change_files_in_folder(original_folder, original_filename, new_folder,
                           new_filename, removeflag, samefolderflag,
                           skipdupflag):
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
        left = original_filename.split("{")[0]
        right = original_filename.split("}")[-1]
        find_pattern = re.compile(left+r'(\d+)'+right)

    # loop all files under original folder
    for filename in os.listdir(original_folder):
        if(filename.startswith('.')):
            continue
        filetype = filename.split('.')[-1]
        m = re.search(find_pattern, filename)
        if(m == None):
            continue
        num = m.group(1).strip('{}')
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


# Change files name upder specific folder
def change_srt_files_in_folder(original_folder, original_filename, new_folder,
                           new_filename, removeflag, samefolderflag,
                           skipdupflag):
    dup_cnt = 1
    comp_newname = False
    # In normal mode, find the last occurance number
    find_pattern = re.compile(r'{.*}')
    if(find_pattern.search(new_filename)):
        comp_newname = True
    if(original_filename == ""):
        find_pattern = re.compile(r'(\d+)\D*$')
    else:
        left = original_filename.split("{")[0]
        right = original_filename.split("}")[-1]
        find_pattern = re.compile(left+r'(\d+)'+right)

    for filename in os.listdir(original_folder):
        filetype = filename.split('.')[-1]
        if not (filetype in sub_filetype):
            continue
        m = re.search(find_pattern, filename)
        num = m.group(1)
        folder_path = original_folder
        old_name = os.path.join(folder_path, filename)
        if not samefolderflag:
            folder_path = new_folder
        if(comp_newname):
            tmp_name = re.sub(r'{.*}', str(num), new_filename)
        else:
            tmp_name = "%s%s"%(new_filename, num)
        new_name = os.path.join(folder_path, "%s.%s"%(tmp_name, filetype))
        isdup = False
        while(True):
            if(file_exist(new_name)):
                isdup = True
                if(skipdupflag):
                    break
                new_name = os.path.join(folder_path, tmp_name + "(%s).%s"%(dup_cnt, filetype))
                dup_cnt += 1
            else:
                break
        dup_cnt = 1
        if(isdup and skipdupflag):
            continue
        else:
            if not removeflag:
                shutil.copy2(old_name, new_name)
            else:
                os.rename(old_name, new_name)
