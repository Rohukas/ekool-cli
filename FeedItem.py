# Üks voo element. Näiteks hinne või teade
class FeedItem:
    def __init__(self, raw_obj):
        self.parse(raw_obj)

    def parse(self, raw_obj):
        self.raw_obj = raw_obj
        self.id = raw_obj.get("id", None)
        self.order_seq = raw_obj.get("orderSeq", None)
        self.last_modified = raw_obj.get("lastModified", None)
        self.item_type = raw_obj.get("itemType", None)
        self.action_type = raw_obj.get("actionType", None)
        self.hot = raw_obj.get("hot", None)
        self.grade_type_id = raw_obj.get("gradeTypeId", None)
        self.grade_type_additional_desc = raw_obj.get("gradeTypeAdditionalDesc", None)
        self.grade = raw_obj.get("abbr", None)
        self.title = raw_obj.get('title', None)
        self.author_name = raw_obj.get("authorName", None)
        self.lesson_date = raw_obj.get("lessonDate", None)
        self.subject_name = raw_obj.get("subjectName", None)
        self.subject_id = raw_obj.get("subjectId", None)
        self.term_name = raw_obj.get("termName", None)
        self.content = raw_obj.get("content", None)
        self.text_content = raw_obj.get("textContent", None)
        self.has_statistics = raw_obj.get("hasStatistics", None)
        self.test = raw_obj.get("test", None)
        self.amendment = raw_obj.get("amendment", None)