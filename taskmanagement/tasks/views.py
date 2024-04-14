from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from . models import Event
from collections import defaultdict


# Create your views here.
class EventManager:
    def tocreate_event(request):
        return render(request, 'create_event.html')
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

    def toupdate_event(request):
        events = Event.objects.all()
        return render(request, 'update_event.html', {'events': events})

    @staticmethod
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

    def todelete_event(request):
        events = Event.objects.all()
        return render(request, 'delete_event.html', {'events': events})

    @staticmethod
    def delete_event(request):
        if request.method == 'POST':
            event_ids = request.POST.getlist('events') #取得checkbox的id
            for event_id in event_ids:
                Event.objects.filter(id=event_id).delete()
            return HttpResponse("选定的事件已成功删除")
        else:
            pass

    @staticmethod
    def categorized_events(request):
        labels = Event.objects.values_list('label', flat=True).distinct()
        categorized_events = {}
        for label in labels:
            events = Event.objects.filter(label=label)
            categorized_events[label] = events
        return render(request, 'categorized_events.html', {'categorized_events': categorized_events})

    @staticmethod
    def search_events(request):
        if request.method == 'GET':
            search_label = request.GET.get('event_label')
            events = Event.objects.filter(label__icontains=search_label)
            if events:
                response = "<br>".join([f"{event.name} - {event.label} - {event.date}" for event in events])
                return HttpResponse(response)
            else:
                return HttpResponse("查詢欄為空白！請重新查詢")
        else:
            pass





