from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response


class AdminOrderableAPIView(APIView):
    def post(self, *args, **kwargs):
        content_type_id = kwargs.get("content_type_id")
        object_id = kwargs.get("object_id")
        content_type = ContentType.objects.get_for_id(content_type_id)
        item = content_type.get_object_for_this_type(id=object_id)
        action = self.request.POST.get("action")

        if action == "move-up":
            item.move_up()
        elif action == "move-down":
            item.move_down()

        return Response(status=status.HTTP_200_OK)