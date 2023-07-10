class Connection:
    def __init__(self, patient_id, country, firstname, lastname, target_low, target_high):
        self.target_high = target_high
        self.target_low = target_low
        self.lastname = lastname
        self.firstname = firstname
        self.country = country
        self.patient_id = patient_id
