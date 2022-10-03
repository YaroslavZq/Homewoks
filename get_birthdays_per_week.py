import datetime

USERS = [{"name": "Roman", "birthday": datetime.date(year=2022, month=9, day=30)},
         {"name": "Ira", "birthday": datetime.date(year=2022, month=9, day=29)},
         {"name": "Vlad", "birthday": datetime.date(year=2022, month=9, day=29)},
         {"name": "Yuriy", "birthday": datetime.date(year=2022, month=10, day=1)},
         {"name": "Anna", "birthday": datetime.date(year=2022, month=9, day=3)},
         {"name": "Olga", "birthday": datetime.date(year=2022, month=10, day=2)}]


def get_birthdays_per_week(users):
    today = datetime.date.today()
    weekends_names = []
    # пишу дні тижндня від сьогодні на цілий тиждень без вихідних
    for i in range(7):
        names = []
        for user in users:
            if today == user.get("birthday"):
                names.append(user.get("name"))
        if today.strftime('%A') in ("Sunday", "Saturday"):
            weekends_names.extend(names)
            today = today + datetime.timedelta(days=1)
            continue
        elif today.strftime('%A') == "Monday":
            names.extend(weekends_names)
        print(today.strftime('%A:'), ", ".join(names))
        today = today + datetime.timedelta(days=1)


get_birthdays_per_week(USERS)
