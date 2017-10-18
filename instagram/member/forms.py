from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login

User = get_user_model()


class LoginForm(forms.Form):
    """
    1. loginForm을 만들고 username, password를 받을 수 있도록 구성
    2. def clean()메서드에서 username, password 사용해서
        authenticate에 성공했는지 실패했는지 판단 실패시 raise forms.validationError
    3. loginForm에 login(request) 메서드를 추가
        이 메서드는 인수로 request 객체를 받으며 호출 시 django.contrib.auth.login()메서드를 실행

    4. 요청에서 username, password를 가져옴
        username, password를 사용한 인증 관련 검증
   """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    # 초기화 메서드를 실행해서 self.user를 정의
    def __init__(self, *args, **kwargs):
        # 원레 상속받은 form 클래스의 초기화가 무시되지 않도록
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        # 인증에 성공하면 self.user 변수에 객체 할당
        self.user = authenticate(
            username=username,
            password=password
        )

        if not self.user:
            raise forms.ValidationError(
                'Invalid Login credentials'
            )
        else:
            # 동적으로
            setattr(self, 'login', self._login)

    def _login(self, request):
        django_login(request, self.user)


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    # clean_<field_name>
    def clean_username(self):
        # 유저가 존재하면 forms.validationerror를 발생
        # 아니면 data를 리턴
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError(f'"{data}" is already exist')
        return data



