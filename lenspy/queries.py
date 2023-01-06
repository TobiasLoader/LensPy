def addReaction(var_dict):
	x="mutation addReaction {{  addReaction(request:         {{        {var_dict}}}        )}}".format(var_dict=var_dict)
	return x

def generateModuleCurrencyApprovalData(var_dict):
	x="query generateModuleCurrencyApprovalData {{  generateModuleCurrencyApprovalData(request:         {{        {var_dict}}}        ) {{    to    from    data  }}}}".format(var_dict=var_dict)
	return x

def approvedModuleAllowanceAmount(var_dict):
	x="query approvedModuleAllowanceAmount {{  approvedModuleAllowanceAmount(request:         {{        {var_dict}}}        ) {{    currency    module    contractAddress    allowance  }}}}".format(var_dict=var_dict)
	return x

def authenticate(var_dict):
	x="mutation Authenticate {{  authenticate(request:         {{        {var_dict}}}        ) {{    accessToken    refreshToken  }}}}".format(var_dict=var_dict)
	return x

def Broadcast(var_dict):
	x="mutation Broadcast {{  broadcast(request:         {{        {var_dict}}}        ) {{    ... on RelayerResult {{      txHash      txId    }}    ... on RelayError {{      reason    }}  }}}}".format(var_dict=var_dict)
	return x

def createBurnProfileTypedData(var_dict):
	x="mutation createBurnProfileTypedData {{  createBurnProfileTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      domain {{        name        chainId        version        verifyingContract      }}      types {{        BurnWithSig {{          name          type        }}      }}      value {{        nonce        deadline        tokenId      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def Challenge(var_dict):
	x="query Challenge {{  challenge(request:         {{        {var_dict}}}        ) {{    text  }}}}".format(var_dict=var_dict)
	return x

def createCollectTypedData(var_dict):
	x="mutation createCollectTypedData {{  createCollectTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      types {{        CollectWithSig {{          name          type        }}      }}      domain {{        name        chainId        version        verifyingContract      }}      value {{        nonce        deadline        profileId        pubId        data      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def createCommentTypedData(var_dict):
	x="mutation createCommentTypedData {{  createCommentTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      types {{        CommentWithSig {{          name          type        }}      }}      domain {{        name        chainId        version        verifyingContract      }}      value {{        nonce        deadline        profileId        profileIdPointed        pubIdPointed        contentURI        collectModule        collectModuleInitData        referenceModule        referenceModuleInitData        referenceModuleData      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def CreateCommentViaDispatcher(var_dict):
	x="mutation CreateCommentViaDispatcher {{  createCommentViaDispatcher(request:         {{        {var_dict}}}        ) {{    ... on RelayerResult {{      txHash      txId    }}    ... on RelayError {{      reason    }}  }}}}".format(var_dict=var_dict)
	return x

def CreateMirrorViaDispatcher(var_dict):
	x="mutation CreateMirrorViaDispatcher {{  createMirrorViaDispatcher(request:         {{        {var_dict}}}        ) {{    ... on RelayerResult {{      txHash      txId    }}    ... on RelayError {{      reason    }}  }}}}".format(var_dict=var_dict)
	return x

def CreatePostViaDispatcher(var_dict):
	x="mutation CreatePostViaDispatcher {{  createPostViaDispatcher(request:         {{        {var_dict}}}        ) {{    ... on RelayerResult {{      txHash      txId    }}    ... on RelayError {{      reason    }}  }}}}".format(var_dict=var_dict)
	return x

def createProfile(var_dict):
	x="mutation createProfile {{  createProfile(request:         {{        {var_dict}}}        ) {{    ... on RelayerResult {{      txHash    }}    ... on RelayError {{      reason    }}    __typename  }}}}".format(var_dict=var_dict)
	return x

def CreateSetProfileImageURIViaDispatcher(var_dict):
	x="mutation CreateSetProfileImageURIViaDispatcher {{  createSetProfileImageURIViaDispatcher(request:         {{        {var_dict}}}        ) {{    ... on RelayerResult {{      txHash      txId    }}    ... on RelayError {{      reason    }}  }}}}".format(var_dict=var_dict)
	return x

