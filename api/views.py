# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('name', 'phone', 'part')


class PersonDetailView(APIView):

    def get_object(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            return Http404

    def get(self, request, person_id):
        person = self.get_object(person_id)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def post(self, request, person_id):
        person = self.get_object(person_id)
        serializer = PersonSerializer(person)
        return Response(serializer.data)
