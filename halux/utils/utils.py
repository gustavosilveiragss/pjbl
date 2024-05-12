from flask import request, redirect, render_template

data = dict(active_page="dashboard")


def is_authenticated():
    return "username" in request.cookies and "password" in request.cookies


def render_template_if_authenticated(route: str, **kwargs):
    if not is_authenticated():
        return redirect("/")
    return render_template(route, data=data, **kwargs)