def CreateSetDispatcherTypedData(var_dict):
	x="mutation CreateSetDispatcherTypedData {{  createSetDispatcherTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      types {{        SetDispatcherWithSig {{          name          type        }}      }}      domain {{        name        chainId        version        verifyingContract      }}      value {{        nonce        deadline        profileId        dispatcher      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def doesFollow(var_dict):
	x="query doesFollow {{  doesFollow(request:         {{        {var_dict}}}        ) {{    followerAddress    profileId    follows  }}}}".format(var_dict=var_dict)
	return x

def exploreProfiles(var_dict):
	x="query exploreProfiles {{  exploreProfiles(request:         {{        {var_dict}}}        ) {{    items {{      ...ProfileFields    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def ExplorePublications(var_dict):
	x="query ExplorePublications {{  explorePublications(request:         {{        {var_dict}}}        ) {{    items {{      __typename      ... on Post {{        ...PostFields      }}      ... on Comment {{        ...CommentFields      }}      ... on Mirror {{        ...MirrorFields      }}    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def createFollowTypedData(var_dict):
	x="mutation createFollowTypedData {{  createFollowTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      domain {{        name        chainId        version        verifyingContract      }}      types {{        FollowWithSig {{          name          type        }}      }}      value {{        nonce        deadline        profileIds        datas      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def followerNftOwnedTokenIds(var_dict):
	x="query followerNftOwnedTokenIds {{  followerNftOwnedTokenIds(request:         {{        {var_dict}}}        ) {{    followerNftAddress    tokensIds  }}}}".format(var_dict=var_dict)
	return x

def followers(var_dict):
	x="query followers {{  followers(request:         {{        {var_dict}}}        ) {{    items {{      wallet {{        ...WalletFields      }}      totalAmountOfTimesFollowed    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def following(var_dict):
	x="query following {{  following(request:         {{        {var_dict}}}        ) {{    items {{      profile {{        ...ProfileFields      }}      totalAmountOfTimesFollowing    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def defaultProfile(var_dict):
	x="query defaultProfile {{  defaultProfile(request:         {{        {var_dict}}}        ) {{    ...ProfileFields  }}}}".format(var_dict=var_dict)
	return x

def profile(var_dict):
	x="query profile {{  profile(request:         {{        {var_dict}}}        ) {{    ...ProfileFields  }}}}".format(var_dict=var_dict)
	return x

def profiles(var_dict):
	x="query profiles {{  profiles(request:         {{        {var_dict}}}        ) {{    items {{      ...ProfileFields    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def publication(var_dict):
	x="query publication {{  publication(request:         {{        {var_dict}}}        ) {{    __typename    ... on Post {{      ...PostFields    }}    ... on Comment {{      ...CommentFields    }}    ... on Mirror {{      ...MirrorFields    }}  }}}}".format(var_dict=var_dict)
	return x

def publications(var_dict):
	x="query publications {{  publications(request:         {{        {var_dict}}}        ) {{    items {{      __typename      ... on Post {{        ...PostFields      }}      ... on Comment {{        ...CommentFields      }}      ... on Mirror {{        ...MirrorFields      }}    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def nfts(var_dict):
	x="query nfts {{  nfts(request:         {{        {var_dict}}}        ) {{    items {{      contractName      contractAddress      symbol      tokenId      owners {{        amount        address      }}      name      description      contentURI      originalContent {{        uri        metaType      }}      chainId      collectionName      ercType    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def globalProtocolStatsuery(var_dict):
	x="query globalProtocolStatsuery globalProtocolStats(        {{        {var_dict}}}        : GlobalProtocolStatsRequest) {{  globalProtocolStats(request:         {{        {var_dict}}}        ) {{    totalProfiles    totalBurntProfiles    totalPosts    totalMirrors    totalComments    totalCollects    totalFollows    totalRevenue {{      asset {{        name        symbol        decimals        address      }}      value    }}  }}}}".format(var_dict=var_dict)
	return x

