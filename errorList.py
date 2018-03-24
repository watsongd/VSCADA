from error import *

class errorList(object):
    error_list = []
    def __init__(self):
        error_list = []

    #Scans through err_list and returns number of times we've encountered the error
    def get_num_errors(self, name):
        #Named tuple for tracking sensors that exceed thresholds

        #Possibly add an updated time to the tuple and compare to current time
        #If the time elapsed has exceeded 2 minutes, resets

        for error in self.error_list:
            if error.name == name:
                error.num_errors = error.num_errors + 1
                print (error.num_errors)
                return error.num_errors
        error = Error(name=name, num_errors=1)
        self.error_list.append(error)
        return 1

    #Removes an error from the list
    def reset_num_errors(self, name):
        #Named tuple for tracking sensors that exceed thresholds

        #Possibly add an updated time to the tuple and compare to current time
        #If the time elapsed has exceeded 2 minutes, resets

        for error in self.error_list:
            if error.name == name:
                self.error_list.remove(error)
        return 1