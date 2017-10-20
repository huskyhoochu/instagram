from django.shortcuts import redirect


def post_main(request):
    return redirect('post:post_list')
