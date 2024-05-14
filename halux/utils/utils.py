from flask import request, redirect, render_template

data = dict(active_page="dashboard")


def is_authenticated():
    return "user_id" in request.cookies and int(request.cookies["user_id"]) >= 1


def is_admin():
    return is_authenticated() and int(request.cookies["user_id"]) == 1


def render_template_if_authenticated(template: str, **kwargs):
    if not is_authenticated():
        return redirect("/")
    return render_template(template, data=data, cookies=request.cookies, **kwargs)


def render_template_if_admin(template: str, **kwargs):
    if not is_admin():
        return redirect("/")
    return render_template(template, data=data, cookies=request.cookies, **kwargs)
