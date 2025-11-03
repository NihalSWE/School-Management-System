# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activities(models.Model):
    activitiesid = models.AutoField(db_column='activitiesID', primary_key=True)  # Field name made lowercase.
    activitiescategoryid = models.IntegerField(db_column='activitiescategoryID')  # Field name made lowercase.
    description = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    time_to = models.CharField(max_length=40, blank=True, null=True)
    time_from = models.CharField(max_length=40, blank=True, null=True)
    time_at = models.CharField(max_length=40, blank=True, null=True)
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'activities'


class Activitiescategory(models.Model):
    activitiescategoryid = models.AutoField(db_column='activitiescategoryID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=255)
    fa_icon = models.CharField(max_length=40, blank=True, null=True)
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'activitiescategory'


class Activitiescomment(models.Model):
    activitiescommentid = models.AutoField(db_column='activitiescommentID', primary_key=True)  # Field name made lowercase.
    activitiesid = models.IntegerField(db_column='activitiesID')  # Field name made lowercase.
    comment = models.TextField()
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'activitiescomment'


class Activitiesmedia(models.Model):
    activitiesmediaid = models.AutoField(db_column='activitiesmediaID', primary_key=True)  # Field name made lowercase.
    activitiesid = models.IntegerField(db_column='activitiesID')  # Field name made lowercase.
    attachment = models.TextField()
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'activitiesmedia'


class Activitiesstudent(models.Model):
    activitiesstudentid = models.AutoField(db_column='activitiesstudentID', primary_key=True)  # Field name made lowercase.
    activitiesid = models.IntegerField(db_column='activitiesID')  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'activitiesstudent'


class Addons(models.Model):
    addonsid = models.AutoField(db_column='addonsID', primary_key=True)  # Field name made lowercase.
    package_name = models.CharField(max_length=180, blank=True, null=True)
    slug = models.CharField(max_length=180, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    version = models.CharField(max_length=11, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    init = models.TextField(blank=True, null=True)
    files = models.TextField(blank=True, null=True)
    preview_image = models.CharField(max_length=180, blank=True, null=True)
    date = models.DateTimeField()
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.CharField(db_column='usertypeID', max_length=100)  # Field name made lowercase.
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'addons'


class Alert(models.Model):
    alertid = models.AutoField(db_column='alertID', primary_key=True)  # Field name made lowercase.
    itemid = models.IntegerField(db_column='itemID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    itemname = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'alert'


class Asset(models.Model):
    assetid = models.AutoField(db_column='assetID', primary_key=True)  # Field name made lowercase.
    serial = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True, db_comment='Title')
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    asset_number = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    asset_condition = models.IntegerField(blank=True, null=True)
    attachment = models.TextField(blank=True, null=True)
    originalfile = models.TextField(blank=True, null=True)
    asset_categoryid = models.IntegerField(db_column='asset_categoryID', blank=True, null=True)  # Field name made lowercase.
    asset_locationid = models.IntegerField(db_column='asset_locationID', blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateField()
    modify_date = models.DateField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asset'


class AssetAssignment(models.Model):
    asset_assignmentid = models.AutoField(db_column='asset_assignmentID', primary_key=True)  # Field name made lowercase.
    assetid = models.IntegerField(db_column='assetID', db_comment='Description and title')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID', blank=True, null=True)  # Field name made lowercase.
    check_out_to = models.IntegerField()
    due_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    assigned_quantity = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    asset_locationid = models.IntegerField(db_column='asset_locationID', blank=True, null=True)  # Field name made lowercase.
    check_out_date = models.DateField(blank=True, null=True)
    check_in_date = models.DateField(blank=True, null=True)
    create_date = models.DateField()
    modify_date = models.DateField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asset_assignment'


class AssetCategory(models.Model):
    asset_categoryid = models.AutoField(db_column='asset_categoryID', primary_key=True)  # Field name made lowercase.
    category = models.CharField(max_length=255)
    create_date = models.DateField()
    modify_date = models.DateField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'asset_category'


class Assignment(models.Model):
    assignmentid = models.AutoField(db_column='assignmentID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=128)
    description = models.TextField()
    deadlinedate = models.DateField()
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    originalfile = models.TextField()
    file = models.TextField()
    classesid = models.TextField(db_column='classesID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    sectionid = models.TextField(db_column='sectionID', blank=True, null=True)  # Field name made lowercase.
    subjectid = models.TextField(db_column='subjectID', blank=True, null=True)  # Field name made lowercase.
    assignusertypeid = models.IntegerField(db_column='assignusertypeID', blank=True, null=True)  # Field name made lowercase.
    assignuserid = models.IntegerField(db_column='assignuserID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'assignment'


class Assignmentanswer(models.Model):
    assignmentanswerid = models.AutoField(db_column='assignmentanswerID', primary_key=True)  # Field name made lowercase.
    assignmentid = models.IntegerField(db_column='assignmentID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    uploaderid = models.IntegerField(db_column='uploaderID')  # Field name made lowercase.
    uploadertypeid = models.IntegerField(db_column='uploadertypeID')  # Field name made lowercase.
    answerfile = models.TextField()
    answerfileoriginal = models.TextField()
    answerdate = models.DateField()

    class Meta:
        managed = False
        db_table = 'assignmentanswer'


class Attendance(models.Model):
    attendanceid = models.AutoField(db_column='attendanceID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='sectionID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertype = models.CharField(max_length=60)
    monthyear = models.CharField(max_length=10)
    a1 = models.CharField(max_length=3, blank=True, null=True)
    a2 = models.CharField(max_length=3, blank=True, null=True)
    a3 = models.CharField(max_length=3, blank=True, null=True)
    a4 = models.CharField(max_length=3, blank=True, null=True)
    a5 = models.CharField(max_length=3, blank=True, null=True)
    a6 = models.CharField(max_length=3, blank=True, null=True)
    a7 = models.CharField(max_length=3, blank=True, null=True)
    a8 = models.CharField(max_length=3, blank=True, null=True)
    a9 = models.CharField(max_length=3, blank=True, null=True)
    a10 = models.CharField(max_length=3, blank=True, null=True)
    a11 = models.CharField(max_length=3, blank=True, null=True)
    a12 = models.CharField(max_length=3, blank=True, null=True)
    a13 = models.CharField(max_length=3, blank=True, null=True)
    a14 = models.CharField(max_length=3, blank=True, null=True)
    a15 = models.CharField(max_length=3, blank=True, null=True)
    a16 = models.CharField(max_length=3, blank=True, null=True)
    a17 = models.CharField(max_length=3, blank=True, null=True)
    a18 = models.CharField(max_length=3, blank=True, null=True)
    a19 = models.CharField(max_length=3, blank=True, null=True)
    a20 = models.CharField(max_length=3, blank=True, null=True)
    a21 = models.CharField(max_length=3, blank=True, null=True)
    a22 = models.CharField(max_length=3, blank=True, null=True)
    a23 = models.CharField(max_length=3, blank=True, null=True)
    a24 = models.CharField(max_length=3, blank=True, null=True)
    a25 = models.CharField(max_length=3, blank=True, null=True)
    a26 = models.CharField(max_length=3, blank=True, null=True)
    a27 = models.CharField(max_length=3, blank=True, null=True)
    a28 = models.CharField(max_length=3, blank=True, null=True)
    a29 = models.CharField(max_length=3, blank=True, null=True)
    a30 = models.CharField(max_length=3, blank=True, null=True)
    a31 = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attendance'


class AutomationRec(models.Model):
    automation_recid = models.AutoField(db_column='automation_recID', primary_key=True)  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    date = models.DateField()
    day = models.CharField(max_length=3)
    month = models.CharField(max_length=3)
    year = models.TextField()  # This field type is a guess.
    nofmodule = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'automation_rec'


class AutomationShudulu(models.Model):
    automation_shuduluid = models.AutoField(db_column='automation_shuduluID', primary_key=True)  # Field name made lowercase.
    date = models.DateField()
    day = models.CharField(max_length=3)
    month = models.CharField(max_length=3)
    year = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'automation_shudulu'


class Book(models.Model):
    bookid = models.AutoField(db_column='bookID', primary_key=True)  # Field name made lowercase.
    book = models.CharField(max_length=60)
    subject_code = models.TextField()
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    due_quantity = models.IntegerField()
    rack = models.TextField()

    class Meta:
        managed = False
        db_table = 'book'


class Candidate(models.Model):
    candidateid = models.AutoField(db_column='candidateID', primary_key=True)  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    verified_by = models.CharField(max_length=100)
    date_verification = models.DateField(blank=True, null=True)
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'candidate'


class Category(models.Model):
    categoryid = models.AutoField(db_column='categoryID', primary_key=True)  # Field name made lowercase.
    hostelid = models.IntegerField(db_column='hostelID')  # Field name made lowercase.
    class_type = models.CharField(max_length=60)
    hbalance = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class CertificateTemplate(models.Model):
    certificate_templateid = models.AutoField(db_column='certificate_templateID', primary_key=True)  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    name = models.CharField(max_length=60)
    theme = models.IntegerField()
    top_heading_title = models.TextField(blank=True, null=True)
    top_heading_left = models.TextField(blank=True, null=True)
    top_heading_right = models.TextField(blank=True, null=True)
    top_heading_middle = models.TextField(blank=True, null=True)
    main_middle_text = models.TextField()
    template = models.TextField()
    footer_left_text = models.TextField(blank=True, null=True)
    footer_right_text = models.TextField(blank=True, null=True)
    footer_middle_text = models.TextField(blank=True, null=True)
    background_image = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'certificate_template'


class Childcare(models.Model):
    childcareid = models.AutoField(db_column='childcareID', primary_key=True)  # Field name made lowercase.
    dropped_at = models.DateTimeField(blank=True, null=True)
    received_at = models.DateTimeField(blank=True, null=True)
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='parentID')  # Field name made lowercase.
    signature = models.TextField(blank=True, null=True)
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    comment = models.TextField(blank=True, null=True)
    received_status = models.IntegerField()
    receiver_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'childcare'


class Classes(models.Model):
    classesid = models.AutoField(db_column='classesID', primary_key=True)  # Field name made lowercase.
    classes = models.CharField(max_length=60)
    classes_numeric = models.IntegerField()
    teacherid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='teacherID')  # Field name made lowercase.
    studentmaxid = models.IntegerField(db_column='studentmaxID', blank=True, null=True)  # Field name made lowercase.
    note = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)

    def __str__(self):
        return self.classes
    
    class Meta:
        managed = False
        db_table = 'classes'


class Complain(models.Model):
    complainid = models.AutoField(db_column='complainID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=255)
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID', blank=True, null=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    attachment = models.TextField(blank=True, null=True)
    originalfile = models.TextField(blank=True, null=True)
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.
    create_date = models.DateTimeField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'complain'


class ConversationMessageInfo(models.Model):
    status = models.IntegerField(blank=True, null=True)
    draft = models.IntegerField(blank=True, null=True)
    fav_status = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'conversation_message_info'


class ConversationMsg(models.Model):
    msg_id = models.AutoField(primary_key=True)
    conversation_id = models.IntegerField()
    user_id = models.IntegerField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    msg = models.TextField()
    attach = models.TextField(blank=True, null=True)
    attach_file_name = models.TextField(blank=True, null=True)
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    start = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conversation_msg'


class ConversationUser(models.Model):
    conversation_id = models.IntegerField()
    user_id = models.IntegerField()
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    is_sender = models.IntegerField(blank=True, null=True)
    trash = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conversation_user'


class Document(models.Model):
    documentid = models.AutoField(db_column='documentID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=128, db_collation='utf8_general_ci')
    file = models.CharField(max_length=200, db_collation='utf8_general_ci')
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'document'


class Eattendance(models.Model):
    eattendanceid = models.AutoField(db_column='eattendanceID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    examid = models.IntegerField(db_column='examID')  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='sectionID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='subjectID')  # Field name made lowercase.
    date = models.DateField()
    studentid = models.IntegerField(db_column='studentID', blank=True, null=True)  # Field name made lowercase.
    s_name = models.CharField(max_length=60, blank=True, null=True)
    eattendance = models.CharField(max_length=20, blank=True, null=True)
    year = models.TextField()  # This field type is a guess.
    eextra = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eattendance'


class Ebooks(models.Model):
    ebooksid = models.AutoField(db_column='ebooksID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    authority = models.IntegerField()
    cover_photo = models.CharField(max_length=200)
    file = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'ebooks'


class Emailsetting(models.Model):
    fieldoption = models.CharField(primary_key=True, max_length=100)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'emailsetting'


class Event(models.Model):
    eventid = models.AutoField(db_column='eventID', primary_key=True)  # Field name made lowercase.
    fdate = models.DateField()
    ftime = models.TimeField()
    tdate = models.DateField()
    ttime = models.TimeField()
    title = models.CharField(max_length=128)
    details = models.TextField()
    photo = models.CharField(max_length=200, blank=True, null=True)
    create_date = models.DateTimeField()
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'event'


class Eventcounter(models.Model):
    eventcounterid = models.AutoField(db_column='eventcounterID', primary_key=True)  # Field name made lowercase.
    eventid = models.IntegerField(db_column='eventID')  # Field name made lowercase.
    username = models.CharField(max_length=40)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=128)
    photo = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField()
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'eventcounter'


class Exam(models.Model):
    examid = models.AutoField(db_column='examID', primary_key=True)  # Field name made lowercase.
    exam = models.CharField(max_length=60)
    date = models.DateField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam'


class Examschedule(models.Model):
    examscheduleid = models.AutoField(db_column='examscheduleID', primary_key=True)  # Field name made lowercase.
    examid = models.IntegerField(db_column='examID')  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='sectionID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='subjectID')  # Field name made lowercase.
    edate = models.DateField()
    examfrom = models.CharField(max_length=10)
    examto = models.CharField(max_length=10)
    room = models.TextField(blank=True, null=True)
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'examschedule'


class Expense(models.Model):
    expenseid = models.AutoField(db_column='expenseID', primary_key=True)  # Field name made lowercase.
    create_date = models.DateField()
    date = models.DateField()
    expenseday = models.CharField(max_length=11)
    expensemonth = models.CharField(max_length=11)
    expenseyear = models.TextField()  # This field type is a guess.
    expense = models.CharField(max_length=128)
    amount = models.FloatField()
    file = models.CharField(max_length=200, blank=True, null=True)
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    uname = models.CharField(max_length=60)
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expense'


class Feetypes(models.Model):
    feetypesid = models.AutoField(db_column='feetypesID', primary_key=True)  # Field name made lowercase.
    feetypes = models.CharField(max_length=60)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feetypes'


class Fmenu(models.Model):
    fmenuid = models.AutoField(db_column='fmenuID', primary_key=True)  # Field name made lowercase.
    menu_name = models.CharField(max_length=128)
    status = models.IntegerField(db_comment='Only for active')
    topbar = models.IntegerField()
    social = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fmenu'


class FmenuRelation(models.Model):
    fmenu_relationid = models.AutoField(db_column='fmenu_relationID', primary_key=True)  # Field name made lowercase.
    fmenuid = models.IntegerField(db_column='fmenuID', blank=True, null=True)  # Field name made lowercase.
    menu_typeid = models.IntegerField(db_column='menu_typeID', blank=True, null=True, db_comment='1 => Pages, 2 => Post, 3 => Links')  # Field name made lowercase.
    menu_parentid = models.CharField(db_column='menu_parentID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    menu_orderid = models.IntegerField(db_column='menu_orderID', blank=True, null=True)  # Field name made lowercase.
    menu_pagesid = models.IntegerField(db_column='menu_pagesID', blank=True, null=True)  # Field name made lowercase.
    menu_label = models.CharField(max_length=254, blank=True, null=True)
    menu_link = models.TextField()
    menu_rand = models.CharField(max_length=128, blank=True, null=True)
    menu_rand_parentid = models.CharField(db_column='menu_rand_parentID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    menu_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fmenu_relation'


class FrontendSetting(models.Model):
    fieldoption = models.CharField(primary_key=True, max_length=100)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'frontend_setting'


class FrontendTemplate(models.Model):
    frontend_templateid = models.AutoField(db_column='frontend_templateID', primary_key=True)  # Field name made lowercase.
    template_name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'frontend_template'


class Globalpayment(models.Model):
    globalpaymentid = models.AutoField(db_column='globalpaymentID', primary_key=True)  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID', blank=True, null=True)  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='sectionID')  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    clearancetype = models.CharField(max_length=40)
    invoicename = models.CharField(max_length=128)
    invoicedescription = models.CharField(max_length=128)
    paymentyear = models.CharField(max_length=5)
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'globalpayment'


class Grade(models.Model):
    gradeid = models.AutoField(db_column='gradeID', primary_key=True)  # Field name made lowercase.
    grade = models.CharField(max_length=60)
    point = models.CharField(max_length=11)
    gradefrom = models.IntegerField()
    gradeupto = models.IntegerField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grade'


class Hmember(models.Model):
    hmemberid = models.AutoField(db_column='hmemberID', primary_key=True)  # Field name made lowercase.
    hostelid = models.IntegerField(db_column='hostelID')  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='categoryID')  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    hbalance = models.CharField(max_length=20, blank=True, null=True)
    hjoindate = models.DateField()

    class Meta:
        managed = False
        db_table = 'hmember'


class Holiday(models.Model):
    holidayid = models.AutoField(db_column='holidayID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    fdate = models.DateField()
    tdate = models.DateField()
    title = models.CharField(max_length=128)
    details = models.TextField()
    photo = models.CharField(max_length=200, blank=True, null=True)
    create_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'holiday'


class Hostel(models.Model):
    hostelid = models.AutoField(db_column='hostelID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=128)
    htype = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hostel'


class HourlyTemplate(models.Model):
    hourly_templateid = models.AutoField(db_column='hourly_templateID', primary_key=True)  # Field name made lowercase.
    hourly_grades = models.CharField(max_length=128)
    hourly_rate = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'hourly_template'


class Income(models.Model):
    incomeid = models.AutoField(db_column='incomeID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=128)
    date = models.DateField()
    incomeday = models.CharField(max_length=11)
    incomemonth = models.CharField(max_length=11)
    incomeyear = models.TextField()  # This field type is a guess.
    amount = models.FloatField()
    file = models.CharField(max_length=200)
    note = models.TextField()
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    create_date = models.DateField()
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'income'


class IniConfig(models.Model):
    configid = models.AutoField(db_column='configID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=255)
    config_key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ini_config'


class Instruction(models.Model):
    instructionid = models.AutoField(db_column='instructionID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=512)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'instruction'


class Invoice(models.Model):
    invoiceid = models.AutoField(db_column='invoiceID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    feetypeid = models.IntegerField(db_column='feetypeID', blank=True, null=True)  # Field name made lowercase.
    feetype = models.CharField(max_length=128)
    amount = models.FloatField()
    discount = models.FloatField()
    userid = models.IntegerField(db_column='userID', blank=True, null=True)  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID', blank=True, null=True)  # Field name made lowercase.
    uname = models.CharField(max_length=60, blank=True, null=True)
    date = models.DateField()
    create_date = models.DateField()
    day = models.CharField(max_length=20, blank=True, null=True)
    month = models.CharField(max_length=20, blank=True, null=True)
    year = models.TextField()  # This field type is a guess.
    paidstatus = models.IntegerField(blank=True, null=True)
    deleted_at = models.IntegerField()
    maininvoiceid = models.IntegerField(db_column='maininvoiceID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'invoice'


class Issue(models.Model):
    issueid = models.AutoField(db_column='issueID', primary_key=True)  # Field name made lowercase.
    lid = models.CharField(db_column='lID', max_length=128)  # Field name made lowercase.
    bookid = models.IntegerField(db_column='bookID')  # Field name made lowercase.
    serial_no = models.CharField(max_length=40)
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issue'


class Leaveapplications(models.Model):
    leaveapplicationid = models.AutoField(db_column='leaveapplicationID', primary_key=True)  # Field name made lowercase.
    leavecategoryid = models.PositiveIntegerField(db_column='leavecategoryID')  # Field name made lowercase.
    apply_date = models.DateTimeField()
    od_status = models.IntegerField()
    from_date = models.DateField()
    from_time = models.TimeField(blank=True, null=True)
    to_date = models.DateField()
    to_time = models.TimeField(blank=True, null=True)
    leave_days = models.IntegerField()
    reason = models.TextField(blank=True, null=True)
    attachment = models.CharField(max_length=200, blank=True, null=True)
    attachmentorginalname = models.CharField(max_length=200, blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.PositiveIntegerField(db_column='create_usertypeID')  # Field name made lowercase.
    applicationto_userid = models.PositiveIntegerField(db_column='applicationto_userID', blank=True, null=True)  # Field name made lowercase.
    applicationto_usertypeid = models.PositiveIntegerField(db_column='applicationto_usertypeID', blank=True, null=True)  # Field name made lowercase.
    approver_userid = models.PositiveIntegerField(db_column='approver_userID', blank=True, null=True)  # Field name made lowercase.
    approver_usertypeid = models.PositiveIntegerField(db_column='approver_usertypeID', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'leaveapplications'


class Leaveassign(models.Model):
    leaveassignid = models.AutoField(db_column='leaveassignID', primary_key=True)  # Field name made lowercase.
    leavecategoryid = models.PositiveIntegerField(db_column='leavecategoryID')  # Field name made lowercase.
    usertypeid = models.PositiveIntegerField(db_column='usertypeID')  # Field name made lowercase.
    leaveassignday = models.IntegerField()
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'leaveassign'


class Leavecategory(models.Model):
    leavecategoryid = models.AutoField(db_column='leavecategoryID', primary_key=True)  # Field name made lowercase.
    leavecategory = models.CharField(max_length=255)
    leavegender = models.IntegerField(blank=True, null=True, db_comment='1 = General, 2 = Male, 3 = Femele')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.PositiveIntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'leavecategory'


class Lmember(models.Model):
    lmemberid = models.AutoField(db_column='lmemberID', primary_key=True)  # Field name made lowercase.
    lid = models.CharField(db_column='lID', max_length=40)  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=40, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    lbalance = models.CharField(max_length=20, blank=True, null=True)
    ljoindate = models.DateField()

    class Meta:
        managed = False
        db_table = 'lmember'


class Location(models.Model):
    locationid = models.AutoField(db_column='locationID', primary_key=True)  # Field name made lowercase.
    location = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    create_date = models.DateField()
    modify_date = models.DateField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'location'


class Loginlog(models.Model):
    loginlogid = models.AutoField(db_column='loginlogID', primary_key=True)  # Field name made lowercase.
    ip = models.CharField(max_length=45, blank=True, null=True)
    browser = models.CharField(max_length=128, blank=True, null=True)
    operatingsystem = models.CharField(max_length=128, blank=True, null=True)
    login = models.PositiveIntegerField(blank=True, null=True)
    logout = models.PositiveIntegerField(blank=True, null=True)
    usertypeid = models.IntegerField(db_column='usertypeID', blank=True, null=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'loginlog'


class Mailandsms(models.Model):
    mailandsmsid = models.AutoField(db_column='mailandsmsID', primary_key=True)  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    users = models.TextField()
    type = models.CharField(max_length=16)
    senderusertypeid = models.IntegerField(db_column='senderusertypeID')  # Field name made lowercase.
    senderid = models.IntegerField(db_column='senderID')  # Field name made lowercase.
    message = models.TextField()
    create_date = models.DateTimeField()
    year = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mailandsms'


class Mailandsmstemplate(models.Model):
    mailandsmstemplateid = models.AutoField(db_column='mailandsmstemplateID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=128)
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    type = models.CharField(max_length=10)
    template = models.TextField()
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mailandsmstemplate'


class Mailandsmstemplatetag(models.Model):
    mailandsmstemplatetagid = models.AutoField(db_column='mailandsmstemplatetagID', primary_key=True)  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    tagname = models.CharField(max_length=128)
    mailandsmstemplatetag_extra = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mailandsmstemplatetag'


class Maininvoice(models.Model):
    maininvoiceid = models.AutoField(db_column='maininvoiceID', primary_key=True)  # Field name made lowercase.
    maininvoiceschoolyearid = models.IntegerField(db_column='maininvoiceschoolyearID')  # Field name made lowercase.
    maininvoiceclassesid = models.IntegerField(db_column='maininvoiceclassesID')  # Field name made lowercase.
    maininvoicestudentid = models.IntegerField(db_column='maininvoicestudentID')  # Field name made lowercase.
    maininvoiceuserid = models.IntegerField(db_column='maininvoiceuserID', blank=True, null=True)  # Field name made lowercase.
    maininvoiceusertypeid = models.IntegerField(db_column='maininvoiceusertypeID', blank=True, null=True)  # Field name made lowercase.
    maininvoiceuname = models.CharField(max_length=60, blank=True, null=True)
    maininvoicedate = models.DateField()
    maininvoicecreate_date = models.DateField()
    maininvoiceday = models.CharField(max_length=20, blank=True, null=True)
    maininvoicemonth = models.CharField(max_length=20, blank=True, null=True)
    maininvoiceyear = models.TextField()  # This field type is a guess.
    maininvoicestatus = models.IntegerField(blank=True, null=True)
    maininvoicedeleted_at = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'maininvoice'


class MakePayment(models.Model):
    make_paymentid = models.AutoField(db_column='make_paymentID', primary_key=True)  # Field name made lowercase.
    month = models.TextField()
    gross_salary = models.TextField()
    total_deduction = models.TextField()
    net_salary = models.TextField()
    payment_amount = models.TextField()
    payment_method = models.IntegerField()
    comments = models.TextField(blank=True, null=True)
    templateid = models.IntegerField(db_column='templateID')  # Field name made lowercase.
    salaryid = models.IntegerField(db_column='salaryID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID', blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)
    total_hours = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'make_payment'


class ManageSalary(models.Model):
    manage_salaryid = models.AutoField(db_column='manage_salaryID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    salary = models.IntegerField()
    template = models.IntegerField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'manage_salary'


class Mark(models.Model):
    markid = models.AutoField(db_column='markID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    examid = models.IntegerField(db_column='examID')  # Field name made lowercase.
    exam = models.CharField(max_length=60)
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='subjectID')  # Field name made lowercase.
    subject = models.CharField(max_length=60)
    year = models.TextField()  # This field type is a guess.
    create_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mark'


class Markpercentage(models.Model):
    markpercentageid = models.AutoField(db_column='markpercentageID', primary_key=True)  # Field name made lowercase.
    markpercentagetype = models.CharField(max_length=100)
    percentage = models.FloatField()
    examid = models.IntegerField(db_column='examID', blank=True, null=True)  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID', blank=True, null=True)  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='subjectID', blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'markpercentage'


class Markrelation(models.Model):
    markrelationid = models.AutoField(db_column='markrelationID', primary_key=True)  # Field name made lowercase.
    markid = models.IntegerField(db_column='markID')  # Field name made lowercase.
    markpercentageid = models.IntegerField(db_column='markpercentageID')  # Field name made lowercase.
    mark = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'markrelation'


class Marksetting(models.Model):
    marksettingid = models.AutoField(db_column='marksettingID', primary_key=True)  # Field name made lowercase.
    examid = models.IntegerField(db_column='examID')  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='subjectID', blank=True, null=True)  # Field name made lowercase.
    marktypeid = models.IntegerField(db_column='marktypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'marksetting'


class Marksettingrelation(models.Model):
    marksettingrelationid = models.AutoField(db_column='marksettingrelationID', primary_key=True)  # Field name made lowercase.
    marktypeid = models.IntegerField(db_column='marktypeID')  # Field name made lowercase.
    marksettingid = models.IntegerField(db_column='marksettingID')  # Field name made lowercase.
    markpercentageid = models.IntegerField(db_column='markpercentageID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'marksettingrelation'


class Media(models.Model):
    mediaid = models.AutoField(db_column='mediaID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    mcategoryid = models.IntegerField(db_column='mcategoryID')  # Field name made lowercase.
    file_name = models.CharField(max_length=255)
    file_name_display = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'media'


class MediaCategory(models.Model):
    mcategoryid = models.AutoField(db_column='mcategoryID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    folder_name = models.CharField(max_length=255)
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'media_category'


class MediaGallery(models.Model):
    media_galleryid = models.AutoField(db_column='media_galleryID', primary_key=True)  # Field name made lowercase.
    media_gallery_type = models.IntegerField()
    file_type = models.CharField(max_length=40, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_original_name = models.CharField(max_length=255, blank=True, null=True)
    file_title = models.TextField()
    file_size = models.CharField(max_length=40, blank=True, null=True)
    file_width_height = models.CharField(max_length=40, blank=True, null=True)
    file_upload_date = models.DateTimeField(blank=True, null=True)
    file_caption = models.TextField(blank=True, null=True)
    file_alt_text = models.CharField(max_length=255, blank=True, null=True)
    file_description = models.TextField(blank=True, null=True)
    file_length = models.CharField(max_length=128, blank=True, null=True)
    file_artist = models.CharField(max_length=128, blank=True, null=True)
    file_album = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media_gallery'


class MediaShare(models.Model):
    shareid = models.AutoField(db_column='shareID', primary_key=True)  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    public = models.IntegerField()
    file_or_folder = models.IntegerField()
    item_id = models.IntegerField()
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'media_share'


class Menu(models.Model):
    menuid = models.AutoField(db_column='menuID', primary_key=True)  # Field name made lowercase.
    menuname = models.CharField(db_column='menuName', max_length=128)  # Field name made lowercase.
    link = models.CharField(max_length=512)
    icon = models.CharField(max_length=128, blank=True, null=True)
    pullright = models.TextField(db_column='pullRight', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField()
    parentid = models.IntegerField(db_column='parentID')  # Field name made lowercase.
    priority = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'menu'


class Migrations(models.Model):
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Notice(models.Model):
    noticeid = models.AutoField(db_column='noticeID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=128)
    notice = models.TextField()
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    date = models.DateField()
    create_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'notice'


class OnlineExam(models.Model):
    onlineexamid = models.AutoField(db_column='onlineExamID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)
    classid = models.IntegerField(db_column='classID', blank=True, null=True)  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='sectionID', blank=True, null=True)  # Field name made lowercase.
    studentgroupid = models.IntegerField(db_column='studentGroupID', blank=True, null=True)  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='subjectID', blank=True, null=True)  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='userTypeID', blank=True, null=True)  # Field name made lowercase.
    instructionid = models.IntegerField(db_column='instructionID', blank=True, null=True)  # Field name made lowercase.
    examstatus = models.CharField(db_column='examStatus', max_length=11)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolYearID')  # Field name made lowercase.
    examtypenumber = models.IntegerField(db_column='examTypeNumber', blank=True, null=True)  # Field name made lowercase.
    startdatetime = models.DateTimeField(db_column='startDateTime', blank=True, null=True)  # Field name made lowercase.
    enddatetime = models.DateTimeField(db_column='endDateTime', blank=True, null=True)  # Field name made lowercase.
    duration = models.IntegerField(blank=True, null=True)
    random = models.IntegerField(blank=True, null=True)
    public = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    marktype = models.IntegerField(db_column='markType')  # Field name made lowercase.
    negativemark = models.IntegerField(db_column='negativeMark', blank=True, null=True)  # Field name made lowercase.
    bonusmark = models.IntegerField(db_column='bonusMark', blank=True, null=True)  # Field name made lowercase.
    point = models.IntegerField(blank=True, null=True)
    percentage = models.IntegerField(blank=True, null=True)
    showmarkafterexam = models.IntegerField(db_column='showMarkAfterExam', blank=True, null=True)  # Field name made lowercase.
    judge = models.IntegerField(blank=True, null=True, db_comment='Auto Judge = 1, Manually Judge = 0')
    paid = models.IntegerField(blank=True, null=True, db_comment='0 = Unpaid, 1 = Paid')
    validdays = models.IntegerField(db_column='validDays', blank=True, null=True)  # Field name made lowercase.
    cost = models.IntegerField(blank=True, null=True)
    img = models.CharField(max_length=512, blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.
    published = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'online_exam'


class OnlineExamQuestion(models.Model):
    onlineexamquestionid = models.AutoField(db_column='onlineExamQuestionID', primary_key=True)  # Field name made lowercase.
    onlineexamid = models.IntegerField(db_column='onlineExamID')  # Field name made lowercase.
    questionid = models.IntegerField(db_column='questionID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'online_exam_question'


class OnlineExamType(models.Model):
    onlineexamtypeid = models.AutoField(db_column='onlineExamTypeID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=512, blank=True, null=True)
    examtypenumber = models.IntegerField(db_column='examTypeNumber', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'online_exam_type'


class OnlineExamUserAnswer(models.Model):
    onlineexamuseranswerid = models.AutoField(db_column='onlineExamUserAnswerID', primary_key=True)  # Field name made lowercase.
    onlineexamquestionid = models.IntegerField(db_column='onlineExamQuestionID')  # Field name made lowercase.
    onlineexamregistereduserid = models.IntegerField(db_column='onlineExamRegisteredUserID', blank=True, null=True)  # Field name made lowercase.
    onlineexamid = models.IntegerField(db_column='onlineExamID')  # Field name made lowercase.
    examtimeid = models.IntegerField(db_column='examtimeID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'online_exam_user_answer'


class OnlineExamUserAnswerOption(models.Model):
    onlineexamuseransweroptionid = models.AutoField(db_column='onlineExamUserAnswerOptionID', primary_key=True)  # Field name made lowercase.
    questionid = models.IntegerField(db_column='questionID')  # Field name made lowercase.
    optionid = models.IntegerField(db_column='optionID', blank=True, null=True)  # Field name made lowercase.
    typeid = models.IntegerField(db_column='typeID')  # Field name made lowercase.
    text = models.TextField(blank=True, null=True)
    time = models.DateTimeField()
    onlineexamid = models.IntegerField(db_column='onlineExamID')  # Field name made lowercase.
    examtimeid = models.IntegerField(db_column='examtimeID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'online_exam_user_answer_option'


class OnlineExamUserStatus(models.Model):
    onlineexamuserstatus = models.AutoField(db_column='onlineExamUserStatus', primary_key=True)  # Field name made lowercase.
    onlineexamid = models.IntegerField(db_column='onlineExamID')  # Field name made lowercase.
    duration = models.IntegerField()
    score = models.IntegerField()
    totalquestion = models.IntegerField(db_column='totalQuestion')  # Field name made lowercase.
    totalanswer = models.IntegerField(db_column='totalAnswer')  # Field name made lowercase.
    nagetivemark = models.IntegerField(db_column='nagetiveMark')  # Field name made lowercase.
    time = models.DateTimeField()
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID', blank=True, null=True)  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='sectionID', blank=True, null=True)  # Field name made lowercase.
    examtimeid = models.IntegerField(db_column='examtimeID', blank=True, null=True)  # Field name made lowercase.
    totalcurrectanswer = models.IntegerField(db_column='totalCurrectAnswer', blank=True, null=True)  # Field name made lowercase.
    totalmark = models.CharField(db_column='totalMark', max_length=40, blank=True, null=True)  # Field name made lowercase.
    totalobtainedmark = models.IntegerField(db_column='totalObtainedMark', blank=True, null=True)  # Field name made lowercase.
    totalpercentage = models.FloatField(db_column='totalPercentage', blank=True, null=True)  # Field name made lowercase.
    statusid = models.IntegerField(db_column='statusID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'online_exam_user_status'


class Onlineadmission(models.Model):
    onlineadmissionid = models.AutoField(db_column='onlineadmissionID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=60, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    religion = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    classesid = models.IntegerField(db_column='classesID', blank=True, null=True)  # Field name made lowercase.
    bloodgroup = models.CharField(max_length=5, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    photo = models.CharField(max_length=200, blank=True, null=True)
    document = models.CharField(max_length=200, blank=True, null=True)
    schoolyearid = models.IntegerField(db_column='schoolyearID', blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True, db_comment='0 = New, 1=Approved, 2 = Waiting, 3 = Declined')

    class Meta:
        managed = False
        db_table = 'onlineadmission'


class Overtime(models.Model):
    date = models.DateTimeField()
    hours = models.IntegerField()
    amount = models.FloatField()
    total_amount = models.FloatField(blank=True, null=True)
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    user_table = models.CharField(max_length=40)
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'overtime'


class Pages(models.Model):
    pagesid = models.AutoField(db_column='pagesID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, db_comment='1 => active, 2 => draft, 3 => trash, 4 => review  ')
    visibility = models.IntegerField(blank=True, null=True, db_comment='1 => public 2 => protected 3 => private ')
    publish_date = models.DateTimeField(blank=True, null=True)
    parentid = models.IntegerField(db_column='parentID')  # Field name made lowercase.
    pageorder = models.IntegerField()
    template = models.CharField(max_length=250, blank=True, null=True)
    featured_image = models.CharField(max_length=11, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    create_userid = models.IntegerField(db_column='create_userID', blank=True, null=True)  # Field name made lowercase.
    create_username = models.CharField(max_length=60, blank=True, null=True)
    create_usertypeid = models.IntegerField(db_column='create_usertypeID', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pages'


class Parents(models.Model):
    parentsid = models.AutoField(db_column='parentsID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=60)
    father_name = models.CharField(max_length=60)
    mother_name = models.CharField(max_length=60)
    father_profession = models.CharField(max_length=40)
    mother_profession = models.CharField(max_length=40)
    email = models.CharField(max_length=40, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=128)
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'parents'


class Payment(models.Model):
    paymentid = models.AutoField(db_column='paymentID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    invoiceid = models.IntegerField(db_column='invoiceID')  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    paymentamount = models.FloatField(blank=True, null=True)
    paymenttype = models.CharField(max_length=128)
    paymentdate = models.DateField()
    paymentday = models.CharField(max_length=11)
    paymentmonth = models.CharField(max_length=10)
    paymentyear = models.TextField()  # This field type is a guess.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    uname = models.CharField(max_length=60)
    transactionid = models.TextField(db_column='transactionID', blank=True, null=True)  # Field name made lowercase.
    globalpaymentid = models.IntegerField(db_column='globalpaymentID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payment'


class PermissionRelationships(models.Model):
    permission_id = models.IntegerField()
    usertype_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'permission_relationships'


class Permissions(models.Model):
    permissionid = models.AutoField(db_column='permissionID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(max_length=255, db_collation='utf8_unicode_ci')
    name = models.CharField(max_length=50, db_collation='utf8_unicode_ci', db_comment='In most cases, this should be the name of the module (e.g. news)')
    active = models.CharField(max_length=3, db_collation='utf8_unicode_ci')

    class Meta:
        managed = False
        db_table = 'permissions'


class Posts(models.Model):
    postsid = models.AutoField(db_column='postsID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, db_comment='1 => active, 2 => draft, 3 => trash, 4 => review  ')
    visibility = models.IntegerField(blank=True, null=True, db_comment='1 => public 2 => protected 3 => private ')
    publish_date = models.DateTimeField(blank=True, null=True)
    parentid = models.IntegerField(db_column='parentID')  # Field name made lowercase.
    postorder = models.IntegerField()
    featured_image = models.CharField(max_length=11, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    create_userid = models.IntegerField(db_column='create_userID', blank=True, null=True)  # Field name made lowercase.
    create_username = models.CharField(max_length=60, blank=True, null=True)
    create_usertypeid = models.IntegerField(db_column='create_usertypeID', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'


class PostsCategories(models.Model):
    posts_categoriesid = models.AutoField(db_column='posts_categoriesID', primary_key=True)  # Field name made lowercase.
    posts_categories = models.CharField(max_length=40, blank=True, null=True)
    posts_slug = models.CharField(max_length=250, blank=True, null=True)
    posts_parent = models.IntegerField(blank=True, null=True)
    posts_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts_categories'


class PostsCategory(models.Model):
    posts_categoryid = models.AutoField(db_column='posts_categoryID', primary_key=True)  # Field name made lowercase.
    postsid = models.IntegerField(db_column='postsID')  # Field name made lowercase.
    posts_categoriesid = models.IntegerField(db_column='posts_categoriesID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'posts_category'


class Product(models.Model):
    productid = models.AutoField(db_column='productID', primary_key=True)  # Field name made lowercase.
    productcategoryid = models.IntegerField(db_column='productcategoryID')  # Field name made lowercase.
    productname = models.CharField(max_length=128)
    productbuyingprice = models.FloatField()
    productsellingprice = models.FloatField()
    productdesc = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product'


class Productcategory(models.Model):
    productcategoryid = models.AutoField(db_column='productcategoryID', primary_key=True)  # Field name made lowercase.
    productcategoryname = models.CharField(max_length=128)
    productcategorydesc = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productcategory'


class Productpurchase(models.Model):
    productpurchaseid = models.AutoField(db_column='productpurchaseID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    productsupplierid = models.IntegerField(db_column='productsupplierID')  # Field name made lowercase.
    productwarehouseid = models.IntegerField(db_column='productwarehouseID')  # Field name made lowercase.
    productpurchasereferenceno = models.CharField(max_length=100)
    productpurchasedate = models.DateField()
    productpurchasefile = models.CharField(max_length=200, blank=True, null=True)
    productpurchasefileorginalname = models.CharField(max_length=200, blank=True, null=True)
    productpurchasedescription = models.TextField(blank=True, null=True)
    productpurchasestatus = models.IntegerField(db_comment='0 = pending, 1 = partial_paid,  2 = fully_paid')
    productpurchaserefund = models.IntegerField(db_comment='0 = not refund, 1 = refund ')
    productpurchasetaxid = models.IntegerField(db_column='productpurchasetaxID')  # Field name made lowercase.
    productpurchasetaxamount = models.FloatField()
    productpurchasediscount = models.FloatField()
    productpurchaseshipping = models.FloatField()
    productpurchasepaymentterm = models.IntegerField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productpurchase'


class Productpurchaseitem(models.Model):
    productpurchaseitemid = models.AutoField(db_column='productpurchaseitemID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    productpurchaseid = models.IntegerField(db_column='productpurchaseID')  # Field name made lowercase.
    productid = models.IntegerField(db_column='productID')  # Field name made lowercase.
    productpurchaseunitprice = models.FloatField()
    productpurchasequantity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'productpurchaseitem'


class Productpurchasepaid(models.Model):
    productpurchasepaidid = models.AutoField(db_column='productpurchasepaidID', primary_key=True)  # Field name made lowercase.
    productpurchasepaidschoolyearid = models.IntegerField(db_column='productpurchasepaidschoolyearID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    productpurchaseid = models.IntegerField(db_column='productpurchaseID')  # Field name made lowercase.
    productpurchasepaiddate = models.DateField()
    productpurchasepaidreferenceno = models.CharField(max_length=100)
    productpurchasepaidamount = models.FloatField()
    productpurchasepaidpaymentmethod = models.IntegerField(db_comment='1 = cash, 2 = cheque, 3 = crediit card, 4 = other')
    productpurchasepaidfile = models.CharField(max_length=200, blank=True, null=True)
    productpurchasepaidorginalname = models.CharField(max_length=200, blank=True, null=True)
    productpurchasepaiddescription = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productpurchasepaid'


class Productsale(models.Model):
    productsaleid = models.AutoField(db_column='productsaleID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    productsalecustomertypeid = models.IntegerField(db_column='productsalecustomertypeID')  # Field name made lowercase.
    productsalecustomerid = models.IntegerField(db_column='productsalecustomerID')  # Field name made lowercase.
    productsalereferenceno = models.CharField(max_length=100)
    productsaledate = models.DateField()
    productsalefile = models.CharField(max_length=200, blank=True, null=True)
    productsalefileorginalname = models.CharField(max_length=200, blank=True, null=True)
    productsaledescription = models.TextField(blank=True, null=True)
    productsalestatus = models.IntegerField(db_comment='0 = select_payment_status, 1 = due,  2 = partial, 3 = Paid')
    productsalerefund = models.IntegerField(db_comment='0 = not refund, 1 = refund ')
    productsaletaxid = models.IntegerField(db_column='productsaletaxID')  # Field name made lowercase.
    productsaletaxamount = models.FloatField()
    productsalediscount = models.FloatField()
    productsaleshipping = models.FloatField()
    productsalepaymentterm = models.IntegerField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productsale'


class Productsaleitem(models.Model):
    productsaleitemid = models.AutoField(db_column='productsaleitemID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    productsaleid = models.IntegerField(db_column='productsaleID')  # Field name made lowercase.
    productid = models.IntegerField(db_column='productID')  # Field name made lowercase.
    productsaleserialno = models.CharField(max_length=100, blank=True, null=True)
    productsaleunitprice = models.FloatField()
    productsalequantity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'productsaleitem'


class Productsalepaid(models.Model):
    productsalepaidid = models.AutoField(db_column='productsalepaidID', primary_key=True)  # Field name made lowercase.
    productsalepaidschoolyearid = models.IntegerField(db_column='productsalepaidschoolyearID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    productsaleid = models.IntegerField(db_column='productsaleID')  # Field name made lowercase.
    productsalepaiddate = models.DateField()
    productsalepaidreferenceno = models.CharField(max_length=100)
    productsalepaidamount = models.FloatField()
    productsalepaidpaymentmethod = models.IntegerField(db_comment='1 = cash, 2 = cheque, 3 = crediit card, 4 = other')
    productsalepaidfile = models.CharField(max_length=200, blank=True, null=True)
    productsalepaidorginalname = models.CharField(max_length=200, blank=True, null=True)
    productsalepaiddescription = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productsalepaid'


class Productsupplier(models.Model):
    productsupplierid = models.AutoField(db_column='productsupplierID', primary_key=True)  # Field name made lowercase.
    productsuppliercompanyname = models.CharField(max_length=128)
    productsuppliername = models.CharField(max_length=40)
    productsupplieremail = models.CharField(max_length=40, blank=True, null=True)
    productsupplierphone = models.CharField(max_length=20, blank=True, null=True)
    productsupplieraddress = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productsupplier'


class Productwarehouse(models.Model):
    productwarehouseid = models.AutoField(db_column='productwarehouseID', primary_key=True)  # Field name made lowercase.
    productwarehousename = models.CharField(max_length=128)
    productwarehousecode = models.CharField(max_length=128)
    productwarehouseemail = models.CharField(max_length=40, blank=True, null=True)
    productwarehousephone = models.CharField(max_length=20, blank=True, null=True)
    productwarehouseaddress = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productwarehouse'


class Promotionlog(models.Model):
    promotionlogid = models.AutoField(db_column='promotionLogID', primary_key=True)  # Field name made lowercase.
    promotiontype = models.CharField(db_column='promotionType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    jumpclassid = models.IntegerField(db_column='jumpClassID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolYearID')  # Field name made lowercase.
    jumpschoolyearid = models.IntegerField(db_column='jumpSchoolYearID')  # Field name made lowercase.
    subjectandsubjectcodeandmark = models.TextField(blank=True, null=True)
    exams = models.TextField(blank=True, null=True)
    markpercentages = models.TextField(blank=True, null=True)
    promotestudents = models.TextField(db_column='promoteStudents', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField()
    created_at = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'promotionlog'


class Purchase(models.Model):
    purchaseid = models.AutoField(db_column='purchaseID', primary_key=True)  # Field name made lowercase.
    assetid = models.IntegerField(db_column='assetID')  # Field name made lowercase.
    vendorid = models.IntegerField(db_column='vendorID')  # Field name made lowercase.
    quantity = models.IntegerField()
    unit = models.IntegerField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    service_date = models.DateField(blank=True, null=True)
    purchase_price = models.FloatField()
    purchased_by = models.IntegerField()
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    status = models.IntegerField()
    expire_date = models.DateField(blank=True, null=True)
    create_date = models.DateField()
    modify_date = models.DateField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'purchase'


class QuestionAnswer(models.Model):
    answerid = models.AutoField(db_column='answerID', primary_key=True)  # Field name made lowercase.
    questionid = models.IntegerField(db_column='questionID')  # Field name made lowercase.
    optionid = models.IntegerField(db_column='optionID', blank=True, null=True)  # Field name made lowercase.
    typenumber = models.IntegerField(db_column='typeNumber')  # Field name made lowercase.
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'question_answer'


class QuestionBank(models.Model):
    questionbankid = models.AutoField(db_column='questionBankID', primary_key=True)  # Field name made lowercase.
    question = models.TextField()
    explanation = models.TextField(blank=True, null=True)
    levelid = models.IntegerField(db_column='levelID', blank=True, null=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='groupID', blank=True, null=True)  # Field name made lowercase.
    totalquestion = models.IntegerField(db_column='totalQuestion', blank=True, null=True)  # Field name made lowercase.
    totaloption = models.IntegerField(db_column='totalOption', blank=True, null=True)  # Field name made lowercase.
    typenumber = models.IntegerField(db_column='typeNumber', blank=True, null=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='parentID', blank=True, null=True)  # Field name made lowercase.
    time = models.IntegerField(blank=True, null=True)
    mark = models.IntegerField(blank=True, null=True)
    hints = models.TextField(blank=True, null=True)
    upload = models.CharField(max_length=512, blank=True, null=True)
    subjectid = models.IntegerField(db_column='subjectID', blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'question_bank'


class QuestionGroup(models.Model):
    questiongroupid = models.AutoField(db_column='questionGroupID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'question_group'


class QuestionLevel(models.Model):
    questionlevelid = models.AutoField(db_column='questionLevelID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'question_level'


class QuestionOption(models.Model):
    optionid = models.AutoField(db_column='optionID', primary_key=True)  # Field name made lowercase.
    questionid = models.IntegerField(db_column='questionID')  # Field name made lowercase.
    name = models.CharField(max_length=512)
    img = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'question_option'


class QuestionType(models.Model):
    questiontypeid = models.AutoField(db_column='questionTypeID', primary_key=True)  # Field name made lowercase.
    typenumber = models.IntegerField(db_column='typeNumber')  # Field name made lowercase.
    name = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'question_type'


class Reset(models.Model):
    resetid = models.AutoField(db_column='resetID', primary_key=True)  # Field name made lowercase.
    keyid = models.CharField(db_column='keyID', max_length=128)  # Field name made lowercase.
    email = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'reset'


class Routine(models.Model):
    routineid = models.AutoField(db_column='routineID', primary_key=True)  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='sectionID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='subjectID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    teacherid = models.IntegerField(db_column='teacherID')  # Field name made lowercase.
    day = models.CharField(max_length=60)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    room = models.TextField()

    class Meta:
        managed = False
        db_table = 'routine'


class SalaryOption(models.Model):
    salary_optionid = models.AutoField(db_column='salary_optionID', primary_key=True)  # Field name made lowercase.
    salary_templateid = models.IntegerField(db_column='salary_templateID')  # Field name made lowercase.
    option_type = models.IntegerField(db_comment='Allowances =1, Dllowances = 2, Increment = 3')
    label_name = models.CharField(max_length=128, blank=True, null=True)
    label_amount = models.FloatField()

    class Meta:
        managed = False
        db_table = 'salary_option'


class SalaryTemplate(models.Model):
    salary_templateid = models.AutoField(db_column='salary_templateID', primary_key=True)  # Field name made lowercase.
    salary_grades = models.CharField(max_length=128)
    basic_salary = models.TextField()
    overtime_rate = models.TextField()

    class Meta:
        managed = False
        db_table = 'salary_template'


class SchoolSessions(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    ip_address = models.CharField(max_length=45)
    timestamp = models.PositiveIntegerField()
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'school_sessions'


class Schoolyear(models.Model):
    schoolyearid = models.AutoField(db_column='schoolyearID', primary_key=True)  # Field name made lowercase.
    schooltype = models.CharField(max_length=40, blank=True, null=True)
    schoolyear = models.CharField(max_length=128)
    schoolyeartitle = models.CharField(max_length=128, blank=True, null=True)
    startingdate = models.DateField()
    endingdate = models.DateField()
    semestercode = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=100)
    create_usertype = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'schoolyear'


class Section(models.Model):
    sectionid = models.AutoField(db_column='sectionID', primary_key=True)  # Field name made lowercase.
    section = models.CharField(max_length=60)
    category = models.CharField(max_length=128)
    capacity = models.IntegerField()
    classesid = models.ForeignKey(Classes, models.DO_NOTHING, db_column='classesID')  # Field name made lowercase.
    teacherid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='teacherID')  # Field name made lowercase.
    note = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)

    def __str__(self):
        return self.section

    class Meta:
        managed = False
        db_table = 'section'


class Setting(models.Model):
    fieldoption = models.CharField(primary_key=True, max_length=100)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'setting'


class Slider(models.Model):
    sliderid = models.AutoField(db_column='sliderID', primary_key=True)  # Field name made lowercase.
    pagesid = models.IntegerField(db_column='pagesID')  # Field name made lowercase.
    slider = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'slider'


class Smssettings(models.Model):
    smssettingsid = models.AutoField(db_column='smssettingsID', primary_key=True)  # Field name made lowercase.
    types = models.CharField(max_length=255, blank=True, null=True)
    field_names = models.CharField(max_length=255, blank=True, null=True)
    field_values = models.CharField(max_length=255, blank=True, null=True)
    smssettings_extra = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'smssettings'


class Sociallink(models.Model):
    sociallinkid = models.AutoField(db_column='sociallinkID', primary_key=True)  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    facebook = models.CharField(max_length=200)
    twitter = models.CharField(max_length=200)
    linkedin = models.CharField(max_length=200)
    googleplus = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sociallink'


class Sponsor(models.Model):
    sponsorid = models.AutoField(db_column='sponsorID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    organisation_name = models.CharField(max_length=180, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    photo = models.CharField(max_length=200, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    create_userid = models.IntegerField(db_column='create_userID', blank=True, null=True)  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID', blank=True, null=True)  # Field name made lowercase.
    create_username = models.CharField(max_length=60, blank=True, null=True)
    schoolyearid = models.IntegerField(db_column='schoolyearID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sponsor'


class Sponsorship(models.Model):
    sponsorshipid = models.AutoField(db_column='sponsorshipID', primary_key=True)  # Field name made lowercase.
    sponsorid = models.IntegerField(db_column='sponsorID')  # Field name made lowercase.
    candidateid = models.IntegerField(db_column='candidateID')  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    amount = models.FloatField()
    payment_date = models.DateTimeField(blank=True, null=True)
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sponsorship'


class Student(models.Model):
    studentid = models.AutoField(db_column='studentID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=60)
    dob = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10)
    religion = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    classesid = models.ForeignKey(Classes, models.DO_NOTHING, db_column='classesID')  # Field name made lowercase.
    sectionid = models.ForeignKey(Section, models.DO_NOTHING, db_column='sectionID')  # Field name made lowercase.
    roll = models.IntegerField()
    bloodgroup = models.CharField(max_length=5, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    registerno = models.CharField(db_column='registerNO', max_length=128, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(max_length=128, blank=True, null=True)
    library = models.IntegerField()
    hostel = models.IntegerField()
    transport = models.IntegerField()
    photo = models.CharField(max_length=200, blank=True, null=True)
    parentid = models.ForeignKey(Parents, models.DO_NOTHING, db_column='parentID', blank=True, null=True)  # Field name made lowercase.
    createschoolyearid = models.IntegerField(db_column='createschoolyearID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=128)
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student'


class Studentextend(models.Model):
    studentextendid = models.AutoField(db_column='studentextendID', primary_key=True)  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    studentgroupid = models.IntegerField(db_column='studentgroupID')  # Field name made lowercase.
    optionalsubjectid = models.IntegerField(db_column='optionalsubjectID')  # Field name made lowercase.
    extracurricularactivities = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'studentextend'


class Studentgroup(models.Model):
    studentgroupid = models.AutoField(db_column='studentgroupID', primary_key=True)  # Field name made lowercase.
    group = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'studentgroup'


class Studentrelation(models.Model):
    studentrelationid = models.AutoField(db_column='studentrelationID', primary_key=True)  # Field name made lowercase.
    srstudentid = models.IntegerField(db_column='srstudentID', blank=True, null=True)  # Field name made lowercase.
    srname = models.CharField(max_length=40)
    srclassesid = models.IntegerField(db_column='srclassesID', blank=True, null=True)  # Field name made lowercase.
    srclasses = models.CharField(max_length=40, blank=True, null=True)
    srroll = models.IntegerField(blank=True, null=True)
    srregisterno = models.CharField(db_column='srregisterNO', max_length=128, blank=True, null=True)  # Field name made lowercase.
    srsectionid = models.IntegerField(db_column='srsectionID', blank=True, null=True)  # Field name made lowercase.
    srsection = models.CharField(max_length=40, blank=True, null=True)
    srstudentgroupid = models.IntegerField(db_column='srstudentgroupID')  # Field name made lowercase.
    sroptionalsubjectid = models.IntegerField(db_column='sroptionalsubjectID')  # Field name made lowercase.
    srschoolyearid = models.IntegerField(db_column='srschoolyearID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'studentrelation'


class SubAttendance(models.Model):
    attendanceid = models.AutoField(db_column='attendanceID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='sectionID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='subjectID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertype = models.CharField(max_length=60)
    monthyear = models.CharField(max_length=10)
    a1 = models.CharField(max_length=3, blank=True, null=True)
    a2 = models.CharField(max_length=3, blank=True, null=True)
    a3 = models.CharField(max_length=3, blank=True, null=True)
    a4 = models.CharField(max_length=3, blank=True, null=True)
    a5 = models.CharField(max_length=3, blank=True, null=True)
    a6 = models.CharField(max_length=3, blank=True, null=True)
    a7 = models.CharField(max_length=3, blank=True, null=True)
    a8 = models.CharField(max_length=3, blank=True, null=True)
    a9 = models.CharField(max_length=3, blank=True, null=True)
    a10 = models.CharField(max_length=3, blank=True, null=True)
    a11 = models.CharField(max_length=3, blank=True, null=True)
    a12 = models.CharField(max_length=3, blank=True, null=True)
    a13 = models.CharField(max_length=3, blank=True, null=True)
    a14 = models.CharField(max_length=3, blank=True, null=True)
    a15 = models.CharField(max_length=3, blank=True, null=True)
    a16 = models.CharField(max_length=3, blank=True, null=True)
    a17 = models.CharField(max_length=3, blank=True, null=True)
    a18 = models.CharField(max_length=3, blank=True, null=True)
    a19 = models.CharField(max_length=3, blank=True, null=True)
    a20 = models.CharField(max_length=3, blank=True, null=True)
    a21 = models.CharField(max_length=3, blank=True, null=True)
    a22 = models.CharField(max_length=3, blank=True, null=True)
    a23 = models.CharField(max_length=3, blank=True, null=True)
    a24 = models.CharField(max_length=3, blank=True, null=True)
    a25 = models.CharField(max_length=3, blank=True, null=True)
    a26 = models.CharField(max_length=3, blank=True, null=True)
    a27 = models.CharField(max_length=3, blank=True, null=True)
    a28 = models.CharField(max_length=3, blank=True, null=True)
    a29 = models.CharField(max_length=3, blank=True, null=True)
    a30 = models.CharField(max_length=3, blank=True, null=True)
    a31 = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sub_attendance'


class Subject(models.Model):
    subjectid = models.AutoField(db_column='subjectID', primary_key=True)  # Field name made lowercase.
    classesid = models.ForeignKey(Classes, models.DO_NOTHING, db_column='classesID')  # Field name made lowercase.
    type = models.IntegerField()
    passmark = models.IntegerField()
    finalmark = models.IntegerField()
    subject = models.CharField(max_length=60)
    subject_author = models.CharField(max_length=100, blank=True, null=True)
    subject_code = models.TextField()
    teacher_name = models.CharField(max_length=60)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'subject'


class Subjectteacher(models.Model):
    subjectteacherid = models.AutoField(db_column='subjectteacherID', primary_key=True)  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='subjectID')  # Field name made lowercase.
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    teacherid = models.IntegerField(db_column='teacherID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subjectteacher'


class Syllabus(models.Model):
    syllabusid = models.AutoField(db_column='syllabusID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    originalfile = models.TextField()
    file = models.TextField(blank=True, null=True)
    classesid = models.IntegerField(db_column='classesID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'syllabus'


class Systemadmin(models.Model):
    systemadminid = models.AutoField(db_column='systemadminID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=60)
    dob = models.DateField()
    sex = models.CharField(max_length=10)
    religion = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    jod = models.DateField()
    photo = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=128)
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)
    active = models.IntegerField()
    systemadminextra1 = models.CharField(max_length=128, blank=True, null=True)
    systemadminextra2 = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'systemadmin'


class Tattendance(models.Model):
    tattendanceid = models.AutoField(db_column='tattendanceID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    teacherid = models.IntegerField(db_column='teacherID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    monthyear = models.CharField(max_length=10)
    a1 = models.CharField(max_length=3, blank=True, null=True)
    a2 = models.CharField(max_length=3, blank=True, null=True)
    a3 = models.CharField(max_length=3, blank=True, null=True)
    a4 = models.CharField(max_length=3, blank=True, null=True)
    a5 = models.CharField(max_length=3, blank=True, null=True)
    a6 = models.CharField(max_length=3, blank=True, null=True)
    a7 = models.CharField(max_length=3, blank=True, null=True)
    a8 = models.CharField(max_length=3, blank=True, null=True)
    a9 = models.CharField(max_length=3, blank=True, null=True)
    a10 = models.CharField(max_length=3, blank=True, null=True)
    a11 = models.CharField(max_length=3, blank=True, null=True)
    a12 = models.CharField(max_length=3, blank=True, null=True)
    a13 = models.CharField(max_length=3, blank=True, null=True)
    a14 = models.CharField(max_length=3, blank=True, null=True)
    a15 = models.CharField(max_length=3, blank=True, null=True)
    a16 = models.CharField(max_length=3, blank=True, null=True)
    a17 = models.CharField(max_length=3, blank=True, null=True)
    a18 = models.CharField(max_length=3, blank=True, null=True)
    a19 = models.CharField(max_length=3, blank=True, null=True)
    a20 = models.CharField(max_length=3, blank=True, null=True)
    a21 = models.CharField(max_length=3, blank=True, null=True)
    a22 = models.CharField(max_length=3, blank=True, null=True)
    a23 = models.CharField(max_length=3, blank=True, null=True)
    a24 = models.CharField(max_length=3, blank=True, null=True)
    a25 = models.CharField(max_length=3, blank=True, null=True)
    a26 = models.CharField(max_length=3, blank=True, null=True)
    a27 = models.CharField(max_length=3, blank=True, null=True)
    a28 = models.CharField(max_length=3, blank=True, null=True)
    a29 = models.CharField(max_length=3, blank=True, null=True)
    a30 = models.CharField(max_length=3, blank=True, null=True)
    a31 = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tattendance'


class Teacher(models.Model):
    teacherid = models.AutoField(db_column='teacherID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=60)
    designation = models.CharField(max_length=128)
    dob = models.DateField()
    sex = models.CharField(max_length=10)
    religion = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    jod = models.DateField()
    photo = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=128)
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)
    active = models.IntegerField()


    def __str__(self):
        return self.name
    
    class Meta:
        managed = False
        db_table = 'teacher'


class Themes(models.Model):
    themesid = models.AutoField(db_column='themesID', primary_key=True)  # Field name made lowercase.
    sortid = models.IntegerField(db_column='sortID')  # Field name made lowercase.
    themename = models.CharField(max_length=128)
    backend = models.IntegerField()
    frontend = models.IntegerField()
    topcolor = models.TextField()
    leftcolor = models.TextField()

    class Meta:
        managed = False
        db_table = 'themes'


class Tmember(models.Model):
    tmemberid = models.AutoField(db_column='tmemberID', primary_key=True)  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    transportid = models.IntegerField(db_column='transportID')  # Field name made lowercase.
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=40, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    tbalance = models.CharField(max_length=11, blank=True, null=True)
    tjoindate = models.DateField()

    class Meta:
        managed = False
        db_table = 'tmember'


class Transaction(models.Model):
    transactionid = models.AutoField(db_column='transactionID', primary_key=True)  # Field name made lowercase.
    login_id = models.IntegerField()
    trans_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    trans_time = models.TimeField(blank=True, null=True)
    table = models.CharField(max_length=200, blank=True, null=True)
    command = models.CharField(max_length=200, blank=True, null=True)
    primary_key = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    create_date = models.DateTimeField(blank=True, null=True)
    create_userid = models.IntegerField(db_column='create_userID', blank=True, null=True)  # Field name made lowercase.
    create_usertypeid = models.IntegerField(db_column='create_usertypeID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transaction'


class Transport(models.Model):
    transportid = models.AutoField(db_column='transportID', primary_key=True)  # Field name made lowercase.
    route = models.TextField()
    vehicle = models.IntegerField()
    fare = models.CharField(max_length=11)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transport'


class Uattendance(models.Model):
    uattendanceid = models.AutoField(db_column='uattendanceID', primary_key=True)  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    monthyear = models.CharField(max_length=10)
    a1 = models.CharField(max_length=3, blank=True, null=True)
    a2 = models.CharField(max_length=3, blank=True, null=True)
    a3 = models.CharField(max_length=3, blank=True, null=True)
    a4 = models.CharField(max_length=3, blank=True, null=True)
    a5 = models.CharField(max_length=3, blank=True, null=True)
    a6 = models.CharField(max_length=3, blank=True, null=True)
    a7 = models.CharField(max_length=3, blank=True, null=True)
    a8 = models.CharField(max_length=3, blank=True, null=True)
    a9 = models.CharField(max_length=3, blank=True, null=True)
    a10 = models.CharField(max_length=3, blank=True, null=True)
    a11 = models.CharField(max_length=3, blank=True, null=True)
    a12 = models.CharField(max_length=3, blank=True, null=True)
    a13 = models.CharField(max_length=3, blank=True, null=True)
    a14 = models.CharField(max_length=3, blank=True, null=True)
    a15 = models.CharField(max_length=3, blank=True, null=True)
    a16 = models.CharField(max_length=3, blank=True, null=True)
    a17 = models.CharField(max_length=3, blank=True, null=True)
    a18 = models.CharField(max_length=3, blank=True, null=True)
    a19 = models.CharField(max_length=3, blank=True, null=True)
    a20 = models.CharField(max_length=3, blank=True, null=True)
    a21 = models.CharField(max_length=3, blank=True, null=True)
    a22 = models.CharField(max_length=3, blank=True, null=True)
    a23 = models.CharField(max_length=3, blank=True, null=True)
    a24 = models.CharField(max_length=3, blank=True, null=True)
    a25 = models.CharField(max_length=3, blank=True, null=True)
    a26 = models.CharField(max_length=3, blank=True, null=True)
    a27 = models.CharField(max_length=3, blank=True, null=True)
    a28 = models.CharField(max_length=3, blank=True, null=True)
    a29 = models.CharField(max_length=3, blank=True, null=True)
    a30 = models.CharField(max_length=3, blank=True, null=True)
    a31 = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uattendance'


class Update(models.Model):
    updateid = models.AutoField(db_column='updateID', primary_key=True)  # Field name made lowercase.
    version = models.CharField(max_length=100)
    date = models.DateTimeField()
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    log = models.TextField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'update'


class User(models.Model):
    userid = models.AutoField(db_column='userID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=60)
    dob = models.DateField()
    sex = models.CharField(max_length=10)
    religion = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    jod = models.DateField()
    photo = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=128)
    usertypeid = models.IntegerField(db_column='usertypeID')  # Field name made lowercase.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'


class Usertype(models.Model):
    usertypeid = models.AutoField(db_column='usertypeID', primary_key=True)  # Field name made lowercase.
    usertype = models.CharField(max_length=60)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    create_userid = models.IntegerField(db_column='create_userID')  # Field name made lowercase.
    create_username = models.CharField(max_length=60)
    create_usertype = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'usertype'


class Vendor(models.Model):
    vendorid = models.AutoField(db_column='vendorID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendor'


class Visitorinfo(models.Model):
    visitorid = models.BigAutoField(db_column='visitorID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=60, blank=True, null=True)
    email_id = models.CharField(max_length=128, blank=True, null=True)
    phone = models.TextField()
    photo = models.CharField(max_length=128, blank=True, null=True)
    company_name = models.CharField(max_length=128, blank=True, null=True)
    coming_from = models.CharField(max_length=128, blank=True, null=True)
    representing = models.CharField(max_length=128, blank=True, null=True)
    to_meet_personid = models.IntegerField(db_column='to_meet_personID')  # Field name made lowercase.
    to_meet_usertypeid = models.IntegerField(db_column='to_meet_usertypeID')  # Field name made lowercase.
    check_in = models.DateTimeField(blank=True, null=True)
    check_out = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'visitorinfo'


class Weaverandfine(models.Model):
    weaverandfineid = models.AutoField(db_column='weaverandfineID', primary_key=True)  # Field name made lowercase.
    globalpaymentid = models.IntegerField(db_column='globalpaymentID')  # Field name made lowercase.
    invoiceid = models.IntegerField(db_column='invoiceID')  # Field name made lowercase.
    paymentid = models.IntegerField(db_column='paymentID')  # Field name made lowercase.
    studentid = models.IntegerField(db_column='studentID')  # Field name made lowercase.
    schoolyearid = models.IntegerField(db_column='schoolyearID')  # Field name made lowercase.
    weaver = models.FloatField()
    fine = models.FloatField()

    class Meta:
        managed = False
        db_table = 'weaverandfine'
