class TrainingResponse:
    def __init__(self, model,
                 utilised_columns,
                 modified_columns,
                 training):
        self.model = model
        self.utilised_columns = utilised_columns
        self.modified_columns = modified_columns
        self.training = training

    def default(self, o):
        return o.__dict__
