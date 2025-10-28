from django.db import models


class AccountEmployeeSalaries(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee_id = models.IntegerField(db_comment='employee_id=user_id')
    date = models.CharField(max_length=255, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_employee_salaries'


class AccountOtherCosts(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_other_costs'


class AccountStudentFees(models.Model):
    id = models.BigAutoField(primary_key=True)
    year_id = models.IntegerField(blank=True, null=True)
    class_id = models.IntegerField(blank=True, null=True)
    student_id = models.IntegerField(blank=True, null=True)
    fee_category_id = models.IntegerField(blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_student_fees'


class AssignStudents(models.Model):
    id = models.BigAutoField(primary_key=True)
    student_id = models.IntegerField(db_comment='user_id=student_id')
    roll = models.IntegerField(blank=True, null=True)
    class_id = models.IntegerField(blank=True, null=True)
    year_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    shift_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assign_students'


class AssignSubjects(models.Model):
    id = models.BigAutoField(primary_key=True)
    class_id = models.IntegerField()
    subject_id = models.IntegerField()
    full_mark = models.FloatField(blank=True, null=True)
    pass_mark = models.FloatField(blank=True, null=True)
    subjective_mark = models.FloatField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assign_subjects'


class Designations(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'designations'


class DiscountStudents(models.Model):
    id = models.BigAutoField(primary_key=True)
    assign_student_id = models.IntegerField()
    fee_category_id = models.IntegerField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discount_students'


class EmployeeAttendances(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee_id = models.IntegerField(db_comment='employee_id=user_id')
    date = models.DateField()
    attend_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_attendances'


class EmployeeLeaves(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee_id = models.IntegerField(db_comment='employee_id=user_id')
    leave_purpose_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_leaves'


class EmployeeSalaryLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee_id = models.IntegerField(db_comment='employee_id=user_id')
    previous_salary = models.FloatField(blank=True, null=True)
    present_salary = models.FloatField(blank=True, null=True)
    increment_salary = models.FloatField(blank=True, null=True)
    effected_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_salary_logs'


class Events(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1000)
    image = models.CharField(max_length=255)
    date = models.DateField()
    status = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'


class ExamTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam_types'


class FailedJobs(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'failed_jobs'


class FeeCategories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fee_categories'


class FeeCategoryAmounts(models.Model):
    id = models.BigAutoField(primary_key=True)
    class_id = models.IntegerField()
    fee_category_id = models.IntegerField()
    amount = models.FloatField()
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fee_category_amounts'


class Groups(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'


class HomePages(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveIntegerField()
    about = models.CharField(max_length=500, blank=True, null=True)
    welcome_text_title = models.CharField(max_length=255, blank=True, null=True)
    welcome_text = models.CharField(max_length=500, blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    welcome_image = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'home_pages'


class LeavePurposes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'leave_purposes'


class MarksGrades(models.Model):
    id = models.BigAutoField(primary_key=True)
    grade_name = models.CharField(max_length=255)
    grade_point = models.CharField(max_length=255)
    start_marks = models.CharField(max_length=255)
    end_marks = models.CharField(max_length=255)
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'marks_grades'


class Migrations(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Notices(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    notice_title = models.CharField(max_length=100)
    notice_file = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notices'


class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class Schools(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(db_comment='0=inactive,1=active')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schools'


class Shifts(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shifts'


class Sliders(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveIntegerField()
    slider_text = models.CharField(max_length=255, blank=True, null=True)
    slider_image = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sliders'


class StudentClasses(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_classes'


class StudentMarks(models.Model):
    id = models.BigAutoField(primary_key=True)
    student_id = models.IntegerField(db_comment='student_id=user_id')
    id_no = models.CharField(max_length=255, blank=True, null=True)
    shift_id = models.IntegerField(blank=True, null=True)
    year_id = models.IntegerField(blank=True, null=True)
    class_id = models.IntegerField(blank=True, null=True)
    assign_subject_id = models.IntegerField(blank=True, null=True)
    exam_type_id = models.IntegerField(blank=True, null=True)
    marks = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_marks'


class Subjects(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subjects'


class Teachers(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveIntegerField(db_comment='who create')
    name = models.CharField(max_length=255)
    designation = models.IntegerField()
    subject = models.IntegerField(blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255)
    status = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teachers'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    usertype = models.CharField(max_length=255, blank=True, null=True, db_comment='student,employee,admin')
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    fname = models.CharField(max_length=255, blank=True, null=True)
    mname = models.CharField(max_length=255, blank=True, null=True)
    religion = models.CharField(max_length=255, blank=True, null=True)
    id_no = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True, db_comment='admin=head of software,operator=computer operator,user=employee')
    join_date = models.DateField(blank=True, null=True)
    designation_id = models.IntegerField(blank=True, null=True)
    salary = models.FloatField(blank=True, null=True)
    status = models.IntegerField(db_comment='0=inactive,1=active')
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Years(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'years'