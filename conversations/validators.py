from django.core.validators import RegexValidator


phone_regex = RegexValidator(
        # TODO revise this regex
        regex=r'^\d{9}$',
        message='Phone number must be entered in the format: 05999999999'
    )
