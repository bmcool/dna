
from scrapy.item import Item, Field

class DjangoItem(Item):
    django_model = Field()
