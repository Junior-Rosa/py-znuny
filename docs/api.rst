API Reference
=============

 Api reference for pyznuny, here you can find all the classes and methods available in the library, with examples of how to use them.

.. currentmodule:: pyznuny

.. _ticketclient:
.. autoclass:: TicketClient
   :members:  ticket, set_endpoint
   :show-inheritance:

.. _ticketclient-ticket:
.. py:attribute:: TicketClient.ticket

TicketClient.ticket
-------------------

The attribute ``TicketClient.ticket`` exposes the following methods.

.. currentmodule:: pyznuny.ticket.routes

.. autoclass:: TicketRoutes
   :members: create, update, get
   :noindex:

.. _ticketclient-set-endpoint:
.. py:attribute:: TicketClient.set_endpoint

TicketClient.set_endpoint
-------------------

The attribute ``TicketClient.set_endpoint`` exposes the following methods.

.. currentmodule:: pyznuny.ticket.endpoints

.. autoclass:: EndpointSetter
   :members: ticket_create, ticket_get, ticket_update
   :noindex:
   
