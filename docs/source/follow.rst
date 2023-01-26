Follow
==================================

There are multiple methods/functions for following a profile

.. py:method:: follow(profileId)

	Takes a ``profileId`` (e.g. "0x01") as input and returns follow typed data. Generates the graphql query string to be executed by the ``GraphQLClient``.
	
	NB: The response typed data subsequently needs to be **signed** and ``broadcast`` before the network accepts you are following the profile. Find an example of that *here*.

.. py:method:: follow_broadcast(profileId,wallet_private_address)

	Takes a ``profileId`` and  ``wallet_private_address`` as input. This method abstracts away the generation of the graphql query, the signature of the response typed data, and the broadcast of signed data.
	
	**Important**: this requires access to the users private address, so it is only a feasible for testing or when running python client-side (eg. in PyScript, see example docs). It is extremely bad practice to ask a user to enter their private address to be sent on to your python server (Flask/Django etc.) where this function is run.