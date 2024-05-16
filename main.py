import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# List contents
def contents_list(folder_id):
   return drive.ListFile({'q' : f"'{folder_id}' in parents and trashed=false"}).GetList()

# Download files
def download_files(file,path):
   file.GetContentFile(path+'\\'+file['title'])

# to check content is file or folder
def is_folder(content):
   if str(content['mimeType']).endswith('.folder'):
      return True
   else:
      return False


# oscillatory_functions
def left(content,dest):
   if is_folder(content):
      dest+= '\\'+content['title']
      os.mkdir(dest)
      content_list = contents_list(content['id'])
      for content in content_list:
         right(content,dest)
   else:
      download_files(content, dest)

def right(content,dest):
   if is_folder(content):
      dest+= '\\'+content['title']
      os.mkdir(dest)
      content_list = contents_list(content['id'])
      for content in content_list:
         left(content,dest)
   else:
      download_files(content, dest)

def mid(folder_id,dest):
   contents = contents_list(folder_id)
   for content in contents:
      left(content,dest)


destination = input('enter destination: ')
with open('urls.txt','r') as f:
   for line in f:
      # try:
         stripped_line = line.strip().split('*#@')
         f_id = stripped_line[0]
         dest = destination+'\\'+stripped_line[1]
         os.mkdir(dest)
         mid(f_id,dest)
      # except Exception as e:
      #    print(e)


