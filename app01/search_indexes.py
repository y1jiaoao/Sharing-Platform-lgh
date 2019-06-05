from haystack import indexes
# 修改此处，为你自己的model
from app01.models import Essay, Patent, Expert


# 修改此处，类名为模型类的名称+Index，比如模型类为GoodsInfo,则这里类名为GoodsInfoIndex
# class AccountIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     # author = indexes.CharField(model_attr='user')
#     # pub_date = indexes.DateTimeField(model_attr='pub_date')
#     # user_name = indexes.CharField(model_attr='user_name')
#     # basic_info = indexes.CharField(model_attr='basic_info')
#
#     def get_model(self):
#         # 修改此处，为你自己的model
#         return Account
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.all()


# 修改此处，类名为模型类的名称+Index，比如模型类为GoodsInfo,则这里类名为GoodsInfoIndex
class EssayIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # author = indexes.CharField(model_attr='user')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')
    # user_name = indexes.CharField(model_attr='user_name')
    # basic_info = indexes.CharField(model_attr='basic_info')

    def get_model(self):
        # 修改此处，为你自己的model
        return Essay

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class PatentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # author = indexes.CharField(model_attr='user')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')
    # user_name = indexes.CharField(model_attr='user_name')
    # basic_info = indexes.CharField(model_attr='basic_info')

    def get_model(self):
        # 修改此处，为你自己的model
        return Patent

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class ExpertIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # author = indexes.CharField(model_attr='user')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')
    # user_name = indexes.CharField(model_attr='user_name')
    # basic_info = indexes.CharField(model_attr='basic_info')

    def get_model(self):
        # 修改此处，为你自己的model
        return Expert

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