def hasTxHashBeenIndexed(var_dict):
	x="query hasTxHashBeenIndexed {{  hasTxHashBeenIndexed(request:         {{        {var_dict}}}        ) {{    __typename    ... on TransactionIndexedResult {{      indexed      txReceipt {{        ...TxReceiptFields      }}      metadataStatus {{        status        reason      }}    }}    ... on TransactionError {{      reason      txReceipt {{        ...TxReceiptFields      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def hidePublication(var_dict):
	x="mutation hidePublication {{  hidePublication(request:         {{        {var_dict}}}        )}}".format(var_dict=var_dict)
	return x

def createMirrorTypedData(var_dict):
	x="mutation createMirrorTypedData {{  createMirrorTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      types {{        MirrorWithSig {{          name          type        }}      }}      domain {{        name        chainId        version        verifyingContract      }}      value {{        nonce        deadline        profileId        profileIdPointed        pubIdPointed        referenceModuleData        referenceModule        referenceModuleInitData      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def MutualFollowersProfiles(var_dict):
	x="query MutualFollowersProfiles {{  mutualFollowersProfiles(request:         {{        {var_dict}}}        ) {{    items {{      ...ProfileFields    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def nftOwnershipChallenge(var_dict):
	x="query nftOwnershipChallenge {{  nftOwnershipChallenge(request:         {{        {var_dict}}}        ) {{    id    text  }}}}".format(var_dict=var_dict)
	return x

def pendingApprovalFollows(var_dict):
	x="query pendingApprovalFollows {{  pendingApprovalFollows(request:         {{        {var_dict}}}        ) {{    items {{      ...ProfileFields    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def createPostTypedData(var_dict):
	x="mutation createPostTypedData {{  createPostTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      types {{        PostWithSig {{          name          type        }}      }}      domain {{        name        chainId        version        verifyingContract      }}      value {{        nonce        deadline        profileId        contentURI        collectModule        collectModuleInitData        referenceModule        referenceModuleInitData      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def ProfileFeed(var_dict):
	x="query ProfileFeed {{  feed(request:         {{        {var_dict}}}        ) {{    items {{      root {{        __typename        ... on Post {{          ...PostFields        }}        ... on Comment {{          ...CommentFields        }}      }}      electedMirror {{        mirrorId        profile {{          id          handle        }}        timestamp      }}      mirrors {{        profile {{          id          handle        }}        timestamp      }}      collects {{        profile {{          id          handle        }}        timestamp      }}      reactions {{        profile {{          id          handle        }}        reaction        timestamp      }}      comments {{        ...CommentFields      }}    }}    pageInfo {{      prev      next      totalCount    }}  }}}}".format(var_dict=var_dict)
	return x

def ProfileFollowRevenue(var_dict):
	x="query ProfileFollowRevenue {{  profileFollowRevenue(request:         {{        {var_dict}}}        ) {{    revenues {{      total {{        asset {{          name          symbol          decimals          address        }}        value      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def ProfilePublicationRevenue(var_dict):
	x="query ProfilePublicationRevenue {{  profilePublicationRevenue(request:         {{        {var_dict}}}        ) {{    items {{      publication {{        __typename        ... on Post {{          ...PostFields        }}        ... on Comment {{          ...CommentFields        }}        ... on Mirror {{          ...MirrorFields        }}      }}      revenue {{        total {{          asset {{            name            symbol            decimals            address          }}          value        }}      }}    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def ProfilePublicationsForSale(var_dict):
	x="query ProfilePublicationsForSale {{  profilePublicationsForSale(request:         {{        {var_dict}}}        ) {{    items {{      __typename      ... on Post {{        ...PostFields      }}      ... on Comment {{        ...CommentFields      }}    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def ProxyAction(var_dict):
	x="mutation ProxyAction {{  proxyAction(request:         {{        {var_dict}}}        )}}".format(var_dict=var_dict)
	return x

