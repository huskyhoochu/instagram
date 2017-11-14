from member.decorators import login_required
from member.forms import User


@login_required
def follow(request, user_pk):
    if request.method == 'POST':
        user = User.objects.get(pk=user_pk)
        User.follow_toggle(user)

    return

