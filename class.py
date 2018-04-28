import re
def finddata(a, b, y, m, d):
    L = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    i = 1
    j = 1
    while True:
        if i == a and j == b:
            return [m, d]
        if j < 7:
            j += 1
        else:
            j = 1
            i += 1
        if d < L[m-1]:
            d += 1
        else:
            d = 1
            if m < 12:
                m += 1
            else:
                m = 1
                y += 1
def findtime(a, b):
    if a <= 4:
        return [100*(7+a), 100*(7+a+b-1)+50]
    else:
        return [1330+100*(a-5), 1320+100*(a+b-5)]

regX1 = "onMouseOut(.*?)</tr>"
regX2 = "&nbsp;(.*?)</td>"
regX3 = "<td>&nbsp;(.*?)</td>"

startyear = 2018
startmonth = 3
startday = 5

f = open("class.txt", "r", encoding="utf-8")
f2 = open("class_schedule.ics", 'w', encoding="utf-8")
content = f.read()
entries = re.findall(regX1, content, re.S)
events = []

for item1 in entries:
    name = re.findall(regX2, item1, re.S)[2]
    fields = re.findall(regX3, item1, re.S)
    index = 0
    while index < len(fields):
        if index==0:
            event = [name];
            # print(name)
        if index==0 or index==1 or index==2 or index==3 or index==6:
            event.append(fields[index])
            # print(fields[index])
        if index == 6:
            events.append(event)
        index += 1

index2 = 0
schedule = []
dic = {}

f2.write("BEGIN:VCALENDAR\nX-WR-TIMEZONE:Asia/Shanghai\n")
while index2 < len(events):
    if len(events[index2][0]) == 1 and index2 > 0:
        events[index2][0] = events[index2-1][0]
    dic['name'] = events[index2][0]
    period = re.findall("(\d+)-(\d+)", events[index2][1], re.S)
    if len(period) == 0:
        temp = re.findall("(\d+)", events[index2][1], re.S)
        period.append((temp[0], temp[0]))
    dic['year'] = startyear
    [dic['month'], dic['day']] = finddata((int)(period[0][0]), (int)(events[index2][2]), startyear, startmonth, startday)
    if "单" in events[index2][1]:
        dic['interval'] = 2
    else:
        dic['interval'] = 1
    dic['count'] = (int)((int)(period[0][1]) - (int)(period[0][0]) + 1)/dic['interval']
    [dic['starttime'], dic['endtime']] = findtime((int)(events[index2][3]), (int)(events[index2][4]))
    dic['place'] = events[index2][5]
    f2.write("BEGIN:VEVENT\n")
    f2.write("DTSTART:%d%02d%02dT%04d00\n" % (dic['year'], dic['month'], dic['day'], dic['starttime']))
    f2.write("DTEND:%d%02d%02dT%04d00\n" % (dic['year'], dic['month'], dic['day'], dic['endtime']))
    f2.write("RRULE:FREQ=WEEKLY;INTERVAL=%d;COUNT=%d\n" % (dic['interval'], dic['count']))
    f2.write("SUMMARY:%s%s\n" % (dic['name'], dic['place']))
    f2.write("END:VEVENT\n")
    index2 += 1
f2.write("END:VCALENDAR\n")
f.close()
f2.close()
