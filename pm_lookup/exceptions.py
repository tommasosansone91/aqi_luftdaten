
class UnknownPollutantException(Exception):

    def __init__(self, pollutant_name, pollutant_labels):
        message = "The pollutant '{}' is unknown. Please choose one among: {}".format(pollutant_name, pollutant_labels)
        super().__init__(message)
