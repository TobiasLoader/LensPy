Broadcast
==================================

Lens Protocol ensures the safety of the users by often requiring a two stage process (like when following a profile). Firstly the user must be logged in (see ``athentication``), then the user sends a graphql request for a typed data response. This is then signed by the user and sent before the request is accepted.

.. py:method:: broadcast(broadcastId,signature)

	Takes the ``broadcastId`` from some typed data response, and the signature of that typed data by the users private key, and returns a broadcast mutation to be executed by the ``GraphQLClient``. 

NB: This is not required if you are using a **dispatcher**.