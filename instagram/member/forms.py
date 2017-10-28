from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.contrib.auth.forms import UserCreationForm

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
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
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


# class SignupForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control'
#             }
#         )
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control'
#             }
#         )
#     )
#     password2 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control'
#             }
#         )
#     )
#     age = forms.IntegerField(
#         widget=forms.NumberInput(
#             attrs={
#                 'class': 'form-control'
#             }
#         )
#     )
#
#     # clean_<field_name>
#     def clean_username(self):
#         # 유저가 존재하면 forms.validationerror를 발생
#         # 아니면 data를 리턴
#         data = self.cleaned_data['username']
#         if User.objects.filter(username=data).exists():
#             raise forms.ValidationError(f'"{data}" is already exist')
#         return data
#
#     def clean_password2(self):
#         password = self.cleaned_data['password']
#         password2 = self.cleaned_data['password2']
#         if password != password2:
#             raise forms.ValidationError('패스워드가 다릅니다')
#         return password2
#
#     def clean(self):
#         if self.is_valid():
#             setattr(self, 'signup', self._signup)
#         return self.cleaned_data
#
#     def _signup(self):
#         username = self.cleaned_data['username']
#         password = self.cleaned_data['password']
#         age = self.cleaned_data['age']
#         return User.objects.create_user(
#             username=username,
#             password=password,
#             age=age,
#         )


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 초기화 과정에서 attrs를 업데이트할 필드 이름 목록
        # 부트스트랩 적용을 위해서
        class_update_fields = ('password1', 'password2')
        for field in class_update_fields:
            # self.fields[field]이 인스턴스에 접근하게 해주는 것
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'img_profile',
            'age',
            'nickname',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'nickname': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }
