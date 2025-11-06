# In backend/views.py
from django.http import JsonResponse
from .models import * 
from django.contrib.auth.hashers import check_password

# DRF Imports
from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# --- 1. IMPORT ALL PERMISSION CLASSES ---
from .permissions import (
    IsAdminOrReadOnly, IsAdminOrStudentOwner, 
    IsAdminOrTeacherOwner, IsAdminOrParentOwner, IsAdminUser,
    IsAdminOrTeacherForMarks,IsAdminOrTeacherForAttendance,
    IsAdminOrTeacherSelfCreateRead, IsAdminOrStaffSelfCreateRead,
    IsAdminOrTeacherWriteOwner,IsStudentOwnerForAnswer
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
    AssignmentanswerSerializer
)

# --- CUSTOM LOGIN VIEW (No Change) ---
class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = None
        # --- All your try/except blocks are 100% correct ---
        try:
            u = Teacher.objects.get(username=username)
            if check_password(password, u.password): user = u
        except Teacher.DoesNotExist: pass
        if not user:
            try:
                u = Student.objects.get(username=username)
                if check_password(password, u.password): user = u
            except Student.DoesNotExist: pass
        if not user:
            try:
                u = Parents.objects.get(username=username)
                if check_password(password, u.password): user = u
            except Parents.DoesNotExist: pass
        if not user:
            try:
                u = Systemadmin.objects.get(username=username)
                if check_password(password, u.password): user = u
            except Systemadmin.DoesNotExist: pass
        if not user:
            try:
                u = User.objects.get(username=username)
                if check_password(password, u.password): user = u
            except User.DoesNotExist: pass

        if user:
            # --- THIS IS THE FIX ---
            tokens = get_tokens_for_user(user) # Get the tokens
            
            # Now, get the user_type string from the user object
            user_type_str = None
            if isinstance(user, Teacher): user_type_str = 'teacher'
            elif isinstance(user, Student): user_type_str = 'student'
            elif isinstance(user, Parents): user_type_str = 'parent'
            elif isinstance(user, Systemadmin): user_type_str = 'systemadmin'
            elif isinstance(user, User): user_type_str = 'staff'

            # Create a new, "smart" response for the frontend
            response_data = {
                'refresh': tokens['refresh'],
                'access': tokens['access'],
                'user_type': user_type_str,
                'email':user.email,
                'userid': user.pk,
                'name': user.name,
                'username': user.username
            }
            return Response(response_data, status=status.HTTP_200_OK)
            # --- END OF FIX ---
            
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# --- API ViewSets ---

class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminOrTeacherOwner]
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']
    
    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')

        # Admin can see all teachers
        if user_type == 'systemadmin':
            return Teacher.objects.all()

        # A Teacher can see their *own* profile
        if user_type == 'teacher':
            return Teacher.objects.filter(teacherid=user_id) 
        raise exceptions.PermissionDenied(detail="You do not have permission to view this list.")
    
    def get_serializer_context(self):
        """
        Passes the 'request' object to the serializer.
        This is required so our AuditBaseSerializer
        can access the logged-in user's ID.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context 

class ParentsViewSet(viewsets.ModelViewSet):
    serializer_class = ParentsSerializer
    permission_classes = [IsAdminOrParentOwner]
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']
    
    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')
        if user_type == 'systemadmin' :
            return Parents.objects.all()
        if user_type == 'parent':
            return Parents.objects.filter(parentsid=user_id)
        return Parents.objects.none()
    
    def get_serializer_context(self):
        """
        Passes the 'request' object to the serializer.
        This is required so our AuditBaseSerializer
        can access the logged-in user's ID.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

