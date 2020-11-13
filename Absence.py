# Üks puudmine
class Absence:
    def __init__(self, raw_obj):
        self.parse(raw_obj)

    def parse(self, raw_obj):
        self.raw_obj = raw_obj
        self.id = raw_obj.get("id", None)
        self.lesson_date = raw_obj.get("lessonDate", None)
        self.lesson_number = raw_obj.get("lessonNumber", None)
        self.lesson_event_id = raw_obj.get("lessonEventId", None)
        self.code = raw_obj.get("code", None)
        self.code_explanation = raw_obj.get("codeExplanation", None)
        self.subject_name = raw_obj.get("subjectName", None)
        self.order_seq = raw_obj.get("orderSeq", None)
        self.teacher_name = raw_obj.get("teacherName", None)
        self.inserted_timestamp = raw_obj.get("insertedTimestamp", None)
        self.reason = raw_obj.get("reason", None)
        self.lateness = raw_obj.get("lateness", None)