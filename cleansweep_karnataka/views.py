from flask import (redirect, request, render_template, session)
import json

from cleansweep.plugin import Plugin
from cleansweep.models import Place, db
from cleansweep.plugins.volunteers import signals

# required for our second view
from . import forms, stats

plugin = Plugin("karnataka", __name__, template_folder="templates")


def init_app(app):
    """Initalized the plugin, called by main.py to load this plugin.
    """
    # and intialize the plugin
    plugin.init_app(app)

    # replace the signup page with new one
    app.view_functions['signups.signup'] = new_signup


def new_signup():
    userdata = session.get("oauth")

    # get district or defalt to bangalore (21)
    district = request.args.get("district", 21)

    # is user autheticated?
    if not userdata:
        return render_template("new_signup.html", userdata=None, district=district)

    form = forms.SignupForm()
    if request.method == "GET":
        form.name.data = userdata['name']
        form.email.data = userdata['email']
    elif request.method == "POST" and form.validate():
        data = _process_signup_data(form.data, userdata['email'])
        place = data.get('place_key') and Place.find(data['place_key'])
        if place:
            place = Place.find(data['place_key'])
            person = place.add_member(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                voterid=data['voterid'],
                details=data)
            db.session.commit()
            signals.add_new_volunteer.send(person)
            return render_template("new_signup.html", userdata=userdata, done=True)
        else:
            # TODO: show error that specified place is not found
            pass

    return render_template("new_signup.html", userdata=userdata, form=form, simple=True, district=district)

def _process_signup_data(formdata, user_email):
    data = dict(formdata, submitted_by=user_email)
    data['voterid_info'] = json.loads(data['voterid_info']) if data.get("voterid_info") else None
    data['proxy_voterid_info'] = json.loads(data['proxy_voterid_info']) if data.get("proxy_voterid_info") else None

    place_info = data['voterid_info'] or data['proxy_voterid_info'] or {}
    if place_info:
        ac = place_info['ac'].split("-")[0].strip()
        pb = place_info['pb'].split("-")[0].strip()
        place_key = "KA/{}/{}".format(ac, pb)
        data['place_key'] = place_key
    return data
