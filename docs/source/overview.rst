Overview
============

Lens Protocol is library that allows developers to build social networks on web3. LensPy is a python library to open the functionality of Lens Protocol to python developers.

See the Lens `Protocol documentation <https://docs.lens.xyz/docs>`_.

A high level view of how to implement functionality with Lens Protocol (eg. user wishes to post):

- user wishes to make a post
- users web client makes a request for relevant typed data to the Lens Protocol server
- the Lens Protocol server responds with typed data for that post
- users web client signs the typed data with their private key (on client-side)
- this is then ``broadcast`` to Lens Protocol, which is then indexed on-chain (Polygon Mainnet)

As a developer using LensPy, you do not need to consider the communication with Lens Protocol (which uses `GraphQL <https://graphql.org/>`_). This is handled by LensPy on your Python server (running Flask, Django etc...). However it is important to note that the server does not have access to users private key, so the signing in the above step needs to take place in the browser client-side. The resulting signature can then be sent to the Python server where LensPy will then ``broadcast`` it to Lens Protocol.

Examples of using LensPy with `Flask <https://flask.palletsprojects.com/en/2.2.x/>`_ and `Django <https://www.djangoproject.com/>`_.