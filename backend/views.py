# In backend/views.py
from django.db import transaction
from django.http import JsonResponse
from .models import * 
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.utils import timezone

# DRF Imports
from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAdminUser


# --- 1. IMPORT OUR NEW HELPERS ---
from .token_utils import get_token_claim
from .hash_utils import check_ci_hash, make_ci_hash
from .mark_services import recompute_mark_grade
# ---

# --- IMPORT ALL PERMISSION CLASSES ---
from .permissions import (
    IsAdminOrReadOnly, IsAdminOrStudentOwner, 
    IsAdminOrTeacherOwner, IsAdminOrParentOwner, IsAdminUser,
    IsAdminOrTeacherForMarks,IsAdminOrTeacherForAttendance,
    IsAdminOrTeacherSelfCreateRead, IsAdminOrStaffSelfCreateRead,
    IsAdminOrTeacherWriteOwner, IsStudentOwnerForAnswer,
    IsAdminOrTeacherWriteReadOnly,IsAdminOrTeacherOrStudentReadOnly,
    IsConversationParticipant,
)
from .jwt_utils import get_tokens_for_user 

# Serializer Imports
from .serializers import (
    TeacherSerializer, ClassesSerializer, SectionSerializer, 
    SubjectSerializer, StudentSerializer, ParentsSerializer,
    SystemadminSerializer, UserSerializer,ExamSerializer, 
    GradeSerializer,MarkSerializer,SubjectteacherSerializer,
    MarkrelationSerializer,MarkpercentageSerializer,
    StudentattendanceSerializer, TeacherattendanceSerializer, 
    UserattendanceSerializer, ExamattendanceSerializer,
    RoutineSerializer, SyllabusSerializer, AssignmentSerializer,
    AssignmentanswerSerializer, HolidaySerializer,SubAttendanceSerializer,
    ExamscheduleSerializer,PromotionlogSerializer,UsertypeSerializer,
    ConversationMsgSerializer,ConversationSerializer,
    
)




# --- 2. CUSTOM LOGIN VIEW (Uses hash_utils) ---
class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = None
        user_object = None
        
        try:
            u = Teacher.objects.get(username=username)
            if check_ci_hash(password, u.password): user_object = u
        except Teacher.DoesNotExist: pass
        if not user_object:
            try:
                u = Student.objects.get(username=username)
                if check_ci_hash(password, u.password): user_object = u
            except Student.DoesNotExist: pass
        if not user_object:
            try:
                u = Parents.objects.get(username=username)
                if check_ci_hash(password, u.password): user_object = u
            except Parents.DoesNotExist: pass
        if not user_object:
            try:
                u = Systemadmin.objects.get(username=username)
                if check_ci_hash(password, u.password): user_object = u
            except Systemadmin.DoesNotExist: pass
        if not user_object:
            try:
                u = User.objects.get(username=username)
                if check_ci_hash(password, u.password): user_object = u
            except User.DoesNotExist: pass

        if user_object:
            # "Migration" logic
            if '$' in user_object.password:
                user_object.password = make_ci_hash(password)
                user_object.save(update_fields=['password'])
            
            user = user_object
            tokens = get_tokens_for_user(user)
            user_type_str = None
            if isinstance(user, Teacher): user_type_str = 'teacher'
            elif isinstance(user, Student): user_type_str = 'student'
            elif isinstance(user, Parents): user_type_str = 'parent'
            elif isinstance(user, Systemadmin): user_type_str = 'systemadmin'
            elif isinstance(user, User): user_type_str = 'staff'

            response_data = {
                'refresh': tokens['refresh'],
                'access': tokens['access'],
                'user_type': user_type_str,
                'email': user.email,
                'userid': user.pk,
                'name': user.name,
                'username': user.username
            }
            return Response(response_data, status=status.HTTP_200_OK)
            
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# --- 3. PUBLIC TEST API VIEW (No Auth) ---
class TestAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [] 

    def get(self, request, *args, **kwargs):
        teacher_data = None
        try:
            teacher = Teacher.objects.first() 
            if teacher:
                teacher_data = TeacherSerializer(teacher).data
        except Exception as e:
            teacher_data = {"error": str(e)}

        student_data = None
        try:
            student = Student.objects.first()
            if student:
                student_data = StudentSerializer(student).data
        except Exception as e:
            student_data = {"error": str(e)}

        response = {
            "status": "success",
            "message": "This is a test endpoint with real database data.",
            "test_teacher": teacher_data or "No teachers found in database.",
            "test_student": student_data or "No students found in database."
        }
        return Response(response, status=status.HTTP_200_OK)


