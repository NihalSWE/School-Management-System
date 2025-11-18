from django.contrib import admin
from .models import *

# Register all models with the Django admin
@admin.register(Activities)
class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('activitiesid', 'activitiescategoryid', 'create_date', 'usertypeid', 'userid')
    list_filter = ('create_date', 'usertypeid')
    search_fields = ('description',)

@admin.register(Activitiescategory)
class ActivitiescategoryAdmin(admin.ModelAdmin):
    list_display = ('activitiescategoryid', 'title', 'schoolyearid', 'create_date')
    search_fields = ('title',)

@admin.register(Activitiescomment)
class ActivitiescommentAdmin(admin.ModelAdmin):
    list_display = ('activitiescommentid', 'activitiesid', 'create_date', 'userid')
    list_filter = ('create_date',)

@admin.register(Activitiesmedia)
class ActivitiesmediaAdmin(admin.ModelAdmin):
    list_display = ('activitiesmediaid', 'activitiesid', 'create_date')

@admin.register(Activitiesstudent)
class ActivitiesstudentAdmin(admin.ModelAdmin):
    list_display = ('activitiesstudentid', 'activitiesid', 'studentid', 'classesid')

@admin.register(Addons)
class AddonsAdmin(admin.ModelAdmin):
    list_display = ('addonsid', 'package_name', 'version', 'status')
    list_filter = ('status',)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('alertid', 'itemid', 'userid', 'usertypeid', 'itemname')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('assetid', 'serial', 'status', 'asset_condition', 'create_date')
    list_filter = ('status', 'asset_condition')

@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ('asset_assignmentid', 'assetid', 'check_out_to', 'status', 'check_out_date')
    list_filter = ('status', 'check_out_date')

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('asset_categoryid', 'category', 'active')
    list_filter = ('active',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignmentid', 'title', 'deadlinedate', 'usertypeid', 'userid')
    search_fields = ('title', 'description')

@admin.register(Assignmentanswer)
class AssignmentanswerAdmin(admin.ModelAdmin):
    list_display = ('assignmentanswerid', 'assignmentid', 'uploaderid', 'answerdate')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendanceid', 'studentid', 'classesid', 'monthyear')
    list_filter = ('monthyear',)

@admin.register(AutomationRec)
class AutomationRecAdmin(admin.ModelAdmin):
    list_display = ('automation_recid', 'studentid', 'date', 'nofmodule')

@admin.register(AutomationShudulu)
class AutomationShuduluAdmin(admin.ModelAdmin):
    list_display = ('automation_shuduluid', 'date', 'day', 'month')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('bookid', 'book', 'author', 'price', 'quantity')
    search_fields = ('book', 'author')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('candidateid', 'studentid', 'verified_by', 'create_date')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryid', 'hostelid', 'class_type', 'hbalance')

@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ('certificate_templateid', 'usertypeid', 'name', 'theme')

@admin.register(Childcare)
class ChildcareAdmin(admin.ModelAdmin):
    list_display = ('childcareid', 'dropped_at', 'received_at', 'parentid', 'received_status')

@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('classesid', 'classes', 'classes_numeric', 'teacherid')
    search_fields = ('classes',)
    list_filter = ('classes_numeric',)

@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    list_display = ('complainid', 'title', 'usertypeid', 'create_date')
    search_fields = ('title',)

@admin.register(ConversationMessageInfo)
class ConversationMessageInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'draft', 'create_date')

@admin.register(ConversationMsg)
class ConversationMsgAdmin(admin.ModelAdmin):
    list_display = ('msg_id', 'conversation_id', 'user_id', 'subject', 'create_date')
    search_fields = ('subject', 'msg')

@admin.register(ConversationUser)
class ConversationUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation_id', 'user_id', 'usertypeid')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('documentid', 'title', 'userid', 'create_date')
    search_fields = ('title',)

@admin.register(Eattendance)
class EattendanceAdmin(admin.ModelAdmin):
    list_display = ('eattendanceid', 'examid', 'classesid', 'date', 'studentid')

@admin.register(Ebooks)
class EbooksAdmin(admin.ModelAdmin):
    list_display = ('ebooksid', 'name', 'author', 'classesid')
    search_fields = ('name', 'author')

