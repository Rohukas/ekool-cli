from Assignment import Assignment

# Kindlas ajavahemikus olevad kodutööd
class AssignmentTimeframe:
    def __init__(self,raw_obj):
        self.parse(raw_obj)


    def parse(self, raw_obj):
        self.start_date = raw_obj["startDate"]
        self.end_date = raw_obj["endDate"]
        self.week_no = raw_obj["weekNo"]
        self.order_timestamp_long = raw_obj["orderTimestampLong"]

        self.assignments = []
        # Lisame kõik kodutood jarjendisse
        for event in raw_obj["eventList"]:
            event = Assignment(event)
            self.assignments.append(event)

