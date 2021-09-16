from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models, transaction
from django.views.decorators.debug import sensitive_variables

from staff.validators import EmployeeNumberMinLengthValidator, EmployeeNumberMaxLengthValidator


# Assuming one staff user will be assigned to one role only
class Staff(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _("Admin")
        EMPLOYEE = 'EMPLOYEE', _("Employee")

    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE, null=False, blank=False)
    employee_number = models.CharField(verbose_name=_("Employee Number"), max_length=4, null=False, blank=False,
                                       validators=[
                                           EmployeeNumberMinLengthValidator,
                                           EmployeeNumberMaxLengthValidator,
                                       ],
                                       unique=True,
                                       )
    role = models.CharField(verbose_name=_("Role"), choices=Role.choices, max_length=10, null=False, blank=False)

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def is_admin(self):
        return self.role == Staff.Role.ADMIN

    @property
    def is_employee(self):
        return self.role == Staff.Role.EMPLOYEE

    @staticmethod
    @sensitive_variables('password')
    def create_staff_user(employee_number, name: str, role, password):
        user = User.objects.filter(staff__employee_number=employee_number).first()
        if user:
            raise ValidationError("User already exists")
        if role not in Staff.Role.values:
            raise ValidationError("Role must be in {}".format(Staff.Role.values))
        validate_password(password)
        name = name.split(" ", 1)
        user, *_ = User.objects.get_or_create(username=employee_number)
        user.first_name = name[0]
        if len(name) > 1:
            user.last_name = name[1]
        user.set_password(raw_password=password)
        user.save()
        staff_user = Staff(user=user, employee_number=employee_number, role=role)
        staff_user.save()
        return staff_user

    @staticmethod
    def change_role(staff_user, role):
        if role not in Staff.Role.values:
            raise ValueError("Role must be in {}".format(Staff.Role.values))
        if not isinstance(staff_user, Staff):
            raise ValueError("staff_user must be instance of StaffUser")
        staff_user.role = role
        staff_user.save()

    def __str__(self):
        try:
            return "{} - {}".format(self.employee_number, self.full_name)
        except:
            return super().__str__()