@admin.register(Emailsetting)
class EmailsettingAdmin(admin.ModelAdmin):
    list_display = ('fieldoption', 'value')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('eventid', 'title', 'fdate', 'tdate', 'create_date')
    search_fields = ('title',)
    list_filter = ('fdate',)

@admin.register(Eventcounter)
class EventcounterAdmin(admin.ModelAdmin):
    list_display = ('eventcounterid', 'eventid', 'username', 'status')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('examid', 'exam', 'date')
    search_fields = ('exam',)

@admin.register(Examschedule)
class ExamscheduleAdmin(admin.ModelAdmin):
    list_display = ('examscheduleid', 'examid', 'classesid', 'edate')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expenseid', 'expense', 'amount', 'date', 'userid')
    list_filter = ('date',)

@admin.register(Feetypes)
class FeetypesAdmin(admin.ModelAdmin):
    list_display = ('feetypesid', 'feetypes')
    search_fields = ('feetypes',)

@admin.register(Fmenu)
class FmenuAdmin(admin.ModelAdmin):
    list_display = ('fmenuid', 'menu_name', 'status', 'topbar')

@admin.register(FmenuRelation)
class FmenuRelationAdmin(admin.ModelAdmin):
    list_display = ('fmenu_relationid', 'fmenuid', 'menu_typeid', 'menu_status')

@admin.register(FrontendSetting)
class FrontendSettingAdmin(admin.ModelAdmin):
    list_display = ('fieldoption', 'value')

@admin.register(FrontendTemplate)
class FrontendTemplateAdmin(admin.ModelAdmin):
    list_display = ('frontend_templateid', 'template_name')

@admin.register(Globalpayment)
class GlobalpaymentAdmin(admin.ModelAdmin):
    list_display = ('globalpaymentid', 'classesid', 'studentid', 'clearancetype')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('gradeid', 'grade', 'point', 'gradefrom', 'gradeupto')

@admin.register(Hmember)
class HmemberAdmin(admin.ModelAdmin):
    list_display = ('hmemberid', 'hostelid', 'studentid', 'hjoindate')

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('holidayid', 'title', 'fdate', 'tdate', 'create_date')
    search_fields = ('title',)

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('hostelid', 'name', 'htype')
    search_fields = ('name',)

@admin.register(HourlyTemplate)
class HourlyTemplateAdmin(admin.ModelAdmin):
    list_display = ('hourly_templateid', 'hourly_grades', 'hourly_rate')

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('incomeid', 'name', 'amount', 'date')
    search_fields = ('name',)

@admin.register(IniConfig)
class IniConfigAdmin(admin.ModelAdmin):
    list_display = ('configid', 'type', 'config_key', 'value')