# --- 2. APPLY THE FIX HERE ---
class SystemadminViewSet(viewsets.ModelViewSet):
    queryset = Systemadmin.objects.all()
    serializer_class = SystemadminSerializer
    permission_classes = [IsAdminUser] # <-- ADDED
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        """
        Passes the 'request' object to the serializer.
        This is required so our AuditBaseSerializer
        can access the logged-in user's ID.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

# --- 3. AND APPLY THE FIX HERE ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # <-- ADDED
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        """
        Passes the 'request' object to the serializer.
        This is required so our AuditBaseSerializer
        can access the logged-in user's ID.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrStudentOwner]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        """
        Passes the 'request' object to the serializer.
        This is required so our AuditBaseSerializer
        can access the logged-in user's ID.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')
        if user_type == 'systemadmin' :
            return Student.objects.all()
        if user_type == 'student':
            return Student.objects.filter(studentid=user_id) 
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Student.objects.filter(classesid__in=class_ids)
        return Student.objects.none()


class ClassesViewSet(viewsets.ModelViewSet):
    serializer_class = ClassesSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        """
        Passes the 'request' object to the serializer.
        This is required so our AuditBaseSerializer
        can access the logged-in user's ID.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')
        if user_type == 'systemadmin' :
            return Classes.objects.all()
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Classes.objects.filter(classesid__in=class_ids)
        return Classes.objects.none()


class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        """
        Passes the 'request' object to the serializer.
        This is required so our AuditBaseSerializer
        can access the logged-in user's ID.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')
        if user_type == 'systemadmin':
            return Section.objects.all()
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Section.objects.filter(classesid__in=class_ids)
        return Section.objects.none()


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    
    def get_serializer_context(self):
        """
        Passes the 'request' object to the serializer.
        This is required so our AuditBaseSerializer
        can access the logged-in user's ID.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')
        if user_type == 'systemadmin' :
            return Subject.objects.all()
        if user_type == 'teacher':
            subject_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('subjectid', flat=True).distinct()
            return Subject.objects.filter(subjectid__in=subject_ids)
        return Subject.objects.none()
    

class RoutineViewSet(viewsets.ModelViewSet):
    """
    API for Class Routines.
    - Admins can create/edit.
    - Teachers, Students, Parents can read.
    """
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [IsAdminOrReadOnly] # <-- Use Admin-Only Write

    def get_queryset(self):
        """Implement row-level security."""
        user = self.request.user # <-- This is the Student object
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')

        if user_type == 'systemadmin':
            return Routine.objects.all()

        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Routine.objects.filter(classesid__in=class_ids)

        if user_type == 'student':
            # --- THIS IS THE FIX ---
            return Routine.objects.filter(classesid=user.classesid_id) # Was user.classesid
        
        if user_type == 'parent':
            student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
            student = Student.objects.filter(pk__in=student_ids).first()
            if student:
                # --- THIS IS THE FIX ---
                return Routine.objects.filter(classesid=student.classesid_id) # Was student.classesid

        return Routine.objects.none()

class SyllabusViewSet(viewsets.ModelViewSet):
    """
    API for Syllabus.
    - Admins can do anything.
    - Teachers can create, read, and update/delete their own.
    - Students/Parents can read.
    """
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    permission_classes = [IsAdminOrTeacherWriteOwner] # <-- Use new Teacher-Write permission

    def get_serializer_context(self):
        """Passes request to the serializer to get the creator's ID."""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        """Implement row-level security."""
        user = self.request.user # <-- This is the Student object
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')

        if user_type == 'systemadmin':
            return Syllabus.objects.all()
        
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Syllabus.objects.filter(classesid__in=class_ids)

        if user_type == 'student':
            # --- THIS IS THE FIX ---
            return Syllabus.objects.filter(classesid=user.classesid_id) # Was user.classesid
        
        if user_type == 'parent':
            student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
            student = Student.objects.filter(pk__in=student_ids).first()
            if student:
                # --- THIS IS THE FIX ---
                return Syllabus.objects.filter(classesid=student.classesid_id) # Was student.classesid

        return Syllabus.objects.none()

