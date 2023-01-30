Profile
==================================

See the Lens Protocol docs for `Profiles <https://docs.lens.xyz/docs/profiles>`_.

.. py:method:: create_profile(handle)

	This method creates a new lens protocol profile with the given ``handle``. Must be authenticated to be able to do this, and the profile will be associated with the Ethereum address used to login at the time of the profile creation.

.. py:method:: get_default_profile(address)
	
	This gets an Ethereum address\'s default Lens profile (a single address can have multiple profiles, so this returns the *canonical* profile).

.. py:method:: delete_profile(profileId)
	
	Returns typed data for deleting the Lens profile with ``profileId``. This requires to be signed then the result ``broadcast`` before the act of deleting the profile is indexed. Note must be logged in to be able to do this.

**Below are some LensPy specific methods**. You won't find these on the main Lens Protocol docs.

.. py:method:: get_profile_id(handle)

	Gets the Lens Protocol ``profileId`` for a given handle name.

.. py:method:: my_profiles(limit)
	
	Gets all data on profiles owned by the public address used to log in (up to ``limit`` number of profiles).

.. py:method:: my_profile_handles(limit)
	
	Gets only the handles of profiles owned by the public address used to login (up to ``limit`` number of profiles).