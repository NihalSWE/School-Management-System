# In backend/views.py
from django.db import transaction
from django.http import JsonResponse
from .models import * 
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

# DRF Imports
from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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
    IsAdminOrTeacherWriteOwner, IsStudentOwnerForAnswer
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
    AssignmentanswerSerializer, HolidaySerializer
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
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrStudentOwner]
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

class TeacherattendanceViewSet(viewsets.ModelViewSet):
    queryset = Tattendance.objects.all()
    serializer_class = TeacherattendanceSerializer
    permission_classes = [IsAdminOrTeacherSelfCreateRead]

    def get_queryset(self):
        # --- HARDENED ---
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)

        if user_type == 'systemadmin':
            return Tattendance.objects.all()

        if user_type == 'teacher':
            return Tattendance.objects.filter(teacherid=user_id)
        
        return Tattendance.objects.none()

class UserattendanceViewSet(viewsets.ModelViewSet):
    queryset = Uattendance.objects.all()
    serializer_class = UserattendanceSerializer
    permission_classes = [IsAdminOrStaffSelfCreateRead]

    def get_queryset(self):
        # --- HARDENED ---
        user_type = get_token_claim(self.request, 'user_type')
        user_id = get_token_claim(self.request, 'user_id', 0)

        if user_type == 'systemadmin':
            return Uattendance.objects.all()

        if user_type == 'staff': # 'staff' is our internal name
            return Uattendance.objects.filter(userid=user_id)
        
        return Uattendance.objects.none()

class ExamattendanceViewSet(viewsets.ModelViewSet):
    queryset = Eattendance.objects.all()
    serializer_class = ExamattendanceSerializer
    permission_classes = [IsAdminOrTeacherForAttendance]
    
    def get_queryset(self):
        # --- HARDENED ---
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
        
# --- TEACHER ASSIGNMENT VIEWSET ---

class SubjectteacherViewSet(viewsets.ModelViewSet):
    queryset = Subjectteacher.objects.all()
    serializer_class = SubjectteacherSerializer
    permission_classes = [IsAdminUser] 
    ordering_fields = ['create_date']
    ordering = ['-create_date']