from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Attendee, ConferenceVO, AccountVO
import json
from common.json import ModelEncoder

class ConferenceVODetailEncoder(ModelEncoder):
    model = ConferenceVO
    properties = ["name", "import_href"]

class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties =[
        "name",
        "email",
     ]

class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]
    encoders = {
        "conference": ConferenceVODetailEncoder(),
    }
        # Get the count of AccountVO objects with email equal to o.email
        # count = AccountVO.objects.filter(email=o.email).count()
        # Return a dictionary with "has_account": True if count > 0

        # Otherwise, return a dictionary with "has_account": False
    def get_extra_data(self, o):
        count = AccountVO.objects.filter(email=o.email).count()
        print(f"count: {count}")
        if count > 0:
            return {
                "has_account": True
            }
        else:
            return {
                "has_account": False
            }
#code along
@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_vo_id=None):
    """
    Lists the attendees names and the link to the attendee
    for the specified conference id.

    Returns a dictionary with a single key "attendees" which
    is a list of attendee names and URLS. Each entry in the list
    is a dictionary that contains the name of the attendee and
    the link to the attendee's information.

    {
        "attendees": [
            {
                "name": attendee's name,
                "href": URL to the attendee,
            },
            ...
        ]
    }
    """

    if request.method == "GET":
        attendees = Attendee.objects.filter(conference=conference_vo_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
        )
    #"POST"
    else:
        content = json.loads(request.body)

        # Get the Conference object and put it in the content dict
        try:
            conference_href = f'/api/conferences/{conference_vo_id}/'
            conference = ConferenceVO.objects.get(import_href=conference_href)
            content["conference"] = conference
        except ConferenceVO.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )

@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_attendee(request, id):
    """
    Returns the details for the Attendee model specified
    by the id parameter.

    This should return a dictionary with email, name,
    company name, created, and conference properties for
    the specified Attendee instance.

    {
        "email": the attendee's email,
        "name": the attendee's name,
        "company_name": the attendee's company's name,
        "created": the date/time when the record was created,
        "conference": {
            "name": the name of the conference,
            "href": the URL to the conference,
        }
    }
    """
    if request.method == "GET":
        attendees = Attendee.objects.get(id=id)
        # attendees.create_badge()
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
    # elif request.method == "POST":
    #     content = json.body(request.body)
    #     try:
    #         conference_href = f'/api/conferences/{conference_vo_id}/'
    #         conference = ConferenceVO.objects.get(import_href=conference_href)
    #         content["conference"] = conference
    #     except ConferenceVO.DoesNotExist:
    #         return JsonResponse(
    #             {"message": "Invalid conference id"},
    #             status=400,
    #         )
    #     attendees = Attendee.objects.create(**content)
    #     return JsonResponse(
    #         attendees,
    #         encoder=AttendeeDetailEncoder,
    #         safe=False,
    #     )
    elif request.method == "PUT":
        content = json.loads(request.body)
        # try:
        #     conference_href = f'/api/conferences/{conference_vo_id}/'
        #     conference = ConferenceVO.objects.get(import_href=conference_href)
        #     content["conference"] = conference
        # except ConferenceVO.DoesNotExist:
        #     return JsonResponse(
        #         {"message": "Invalid conference id"},
        #         status=400,
        #     )

        Attendee.objects.filter(id=id).update(**content)
        attendees = Attendee.objects.get(id=id)
        return JsonResponse(
            attendees,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
    else:
        count, _ = Attendee.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    # return JsonResponse(
    #     {
    #         "email": attendees.email,
    #         "name": attendees.name,
    #         "company_name": attendees.company_name,
    #         "created": attendees.created,
    #         "conference": {
    #             "name": attendees.conference.name,
    #             "href": attendees.conference.get_api_url(),
    #     }
    #     }
    # )
