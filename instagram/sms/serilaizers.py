import re

from rest_framework import serializers


class SMSSerializer(serializers.Serializer):
    receiver = serializers.CharField()
    message = serializers.CharField(max_length=90)

    def validate_receiver(self, value):
        pattern = re.compile(r'^(010)(\d{4})(\d{4})$')

        if pattern.match(value):
            return value
        else:
            raise serializers.ValidationError('전화번호가 일치하지 않습니다')


"""
receiver에 휴대전화 형식의 데이터가 왔는지 validate
message에 90자 이하의 문자열이 왔는지 Validate

is_valid() 검사 후
serializer.data에 있는 내용을 이용해서 send 처리
"""