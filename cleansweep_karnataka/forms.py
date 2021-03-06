from flask_wtf import Form
from wtforms import (
    BooleanField, DateField, IntegerField, HiddenField,
    StringField, TextAreaField,
    SelectField, RadioField, SelectMultipleField,
    validators, ValidationError,
    widgets)

from cleansweep.models import Member

def radio_field(label, values,  **kwargs):
    choices = [(v, v) for v in values]

    required = kwargs.pop("required", False)
    default = kwargs.pop("default", "")
    if not required:
        choices += [("", "Not Specified")]
    else:
        kwargs['validators'] = [validators.Required()]
    return RadioField(label, choices=choices, default=default, **kwargs)

def checkbox_field(label, values, validators=None):
    return SelectMultipleField(
        label,
        choices=[(v, v) for v in values],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        validators=validators or []
        )

class DateField2(DateField):
    def process_formdata(self, valuelist):
        # ignore empty values
        valuelist = [v for v in valuelist if v]
        return DateField.process_formdata(self, valuelist)

class SignupForm(Form):
    name = StringField('Name', [validators.Required()])
    gender = SelectField('Gender', [validators.Required()], choices=[('male', 'Male'), ('female', 'Female')])

    phone = StringField('Personal Mobile No.', [validators.Required()])
    email = StringField('Personal E-Mail ID', [validators.Required()])

    is_voter_at_residence = radio_field(
        "Is your Voter ID address same as your residential address?",
        ['YES', 'NO', "I don't have a valid Voter ID"],
        required=True,
        default="YES")
    voterid = StringField("Personal Voter ID")
    voterid_info = HiddenField()
    proxy_voterid = StringField("Proxy Voter ID")
    proxy_voterid_info = HiddenField()

    def validate_voterid(self, field):
        if self.is_voter_at_residence.data in ["YES", "NO"]:
            value = field.data
            if not value:
                raise ValidationError("This field is Required")
            if not self.voterid_info.data:
                raise ValidationError("Please verify the Voter ID before submit")

    def validate_proxy_voterid(self, field):
        if self.is_voter_at_residence.data != "YES":
            value = field.data
            if not value:
                raise ValidationError("This field is Required")
            if not self.proxy_voterid_info.data:
                raise ValidationError("Please verify the Voter ID before submit")

    def validate_email(self, field):
        if field.data.strip() != 'NA':
            v = validators.Email()
            v(self, field)
            if Member.find(email=field.data):
                raise ValidationError("This email address is already registered.")


class SignupForm2(Form):
    name = StringField('Name', [validators.Required()])
    father_name = StringField('Father Name')
    gender = SelectField('Gender', [validators.Required()], choices=[('male', 'Male'), ('female', 'Female')])
    date_of_birth = DateField2('Date of Birth', format='%d-%m-%Y')

    mobile = StringField('Personal Mobile No.', [validators.Required()])
    mobile2 = StringField('Personal Mobile No. 2')
    email = StringField('Personal E-Mail ID', [validators.Required()])

    emergency_contact = TextAreaField('EMERGENCY CONTACT NAME, RELATIONSHIP & MOBILE NUMBER')

    address = TextAreaField('Residential Address')
    pincode = StringField('PIN Code')

    employer = StringField('EMPLOYER NAME OR PROFESSION')

    livelihood = radio_field("Your Occupation", ['SALARIED EMPLOYEE', 'SELF EMPLOYED', 'RETIRED', 'STUDENT', 'OTHER'])
    choice_of_communication = checkbox_field("Your Preferred Choice of Communication",
        ['SMS', 'WHATSAPP', 'E-MAIL', 'FACEBOOK', 'TWITTER'])

    work_from = radio_field('WHERE YOU WOULD LIKE TO WORK FROM', ['HOME', 'OUTSIDE', 'BOTH'])
    internet_connection = radio_field("DO YOU HAVE INTERNET CONNECTION AT HOME", ['YES', 'NO'])

    how_much_time = radio_field("HOW MUCH TIME YOU CAN VOLUNTEER", [
        "FULL TIME",
        "2-4 HOURS DAILY",
        "1 HOUR/DAY ON WEEKDAYS",
        "ONLY WEEKEND"
        ])

    languages = checkbox_field("Languages That You Can Speak", [
        "KANNADA",
        "ENGLISH",
        "HINDI", 
        "OTHER SOUTH INDIAN LANGUAGE"
    ])

    skills = checkbox_field("Areas where you can volunteer for Central Team", [
        "Accounting/Finance",
        "Content Translators (Like Kannada News to Eng or Viceversa)",
        "Coordinators/ managers",
        "Creative (poets, musicians, artists, street theater)",
        "Data entry from Anywhere",
        "Designers on Photoshop / CorelDraw",
        "Doctor/ Healthcare",
        "Event Management",
        "FB / E-mail Content writing",
        "Following on FB / Twitter for Feeder service",
        "Fund Raising",
        "Graphic designing",
        "Handle Helpline calls from Home",
        "Joomal / Drupal / Webdesigning Expert",
        "Legal Service",
        "Logistic  Management",
        "Media / Journalism / Communication",
        "Office administration",
        "On the ground work",
        "Online Researchers",
        "Photographer/Videographer",
        "Public Speaking",
        "Publicity / Advertisement",
        "RTI Activist",
        "Social Media Moderator (FB / Twitter)",
        "Sourcing of News from online",
        "System administrator",
        "Technical support / Information Tech.",
        "Tele campaigning",
        "Trainers",
        "Video Editor / Film Maker",
        "Volunteer management",
    ])

    active_volunteer = radio_field("Have you volunteered for Aam Aadmi Party before?", ['YES', 'NO'])

    contributions = checkbox_field("What did you volunteer?", [
            "On-ground activities in Karnataka",
            "Remote/back-office activities in Karnataka",
            "On-ground activities in Delhi",
            "Remote/back-office activities in Delhi",
        ])

    reporting_person_name = StringField("Name of the person that you've reported to")
    reporting_person_mobile = StringField("Mobile number of the person that you've reported to")

    is_voter_at_residence = radio_field("Is your Voter ID address same as your residential address?", ['YES', 'NO', "I don't have a valid Voter ID"], required=True)
    voterid = StringField("Personal Voter ID")
    voterid_info = HiddenField()
    proxy_voterid = StringField("Proxy Voter ID")
    proxy_voterid_info = HiddenField()

    def validate_voterid(self, field):
        if self.is_voter_at_residence.data in ["YES", "NO"]:
            value = field.data
            if not value:
                raise ValidationError("This field is Required")
            if not self.voterid_info.data:
                raise ValidationError("Please verify the Voter ID before submit")

    def validate_proxy_voterid(self, field):
        if self.is_voter_at_residence.data != "YES":
            value = field.data
            if not value:
                raise ValidationError("This field is Required")
            if not self.proxy_voterid_info.data:
                raise ValidationError("Please verify the Voter ID before submit")

    def validate_email(self, field):
        if field.data.strip() != 'NA':
            v = validators.Email()
            v(self, field)