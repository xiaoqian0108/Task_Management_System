from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django import forms
from . models import Event
from datetime import datetime
from .week_events import WeekEvents

# Create your views here.
class JumpToPage:
    @staticmethod
    def get_all_events():
        return Event.objects.all()
    def tocreate_event(request):
        return render(request, 'create_event.html')
    def toupdate_event(request):
        events = JumpToPage.get_all_events()
        return render(request, 'update_event.html', {'events': events})
    def todelete_event(request):
        events = JumpToPage.get_all_events()
        return render(request, 'delete_event.html', {'events': events})
    

class EventManager:
    @staticmethod
    def create_event(request):
        if request.method == 'POST':
            name = request.POST.get('event_name')
            label = request.POST.get('event_label')
            date = request.POST.get('event_date')
            if name and label and date:
                Event.objects.create(name=name, label=label, date=date)
                return HttpResponse("Event創建成功。")
            else:
                return HttpResponse("Event創建失敗。")
        else:
            pass

    def update_event(request):
        if request.method == 'POST':
            name = request.POST.get('event_name')
            label = request.POST.get('event_label')
            date = request.POST.get('event_date')

            event_id = request.POST.get('event_id')

            if not (name or label or date):
                return HttpResponse("請輸入更新的內容！")
            else:
                event = get_object_or_404(Event, pk=event_id)
                if name:
                    event.name = name
                if label:
                    event.label = label
                if date:
                    event.date = date
                event.save()
            return HttpResponse("修改成功！")
        else:
            return HttpResponse("修改失敗！")

    def delete_event(request):
        if request.method == 'POST':
            event_ids = request.POST.getlist('events') #取得checkbox的id
            if event_ids:
                for event_id in event_ids:
                    Event.objects.filter(id=event_id).delete()
                return HttpResponse("已成功删除")
            else:
                return HttpResponse("删除失敗！")
        else:
            pass

    def categorized_events(request):
        labels = Event.objects.values_list('label', flat=True).distinct()
        categorized_events = {}
        for label in labels:
            events = Event.objects.filter(label=label)
            categorized_events[label] = events
        return render(request, 'categorized_events.html', {'categorized_events': categorized_events})

    def search_events(request):
        if request.method == 'GET':
            search_label = request.GET.get('event_label')
            if search_label:
                events = Event.objects.filter(label__icontains=search_label)
                if events:
                    response = "<br>".join([f"{event.name} - {event.label} - {event.date}" for event in events])
                    return HttpResponse(response)
                else:
                    return HttpResponse("沒有找到！請重新輪入")
            else:
                return HttpResponse("空白內容！")
        else:
            pass
            
    def list_event(request):
        events = Event.objects.all()
        return render(request, 'list_event.html', {'events': events})
    
    def update_event_detail(request, event_id):
        if request.method == 'POST':
            event = get_object_or_404(Event, pk=event_id)
            event.description = request.POST.get('event_description')
            event.save()
            return HttpResponse("更新成功！")
        else:
            event = get_object_or_404(Event, pk=event_id)
            return render(request, 'event_detail.html', {'event': event})

    def week_events(request):
        current_date = datetime.now().date()
        all_events = Event.objects.all().order_by('date')

        events_by_week = {}
        for event in all_events:
            week_number = WeekEvents.get_week_number(event.date)
            if week_number not in events_by_week:
                events_by_week[week_number] = []
            events_by_week[week_number].append(event)

        weeks_data = []
        for week_number, events in events_by_week.items():
            week_start, week_end = WeekEvents.get_week_range_for_number(current_date.year, week_number)
            week_title = f"{week_start.strftime('%Y/%m/%d')} - {week_end.strftime('%Y/%m/%d')}"
            weeks_data.append({'week_title': week_title, 'events': events})

        return render(request, 'week_events.html', {'weeks_data': weeks_data})


