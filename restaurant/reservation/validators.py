from django.core.validators import MaxValueValidator, MinValueValidator

validate_max_number_of_seats = MaxValueValidator(12)
validate_min_number_of_seats = MinValueValidator(1)
