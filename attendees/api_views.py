from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Attendee
import json
from common.json import ModelEncoder
from events.models import Conference

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
        # "conference",
    ]
    def get_extra_data(self, o):
        return { "conference": o.conference.name, "badge": hasattr(o, "badge")}


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
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
        attendees = Attendee.objects.filter(conference=conference_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
        )
    else:
        content = json.loads(request.body)

        # Get the Conference object and put it in the content dict
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
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
    attendees = Attendee.objects.get(id=id)
    # attendees.create_badge()
    return JsonResponse(
        attendees,
        encoder=AttendeeDetailEncoder,
        safe=False
    )
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
