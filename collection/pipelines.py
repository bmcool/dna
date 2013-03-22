
class DjangoModelPipeline(object):
    def process_item(self, item, spider):
        source = item['django_model']
        source.save()