# --- 4. API ViewSets (ALL HARDENED) ---

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('-teacherid')
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminOrTeacherOwner]
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']
    
    def get_queryset(self):
        # --- HARDENED ---
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0) # Safe default
        
        if user_type == 'systemadmin' :
            return Teacher.objects.all()
        if user_type == 'teacher':
            return Teacher.objects.filter(teacherid=user_id) 
        
        # All other roles (student, parent, staff) are forbidden
        raise exceptions.PermissionDenied(detail="You do not have permission to view this list.")
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context 

class ParentsViewSet(viewsets.ModelViewSet):
    queryset = Parents.objects.all().order_by('-parentsid')
    serializer_class = ParentsSerializer
    permission_classes = [IsAdminOrParentOwner]
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']
    
    def get_queryset(self):
        # --- HARDENED ---
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)
        
        if user_type == 'systemadmin' :
            return Parents.objects.all()
        if user_type == 'parent':
            return Parents.objects.filter(parentsid=user_id)
        
        # Admins can create, but only owners can list
        if user_type == 'systemadmin' and self.action == 'create':
             return Parents.objects.none()
        
        # All other roles are forbidden
        raise exceptions.PermissionDenied(detail="You do not have permission to view this list.")
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class SystemadminViewSet(viewsets.ModelViewSet):
    queryset = Systemadmin.objects.all()
    serializer_class = SystemadminSerializer
    permission_classes = [IsAdminUser] 
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] 
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-studentid')
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrTeacherOrStudentReadOnly]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        # --- HARDENED ---
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)
        
        if user_type == 'systemadmin' :
            return Student.objects.all()
        if user_type == 'student':
            return Student.objects.filter(studentid=user_id) 
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Student.objects.filter(classesid__in=class_ids)
        
        # All other roles are forbidden
        raise exceptions.PermissionDenied(detail="You do not have permission to view this list.")
    
    # --- THIS IS THE "FLAWLESS" NEW PROMOTION FEATURE ---
    @action(
        detail=False, 
        methods=['post'], 
        url_path='promote',
        permission_classes=[IsAdminUser] # "Flawless" safety net
    )
    def promote(self, request):
        """
        "Flawless" Admin tool to promote students from one
        class and school year to a new one.
        """
        # 1. "Flawlessly" get data
        data = request.data
        from_schoolyear_id = data.get('schoolyearid')
        from_class_id = data.get('classesid')
        to_schoolyear_id = data.get('jumpschoolyearid')
        to_class_id = data.get('jumpclassid')
        promotion_type = data.get('promotiontype', 'Normal')

        # 2. "Flawless" Validation
        if not all([from_schoolyear_id, from_class_id, to_schoolyear_id, to_class_id]):
            return Response(
                {'error': 'Missing required fields: schoolyearid, classesid, jumpschoolyearid, or jumpclassid.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        promoted_student_ids = []
        
        # 3. "Flawless" Atomic Transaction (Our "Safety Net")
        try:
            with transaction.atomic():
                
                # --- "FLAWLESS" FIX: GET THE "TO" CLASS OBJECT ---
                try:
                    to_class_object = Classes.objects.get(classesid=to_class_id)
                except Classes.DoesNotExist:
                    raise Exception(f"Promotion failed: The 'To' Class (ID: {to_class_id}) does not exist.")
                # ---
                
                # 4. Find all "flawless" students to promote
                students_to_promote = Student.objects.filter(
                    schoolyearid=from_schoolyear_id,
                    classesid=from_class_id
                )
                
                if not students_to_promote.exists():
                    return Response(
                        {'error': 'No students found in the "From" class to promote.'},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # 5. "Flawlessly" promote them
                for student in students_to_promote:
                    student.schoolyearid = to_schoolyear_id
                    
                    # --- "FLAWLESS" FIX: ASSIGN THE OBJECT ---
                    student.classesid = to_class_object
                    # ---
                    
                    student.save(update_fields=['schoolyearid', 'classesid'])
                    promoted_student_ids.append(student.studentid)

                # 6. "Flawlessly" log this "flawless" action
                log_data = {
                    'promotiontype': promotion_type,
                    'classesid': from_class_id,
                    'jumpclassid': to_class_id,
                    'schoolyearid': from_schoolyear_id,
                    'jumpschoolyearid': to_schoolyear_id,
                    'promotestudents': str(promoted_student_ids),
                    'status': 1
                }
                
                log_serializer = PromotionlogSerializer(
                    data=log_data,
                    context={'request': request}
                )
                
                if log_serializer.is_valid():
                    log_serializer.save()
                else:
                    raise Exception(f"Failed to create promotion log: {log_serializer.errors}")

        except Exception as e:
            # The "flawless" transaction failed
            return Response(
                {'error': f"{e}"}, # "Flawlessly" show the real error
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # 7. "Flawless" Success
        return Response(
            {'status': f"Successfully promoted {len(promoted_student_ids)} students."},
            status=status.HTTP_200_OK
        )


class ClassesViewSet(viewsets.ModelViewSet):
    serializer_class = ClassesSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        # --- HARDENED ---
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)
        
        # Read-only is allowed for all authenticated users
        if user_type: 
            return Classes.objects.all()
        
        return Classes.objects.none()


class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        # --- HARDENED ---
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)
        
        # Read-only is allowed for all authenticated users
        if user_type:
            return Section.objects.all()
        
        return Section.objects.none()


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        # --- HARDENED ---
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)
        
        # Read-only is allowed for all authenticated users
        if user_type:
            return Subject.objects.all()
            
        return Subject.objects.none()
    

# --- MARKING SYSTEM "SETUP" VIEWSETS ---

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAdminUser]
    ordering_fields = ['create_date']
    ordering = ['-create_date']

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminUser]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
  

