# Ühe kodutöö class
class Assignment:
    def __init__(self, obj):
        self.raw_obj = obj
        self.parse_assignment(obj)


    def parse_assignment(self, json_obj):
        self.author = json_obj.get("authorName", None)
        self.title = json_obj.get("title", None)
        self.order_timestamp_long = json_obj.get("orderTimestampLong", None)
        self.content = json_obj.get("content", None)
        self.comments = json_obj.get("comments", None)
        self.url = json_obj.get("url",None)
        self.id = json_obj.get("id",None)
        self.is_hot = json_obj.get("isHot", None)
        self.subject_name = json_obj.get("subjectName",None)
        self.deadLine = json_obj.get("deadLine")
        self.added = json_obj.get("added")
        self.is_done = json_obj.get("isDone",None)
        self.is_test = json_obj.get("isTest", None)
        self.is_graded = json_obj.get("isGraded", None)
        self.teacher_attachments = json_obj.get("teacherAttachments", None)
        self.type_id = json_obj.get("typeId",None)

