#This script open the file in a list

import cataliistSanitizer

class AtheleteList(list):
    def __init__(self,a_name,a_dob=None,a_times=[]):
        list.__init__([])
        self.name = a_name
        self.dob = a_dob
        self.extend(a_times)

    def top3(self):
        return(sorted(set([cataliistSanitizer.sanitize(each) for each in self]))[0:3])



def filePicker(file):
    try:
        with open(file) as fh:
            data = fh.readline().strip().split(',')
            return(AtheleteList(data.pop(0),data.pop(0),data))
    except IOError as err:
        print("File Error" +str(err))
        return(None)  
