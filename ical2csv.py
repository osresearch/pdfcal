#!/usr/bin/env python3
from icalendar import Calendar, Event
import recurring_ical_events
from dateutil import rrule
import datetime
import sys

def create_entry(entries, start, ev_len, title):
	ymd = start.strftime("%Y-%m-%d")
	if ev_len.seconds == 0:
		# this is an all day event
		hms = "00:00"
		size = 0
	else:
		hms = start.strftime("%H:%M")
		size = ev_len.seconds

	if ymd not in entries:
		entries[ymd] = {}
	day = entries[ymd]
	if hms not in day:
		day[hms] = []
	day[hms].append([size, title])

def process_ical(year, cal, entries):
	for ev in recurring_ical_events.of(cal).between((year,1,1), ((year+1),1,1)):
		start = ev["DTSTART"].dt
		end = ev["DTEND"].dt
		title = ev["SUMMARY"]

		if type(start) == datetime.date:
			# this is an all day event, handle it like a recurring.
			# note that the end day is *not* included in the recurrance
			while start < end:
				create_entry(entries, start, datetime.timedelta(), title)
				start += datetime.timedelta(days=1)
		else:
			create_entry(entries, start, end - start, title)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		year = int(sys.argv[1])
	else:
		year = 2025

	entries = {}
	process_ical(year, Calendar.from_ical(sys.stdin.read()), entries)

	for ymd,evs in sorted(entries.items()):
		for hms,evs in sorted(evs.items()):
			for ev in evs:
				print(ymd+","+hms+","+str(ev[0])+","+ev[1])


