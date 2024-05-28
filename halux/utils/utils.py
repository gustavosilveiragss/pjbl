from flask import request, redirect, render_template

data = dict(active_page="dashboard")


def is_authenticated():
    return "user_id" in request.cookies and get_user_id() >= 1


def is_admin():
    return is_authenticated() and get_user_id() == 1

def get_user_id():
    return int(request.cookies["user_id"]) if "user_id" in request.cookies else -1


def render_template_if_authenticated(template: str, **kwargs):
    if not is_authenticated():
        return redirect("/")
    return render_template(template, data=data, cookies=request.cookies, **kwargs)


def render_template_if_admin(template: str, **kwargs):
    if not is_admin():
        return redirect("/")
    return render_template(template, data=data, cookies=request.cookies, **kwargs)
