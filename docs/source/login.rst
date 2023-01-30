Login
==================================

See the Lens Protocol docs for `Login <https://docs.lens.xyz/docs/login>`_.

There are multiple methods regarding logging in to be authenticated as the owner of a profile. Lens profiles are associated with an Ethereum address. The first of the methods below, ``login``, is meant for use with PyScript or local testing only (since it takes a users private address as a parameter so cannot be deployed to a python server and used with real accounts).

.. py:method:: login(public_address,private_address)
	
	Log in to Lens Protocol with the key pair supplied. This is a LensPy method that simplifies getting started with Lens Protocol. It implements ``Challenge`` and ``Authenticate`` in a single method. If successful, the user is authenticated and can make ``mutations`` that can write to the blockchain (as opposed to only ``queries`` that read).
	
	**Note**: unless using some client side python like PyScript, do not use in production as it could expose users private addresses.

.. py:method:: challenge(address)

	Requests a ``challenge`` for authentification of the ``address`` from Lens. Returns typed data, which once signed can be used with the ``authenticate`` method below.

.. py:method:: authenticate(address,signature)
	
	Takes a public address and a signature (signed from the typed data of ``challenge`` response) and responds with an ``accessToken`` that authenticates the ``GraphQL`` client (this happens within LensPy so you do not need to think about this).

------------------
To be implemented
------------------

- Refresh
- Verify
