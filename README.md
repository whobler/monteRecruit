# Wojciech Hobler recruitment task

This project provides API endpoints for possible front-end use to a ticket-selling platform. 
It is very simplified and should be only used to assess Python writing skills.

This project uses django-cron to periodically erase outdated Reservations.
In order to make it work automatically a proper job should be added to crontab.
Otherwise it can be run manually by `./manage.py runcrons` command
(see [django-cron documentation](https://django-cron.readthedocs.io/en/latest/installation.html) for more info)

available URL's to use:
### /tickets/events/EVENT_ID
example: `/tickets/events/1)`


### /tickets/events/EVENT_ID/available_tickets
example: `/tickets/events/1/available_tickets`


### /tickets/reserve_ticket/TICKET_IDS
example: `/tickets/reserve_ticket/1,7,10`


### /tickets/pay/RESERVATION_ID/AMOUNT/TOKEN/CURRENCY
example: `/tickets/pay/1/10/1/EUR`
(this propably should be reworked)


###/tickets/reservations/RESERVATION_ID
example: `/tickets/reservations/1`


### /tickets/statistics/STATISTICS_TYPE
examples:
`/tickets/statistics/reserved_tickets_per_event`

or

`/tickets/statistics/reserved_tickets_by_type`


All endpoints return a JSON object for easy use with front-end.
The format and details can be easily changed.

Future improvements could include (but are not limited to):

1. rate limiting
2. using UUID instead of ID's
3. more useful statistics (like histograms)
4. more tests to ensure quality