class ExamscheduleViewSet(viewsets.ModelViewSet):
    """
    API for Exam Schedules.
    - Admins/Teachers can write.
    - Students/Parents can read.
    """
    queryset = Examschedule.objects.all().order_by('-examscheduleid')
    serializer_class = ExamscheduleSerializer
    permission_classes = [IsAdminOrTeacherWriteReadOnly] # <-- Use our new "flawless" permission

    def get_queryset(self):
        # "Flawless" hardened logic, similar to Routine
        user = self.request.user
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)

        if user_type == 'systemadmin':
            return Examschedule.objects.all()

        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Examschedule.objects.filter(classesid__in=class_ids)

        if user_type == 'student' and hasattr(user, 'classesid_id'):
            return Examschedule.objects.filter(classesid=user.classesid_id)

        if user_type == 'parent':
            try:
                student = Student.objects.filter(parentid=user_id).first()
                if student:
                    return Examschedule.objects.filter(classesid=student.classesid_id)
            except ObjectDoesNotExist:
                return Examschedule.objects.none()

        return Examschedule.objects.none()  
  

# --- THE MAIN MARK VIEWSET ---

class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    permission_classes = [IsAdminOrTeacherForMarks]
    ordering_fields = ['create_date']
    ordering = ['-create_date']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def get_queryset(self):
        # --- HARDENED ---
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)

        if not user_id:
            return Mark.objects.none()

        if user_type == 'systemadmin':
            return Mark.objects.all()

        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Mark.objects.filter(classesid__in=class_ids)

        if user_type == 'student':
            return Mark.objects.filter(studentid=user_id)

        if user_type == 'parent':
            student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
            return Mark.objects.filter(studentid__in=student_ids)

        return Mark.objects.none()


class MarkrelationViewSet(viewsets.ModelViewSet):
    queryset = Markrelation.objects.all()
    serializer_class = MarkrelationSerializer
    permission_classes = [IsAdminOrTeacherForMarks]

    # --- THIS IS THE "FLAWLESS" FIX ---

    def perform_create(self, serializer):
        """Called when a new score is ADDED."""
        mark_relation = serializer.save()
        # After saving, recompute the total grade
        recompute_mark_grade(mark_relation.markid)

    def perform_update(self, serializer):
        """Called when a score is EDITED."""
        mark_relation = serializer.save()
        # After updating, recompute the total grade
        recompute_mark_grade(mark_relation.markid)

    def perform_destroy(self, instance):
        """Called when a score is DELETED."""
        mark_id = instance.markid
        instance.delete()
        # After deleting, recompute the total grade
        recompute_mark_grade(mark_id)
    
class MarkpercentageViewSet(viewsets.ModelViewSet):
    queryset = Markpercentage.objects.all()
    serializer_class = MarkpercentageSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


# --- ATTENDANCE VIEWSETS ---

class StudentattendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = StudentattendanceSerializer
    permission_classes = [IsAdminOrTeacherForAttendance]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        # --- HARDENED ---
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)

        if not user_id:
            return Attendance.objects.none()

        if user_type == 'systemadmin':
            return Attendance.objects.all()

        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Attendance.objects.filter(classesid__in=class_ids)

        if user_type == 'student':
            return Attendance.objects.filter(studentid=user_id)

        if user_type == 'parent':
            student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
            return Attendance.objects.filter(studentid__in=student_ids)

        return Attendance.objects.none()
    
    # --- THIS IS THE NEW "BULK" FEATURE ---
    @action(detail=False, methods=['post'], url_path='bulk-upsert')
    def bulk_upsert(self, request):
        """
        "Flawless" bulk API for teachers to submit attendance
        for an entire class on a single day.
        """
        # 1. Get data from the JSON body
        payload = request.data
        schoolyear_id = payload.get('schoolyearid')
        class_id = payload.get('classesid')
        section_id = payload.get('sectionid')
        date_str = payload.get('date')
        records = payload.get('records', [])

        # --- 2. Get data from the token ---
        user_id = get_token_claim(request, 'user_id', 0) # <-- GET USER ID
        user_type_str = get_token_claim(request, 'user_type', 'teacher')

        # 3. Validation
        if not all([schoolyear_id, class_id, section_id, date_str, records]):
            return Response({'error': 'Missing required fields: schoolyearid, classesid, sectionid, date, or records.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            # 4. Get the day and month
            day_num = int(date_str.split('-')[2])
            day_col = f'a{day_num}'
            month_year = date_str[0:7]
        except Exception as e:
            return Response({'error': f"Invalid date format: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        errors = []

        # 6. --- Start "Flawless" Transaction ---
        try:
            with transaction.atomic():
                for rec in records:
                    student_id = rec.get('studentid')
                    attendance_status = rec.get('status')
                    
                    if not all([student_id, attendance_status]):
                        errors.append(f"Skipped record: missing studentid or status.")
                        continue

                    # 7. This is the "Upsert" logic with ALL correct field names
                    obj, created = Attendance.objects.get_or_create(
                        schoolyearid=schoolyear_id,
                        studentid=student_id,
                        monthyear=month_year,
                        classesid=class_id,
                        defaults={
                            'sectionid': section_id,
                            
                            # --- THESE ARE THE "FLAWLESS" FIXES ---
                            # Both fields are now provided, matching your model
                            'userid': user_id,           # The integer ID
                            'usertype': user_type_str,  # The string name
                        }
                    )
                    
                    # 8. Set the value for the correct day column
                    setattr(obj, day_col, attendance_status)
                    obj.save()

        except Exception as e:
            return Response({'error': f"Transaction failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 9. Success!
        if errors:
            return Response({'status': 'Partial success', 'errors': errors}, status=status.HTTP_207_MULTI_STATUS)
        
        return Response({'status': 'Attendance successfully saved'}, status=status.HTTP_200_OK)


class SubAttendanceViewSet(viewsets.ModelViewSet):
    """
    API for Subject-wise Attendance.
    - Admins/Teachers can write.
    - Students/Parents can read.
    - Provides a 'bulk-upsert' action for teachers.
    """
    queryset = SubAttendance.objects.all()
    serializer_class = SubAttendanceSerializer
    permission_classes = [IsAdminOrTeacherForAttendance] # We can re-use the same permission

    def get_queryset(self):
        # This is "flawless" hardened logic, copied from Studentattendance
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)

        if not user_id:
            return SubAttendance.objects.none()

        if user_type == 'systemadmin':
            return SubAttendance.objects.all()

        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return SubAttendance.objects.filter(classesid__in=class_ids)

        if user_type == 'student':
            return SubAttendance.objects.filter(studentid=user_id)

        if user_type == 'parent':
            student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
            return SubAttendance.objects.filter(studentid__in=student_ids)

        return SubAttendance.objects.none()

    # --- "FLAWLESS" BULK FEATURE FOR SUBJECTS ---
    @action(detail=False, methods=['post'], url_path='bulk-upsert')
    def bulk_upsert(self, request):
        """
        "Flawless" bulk API for teachers to submit SUBJECT attendance
        for an entire class on a single day.
        """
        # 1. Get data from the JSON body
        payload = request.data
        schoolyear_id = payload.get('schoolyearid')
        class_id = payload.get('classesid')
        section_id = payload.get('sectionid')
        subject_id = payload.get('subjectid')  # <-- THE NEW REQUIRED FIELD
        date_str = payload.get('date')
        records = payload.get('records', [])

        # 2. Get data from the token (for the 'defaults')
        user_id = get_token_claim(request, 'user_id', 0)
        user_type_str = get_token_claim(request, 'user_type', 'teacher')

        # 3. Validation
        if not all([schoolyear_id, class_id, section_id, subject_id, date_str, records]):
            return Response({'error': 'Missing required fields: schoolyearid, classesid, sectionid, subjectid, date, or records.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            # 4. Get the day and month
            day_num = int(date_str.split('-')[2])
            day_col = f'a{day_num}'
            month_year = date_str[0:7]
        except Exception as e:
            return Response({'error': f"Invalid date format: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        errors = []

        # 5. --- Start "Flawless" Transaction ---
        try:
            with transaction.atomic():
                for rec in records:
                    student_id = rec.get('studentid')
                    attendance_status = rec.get('status')

                    if not all([student_id, attendance_status]):
                        errors.append(f"Skipped record: missing studentid or status.")
                        continue

                    # 6. This is the "Upsert" logic, now including 'subjectid'
                    obj, created = SubAttendance.objects.get_or_create(
                        schoolyearid=schoolyear_id,
                        studentid=student_id,
                        monthyear=month_year,
                        classesid=class_id,
                        subjectid=subject_id,  # <-- THE NEW KEY
                        defaults={
                            'sectionid': section_id,
                            'userid': user_id,
                            'usertype': user_type_str,
                        }
                    )

                    # 7. Set the value for the correct day column
                    setattr(obj, day_col, attendance_status)
                    obj.save()

        except Exception as e:
            return Response({'error': f"Transaction failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 8. Success!
        if errors:
            return Response({'status': 'Partial success', 'errors': errors}, status=status.HTTP_207_MULTI_STATUS)

        return Response({'status': 'Subject attendance successfully saved'}, status=status.HTTP_200_OK)




class TeacherattendanceViewSet(viewsets.ModelViewSet):
    queryset = Tattendance.objects.all()
    serializer_class = TeacherattendanceSerializer
    permission_classes = [IsAdminOrTeacherSelfCreateRead]

    def get_queryset(self):
        # ... (this get_queryset method is already "flawless") ...
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)
        if user_type == 'systemadmin':
            return Tattendance.objects.all()
        if user_type == 'teacher':
            return Tattendance.objects.filter(teacherid=user_id)
        return Tattendance.objects.none()

    # --- "FLAWLESS" FIX FOR SELF-ATTENDANCE ---
    def create(self, request, *args, **kwargs):
        """
        "Flawless" security hijack for a Teacher POST.
        This forces the attendance to be for the logged-in teacher and today.
        This bypasses the serializer validation.
        """
        user_id = get_token_claim(request, 'user_id', 0)
        user_type = get_token_claim(request, 'user_type')

        if user_type != 'teacher':
            raise exceptions.PermissionDenied("Only teachers can mark self-attendance.")

        today = timezone.now().date()
        day_num = today.day
        day_col = f'a{day_num}'
        month_year = today.strftime("%Y-%m")
        # We assume schoolyearid=1 for self-attendance.
        # This can be changed to pull from request.data if needed.
        schoolyear_id = request.data.get('schoolyearid', 1) 

        # "Flawless" Upsert logic
        try:
            obj, created = Tattendance.objects.get_or_create(
                schoolyearid=schoolyear_id,
                teacherid=user_id,
                monthyear=month_year,
                defaults={'usertypeid': 2} # 2 = Teacher
            )
            
            attendance_status = request.data.get('status', 'P')
            setattr(obj, day_col, attendance_status)
            obj.save()
            
            # Return a "flawless" 200 OK response
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f"Transaction failed: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # --- "FLAWLESS" BULK FEATURE FOR ADMINS ---
    @action(detail=False, methods=['post'], url_path='bulk-upsert')
    def bulk_upsert(self, request):
        # ... (this bulk_upsert method is already "flawless") ...
        # (No changes needed here)
        payload = request.data
        schoolyear_id = payload.get('schoolyearid')
        date_str = payload.get('date')
        records = payload.get('records', [])
        if not all([schoolyear_id, date_str, records]):
            return Response({'error': 'Missing required fields: schoolyearid, date, or records.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            day_num = int(date_str.split('-')[2])
            day_col = f'a{day_num}'
            month_year = date_str[0:7]
        except Exception as e:
            return Response({'error': f"Invalid date format: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        errors = []
        try:
            with transaction.atomic():
                for rec in records:
                    teacher_id = rec.get('teacherid')
                    attendance_status = rec.get('status')
                    if not all([teacher_id, attendance_status]):
                        errors.append(f"Skipped record: missing teacherid or status.")
                        continue
                    obj, created = Tattendance.objects.get_or_create(
                        schoolyearid=schoolyear_id,
                        teacherid=teacher_id,
                        monthyear=month_year,
                        defaults={'usertypeid': 1}
                    )
                    setattr(obj, day_col, attendance_status)
                    obj.save()
        except Exception as e:
            return Response({'error': f"Transaction failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if errors:
            return Response({'status': 'Partial success', 'errors': errors}, status=status.HTTP_207_MULTI_STATUS)
        return Response({'status': 'Teacher attendance successfully saved'}, status=status.HTTP_200_OK)

class UserattendanceViewSet(viewsets.ModelViewSet):
    queryset = Uattendance.objects.all()
    serializer_class = UserattendanceSerializer
    permission_classes = [IsAdminOrStaffSelfCreateRead]

    def get_queryset(self):
        # ... (this get_queryset method is already "flawless") ...
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)
        if user_type == 'systemadmin':
            return Uattendance.objects.all()
        if user_type == 'staff':
            return Uattendance.objects.filter(userid=user_id)
        return Uattendance.objects.none()

    # --- "FLAWLESS" FIX FOR SELF-ATTENDANCE ---
    def create(self, request, *args, **kwargs):
        """
        "Flawless" security hijack for a Staff POST.
        This forces the attendance to be for the logged-in staff member and today.
        """
        user_id = get_token_claim(request, 'user_id', 0)
        user_type = get_token_claim(request, 'user_type')

        if user_type != 'staff':
            raise exceptions.PermissionDenied("Only staff can mark self-attendance.")

        today = timezone.now().date()
        day_num = today.day
        day_col = f'a{day_num}'
        month_year = today.strftime("%Y-%m")
        schoolyear_id = request.data.get('schoolyearid', 1) # Assume 1

        # "Flawless" Upsert logic
        try:
            obj, created = Uattendance.objects.get_or_create(
                schoolyearid=schoolyear_id,
                userid=user_id,
                monthyear=month_year,
                defaults={'usertypeid': 5} # 5 = Staff
            )
            
            attendance_status = request.data.get('status', 'P')
            setattr(obj, day_col, attendance_status)
            obj.save()

            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f"Transaction failed: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # --- "FLAWLESS" BULK FEATURE FOR ADMINS ---
    @action(detail=False, methods=['post'], url_path='bulk-upsert')
    def bulk_upsert(self, request):
        # ... (this bulk_upsert method is already "flawless") ...
        # (No changes needed here)
        payload = request.data
        schoolyear_id = payload.get('schoolyearid')
        date_str = payload.get('date')
        records = payload.get('records', [])
        if not all([schoolyear_id, date_str, records]):
            return Response({'error': 'Missing required fields: schoolyearid, date, or records.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            day_num = int(date_str.split('-')[2])
            day_col = f'a{day_num}'
            month_year = date_str[0:7]
        except Exception as e:
            return Response({'error': f"Invalid date format: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        errors = []
        try:
            with transaction.atomic():
                for rec in records:
                    user_id = rec.get('userid')
                    attendance_status = rec.get('status')
                    if not all([user_id, attendance_status]):
                        errors.append(f"Skipped record: missing userid or status.")
                        continue
                    obj, created = Uattendance.objects.get_or_create(
                        schoolyearid=schoolyear_id,
                        userid=user_id,
                        monthyear=month_year,
                        defaults={'usertypeid': 1}
                    )
                    setattr(obj, day_col, attendance_status)
                    obj.save()
        except Exception as e:
            return Response({'error': f"Transaction failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if errors:
            return Response({'status': 'Partial success', 'errors': errors}, status=status.HTTP_207_MULTI_STATUS)
        return Response({'status': 'User attendance successfully saved'}, status=status.HTTP_200_OK)

class ExamattendanceViewSet(viewsets.ModelViewSet):
    queryset = Eattendance.objects.all().order_by('-eattendanceid')
    serializer_class = ExamattendanceSerializer
    permission_classes = [IsAdminOrTeacherForAttendance]
    
    def get_queryset(self):
        # ... (this 'get_queryset' method is already "flawless") ...
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)
        if not user_id:
            return Eattendance.objects.none()
        if user_type == 'systemadmin':
            return Eattendance.objects.all()
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Eattendance.objects.filter(classesid__in=class_ids)
        if user_type == 'student':
            return Eattendance.objects.filter(studentid=user_id)
        if user_type == 'parent':
            student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
            return Eattendance.objects.filter(studentid__in=student_ids)
        return Eattendance.objects.none()

    # --- "FLAWLESS" BULK FEATURE (from screenshot image_17d35e.png) ---
    @action(detail=False, methods=['post'], url_path='bulk-upsert')
    def bulk_upsert(self, request):
        """
        "Flawless" bulk API for Admins/Teachers to submit Exam Attendance
        for an entire class.
        This model is NOT a crosstab, so it's a simple update_or_create.
        """
        # 1. Get data from the JSON body
        payload = request.data
        schoolyear_id = payload.get('schoolyearid')
        exam_id = payload.get('examid')
        class_id = payload.get('classesid')
        section_id = payload.get('sectionid')
        subject_id = payload.get('subjectid')
        date = payload.get('date')
        records = payload.get('records', []) # List of student statuses

        # 2. Validation
        if not all([schoolyear_id, exam_id, class_id, section_id, subject_id, date, records]):
            return Response({'error': 'Missing required fields: schoolyearid, examid, classesid, sectionid, subjectid, date, or records.'},
                            status=status.HTTP_400_BAD_REQUEST)

        errors = []

        # 3. --- Start "Flawless" Transaction ---
        try:
            with transaction.atomic():
                for rec in records:
                    student_id = rec.get('studentid')
                    attendance_status = rec.get('status')
                    
                    if not all([student_id, attendance_status]):
                        errors.append(f"Skipped record: missing studentid or status.")
                        continue

                    # 4. "Flawless" Upsert logic
                    # This finds a row or creates it
                    obj, created = Eattendance.objects.update_or_create(
                        schoolyearid=schoolyear_id,
                        examid=exam_id,
                        classesid=class_id,
                        subjectid=subject_id,
                        date=date,
                        studentid=student_id,
                        defaults={
                            'sectionid': section_id,
                            'eattendance': attendance_status, # This is the status field
                            'year': date.split('-')[0] # Get the year from the date
                        }
                    )

        except Exception as e:
            return Response({'error': f"Transaction failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 5. Success!
        if errors:
            return Response({'status': 'Partial success', 'errors': errors}, status=status.HTTP_207_MULTI_STATUS)
        
        return Response({'status': 'Exam attendance successfully saved'}, status=status.HTTP_200_OK)


# --- ACADEMIC MODULE VIEWSETS ---

class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        # --- HARDENED ---
        user = self.request.user 
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)

        if user_type == 'systemadmin':
            return Routine.objects.all()

        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Routine.objects.filter(classesid__in=class_ids)

        if user_type == 'student' and hasattr(user, 'classesid_id'):
            return Routine.objects.filter(classesid=user.classesid_id)
        
        if user_type == 'parent':
            try:
                student = Student.objects.filter(parentid=user_id).first()
                if student:
                    return Routine.objects.filter(classesid=student.classesid_id)
            except ObjectDoesNotExist:
                return Routine.objects.none()

        return Routine.objects.none()

class SyllabusViewSet(viewsets.ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    permission_classes = [IsAdminOrTeacherWriteOwner]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        # --- HARDENED ---
        user = self.request.user
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)

        if user_type == 'systemadmin':
            return Syllabus.objects.all()
        
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Syllabus.objects.filter(classesid__in=class_ids)

        if user_type == 'student' and hasattr(user, 'classesid_id'):
            return Syllabus.objects.filter(classesid=user.classesid_id)
        
        if user_type == 'parent':
            try:
                student = Student.objects.filter(parentid=user_id).first()
                if student:
                    return Syllabus.objects.filter(classesid=student.classesid_id)
            except ObjectDoesNotExist:
                return Syllabus.objects.none()

        return Syllabus.objects.none()

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAdminOrTeacherWriteOwner]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        # --- HARDENED ---
        user = self.request.user
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)

        if user_type == 'systemadmin':
            return Assignment.objects.all()
        
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            class_id_strings = [str(cid) for cid in class_ids]
            return Assignment.objects.filter(classesid__in=class_id_strings)

        if user_type == 'student' and hasattr(user, 'classesid_id'):
            return Assignment.objects.filter(classesid=str(user.classesid_id))
        
        if user_type == 'parent':
            try:
                student = Student.objects.filter(parentid=user_id).first()
                if student:
                    return Assignment.objects.filter(classesid=str(student.classesid_id))
            except ObjectDoesNotExist:
                return Assignment.objects.none()

        return Assignment.objects.none()
        
class AssignmentanswerViewSet(viewsets.ModelViewSet):
    queryset = Assignmentanswer.objects.all()
    serializer_class = AssignmentanswerSerializer
    permission_classes = [IsStudentOwnerForAnswer]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        # --- HARDENED ---
        user = self.request.user
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)

        if user_type == 'systemadmin':
            return Assignmentanswer.objects.all()
        
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            class_id_strings = [str(cid) for cid in class_ids]
            assignment_ids = Assignment.objects.filter(classesid__in=class_id_strings).values_list('assignmentid', flat=True)
            return Assignmentanswer.objects.filter(assignmentid__in=assignment_ids)

        if user_type == 'student':
            return Assignmentanswer.objects.filter(uploaderid=user_id)
        
        if user_type == 'parent':
            student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
            return Assignmentanswer.objects.filter(uploaderid__in=student_ids)

        return Assignmentanswer.objects.none()


# --- HOLIDAY VIEWSET ---

class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all().order_by('-fdate')
    serializer_class = HolidaySerializer
    permission_classes = [IsAdminOrReadOnly] 

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
  
class UsertypeViewSet(viewsets.ModelViewSet):
    """
    SAFE & NEW: Read-only ViewSet for the frontend dropdown.
    NOW "UNLOCKED" FOR ADMIN TO CREATE/EDIT.
    """
    queryset = Usertype.objects.all().order_by('usertypeid')
    serializer_class = UsertypeSerializer
    permission_classes = [IsAdminUser] # Only Admin can see/create roles

    # --- ADD THIS METHOD ---
    def get_serializer_context(self):
        """
        Passes the 'request' object to the AuditBaseSerializer
        so it can find the logged-in Admin's ID.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
      
# --- TEACHER ASSIGNMENT VIEWSET ---

class SubjectteacherViewSet(viewsets.ModelViewSet):
    queryset = Subjectteacher.objects.all()
    serializer_class = SubjectteacherSerializer
    permission_classes = [IsAdminUser] 
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    
    
#-----------Message-----
class ConversationViewSet(viewsets.ViewSet):
    """
    SAFE & NEW: Handles the Inbox (list) and Compose (create)
    """
    permission_classes = [permissions.IsAuthenticated] # From rest_framework

    def list(self, request):
        # --- INBOX ---
        user_id = get_token_claim(request, 'user_id', 0)
        user_type = get_token_claim(request, 'user_type')
        
        usertypeid_map = {'systemadmin': 1, 'teacher': 2, 'student': 3, 'parent': 4, 'staff': 5}
        user_type_id = usertypeid_map.get(user_type)

        # 1. Find all conversation IDs this user is part of
        user_convo_ids = ConversationUser.objects.filter(
            user_id=user_id,
            usertypeid=user_type_id
        ).values_list('conversation_id', flat=True)

        # 2. Get the *first* message (the subject) for those conversations
        queryset = ConversationMsg.objects.filter(
            conversation_id__in=user_convo_ids,
            start=1  # 'start=1' means it's the first message
        ).order_by('-modify_date')

        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # --- COMPOSE NEW MESSAGE ---
        data = request.data
        usertypeid_map = {'systemadmin': 1, 'teacher': 2, 'student': 3, 'parent': 4, 'staff': 5}

        # 1. Sender (from token)
        sender_id = get_token_claim(request, 'user_id', 0)
        sender_type_str = get_token_claim(request, 'user_type')
        sender_type_id = usertypeid_map.get(sender_type_str)

        # 2. Receiver (from body)
        receiver_type_str = data.get('receiver_type') # e.g., 'teacher'
        receiver_id = data.get('receiver_id')       # e.g., 2
        receiver_type_id = usertypeid_map.get(receiver_type_str)

        subject = data.get('subject')
        message = data.get('msg')

        # 3. Validation
        if not all([receiver_id, receiver_type_str, subject, message, receiver_type_id]):
            return Response({'error': 'Missing or invalid fields: receiver_id, receiver_type, subject, or msg.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # 4. Create 3 database entries in one "safe" transaction
        try:
            with transaction.atomic():
                # A. Get a new ID
                max_id_result = ConversationMsg.objects.aggregate(Max('conversation_id'))
                max_id = max_id_result['conversation_id__max'] or 0
                new_convo_id = max_id + 1
                now = timezone.now()

                # B. Create the Message
                msg_obj = ConversationMsg.objects.create(
                    conversation_id=new_convo_id,
                    user_id=sender_id,
                    usertypeid=sender_type_id,
                    subject=subject,
                    msg=message,
                    create_date=now,
                    modify_date=now,
                    start=1 # This is the "start" message
                )
                # C. Link the Sender
                ConversationUser.objects.create(
                    conversation_id=new_convo_id,
                    user_id=sender_id,
                    usertypeid=sender_type_id,
                    is_sender=1
                )
                # D. Link the Receiver
                ConversationUser.objects.create(
                    conversation_id=new_convo_id,
                    user_id=receiver_id,
                    usertypeid=receiver_type_id,
                    is_sender=0
                )
                
                serializer = ConversationMsgSerializer(msg_obj)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f"Message failed to send: {e}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConversationMsgViewSet(viewsets.ModelViewSet):
    """
    SAFE & NEW: Handles viewing a conversation (list) and replying (create)
    """
    serializer_class = ConversationMsgSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]

    def get_queryset(self):
        # --- VIEW A SINGLE CONVERSATION'S REPLIES ---
        convo_id = self.kwargs.get('convo_id')
        if not convo_id:
             return ConversationMsg.objects.none()
        # Return all messages, oldest first
        return ConversationMsg.objects.filter(
            conversation_id=convo_id
        ).order_by('create_date')
    
    def get_serializer_context(self):
        # Pass the request to the serializer so it knows *who* is replying
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        # --- SEND A REPLY ---
        # Get the convo_id from the URL and save it with the reply
        convo_id = self.kwargs.get('convo_id')
        serializer.save(conversation_id=convo_id)