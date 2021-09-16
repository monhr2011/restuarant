from django.core.validators import MaxLengthValidator, MinLengthValidator

EmployeeNumberMinLengthValidator = MinLengthValidator(limit_value=4)
EmployeeNumberMaxLengthValidator = MaxLengthValidator(limit_value=4)
