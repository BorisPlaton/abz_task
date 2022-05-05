from django import forms

from employees.models import Employee


class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = (
            'first_name',
            'second_name',
            'patronymic',
            'position',
            'parent',
            'date_employment',
            'payment',
            'employee_photo',
        )

    def __init__(self, *args, **kwargs):
        super(EmployeeEditForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    'class': 'form-control form-control-sm ms-2',
                    'placeholder': field.label,
                }
            )

        self.fields['employee_photo'].widget.attrs.update({
            'class': 'form-control form-control-sm mt-2',
        })
