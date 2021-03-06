import os

class GoogleDrive():
  def __init__(self, path = "drive"):
    # Install the PyDrive wrapper & import libraries.
    # This only needs to be done once in a notebook.
    !pip install -U -q PyDrive
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    from google.colab import auth
    from oauth2client.client import GoogleCredentials

    # Authenticate and create the PyDrive client.
    # This only needs to be done once in a notebook.
    auth.authenticate_user()
    gauth = GoogleAuth()
    gauth.credentials = GoogleCredentials.get_application_default()
    self._drive = GoogleDrive(gauth)
    self.path = path
    if os.path.isdir(path):
      print("{} already exists".format(path))
    else:
      os.mkdir(path)

  def load(self, parentId, parent):
    files = self._drive.ListFile({'q': "'{}' in parents".format(parentId)}).GetList()
    if not parent:
      parent = parentId
    
    path = '/'.join([self.path, parent])
    if not os.path.isdir(path):
      os.mkdir(path)
    
    for file in files:
      title = file['title']
      path = '/'.join([self.path, parent, title])
      print ("Saving {} in {}".format(title, path))
      file.GetContentFile(path)
  
  def save(self, source = "results", target = "1Twv_oBTB_P9aQ7VWinMOwsLScj6N8Hfc"):
    if not os.path.isdir(source):
      print ("Please provide a valid path to save in google drive")
    
    for title in os.listdir(source):
      path = '/'.join([source, title])
      if not os.path.isdir(path):
        dFile = self._drive.CreateFile({'title': title, "parents": [{"id": target}]})
        dFile.SetContentFile(path)
        dFile.Upload()
        print('Uploaded file with ID {}'.format(dFile.get('id')))
      
# Test
g = GoogleDrive()
g.load("1s5tKKGpwkL7jSCqD96oiMMEnxeG0SIxN", "UniqueGraphs")
g.save("drive/UniqueGraphs")