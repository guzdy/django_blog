from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    #  django haystack 的规定。要相对某个 app 下的数据进行全文检索，
    # 就要在该 app 下创建一个 search_indexes.py 文件，
    # 然后创建一个 XXIndex 类（XX 为含有被检索数据的模型，如这里的 Post），
    # 并且继承 SearchIndex 和 Indexable

    # 索引就像是一本书的目录，可以为读者提供更快速的导航与查找。
    # 在这里也是同样的道理，当数据量非常大的时候，
    # 若要从这些数据里找出所有的满足搜索条件的几乎是不太可能的，
    # 将会给服务器带来极大的负担。所以我们需要为指定的数据添加一个索引（目录）
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().published.all()
