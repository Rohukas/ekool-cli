from Absence import Absence

# Puudumiste class
class Absences:
    def __init__(self, raw_obj):
        self.parse(raw_obj)
    def parse(self, raw_obj):
        self.absences = []
        for absence_raw in raw_obj:
            self.absences.append(Absence(absence_raw))