def PublicationRevenue(var_dict):
	x="query PublicationRevenue {{  publicationRevenue(request:         {{        {var_dict}}}        ) {{    publication {{      __typename      ... on Post {{        ...PostFields      }}      ... on Comment {{        ...CommentFields      }}      ... on Mirror {{        ...MirrorFields      }}    }}    revenue {{      total {{        asset {{          name          symbol          decimals          address        }}        value      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def Refresh(var_dict):
	x="mutation Refresh {{  refresh(request:         {{        {var_dict}}}        ) {{    accessToken    refreshToken  }}}}".format(var_dict=var_dict)
	return x

def removeReaction(var_dict):
	x="mutation removeReaction {{  removeReaction(request:         {{        {var_dict}}}        )}}".format(var_dict=var_dict)
	return x

def reportPublication(var_dict):
	x="mutation reportPublication {{  reportPublication(request:         {{        {var_dict}}}        )}}".format(var_dict=var_dict)
	return x

def SearchProfiles(var_dict):
	x="query SearchProfiles {{  search(request:         {{        {var_dict}}}        ) {{    ... on ProfileSearchResult {{      __typename      items {{        ... on Profile {{          ...ProfileFields        }}      }}      pageInfo {{        ...CommonPaginatedResultInfoFields      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def SearchPublications(var_dict):
	x="query SearchPublications {{  search(request:         {{        {var_dict}}}        ) {{    ... on PublicationSearchResult {{      __typename      items {{        __typename        ... on Comment {{          ...CommentFields        }}        ... on Post {{          ...PostFields        }}      }}      pageInfo {{        ...CommonPaginatedResultInfoFields      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def createSetDefaultProfileTypedData(var_dict):
	x="mutation createSetDefaultProfileTypedData {{  createSetDefaultProfileTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      types {{        SetDefaultProfileWithSig {{          name          type        }}      }}      domain {{        name        chainId        version        verifyingContract      }}      value {{        nonce        deadline        wallet        profileId      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def createSetFollowModuleTypedData(var_dict):
	x="mutation createSetFollowModuleTypedData {{  createSetFollowModuleTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      types {{        SetFollowModuleWithSig {{          name          type        }}      }}      domain {{        name        chainId        version        verifyingContract      }}      value {{        nonce        deadline        profileId        followModule        followModuleInitData      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def createSetFollowNFTUriTypedData(var_dict):
	x="mutation createSetFollowNFTUriTypedData {{  createSetFollowNFTUriTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      types {{        SetFollowNFTURIWithSig {{          name          type        }}      }}      domain {{        name        chainId        version        verifyingContract      }}      value {{        nonce        profileId        deadline        followNFTURI      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def createSetProfileImageURITypedData(var_dict):
	x="mutation createSetProfileImageURITypedData {{  createSetProfileImageURITypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      domain {{        name        chainId        version        verifyingContract      }}      types {{        SetProfileImageURIWithSig {{          name          type        }}      }}      value {{        nonce        deadline        imageURI        profileId      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def createSetProfileImageURITypedData(var_dict):
	x="mutation createSetProfileImageURITypedData {{  createSetProfileImageURITypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      domain {{        name        chainId        version        verifyingContract      }}      types {{        SetProfileImageURIWithSig {{          name          type        }}      }}      value {{        nonce        deadline        imageURI        profileId      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def createSetProfileMetadataTypedData(var_dict):
	x="mutation createSetProfileMetadataTypedData {{  createSetProfileMetadataTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      types {{        SetProfileMetadataURIWithSig {{          name          type        }}      }}      domain {{        name        chainId        version        verifyingContract      }}      value {{        nonce        deadline        profileId        metadata      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def timeline(var_dict):
	x="query timeline {{  timeline(request:         {{        {var_dict}}}        ) {{    items {{      __typename      ... on Post {{        ...PostFields      }}      ... on Comment {{        ...CommentFields      }}      ... on Mirror {{        ...MirrorFields      }}    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def createToggleFollowTypedData(var_dict):
	x="mutation createToggleFollowTypedData {{  createToggleFollowTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      domain {{        name        chainId        version        verifyingContract      }}      types {{        ToggleFollowWithSig {{          name          type        }}      }}      value {{        nonce        deadline        profileIds        enables      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def createUnfollowTypedData(var_dict):
	x="mutation createUnfollowTypedData {{  createUnfollowTypedData(request:         {{        {var_dict}}}        ) {{    id    expiresAt    typedData {{      domain {{        name        chainId        version        verifyingContract      }}      types {{        BurnWithSig {{          name          type        }}      }}      value {{        nonce        deadline        tokenId      }}    }}  }}}}".format(var_dict=var_dict)
	return x

