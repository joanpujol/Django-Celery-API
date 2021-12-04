from django.core.validators import RegexValidator


phone_validation = RegexValidator(
        # TODO revise this regex
        regex=r'^\d{9}$',
        message='Phone number must be entered in the format: 05999999999'
    )

chat_validation = RegexValidator(
    regex=r"[a-zA-Z0-9{}$%_-\/~@#$%^&()!?]",
    message="Text contains invalid chartacter"
)