@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ('instructionid', 'title')
    search_fields = ('title',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoiceid', 'studentid', 'feetype', 'amount', 'date', 'paidstatus')
    list_filter = ('paidstatus', 'date')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('issueid', 'bookid', 'issue_date', 'due_date', 'return_date')

@admin.register(Leaveapplications)
class LeaveapplicationsAdmin(admin.ModelAdmin):
    list_display = ('leaveapplicationid', 'leavecategoryid', 'apply_date', 'from_date', 'status')
    list_filter = ('status', 'apply_date')

@admin.register(Leaveassign)
class LeaveassignAdmin(admin.ModelAdmin):
    list_display = ('leaveassignid', 'leavecategoryid', 'usertypeid', 'leaveassignday')

@admin.register(Leavecategory)
class LeavecategoryAdmin(admin.ModelAdmin):
    list_display = ('leavecategoryid', 'leavecategory', 'leavegender')
    search_fields = ('leavecategory',)

@admin.register(Lmember)
class LmemberAdmin(admin.ModelAdmin):
    list_display = ('lmemberid', 'studentid', 'name', 'ljoindate')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('locationid', 'location', 'active')
    search_fields = ('location',)

@admin.register(Loginlog)
class LoginlogAdmin(admin.ModelAdmin):
    list_display = ('loginlogid', 'ip', 'login', 'usertypeid', 'userid')
    list_filter = ('login',)

@admin.register(Mailandsms)
class MailandsmsAdmin(admin.ModelAdmin):
    list_display = ('mailandsmsid', 'usertypeid', 'type', 'create_date')
    list_filter = ('type',)

@admin.register(Mailandsmstemplate)
class MailandsmstemplateAdmin(admin.ModelAdmin):
    list_display = ('mailandsmstemplateid', 'name', 'usertypeid', 'type')
    search_fields = ('name',)

@admin.register(Mailandsmstemplatetag)
class MailandsmstemplatetagAdmin(admin.ModelAdmin):
    list_display = ('mailandsmstemplatetagid', 'usertypeid', 'tagname')

@admin.register(Maininvoice)
class MaininvoiceAdmin(admin.ModelAdmin):
    list_display = ('maininvoiceid', 'maininvoicestudentid', 'maininvoicedate', 'maininvoicestatus')
    list_filter = ('maininvoicestatus',)

@admin.register(MakePayment)
class MakePaymentAdmin(admin.ModelAdmin):
    list_display = ('make_paymentid', 'userid', 'payment_amount', 'create_date')

@admin.register(ManageSalary)
class ManageSalaryAdmin(admin.ModelAdmin):
    list_display = ('manage_salaryid', 'userid', 'salary', 'template')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('markid', 'exam', 'studentid', 'subject', 'year')

@admin.register(Markpercentage)
class MarkpercentageAdmin(admin.ModelAdmin):
    list_display = ('markpercentageid', 'markpercentagetype', 'percentage')

@admin.register(Markrelation)
class MarkrelationAdmin(admin.ModelAdmin):
    list_display = ('markrelationid', 'markid', 'markpercentageid')

@admin.register(Marksetting)
class MarksettingAdmin(admin.ModelAdmin):
    list_display = ('marksettingid', 'examid', 'classesid', 'subjectid')

@admin.register(Marksettingrelation)
class MarksettingrelationAdmin(admin.ModelAdmin):
    list_display = ('marksettingrelationid', 'marktypeid', 'marksettingid')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('mediaid', 'userid', 'mcategoryid', 'file_name')

@admin.register(MediaCategory)
class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ('mcategoryid', 'userid', 'folder_name', 'create_time')

@admin.register(MediaGallery)
class MediaGalleryAdmin(admin.ModelAdmin):
    list_display = ('media_galleryid', 'file_type', 'file_name', 'file_upload_date')

@admin.register(MediaShare)
class MediaShareAdmin(admin.ModelAdmin):
    list_display = ('shareid', 'classesid', 'public', 'file_or_folder')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('menuid', 'menuname', 'link', 'status', 'priority')
    search_fields = ('menuname',)

@admin.register(Migrations)
class MigrationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'version')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('noticeid', 'title', 'date', 'create_date')
    search_fields = ('title',)

@admin.register(OnlineExam)
class OnlineExamAdmin(admin.ModelAdmin):
    list_display = ('onlineexamid', 'name', 'examstatus', 'startdatetime')
    search_fields = ('name',)

@admin.register(OnlineExamQuestion)
class OnlineExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('onlineexamquestionid', 'onlineexamid', 'questionid')

@admin.register(OnlineExamType)
class OnlineExamTypeAdmin(admin.ModelAdmin):
    list_display = ('onlineexamtypeid', 'title', 'examtypenumber')

@admin.register(OnlineExamUserAnswer)
class OnlineExamUserAnswerAdmin(admin.ModelAdmin):
    list_display = ('onlineexamuseranswerid', 'onlineexamquestionid', 'onlineexamid')

@admin.register(OnlineExamUserAnswerOption)
class OnlineExamUserAnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('onlineexamuseransweroptionid', 'questionid', 'onlineexamid')

@admin.register(OnlineExamUserStatus)
class OnlineExamUserStatusAdmin(admin.ModelAdmin):
    list_display = ('onlineexamuserstatus', 'onlineexamid', 'score', 'time')

@admin.register(Onlineadmission)
class OnlineadmissionAdmin(admin.ModelAdmin):
    list_display = ('onlineadmissionid', 'name', 'classesid', 'status')
    list_filter = ('status',)

@admin.register(Overtime)
class OvertimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'hours', 'userid')

@admin.register(Pages)
class PagesAdmin(admin.ModelAdmin):
    list_display = ('pagesid', 'title', 'status', 'visibility')
    search_fields = ('title',)

