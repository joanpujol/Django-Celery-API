from django.core.validators import RegexValidator


phone_validation = RegexValidator(
    regex=r'^\+?(?:[0-9]?){6,14}$',  # Optionally can include country prefix (+34)
    message='Phone number must be entered in the format: 05999999999'
)

chat_validation = RegexValidator(
    regex=r"[a-zA-Z0-9/{}\$%_-~@#%\^&\(\)!\?\\]",
    message="Text contains invalid character"
)
