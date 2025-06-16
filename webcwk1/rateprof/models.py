from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Validator for year (Must be a 4-digit number)
def validate_year(value):
    if value < 1000 or value > 9999:
        raise ValidationError("Year must be a 4-digit number (e.g., 2018).")

# Validator for semester (Must be 1 or 2)
def validate_semester(value):
    if value not in [1, 2]:
        raise ValidationError("Semester must be either 1 or 2.")

# Validator for 3-character length
def validate_three_chars(value):
    if len(value) != 3:
        raise ValidationError("Value must be exactly 3 characters long.")

class Professor(models.Model):
    identifier = models.CharField(max_length=3, unique=True, validators=[validate_three_chars])
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return f"{self.identifier} - {self.name}"

class Module(models.Model):
    code = models.CharField(max_length=3, validators=[validate_three_chars])
    name = models.CharField(max_length=255)
    year = models.IntegerField(validators=[validate_year])
    semester = models.IntegerField(validators=[validate_semester])
    professors = models.ManyToManyField(Professor, related_name='modules')

    class Meta:
        unique_together = ('code', 'year', 'semester') 
    
    def __str__(self):
        return f"{self.code} ({self.year} S{self.semester})"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='ratings')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='ratings')
    year = models.IntegerField(validators=[validate_year])
    semester = models.IntegerField(validators=[validate_semester])
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ('user', 'professor', 'module', 'year', 'semester')

    def clean(self):
        if not Module.objects.filter(id=self.module.id, year=self.year, semester=self.semester, professors=self.professor).exists():
            raise ValidationError(f"Professor {self.professor.name} is not teaching {self.module.name} in {self.year} Semester {self.semester}.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
