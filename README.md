# monteRecruit

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


At the moment all the API endpoints use GET method. 
Some of them should use POST in a final application.
It is done for simplicity and as a proof of concept.