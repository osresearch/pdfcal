# Annual agenda generator
![Remarkable tablet with April 15th calendar displayed](tablet.jpg)

This python tool outputs a page-per-day agenda PDF with internal links to
allow easy navigation from tablets like the Remarkable.  The template is
relatively hard-coded and could probably be made more generic. I use the
check boxes on the right hand side as a Todo list for un-timed items to
be done that day.

```
pip install -r requirements.txt
python3 ./make-calendar
```


* To navigate to a specific day, click on the days of the month.
* For a month overview, click on the month name
* For a year overview, click on the date at the top right

If you re-generate the PDF it is possible to `ssh` into the Remarkable
and change out the file while preserving all of the written notes so far.
The file is stored in `/root/.local/share/remarkable/xochitl/`, although renamed
to a UUID, so you have to find the one to replace based on the size or date it
was installed.  Mine was `6c0a555b-fc8a-4143-9a1b-2efdb3dad7da`, although yours
is likely different.

If you have an iCal file and want to pre-populate events into the calendar,
add them on the command line:

```
curl 'https://ics.calendarlabs.com/76/7f1396de/US_Holidays.ics' > holidays.ics
python3 ./make-calendar holidays.ics
```

Recurring events are supported thanks to [`recurring-ical-events`](https://github.com/niccokunzmann/python-recurring-ical-events),
which handles the complexity of the iCal `RRULE` format and `EXDATE`.
However, timezones are sort of punted on (everything is done in "local" time, with the
assumption that you'll be in the timezone where the event is specified)
and overlapping events are not properly rendered (they will overlap on the calendar).
