class Training:

    def __init__(self, id,
                 model_id,
                 date,
                 utilised_columns,
                 modified_columns,
                 parameters_vector,
                 model_body,
                 weights):
        self.id = id
        self.model_id = model_id
        self.date = str(date)
        self.utilised_columns = utilised_columns
        self.modified_columns = modified_columns
        self.parameters_vector = parameters_vector
        self.model_body = model_body
        self.weights = weights