@admin.register(Parents)
class ParentsAdmin(admin.ModelAdmin):
    list_display = ('parentsid', 'name', 'email', 'phone', 'active')
    search_fields = ('name', 'email')
    list_filter = ('active',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('paymentid', 'studentid', 'paymentamount', 'paymentdate')
    list_filter = ('paymentdate',)

@admin.register(PermissionRelationships)
class PermissionRelationshipsAdmin(admin.ModelAdmin):
    list_display = ('id', 'permission_id', 'usertype_id')

@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ('permissionid', 'name', 'description', 'active')
    search_fields = ('name',)

@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('postsid', 'title', 'status', 'publish_date')
    search_fields = ('title',)

@admin.register(PostsCategories)
class PostsCategoriesAdmin(admin.ModelAdmin):
    list_display = ('posts_categoriesid', 'posts_categories')
    search_fields = ('posts_categories',)

@admin.register(PostsCategory)
class PostsCategoryAdmin(admin.ModelAdmin):
    list_display = ('posts_categoryid', 'postsid', 'posts_categoriesid')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productid', 'productname', 'productbuyingprice', 'productsellingprice')
    search_fields = ('productname',)

@admin.register(Productcategory)
class ProductcategoryAdmin(admin.ModelAdmin):
    list_display = ('productcategoryid', 'productcategoryname')
    search_fields = ('productcategoryname',)

@admin.register(Productpurchase)
class ProductpurchaseAdmin(admin.ModelAdmin):
    list_display = ('productpurchaseid', 'productpurchasereferenceno', 'productpurchasedate', 'productpurchasestatus')

@admin.register(Productpurchaseitem)
class ProductpurchaseitemAdmin(admin.ModelAdmin):
    list_display = ('productpurchaseitemid', 'productpurchaseid', 'productid', 'productpurchasequantity')

@admin.register(Productpurchasepaid)
class ProductpurchasepaidAdmin(admin.ModelAdmin):
    list_display = ('productpurchasepaidid', 'productpurchaseid', 'productpurchasepaidamount')

@admin.register(Productsale)
class ProductsaleAdmin(admin.ModelAdmin):
    list_display = ('productsaleid', 'productsalereferenceno', 'productsaledate', 'productsalestatus')

@admin.register(Productsaleitem)
class ProductsaleitemAdmin(admin.ModelAdmin):
    list_display = ('productsaleitemid', 'productsaleid', 'productid', 'productsalequantity')

@admin.register(Productsalepaid)
class ProductsalepaidAdmin(admin.ModelAdmin):
    list_display = ('productsalepaidid', 'productsaleid', 'productsalepaidamount')

@admin.register(Productsupplier)
class ProductsupplierAdmin(admin.ModelAdmin):
    list_display = ('productsupplierid', 'productsuppliercompanyname', 'productsuppliername')
    search_fields = ('productsuppliercompanyname',)

@admin.register(Productwarehouse)
class ProductwarehouseAdmin(admin.ModelAdmin):
    list_display = ('productwarehouseid', 'productwarehousename', 'productwarehousecode')
    search_fields = ('productwarehousename',)

@admin.register(Promotionlog)
class PromotionlogAdmin(admin.ModelAdmin):
    list_display = ('promotionlogid', 'promotiontype', 'classesid', 'status')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('purchaseid', 'assetid', 'quantity', 'purchase_date')

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('answerid', 'questionid', 'optionid', 'typenumber')

@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('questionbankid', 'levelid', 'groupid', 'mark')
    search_fields = ('question',)

@admin.register(QuestionGroup)
class QuestionGroupAdmin(admin.ModelAdmin):
    list_display = ('questiongroupid', 'title')

@admin.register(QuestionLevel)
class QuestionLevelAdmin(admin.ModelAdmin):
    list_display = ('questionlevelid', 'name')

@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('optionid', 'questionid', 'name')

@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('questiontypeid', 'typenumber', 'name')

@admin.register(Reset)
class ResetAdmin(admin.ModelAdmin):
    list_display = ('resetid', 'keyid', 'email')

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('routineid', 'classesid', 'subjectid', 'day', 'start_time')

@admin.register(SalaryOption)
class SalaryOptionAdmin(admin.ModelAdmin):
    list_display = ('salary_optionid', 'salary_templateid', 'option_type', 'label_name')

@admin.register(SalaryTemplate)
class SalaryTemplateAdmin(admin.ModelAdmin):
    list_display = ('salary_templateid', 'salary_grades', 'basic_salary')

@admin.register(SchoolSessions)
class SchoolSessionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'timestamp')

