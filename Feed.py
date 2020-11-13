from FeedItem import FeedItem

'''
[
  {
    "id": 15168744039,
    "orderSeq": 1578034902175,
    "lastModified": "03.01.2020 09:01",
    "itemType": 1,
    "actionType": 1,
    "hot": false,
    "gradeTypeId": 18,
    "gradeTypeAdditionalDesc": null,
    "abbr": "B",
    "authorName": "Kristi Juuse",
    "lessonDate": null,
    "subjectName": "F\\u00fc\\u00fcsika",
    "subjectId": 3934750370,
    "termName": null,
    "textContent": "",
    "hasStatistics": true,
    "test": false,
    "amendment": false
  },
  {
    "id": 15168744032,
    "orderSeq": 1578034874017,
    "lastModified": "03.01.2020 09:01",
    "itemType": 1,
    "actionType": 1,
    "hot": false,
    "gradeTypeId": 5,
    "gradeTypeAdditionalDesc": null,
    "abbr": "B",
    "authorName": "Kristi Juuse",
    "lessonDate": null,
    "subjectName": "F\\u00fc\\u00fcsika",
    "subjectId": 3934750370,
    "termName": null,
    "textContent": "",
    "hasStatistics": true,
    "test": true,
    "amendment": false
  }...
]
'''
# Voo class
class Feed:
    def __init__(self, raw_obj):
        self.parse(raw_obj)


    def parse(self, raw_obj):
        self.feed = []
        for feed_item_raw in raw_obj:
            feeditem = FeedItem(feed_item_raw)
            # Ära lisa reklaame. Reklaamide ID on 20
            try:
              if (feeditem.item_type == 20):
                continue
            except:
              pass
            self.feed.append(FeedItem(feed_item_raw))


