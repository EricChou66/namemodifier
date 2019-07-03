import re
import os

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
                           new_filename, complexflag, samefolderflag,
                           skipdupflag):
    dup_cnt = 1
    comp_newname = False
    # In normal mode, find the last occurance number
    find_pattern = re.compile(r'{.*}')
    if(find_pattern.search(new_filename)):
        comp_newname = True
    if(not complexflag):
        find_pattern = re.compile(r'(\d+)\D*$')
    else:
        left = original_filename.split("{")[0]
        right = original_filename.split("}")[-1]
        find_pattern = re.compile(left+r'(\d+)'+right)

    for filename in os.listdir(original_folder):
        if(filename.startswith('.')):
            continue
        filetype = filename.split('.')[-1]
        m = re.search(find_pattern, filename)
        if(m == None):
            continue
        num = m.group(1).strip('{}')
        folder_path = original_folder
        old_name = folder_path + "/" + filename
        if not samefolderflag:
            folder_path = new_folder
        if(comp_newname):
            tmp_name = re.sub(r'{.*}', (num), new_filename)
            print(tmp_name)
        else:
            tmp_name = "%s%s"%(new_filename, num)
        new_name = folder_path + "/" + "%s.%s"%(tmp_name, filetype)
        isdup = False
        while(True):
            if(file_exist(new_name)):
                isdup = True
                if(skipdupflag):
                    break
                new_name = folder_path + "/" + tmp_name + "(%s).%s"%(dup_cnt, filetype)
                dup_cnt += 1
            else:
                break
        if(isdup and skipdupflag):
            continue
        else:
            os.rename(old_name, new_name)


# Change files name upder specific folder
def change_srt_files_in_folder(original_folder, original_filename, new_folder,
                           new_filename, complexflag, samefolderflag,
                           skipdupflag):
    dup_cnt = 1
    comp_newname = False
    # In normal mode, find the last occurance number
    find_pattern = re.compile(r'{.*}')
    if(find_pattern.search(new_filename)):
        comp_newname = True
    if(not complexflag):
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
        old_name = folder_path + "/" + filename
        if not samefolderflag:
            folder_path = new_folder
        if(comp_newname):
            tmp_name = re.sub(r'{.*}', str(num), new_filename)
        else:
            tmp_name = "%s%s"%(new_filename, num)
        new_name = folder_path + "/" + "%s.%s"%(tmp_name, filetype)
        isdup = False
        while(True):
            if(file_exist(new_name)):
                isdup = True
                if(skipdupflag):
                    break
                new_name = folder_path + "/" + tmp_name + "(%s).%s"%(dup_cnt, filetype)
                dup_cnt += 1
            else:
                break
        if(isdup and skipdupflag):
            continue
        else:
            os.rename(old_name, new_name)

