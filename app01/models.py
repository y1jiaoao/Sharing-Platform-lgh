from django.db import models
from mongoengine import *

class Project(models.Model):
    project_id = models.AutoField(db_column='Project_id', primary_key=True)  # Field name made lowercase.
    project_name = models.CharField(db_column='Project_name', max_length=255)  # Field name made lowercase.
    institute = models.CharField(db_column='Institute', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direction = models.CharField(db_column='Direction', max_length=255, blank=True, null=True)  # Field name made lowercase.
    introduction = models.CharField(db_column='Introduction', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    experts = models.CharField(db_column='Experts', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Project'


class TMessage(models.Model):
    index = models.BigAutoField(db_column='Index', primary_key=True)  # Field name made lowercase.
    receive_id = models.IntegerField(db_column='Receive_id')  # Field name made lowercase.
    request_id = models.IntegerField(db_column='Request_id')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255, blank=True, null=True)  # Field name made lowercase.
    request_date = models.DateTimeField(db_column='Request_date')  # Field name made lowercase.
    send_date = models.DateTimeField(db_column='Send_date')  # Field name made lowercase.
    state = models.PositiveIntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_message'


class Account(models.Model):
    user_id = models.AutoField(primary_key=True)
    type = models.IntegerField(default=1)
    user_name = models.CharField(unique=True, max_length=22)
    password = models.CharField(max_length=22)
    real_name = models.CharField(max_length=22, blank=True, null=True)
    tel = models.CharField(max_length=22, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    basic_info = models.CharField(max_length=255, blank=True, null=True)
    money = models.FloatField(default=0.0)

    class Meta:
        managed = False
        db_table = 'account'
'''
class EssayAuthor(Document):
    name = StringField()
    org = StringField()
    id = StringField()

class Essay(Document):
    _id = IntField(primary_key=True)
    id = StringField()
    title = StringField()
    authors = ListField(ReferenceField(EssayAuthor))
    year = IntField()
    keywords = ListField(StringField())
    n_citation = IntField()
    page_start = StringField()
    page_end = StringField()
    lang = StringField()
    volume = StringField()
    issue = StringField()
    doi = StringField()
    url = ListField(StringField())
    abstract = StringField()
    clicks = DecimalField()
    downloads = DecimalField()
    meta = {'collection': 'papers'}
'''
class Essay(models.Model):
    paper_id = models.AutoField(db_column='Paper_id', primary_key=True)  # Field name made lowercase.
    paper_name = models.CharField(db_column='Paper_name', max_length=255)  # Field name made lowercase.
    author_id = models.IntegerField(db_column='Author_id')  # Field name made lowercase.
    author_name = models.CharField(db_column='Author_name', max_length=255)  # Field name made lowercase.
    research_areas = models.CharField(db_column='Research_areas', max_length=255, blank=True, null=True)  # Field name made lowercase.
    introduction = models.CharField(db_column='Introduction', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    institute = models.CharField(db_column='Institute', max_length=255, blank=True, null=True)  # Field name made lowercase.
    openness = models.PositiveIntegerField(db_column='Openness')  # Field name made lowercase.
    public_content = models.CharField(db_column='Public_content', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    published_time = models.DateField(db_column='Published_time', blank=True, null=True)  # Field name made lowercase.
    times_cited = models.PositiveIntegerField(db_column='Times_cited', blank=True, null=True)  # Field name made lowercase.
    price = models.PositiveIntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=8)  # Field name made lowercase.
    download_link = models.CharField(db_column='Download_link', max_length=255, blank=True, null=True)  # Field name made lowercase.
    download_times = models.PositiveIntegerField(db_column='Download_times', blank=True, null=True)  # Field name made lowercase.
    document_id = models.CharField(db_column='Document_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    keywords = models.CharField(db_column='keywords', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='clicks')
    db = models.CharField(db_column='db', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cssci = models.CharField(db_column='cssci', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'essay'
'''
class ExpertTag(Document):
    w = IntField()
    t = StringField()
class ExpertPub(Document):
    i = StringField()
    r = IntField()
class Expert(Document):
    _id = IntField(primary_key=True)
    id = StringField()
    name = StringField()
    h_index = IntField()
    h_pubs = IntField()
    tags = ListField(ReferenceField(ExpertTag))
    n_citation = IntField()
    pubs = ListField(ReferenceField(ExpertPub))
    institute = ListField(StringField())
    meta = {'collections': 'expert'}
'''
class Expert(models.Model):
    expert_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    institute = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    direction = models.CharField(max_length=255, blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expert'



class Feedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    send = models.IntegerField(db_column='send_id')
    content = models.CharField(db_column='content',max_length=1015, blank=True, null=True)
    send_date = models.DateTimeField(db_column='send_date')

    class Meta:
        managed = False
        db_table = 'feedback'


class Message(models.Model):
    index = models.BigAutoField(primary_key=True)
    send = models.ForeignKey(Account, related_name='sender', on_delete=models.CASCADE)
    receive = models.ForeignKey(Account, related_name='receiver', on_delete= models.CASCADE)
    content = models.CharField(db_column='Content', max_length=1015, blank=True,
                               null=True)  # Field name made lowercase.
    send_date = models.DateTimeField()
    state = models.PositiveIntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255)  # Field name made lowercase.
    send_name = models.CharField(db_column='send_name', max_length=22)

    class Meta:
        managed = False
        db_table = 'message'


class MessageText(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=4096, blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'message_text'


class Patent(models.Model):
    patent_id = models.AutoField(db_column='Patent_id', primary_key=True)  # Field name made lowercase.
    patent_name = models.CharField(db_column='Patent_name', max_length=255)  # Field name made lowercase.
    author_id = models.IntegerField(db_column='Author_id')  # Field name made lowercase.
    author_name = models.CharField(db_column='Author_name', max_length=255)  # Field name made lowercase.
    research_areas = models.CharField(db_column='Research_areas', max_length=255, blank=True, null=True)  # Field name made lowercase.
    introduction = models.CharField(db_column='Introduction', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    institute = models.CharField(db_column='Institute', max_length=255, blank=True, null=True)  # Field name made lowercase.
    openness = models.PositiveIntegerField(db_column='Openness')  # Field name made lowercase.
    public_number = models.CharField(db_column='Public_number', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    published_time = models.DateField(db_column='Published_time', blank=True, null=True)  # Field name made lowercase.
    owner_id = models.IntegerField(db_column='Owner_id')  # Field name made lowercase.
    owner_name = models.CharField(db_column='Owner_name', max_length=255)  # Field name made lowercase.
    price = models.PositiveIntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=8)  # Field name made lowercase.
    download_link = models.CharField(db_column='Download_link', max_length=255, blank=True, null=True)  # Field name made lowercase.
    download_times = models.PositiveIntegerField(db_column='Download_times', blank=True, null=True)  # Field name made lowercase.
    document_id = models.CharField(db_column='Document_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='department', max_length=255, blank=True, null=True)
    appliant = models.CharField(db_column='appliant', max_length=255, blank=True, null=True)
    keywords = models.CharField(db_column='keywords', max_length=255, blank=True, null=True)
    address = models.CharField(db_column='address', max_length=255, blank=True, null=True)
    agent = models.CharField(db_column='agent', max_length=255, blank=True, null=True)
    agency = models.CharField(db_column='agency', max_length=255, blank=True, null=True)
    code = models.IntegerField(db_column='code')
    sovereignty = models.CharField(db_column='sovereignty', max_length=2000, blank=True, null=True)
    page = models.IntegerField(db_column='page')
    main_cls_num = models.CharField(db_column='main_cls_num', max_length=255, blank=True, null=True)
    patent_cls_num = models.CharField(db_column='patent_cls_num', max_length=255, blank=True, null=True)
    app_num = models.CharField(db_column='app_num', max_length=255, blank=True, null=True)
    app_date = models.DateField(db_column='app_date', blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='clicks')
    source = models.CharField(db_column='Source', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'patent'


class Collect(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)  # Field name made lowercase.
    user_id = models.IntegerField(db_column='user_id')
    collection_id = models.IntegerField(db_column='collection_id')
    collection_name = models.CharField(db_column='collection_name', max_length=255)
    type = models.CharField(db_column='type', max_length=11)

    class Meta:
        managed = False
        db_table = 'collect'


class Identify(models.Model):
    id = models.BigAutoField(primary_key=True)
    identify_user = models.IntegerField()
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    institute = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    direction = models.CharField(max_length=255)
    introduction = models.CharField(max_length=255)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'identify'


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=11)
    comment_name = models.CharField(max_length=22)
    resource_id = models.IntegerField()
    comment_date = models.DateTimeField()
    content = models.CharField(max_length=1015)

    class Meta:
        managed = False
        db_table = 'comment'


class Hotspot(models.Model):
    num = models.IntegerField(blank=True, null=True)
    keyword = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'hotspot'
