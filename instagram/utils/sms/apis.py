from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

from utils.sms.serilaizers import SMSSerializer


class SendSMS(APIView):
    api_key = "NCSGLMHSQ2FTVZUA"
    api_secret = "2ZNM5ZPZR07QHSLHVIFAH3XZR1GAGM2F"

    def post(self, request):
        serializer = SMSSerializer(data=request.data)

        if serializer.is_valid():
            # 4 params(to, from, type, text) are mandatory. must be filled
            params = {
                'type': 'sms',
                'to': serializer.validated_data['receiver'],
                'from': '01029953874',
                'text': serializer.validated_data['message'],
                }

            cool = Message(self.api_key, self.api_secret)

            try:
                response = cool.send(params)
                print("Success Count : %s" % response['success_count'])
                print("Error Count : %s" % response['error_count'])
                print("Group ID : %s" % response['group_id'])

                if "error_list" in response:
                    print("Error List : %s" % response['error_list'])

            except CoolsmsException as e:
                print("Error Code : %s" % e.code)
                print("Error Message : %s" % e.msg)

        return Response(status=status.HTTP_200_OK)
