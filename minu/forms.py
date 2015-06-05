from wtforms import validators, StringField
from wtforms.ext.csrf.session import SessionSecureForm
from wtforms.validators import ValidationError




#For CSRF security override with Pyramid session get_csrf_token
class BaseForm(SessionSecureForm):
    def generate_csrf_token(self, session):
        """Get the session's CSRF token."""
        return session.get_csrf_token()

    def validate_csrf_token(form, field):
        """Validate the CSRF token."""
        if field.data != field.current_token:
            raise ValidationError('Invalid CSRF token; the form probably expired.  Try again.')



class DepartmentForm(BaseForm):
    department_name = StringField(u'Department Name', [validators.Length(min=3, max=60),
                                         validators.InputRequired(message=(u'Input Department Name'))])
