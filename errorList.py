from error import *

class errorList(object):
    error_list = []
    def __init__(self):
        error_list = []

    #Scans through err_list and returns number of times we've encountered the error
    def get_num_errors(self, sensor_id):
        #Named tuple for tracking sensors that exceed thresholds

        #Possibly add an updated time to the tuple and compare to current time
        #If the time elapsed has exceeded 2 minutes, resets

        for error in self.error_list:
            if error.sensor_id == sensor_id:
                error.num_errors = error.num_errors + 1
                print (error.num_errors)
                return error.num_errors
        error = Error(sensor_id=sensor_id, num_errors=1, critical_error=False)
        self.error_list.append(error)
        return 1

    #Removes an error from the list
    def reset_num_errors(self, sensor_id):

        for error in self.error_list:
            if error.sensor_id == sensor_id:
                self.error_list.remove(error)
        return 1


    #Sets an error to critical
    def set_critical_error(self, sensor_id):

        for error in self.error_list:
            if error.sensor_id == sensor_id:
                error.critical_error = True
        return 1
    
    #Checks all errors in list to see if any have exceeded the range
    def check_critical_errors(self):

        for error in self.error_list:
            if error.critical_error == True:
                return True
        return False