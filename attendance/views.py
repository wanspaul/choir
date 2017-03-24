import calendar
import logging

from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Count, Case, When, IntegerField
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import View
from datetime import datetime, timedelta, date

from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import Song, Practice, Person, Attendance
from choir.common.api_result import APIResult, APIStatusMessage, APIResultSerializer
from choir.common.api_result import APIStatusCode


class AttendanceHomeView(View):

    def get(self, request):

        last_practice = Practice.objects.last()

        if last_practice:
            attendance_info = Attendance.objects.select_related('person').filter(
                practice=last_practice.id, is_join=True).aggregate(
                attendance_count=Count('id'),
                s_count=Count(Case(When(person__part='S', then=1), output_field=IntegerField())),
                a_count=Count(Case(When(person__part='A', then=1), output_field=IntegerField())),
                t_count=Count(Case(When(person__part='T', then=1), output_field=IntegerField())),
                b_count=Count(Case(When(person__part='B', then=1), output_field=IntegerField()))
            )
        else:
            attendance_info = None

        today = datetime.now().date()
        last_day = calendar.monthrange(today.year, today.month)[1]
        first_date = date(today.year, today.month, 1).strftime('%m%d')
        last_date = date(today.year, today.month, last_day).strftime('%m%d')
        birthday_list = Person.objects.filter(
            birth_monthday__gte=first_date, birth_monthday__lte=last_date).all()

        logging.info(birthday_list)
        context = {
            'last_practice': last_practice,
            'attendance_info': attendance_info,
            'birthday_list': birthday_list
        }

        return TemplateResponse(request, 'attendance/home.html', context)


class PracticeAddView(View):

    def get(self, request):

        song_list = Song.objects.all().order_by('-no')

        context = {
            'practice_dt': datetime.now(),
            'song_list': song_list
        }

        return TemplateResponse(request, 'attendance/add_practice.html', context)

    def post(self, request):

        practice_dt = request.POST.get('practice_dt')
        song_no = request.POST.get('song')

        song = Song.objects.get(pk=song_no)
        person_list = Person.objects.all()
        attendance_list = []

        with transaction.atomic():
            practice = Practice()
            practice.practice_dt = practice_dt
            practice.song = song
            practice.save()

            for person in person_list:
                attendance = Attendance()
                attendance.practice = practice
                attendance.person = person
                attendance_list.append(attendance)

            Attendance.objects.bulk_create(attendance_list)

        return HttpResponseRedirect(reverse('attendance:home'))


class ChoirListView(View):

    def get(self, request, practice_id, part):

        person_list = Attendance.objects.select_related('person', 'practice').filter(
            practice__id=practice_id, person__part=part
        ).order_by('person__name')

        logging.info(len(person_list))

        if part == 'S':
            part_string = '소프라노'
            label_color = 'label-info'
        elif part == 'A':
            part_string = '알토'
            label_color = 'label-warning'
        elif part == 'T':
            part_string = '테너'
            label_color = 'label-success'
        elif part == 'B':
            part_string = '베이스'
            label_color = 'label-primary'
        else:
            # error.
            pass

        context = {
            'part': part,
            'part_string': part_string,
            'label_color': label_color,
            'person_list': person_list
        }

        return TemplateResponse(request, 'attendance/choir_list.html', context)


class PersonAddView(View):

    def get(self, request):

        part = request.GET.get('part')
        practice = Practice.objects.last()

        context = {
            'part': part,
            'practice': practice
        }

        return TemplateResponse(request, 'attendance/add_person.html', context)

    def post(self, request):

        name = request.POST.get('name')
        part = request.POST.get('part')
        birth = request.POST.get('birth')
        phone = request.POST.get('phone')
        practice_id = request.POST.get('practice_id')

        if birth and birth != '':
            birth_monthday = birth[2:6]

        with transaction.atomic():
            person = Person()
            person.name = name
            person.part = part
            person.birth = birth
            person.birth_monthday = birth_monthday
            person.phone = phone
            person.save()

            practice = Practice.objects.get(pk=practice_id)

            attendance = Attendance()
            attendance.practice = practice
            attendance.person = person

            attendance.save()

        return HttpResponseRedirect(reverse('attendance:choir_list', kwargs={'practice_id': practice_id, 'part': part}))


class AttendanceEditView(APIView):

    def post(self, request):

        person_id = request.POST.get('person_id')
        practice_id = request.POST.get('practice_id')
        is_join = request.POST.get('is_join')

        attendance = Attendance.objects.get(person=person_id, practice=practice_id)

        if is_join == 'true':
            attendance.is_join = True
        else:
            attendance.is_join = False

        attendance.save()

        api_result = APIResult()

        if False:
            api_result.status = APIStatusCode.ERROR
            api_result.message = APIStatusMessage.ERROR

        return Response(APIResultSerializer(api_result).data)


class PersonEditView(View):

    def get(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        practice = Practice.objects.last()
        context = {
            'person': person,
            'practice': practice
        }
        return TemplateResponse(request, 'attendance/edit_person.html', context)

    def post(self, request, person_id):

        name = request.POST.get('name')
        part = request.POST.get('part')
        birth = request.POST.get('birth')
        phone = request.POST.get('phone')
        origin_part = request.POST.get('origin_part')
        practice_id = request.POST.get('practice_id')
        if birth and birth != '':
            birth_monthday = birth[2:6]

        Person.objects.filter(pk=person_id).update(
            name=name, part=part, birth=birth, phone=phone, birth_monthday=birth_monthday
        )

        return HttpResponseRedirect(reverse('attendance:choir_list', kwargs={'practice_id': practice_id, 'part': origin_part}))