@admin.register(Schoolyear)
class SchoolyearAdmin(admin.ModelAdmin):
    list_display = ('schoolyearid', 'schoolyear', 'startingdate', 'endingdate')
    search_fields = ('schoolyear',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('sectionid', 'section', 'classesid', 'teacherid')
    search_fields = ('section',)
    list_filter = ('classesid',)

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('fieldoption', 'value')

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('sliderid', 'pagesid', 'slider')

@admin.register(Smssettings)
class SmssettingsAdmin(admin.ModelAdmin):
    list_display = ('smssettingsid', 'types', 'field_names')

@admin.register(Sociallink)
class SociallinkAdmin(admin.ModelAdmin):
    list_display = ('sociallinkid', 'usertypeid', 'userid')

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('sponsorid', 'name', 'organisation_name', 'phone')
    search_fields = ('name',)

@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ('sponsorshipid', 'sponsorid', 'studentid', 'amount')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('studentid', 'name', 'classesid', 'sectionid', 'roll', 'active')
    search_fields = ('name', 'registerno')
    list_filter = ('classesid', 'active')
    list_select_related = ('classesid', 'sectionid', 'parentid')

@admin.register(Studentextend)
class StudentextendAdmin(admin.ModelAdmin):
    list_display = ('studentextendid', 'studentid', 'studentgroupid')

@admin.register(Studentgroup)
class StudentgroupAdmin(admin.ModelAdmin):
    list_display = ('studentgroupid', 'group')

@admin.register(Studentrelation)
class StudentrelationAdmin(admin.ModelAdmin):
    list_display = ('studentrelationid', 'srstudentid', 'srname')

@admin.register(SubAttendance)
class SubAttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendanceid', 'studentid', 'subjectid', 'monthyear')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subjectid', 'subject', 'classesid', 'type', 'teacher_name')
    search_fields = ('subject',)
    list_filter = ('classesid', 'type')

@admin.register(Subjectteacher)
class SubjectteacherAdmin(admin.ModelAdmin):
    list_display = ('subjectteacherid', 'subjectid', 'classesid', 'teacherid')

@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('syllabusid', 'title', 'date', 'classesid')
    search_fields = ('title',)

@admin.register(Systemadmin)
class SystemadminAdmin(admin.ModelAdmin):
    list_display = ('systemadminid', 'name', 'email', 'active')
    search_fields = ('name', 'email')
    list_filter = ('active',)

@admin.register(Tattendance)
class TattendanceAdmin(admin.ModelAdmin):
    list_display = ('tattendanceid', 'teacherid', 'monthyear')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacherid', 'name', 'designation', 'email', 'active')
    search_fields = ('name', 'email')
    list_filter = ('active',)

@admin.register(Themes)
class ThemesAdmin(admin.ModelAdmin):
    list_display = ('themesid', 'themename', 'backend', 'frontend')

@admin.register(Tmember)
class TmemberAdmin(admin.ModelAdmin):
    list_display = ('tmemberid', 'studentid', 'transportid')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transactionid', 'trans_name', 'trans_date', 'table')

@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('transportid', 'route', 'vehicle', 'fare')

@admin.register(Uattendance)
class UattendanceAdmin(admin.ModelAdmin):
    list_display = ('uattendanceid', 'userid', 'monthyear')

@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('updateid', 'version', 'date', 'status')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'name', 'email', 'active')
    search_fields = ('name', 'email')
    list_filter = ('active',)

@admin.register(Usertype)
class UsertypeAdmin(admin.ModelAdmin):
    list_display = ('usertypeid', 'usertype')
    search_fields = ('usertype',)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendorid', 'name', 'email', 'phone')
    search_fields = ('name',)

@admin.register(Visitorinfo)
class VisitorinfoAdmin(admin.ModelAdmin):
    list_display = ('visitorid', 'name', 'to_meet_personid', 'check_in', 'status')

@admin.register(Weaverandfine)
class WeaverandfineAdmin(admin.ModelAdmin):
    list_display = ('weaverandfineid', 'studentid', 'weaver', 'fine')