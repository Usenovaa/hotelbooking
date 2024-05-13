from django.core.mail import send_mail

def send_activation_code(email, activation_code):
    message = f'''
    Вы успешно прошли регистрацию.
    Активируйте свой аккаунт отправив нам код активации: {activation_code}
    '''
    send_mail(
        'Активация аккаунта',
        message,
        'hotelo@gmail.com',
        [email]
    )