class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API for Assignments.
    - Admins can do anything.
    - Teachers can create, read, and update/delete their own.
    - Students/Parents can read.
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAdminOrTeacherWriteOwner] # <-- Use new Teacher-Write permission

    def get_serializer_context(self):
        """Passes request to the serializer to get the creator's ID."""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        """Implement row-level security."""
        user = self.request.user # <-- This is the Student object
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')

        if user_type == 'systemadmin':
            return Assignment.objects.all()
        
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            # Convert class IDs to strings for filtering the TextField
            class_id_strings = [str(cid) for cid in class_ids]
            return Assignment.objects.filter(classesid__in=class_id_strings)

        if user_type == 'student':
            # --- THIS IS THE FIX ---
            # Convert the student's class ID to a string to filter the TextField
            return Assignment.objects.filter(classesid=str(user.classesid_id)) # Was user.classesid
        
        if user_type == 'parent':
            student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
            student = Student.objects.filter(pk__in=student_ids).first()
            if student:
                # --- THIS IS THE FIX ---
                return Assignment.objects.filter(classesid=str(student.classesid_id)) # Was student.classesid

        return Assignment.objects.none()



class AssignmentanswerViewSet(viewsets.ModelViewSet):
    """
    API for Students to submit Assignment Answers.
    - Students can create/read/update/delete their own.
    - Teachers can read all.
    - Parents can read their child's.
    """
    queryset = Assignmentanswer.objects.all()
    serializer_class = AssignmentanswerSerializer
    permission_classes = [IsStudentOwnerForAnswer]

    def get_serializer_context(self):
        """Passes request to the serializer to get the creator's ID."""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        """Implement row-level security."""
        user = self.request.user
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')

        if user_type == 'systemadmin':
            return Assignmentanswer.objects.all()
        
        # Teachers see answers for assignments in their classes
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            class_id_strings = [str(cid) for cid in class_ids]
            assignment_ids = Assignment.objects.filter(classesid__in=class_id_strings).values_list('assignmentid', flat=True)
            return Assignmentanswer.objects.filter(assignmentid__in=assignment_ids)

        # Students see only their own answers
        if user_type == 'student':
            return Assignmentanswer.objects.filter(uploaderid=user_id)
        
        # Parents see their child's answers
        if user_type == 'parent':
            student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
            return Assignmentanswer.objects.filter(uploaderid__in=student_ids)

        return Assignmentanswer.objects.none()


# --- 4. MARKING SYSTEM "SETUP" VIEWSETS ---
# These are locked down to Admins only using our IsAdminUser permission.

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAdminUser] # <-- SECURED
    ordering_fields = ['create_date']
    ordering = ['-create_date']

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminUser] # <-- SECURED
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    

# --- 5. THE MAIN MARK VIEWSET ---

