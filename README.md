# namemodifier

### description: 

- Modify a series of file's name for a specific file type

- File name must contain a number

- for example: XXXX01.mp4 -> GOT S1 01.mp4

### usage: ```./namemodifier.py [-h] [-n filename] [-t file_type] [-l file_location]```

- "-h" for help 

- "-n" the file name that you want to change to(not include the number)

- "-t" the specific file type that you want to change

- "-l" the specific location of the files(a folder)
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
"namemodifier.py" 49L, 1653C
 + README.md  namemodifier.py                                                                                X
 17         if(filetype != None) and (filenames.endswith(filetype)):
 18             pass
 19         else:
 20             continue
 21         m = re.search(find_pattern, filenames)
 22         if(m == None):
 23             continue
 24         num = m.group(0)
 25         new_name = ""
 26         if(filename != None):
 27             new_name = "%s_%s.%s"%(filename,num,filetype)
 28         else:
 29             new_name = "%s.%s"%(num,filetype)
 30         os.rename(filenames,new_name)
 31     return
 32
 33 if __name__ == '__main__':
 34     progname = 'namemodifier.py'
 35     usage_content = "%s [-h] [-n filename] [-t file_type] [-l file_location]"%(progname)
 36     parser = argparse.ArgumentParser(prog=progname, usage=usage_content, add_help = False)
 37     parser.add_argument('-h', help='print help', action='store_true')
 38     parser.add_argument('-n', type=str, help='filename')
 39     parser.add_argument('-l', type=str, help='file_location')
 40     parser.add_argument('-t', type=str, help='file_type')
 41     args = parser.parse_args()
 42     if (args.h == True):
 43         parser.print_help()
 44         exit()
 45     if (args.t == None):
 46         print('you must specify the file type')
 47         exit()
 48     change_name(args.n, args.t, args.l)
 49
 + README.md  namemodifier.py                                                                                X
  1 # namemodifier
  2
  3
  4 ### usage: ./namemodifier.py [-h] [-n filename] [-t file_type] [-l file_location]"%(progname)
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
 + README.md  namemodifier.py                                                                                X
  1 #!/usr/bin/python3
  2
  3 import sys, os, argparse, re
  4
  5 def change_name(filename, filetype, location):
  6     filetype = filetype.strip('.\n\t\r')
  7     print(filetype)
  8     if (location == None):
  9         location = '.'
 10     else:
 11         #path = os.path.abspath(location)
 12         if(os.path.isdir(location) != True):
 13             print('The location you input is not exist, please check it')
 14             exit()
 15     find_pattern = re.compile(r'(\d+)')
 16     for filenames in os.listdir(location):
 17         if(filetype != None) and (filenames.endswith(filetype)):
 18             pass
 19         else:
 20             continue
 21         m = re.search(find_pattern, filenames)
 22         if(m == None):
 23             continue
 24         num = m.group(0)
 25         new_name = ""
 26         if(filename != None):
 27             new_name = "%s_%s.%s"%(filename,num,filetype)
 28         else:
 29             new_name = "%s.%s"%(num,filetype)
 30         os.rename(filenames,new_name)
 31     return
 32
 33 if __name__ == '__main__':
 + README.md  namemodifier.py                                                                                X
  1 # namemodifier
  2
  3 ### description: This
  4
  5 ### usage: ```./namemodifier.py [-h] [-n filename] [-t file_type] [-l file_location]```
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
-- VISUAL --                                                                                       5description: This

### usage: ```./namemodifier.py [-h] [-n filename] [-t file_type] [-l file_location]```
