from datetime import timedelta, datetime

class WeekEvents:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.events = []

    def add_event(self, event):
        # 確保事件在這一周內
        if self.start_date <= event.date <= self.end_date:
            self.events.append(event)

    def get_events(self):
        return self.events

    def get_week_title(self):
        return f"{self.start_date.strftime('%Y/%m/%d')} - {self.end_date.strftime('%Y/%m/%d')}"

    @staticmethod
    def get_week_range(date):
        # 找到一周的第一天（星期一）
        start_date = date - timedelta(days=date.weekday())
        # 找到一周的最後一天（星期日）
        end_date = start_date + timedelta(days=6)
        return start_date, end_date
    
    @staticmethod
    def get_week_range_for_number(year, week_number):
        january_1 = WeekEvents.get_week_range(datetime(year, 1, 1))[0]
        first_day_of_week = january_1 + timedelta(weeks=week_number - 1)
        start_date = first_day_of_week - timedelta(days=first_day_of_week.weekday())
        end_date = start_date + timedelta(days=6)
        return start_date, end_date

    @staticmethod
    def get_week_number(date):
        january_1 = date.replace(month=1, day=1)
        days_offset = january_1.weekday()
        week_number = ((date - january_1).days + days_offset) // 7 + 1
        return week_number