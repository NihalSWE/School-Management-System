# In backend/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

#--for documentation
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# --- 1. IMPORT THE DEFAULT VIEW WITH A NEW NAME ---
from rest_framework_simplejwt.views import TokenRefreshView as DefaultTokenRefreshView

# --- 2. IMPORT OUR NEW CUSTOM SERIALIZER ---
from .serializers import CustomTokenRefreshSerializer


# --- 3. CREATE A CUSTOM VIEW THAT USES OUR SERIALIZER ---
class CustomTokenRefreshView(DefaultTokenRefreshView):
    """
    This custom view uses our CustomTokenRefreshSerializer
    to refresh tokens without checking the database.
    """
    serializer_class = CustomTokenRefreshSerializer


# --- 4. ROUTER (No Change) ---
router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet, basename='teacher')
router.register(r'classes', views.ClassesViewSet, basename='class')
router.register(r'sections', views.SectionViewSet, basename='section')
router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r'routines', views.RoutineViewSet, basename='routine')
router.register(r'syllabuses', views.SyllabusViewSet, basename='syllabus')
router.register(r'assignments', views.AssignmentViewSet, basename='assignment')
router.register(r'assignmentanswers', views.AssignmentanswerViewSet, basename='assignmentanswer')
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'parents', views.ParentsViewSet, basename='parent')
router.register(r'systemadmins', views.SystemadminViewSet, basename='systemadmin')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'exams', views.ExamViewSet, basename='exam')
router.register(r'grades', views.GradeViewSet, basename='grade')
router.register(r'examschedules', views.ExamscheduleViewSet, basename='examschedule')
router.register(r'marks', views.MarkViewSet, basename='mark')
router.register(r'markrelations', views.MarkrelationViewSet, basename='markrelation')
router.register(r'markpercentages', views.MarkpercentageViewSet, basename='markpercentage')
router.register(r'subjectteachers', views.SubjectteacherViewSet, basename='subjectteacher')
router.register(r'studentattendance', views.StudentattendanceViewSet, basename='studentattendance')
router.register(r'teacherattendance', views.TeacherattendanceViewSet, basename='teacherattendance')
router.register(r'userattendance', views.UserattendanceViewSet, basename='userattendance')
router.register(r'examattendance', views.ExamattendanceViewSet, basename='examattendance')
router.register(r'subattendance', views.SubAttendanceViewSet, basename='subattendance')
router.register(r'usertypes', views.UsertypeViewSet, basename='usertype')
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'media-folders', views.MediaCategoryViewSet, basename='media-category')
router.register(r'media-files', views.MediaViewSet, basename='media-file')
router.register(r'question-groups', views.QuestionGroupViewSet, basename='question-group')
router.register(r'question-levels', views.QuestionLevelViewSet, basename='question-level')
router.register(r'instructions', views.InstructionViewSet, basename='instruction')
router.register(r'question-bank', views.QuestionBankViewSet, basename='question-bank')
router.register(r'online-exam-types', views.OnlineExamTypeViewSet, basename='online-exam-type')
router.register(r'online-exams', views.OnlineExamViewSet, basename='online-exam')
router.register(r'online-exam-questions', views.OnlineExamQuestionViewSet, basename='online-exam-question')
router.register(r'transport-routes', views.TransportViewSet, basename='transport-route')
router.register(r'transport-members', views.TmemberViewSet, basename='transport-member')
router.register(r'hostels', views.HostelViewSet, basename='hostel')
router.register(r'hostel-categories', views.CategoryViewSet, basename='hostel-category')
router.register(r'hostel-members', views.HmemberViewSet, basename='hostel-member')
router.register(r'salary-templates', views.SalaryTemplateViewSet, basename='salary-template')
router.register(r'salary-options', views.SalaryOptionViewSet, basename='salary-option')
router.register(r'hourly-templates', views.HourlyTemplateViewSet, basename='hourly-template')
router.register(r'manage-salary', views.ManageSalaryViewSet, basename='manage-salary')
router.register(r'make-payment', views.MakePaymentViewSet, basename='make-payment')
router.register(r'overtime', views.OvertimeViewSet, basename='overtime')
router.register(r'vendors', views.VendorViewSet, basename='vendor')
router.register(r'locations', views.LocationViewSet, basename='location')
router.register(r'asset-categories', views.AssetCategoryViewSet, basename='asset-category')
router.register(r'assets', views.AssetViewSet, basename='asset')
router.register(r'purchases', views.PurchaseViewSet, basename='purchase')
router.register(r'asset-assignments', views.AssetAssignmentViewSet, basename='asset-assignment')
router.register(r'product-categories', views.ProductcategoryViewSet, basename='product-category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'product-suppliers', views.ProductsupplierViewSet, basename='product-supplier')
router.register(r'product-warehouses', views.ProductwarehouseViewSet, basename='product-warehouse')
router.register(r'product-purchases', views.ProductpurchaseViewSet, basename='product-purchase')
router.register(r'product-purchase-items', views.ProductpurchaseitemViewSet, basename='product-purchase-item')
router.register(r'product-purchase-paid', views.ProductpurchasepaidViewSet, basename='product-purchase-paid')
router.register(r'product-sales', views.ProductsaleViewSet, basename='product-sale')
router.register(r'product-sale-items', views.ProductsaleitemViewSet, basename='product-sale-item')
router.register(r'product-sale-paid', views.ProductsalepaidViewSet, basename='product-sale-paid')
router.register(r'leave-categories', views.LeavecategoryViewSet, basename='leave-category')
router.register(r'leave-assigns', views.LeaveassignViewSet, basename='leave-assign')
router.register(r'leave-applications', views.LeaveapplicationsViewSet, basename='leave-application')
router.register(r'activities-categories', views.ActivitiescategoryViewSet, basename='activities-category')
router.register(r'activities', views.ActivitiesViewSet, basename='activities')
router.register(r'childcare', views.ChildcareViewSet, basename='childcare')
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'ebooks', views.EbooksViewSet, basename='ebook')
router.register(r'library-members', views.LmemberViewSet, basename='library-member')
router.register(r'book-issues', views.IssueViewSet, basename='book-issue')
router.register(r'sponsors', views.SponsorViewSet, basename='sponsor')
router.register(r'candidates', views.CandidateViewSet, basename='candidate')
router.register(r'sponsorships', views.SponsorshipViewSet, basename='sponsorship')
router.register(r'fee-types', views.FeetypesViewSet, basename='fee-type')
router.register(r'expenses', views.ExpenseViewSet, basename='expense')
router.register(r'incomes', views.IncomeViewSet, basename='income')
router.register(r'global-payments', views.GlobalpaymentViewSet, basename='global-payment')
router.register(r'main-invoices', views.MaininvoiceViewSet, basename='main-invoice')
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')
router.register(r'payments', views.PaymentViewSet, basename='payment')
router.register(r'notices', views.NoticeViewSet, basename='notice')
router.register(r'events', views.EventViewSet, basename='event')
router.register(r'holidays', views.HolidayViewSet, basename='holiday')
router.register(r'online-admissions', views.OnlineadmissionViewSet, basename='online-admission')
router.register(r'public-admission', views.PublicOnlineadmissionViewSet, basename='public-admission')
router.register(r'visitor-info', views.VisitorinfoViewSet, basename='visitor-info')


# --- 5. URLPATTERNS (Updated) ---
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='custom_login'),
    
    path('test/', views.TestAPIView.as_view(), name='test_api'),
    # --- 6. USE OUR NEW CUSTOM REFRESH VIEW ---
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    # --- NEW MESSAGE (REPLY/VIEW) ROUTE ---
    path(
        'conversations/msgs/<int:convo_id>/', 
        views.ConversationMsgViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='conversation-msgs'
    ),
    
    # --- "FLAWLESS" DOCUMENTATION URLS ---
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # --- 2. THIS IS THE "FLAWLESS" FIX ---
    # We replaced 'SpectacularSwaggerView' with 'SpectacularRedocView'
    path('docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # ---
    
    path('', include(router.urls)),
]