def notifications(var_dict):
	x="query notifications {{  notifications(request:         {{        {var_dict}}}        ) {{    items {{      ... on NewFollowerNotification {{        notificationId        ...NewFollowerNotificationFields      }}      ... on NewMirrorNotification {{        notificationId        ...NewMirrorNotificationFields      }}      ... on NewCollectNotification {{        notificationId        ...NewCollectNotificationFields      }}      ... on NewCommentNotification {{        notificationId        ...NewCommentNotificationFields      }}      ... on NewMentionNotification {{        notificationId        ...NewMentionNotificationFields      }}      ... on NewReactionNotification {{        notificationId        ...NewReactionNotificationFields      }}    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}fragment CommentWithCommentedPublicationFields on Comment {{  ...CommentFields  commentOn {{    ... on Post {{      ...PostFields    }}    ... on Mirror {{      ...MirrorFields    }}    ... on Comment {{      ...CommentFields    }}  }}}}fragment NewFollowerNotificationFields on NewFollowerNotification {{  __typename  createdAt  isFollowedByMe  wallet {{    ...WalletFields  }}}}fragment NewCollectNotificationFields on NewCollectNotification {{  __typename  createdAt  wallet {{    ...WalletFields  }}  collectedPublication {{    __typename    ... on Post {{      ...PostFields    }}    ... on Mirror {{      ...MirrorFields    }}    ... on Comment {{      ...CommentFields    }}  }}}}fragment NewMirrorNotificationFields on NewMirrorNotification {{  __typename  createdAt  profile {{    ...ProfileFields  }}  publication {{    ... on Post {{      ...PostFields    }}    ... on Comment {{      ...CommentFields    }}  }}}}fragment NewCommentNotificationFields on NewCommentNotification {{  __typename  createdAt  profile {{    ...ProfileFields  }}  comment {{    ...CommentWithCommentedPublicationFields  }}}}fragment NewMentionNotificationFields on NewMentionNotification {{  __typename  mentionPublication {{    ... on Post {{      ...PostFields    }}    ... on Comment {{      ...CommentFields    }}  }}  createdAt}}fragment NewReactionNotificationFields on NewReactionNotification {{  __typename  createdAt  profile {{    ...ProfileFields  }}  reaction  publication {{    ... on Post {{      ...PostFields    }}    ... on Mirror {{      ...MirrorFields    }}    ... on Comment {{      ...CommentFields    }}  }}}}".format(var_dict=var_dict)
	return x

def verify(var_dict):
	x="query verify {{  verify(request:         {{        {var_dict}}}        )}}".format(var_dict=var_dict)
	return x

def whoCollectedPublication(var_dict):
	x="query whoCollectedPublication {{  whoCollectedPublication(request:         {{        {var_dict}}}        ) {{    items {{      ...WalletFields    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

def WhoReactedPublication(var_dict):
	x="query WhoReactedPublication {{  whoReactedPublication(request:         {{        {var_dict}}}        ) {{    items {{      reactionId      reaction      reactionAt      profile {{        ...ProfileFields      }}    }}    pageInfo {{      ...CommonPaginatedResultInfoFields    }}  }}}}".format(var_dict=var_dict)
	return x

