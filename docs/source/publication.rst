Publication
==================================

See the Lens Protocol docs for `Publications <https://docs.lens.xyz/docs/publication-1>`_.

.. py:method:: comment(profileId,publicationId,contentURI,collectModule,referenceModule)

	Return typed data for leaving a comment on a specific publication. This typed data needs to be signed and ``broadcast``. The parameters ``profileId``, ``publicationId`` and ``contentURI`` are required parameters. ``collectModule`` and ``referenceModule`` are optional since LensPy provide some defaults if you are not sure. Look at the Lens Protocol docs for a detailed explanation of ``collectModule`` and ``referenceModule``.
	
.. py:method:: mirror(profileId,publicationId,referenceModule)
	
	Return typed data for mirroring a specific publication. This typed data needs to be signed and ``broadcast``. The parameters ``profileId`` and ``publicationId`` are required parameters. ``referenceModule`` is optional since LensPy provides a default if you are not sure. Take a look at the Lens Protocol docs for a detailed explanation of ``referenceModule``.

.. py:method:: post(profileId,contentURI,collectModule,referenceModule)
	
	Return typed data for creating a post. This typed data needs to be signed and ``broadcast``. The parameters ``profileId`` and ``contentURI`` are required parameters. ``collectModule`` and ``referenceModule`` are optional since LensPy provide some defaults if you are not sure. Look at the Lens Protocol docs for a detailed explanation of ``collectModule`` and ``referenceModule``.