class MarkViewSet(viewsets.ModelViewSet):
    """
    This ViewSet handles Marks and applies role-based row-level security.
    - Admins see all.
    - Teachers see marks for students in their classes.
    - Students see only their own marks.
    - Parents see only their child's marks.
    """
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    permission_classes = [IsAdminOrTeacherForMarks] # <-- USE OUR NEW PERMISSION
    ordering_fields = ['create_date']
    ordering = ['-create_date']

    def get_serializer_context(self):
        """
        Passes the 'request' object to the serializer.
        This is required so our serializer's create() method
        can access the logged-in user's ID.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def get_queryset(self):
        """
        This implements the row-level security.
        """
        user = self.request.user
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')

        if not user_id:
            return Mark.objects.none()

        # 1. Admins see everything (FIX: REMOVED .select_related())
        if user_type == 'systemadmin':
            return Mark.objects.all()

        # 2. Teachers see marks for students in their classes (FIX: REMOVED .select_related())
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Mark.objects.filter(classesid__in=class_ids)

        # 3. Students see only their own marks (FIX: REMOVED .select_related())
        if user_type == 'student':
            return Mark.objects.filter(studentid=user_id)

        # 4. Parents see their child's marks (FIX: REMOVED .select_related())
        if user_type == 'parent':
            student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
            return Mark.objects.filter(studentid__in=student_ids)

        # 5. If no role matches, return nothing
        return Mark.objects.none()


class MarkrelationViewSet(viewsets.ModelViewSet):
    """
    This API saves the *actual* score (e.g., "85") and
    links it to a Mark "header" record.
    """
    queryset = Markrelation.objects.all()
    serializer_class = MarkrelationSerializer
    # Teachers and Admins can add marks
    permission_classes = [IsAdminOrTeacherForMarks]
    
class MarkpercentageViewSet(viewsets.ModelViewSet):
    """
    Admin-only API for creating Mark Distribution types (e.g., "Theory")
    from the Markpercentage model.
    """
    queryset = Markpercentage.objects.all()
    serializer_class = MarkpercentageSerializer
    permission_classes = [IsAdminUser] # Admin-only

    def get_serializer_context(self):
        """ Passes the 'request' object to the serializer. """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context




class StudentattendanceViewSet(viewsets.ModelViewSet):
    """
    API for Student Attendance (the 'Attendance' model).
    - Teachers can create/update.
    - Students/Parents can read their own.
    - Admins can do anything.
    """
    queryset = Attendance.objects.all()
    serializer_class = StudentattendanceSerializer
    permission_classes = [IsAdminOrTeacherForAttendance] # <-- Use Teacher permission

    def get_serializer_context(self):
        """Passes request to the serializer to get the creator's ID."""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        """Implement row-level security."""
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')

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

        return Attendance.objects.none() # 'staff' sees nothing

class TeacherattendanceViewSet(viewsets.ModelViewSet):
    """
    API for Teacher Attendance (the 'Tattendance' model).
    - Admins can do anything.
    - Teachers can CREATE and READ their OWN records.
    """
    queryset = Tattendance.objects.all()
    serializer_class = TeacherattendanceSerializer
    permission_classes = [IsAdminOrTeacherSelfCreateRead] # <-- Use new "self-create" rule

    def get_queryset(self):
        """Implement row-level security."""
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')

        if user_type == 'systemadmin':
            return Tattendance.objects.all()

        if user_type == 'teacher':
            return Tattendance.objects.filter(teacherid=user_id)
        
        return Tattendance.objects.none()

class UserattendanceViewSet(viewsets.ModelViewSet):
    """
    API for Staff/User Attendance (the 'Uattendance' model).
    - Admins can do anything.
    - Staff can CREATE and READ their OWN records.
    """
    queryset = Uattendance.objects.all()
    serializer_class = UserattendanceSerializer
    permission_classes = [IsAdminOrStaffSelfCreateRead] # <-- Use new "self-create" rule

    def get_queryset(self):
        """Implement row-level security."""
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')

        if user_type == 'systemadmin':
            return Uattendance.objects.all()

        if user_type == 'staff':
            return Uattendance.objects.filter(userid=user_id)
        
        return Uattendance.objects.none()

class ExamattendanceViewSet(viewsets.ModelViewSet):
    """
    API for Exam Attendance (the 'Eattendance' model).
    """
    queryset = Eattendance.objects.all()
    serializer_class = ExamattendanceSerializer
    permission_classes = [IsAdminOrTeacherForAttendance] # <-- Use Teacher permission
    
    def get_queryset(self):
        """Implement row-level security."""
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')

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









   
# --- 6. TEACHER ASSIGNMENT VIEWSET ---

class SubjectteacherViewSet(viewsets.ModelViewSet):
    """
    This is the "glue" API.
    Admins use this to assign teachers to their classes and subjects.
    """
    queryset = Subjectteacher.objects.all()
    serializer_class = SubjectteacherSerializer
    permission_classes = [IsAdminUser] # <-- SECURED: Only Admins can assign teachers
    ordering_fields = ['create_date']
    ordering = ['-create_date']