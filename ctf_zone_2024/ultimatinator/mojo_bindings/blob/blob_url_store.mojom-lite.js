// third_party/blink/public/mojom/blob/blob_url_store.mojom-lite.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2018 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
/**
 * @fileoverview
 * @suppress {missingRequire}
 */
'use strict';


mojo.internal.exportModule('blink.mojom');








/**
 * @implements {mojo.internal.interfaceSupport.PendingReceiver}
 * @export
 */
blink.mojom.BlobURLStorePendingReceiver = class {
  /**
   * @param {!MojoHandle|!mojo.internal.interfaceSupport.Endpoint} handle
   */
  constructor(handle) {
    /** @public {!mojo.internal.interfaceSupport.Endpoint} */
    this.handle = mojo.internal.interfaceSupport.getEndpointForReceiver(handle);
  }

  /** @param {string=} scope */
  bindInBrowser(scope = 'context') {
    mojo.internal.interfaceSupport.bind(
        this.handle,
        blink.mojom.BlobURLStore.$interfaceName,
        scope);
  }
};



/**
 * @export
 * @implements { blink.mojom.BlobURLStoreInterface }
 */
blink.mojom.BlobURLStoreRemote = class {
  /** @param {MojoHandle|mojo.internal.interfaceSupport.Endpoint=} handle */
  constructor(handle = undefined) {
    /**
     * @private {!mojo.internal.interfaceSupport.InterfaceRemoteBase<!blink.mojom.BlobURLStorePendingReceiver>}
     */
    this.proxy =
        new mojo.internal.interfaceSupport.InterfaceRemoteBase(
          blink.mojom.BlobURLStorePendingReceiver,
          handle);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceRemoteBaseWrapper<!blink.mojom.BlobURLStorePendingReceiver>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceRemoteBaseWrapper(this.proxy);

    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.proxy.getConnectionErrorEventRouter();
  }

  
  /**
   * @param { !blink.mojom.BlobRemote } blob
   * @param { !url.mojom.Url } url
   * @param { !mojoBase.mojom.UnguessableToken } unsafeAgentClusterId
   * @param { ?network.mojom.SchemefulSite } unsafeTopLevelSite
   * @return {!Promise}
   */

  register(
      blob,
      url,
      unsafeAgentClusterId,
      unsafeTopLevelSite) {
    return this.proxy.sendMessage(
        0,
        blink.mojom.BlobURLStore_Register_ParamsSpec.$,
        blink.mojom.BlobURLStore_Register_ResponseParamsSpec.$,
        [
          blob,
          url,
          unsafeAgentClusterId,
          unsafeTopLevelSite
        ]);
  }

  
  /**
   * @param { !url.mojom.Url } url
   */

  revoke(
      url) {
    this.proxy.sendMessage(
        1,
        blink.mojom.BlobURLStore_Revoke_ParamsSpec.$,
        null,
        [
          url
        ]);
  }

  
  /**
   * @param { !url.mojom.Url } url
   * @param { !network.mojom.URLLoaderFactoryPendingReceiver } factory
   * @return {!Promise<{
        unsafeAgentClusterId: ?mojoBase.mojom.UnguessableToken,
        unsafeTopLevelSite: ?network.mojom.SchemefulSite,
   *  }>}
   */

  resolveAsURLLoaderFactory(
      url,
      factory) {
    return this.proxy.sendMessage(
        2,
        blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_ParamsSpec.$,
        blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_ResponseParamsSpec.$,
        [
          url,
          factory
        ]);
  }

  
  /**
   * @param { !url.mojom.Url } url
   * @param { !blink.mojom.BlobURLTokenPendingReceiver } token
   * @return {!Promise<{
        unsafeAgentClusterId: ?mojoBase.mojom.UnguessableToken,
   *  }>}
   */

  resolveForNavigation(
      url,
      token) {
    return this.proxy.sendMessage(
        3,
        blink.mojom.BlobURLStore_ResolveForNavigation_ParamsSpec.$,
        blink.mojom.BlobURLStore_ResolveForNavigation_ResponseParamsSpec.$,
        [
          url,
          token
        ]);
  }
};

/**
 * An object which receives request messages for the BlobURLStore
 * mojom interface. Must be constructed over an object which implements that
 * interface.
 *
 * @export
 */
blink.mojom.BlobURLStoreReceiver = class {
  /**
   * @param {!blink.mojom.BlobURLStoreInterface } impl
   */
  constructor(impl) {
    /** @private {!mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal<!blink.mojom.BlobURLStoreRemote>} */
    this.helper_internal_ = new mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal(
        blink.mojom.BlobURLStoreRemote);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceReceiverHelper<!blink.mojom.BlobURLStoreRemote>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceReceiverHelper(this.helper_internal_);


    this.helper_internal_.registerHandler(
        0,
        blink.mojom.BlobURLStore_Register_ParamsSpec.$,
        blink.mojom.BlobURLStore_Register_ResponseParamsSpec.$,
        impl.register.bind(impl));
    this.helper_internal_.registerHandler(
        1,
        blink.mojom.BlobURLStore_Revoke_ParamsSpec.$,
        null,
        impl.revoke.bind(impl));
    this.helper_internal_.registerHandler(
        2,
        blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_ParamsSpec.$,
        blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_ResponseParamsSpec.$,
        impl.resolveAsURLLoaderFactory.bind(impl));
    this.helper_internal_.registerHandler(
        3,
        blink.mojom.BlobURLStore_ResolveForNavigation_ParamsSpec.$,
        blink.mojom.BlobURLStore_ResolveForNavigation_ResponseParamsSpec.$,
        impl.resolveForNavigation.bind(impl));
    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.helper_internal_.getConnectionErrorEventRouter();
  }
};

/**
 *  @export
 */
blink.mojom.BlobURLStore = class {
  /**
   * @return {!string}
   */
  static get $interfaceName() {
    return "blink.mojom.BlobURLStore";
  }

  /**
   * Returns a remote for this interface which sends messages to the browser.
   * The browser must have an interface request binder registered for this
   * interface and accessible to the calling document's frame.
   *
   * @return {!blink.mojom.BlobURLStoreRemote}
   * @export
   */
  static getRemote() {
    let remote = new blink.mojom.BlobURLStoreRemote;
    remote.$.bindNewPipeAndPassReceiver().bindInBrowser();
    return remote;
  }
};


/**
 * An object which receives request messages for the BlobURLStore
 * mojom interface and dispatches them as callbacks. One callback receiver exists
 * on this object for each message defined in the mojom interface, and each
 * receiver can have any number of listeners added to it.
 *
 * @export
 */
blink.mojom.BlobURLStoreCallbackRouter = class {
  constructor() {
    this.helper_internal_ = new mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal(
      blink.mojom.BlobURLStoreRemote);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceReceiverHelper<!blink.mojom.BlobURLStoreRemote>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceReceiverHelper(this.helper_internal_);

    this.router_ = new mojo.internal.interfaceSupport.CallbackRouter;

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.register =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        0,
        blink.mojom.BlobURLStore_Register_ParamsSpec.$,
        blink.mojom.BlobURLStore_Register_ResponseParamsSpec.$,
        this.register.createReceiverHandler(true /* expectsResponse */));
    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.revoke =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        1,
        blink.mojom.BlobURLStore_Revoke_ParamsSpec.$,
        null,
        this.revoke.createReceiverHandler(false /* expectsResponse */));
    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.resolveAsURLLoaderFactory =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        2,
        blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_ParamsSpec.$,
        blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_ResponseParamsSpec.$,
        this.resolveAsURLLoaderFactory.createReceiverHandler(true /* expectsResponse */));
    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.resolveForNavigation =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        3,
        blink.mojom.BlobURLStore_ResolveForNavigation_ParamsSpec.$,
        blink.mojom.BlobURLStore_ResolveForNavigation_ResponseParamsSpec.$,
        this.resolveForNavigation.createReceiverHandler(true /* expectsResponse */));
    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.helper_internal_.getConnectionErrorEventRouter();
  }

  /**
   * @param {number} id An ID returned by a prior call to addListener.
   * @return {boolean} True iff the identified listener was found and removed.
   * @export
   */
  removeListener(id) {
    return this.router_.removeListener(id);
  }
};




/**
 * @implements {mojo.internal.interfaceSupport.PendingReceiver}
 * @export
 */
blink.mojom.BlobURLTokenPendingReceiver = class {
  /**
   * @param {!MojoHandle|!mojo.internal.interfaceSupport.Endpoint} handle
   */
  constructor(handle) {
    /** @public {!mojo.internal.interfaceSupport.Endpoint} */
    this.handle = mojo.internal.interfaceSupport.getEndpointForReceiver(handle);
  }

  /** @param {string=} scope */
  bindInBrowser(scope = 'context') {
    mojo.internal.interfaceSupport.bind(
        this.handle,
        blink.mojom.BlobURLToken.$interfaceName,
        scope);
  }
};



/**
 * @export
 * @implements { blink.mojom.BlobURLTokenInterface }
 */
blink.mojom.BlobURLTokenRemote = class {
  /** @param {MojoHandle|mojo.internal.interfaceSupport.Endpoint=} handle */
  constructor(handle = undefined) {
    /**
     * @private {!mojo.internal.interfaceSupport.InterfaceRemoteBase<!blink.mojom.BlobURLTokenPendingReceiver>}
     */
    this.proxy =
        new mojo.internal.interfaceSupport.InterfaceRemoteBase(
          blink.mojom.BlobURLTokenPendingReceiver,
          handle);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceRemoteBaseWrapper<!blink.mojom.BlobURLTokenPendingReceiver>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceRemoteBaseWrapper(this.proxy);

    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.proxy.getConnectionErrorEventRouter();
  }

  
  /**
   * @param { !blink.mojom.BlobURLTokenPendingReceiver } token
   */

  clone(
      token) {
    this.proxy.sendMessage(
        0,
        blink.mojom.BlobURLToken_Clone_ParamsSpec.$,
        null,
        [
          token
        ]);
  }

  
  /**
   * @return {!Promise<{
        token: !mojoBase.mojom.UnguessableToken,
   *  }>}
   */

  getToken() {
    return this.proxy.sendMessage(
        1,
        blink.mojom.BlobURLToken_GetToken_ParamsSpec.$,
        blink.mojom.BlobURLToken_GetToken_ResponseParamsSpec.$,
        [
        ]);
  }
};

/**
 * An object which receives request messages for the BlobURLToken
 * mojom interface. Must be constructed over an object which implements that
 * interface.
 *
 * @export
 */
blink.mojom.BlobURLTokenReceiver = class {
  /**
   * @param {!blink.mojom.BlobURLTokenInterface } impl
   */
  constructor(impl) {
    /** @private {!mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal<!blink.mojom.BlobURLTokenRemote>} */
    this.helper_internal_ = new mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal(
        blink.mojom.BlobURLTokenRemote);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceReceiverHelper<!blink.mojom.BlobURLTokenRemote>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceReceiverHelper(this.helper_internal_);


    this.helper_internal_.registerHandler(
        0,
        blink.mojom.BlobURLToken_Clone_ParamsSpec.$,
        null,
        impl.clone.bind(impl));
    this.helper_internal_.registerHandler(
        1,
        blink.mojom.BlobURLToken_GetToken_ParamsSpec.$,
        blink.mojom.BlobURLToken_GetToken_ResponseParamsSpec.$,
        impl.getToken.bind(impl));
    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.helper_internal_.getConnectionErrorEventRouter();
  }
};

/**
 *  @export
 */
blink.mojom.BlobURLToken = class {
  /**
   * @return {!string}
   */
  static get $interfaceName() {
    return "blink.mojom.BlobURLToken";
  }

  /**
   * Returns a remote for this interface which sends messages to the browser.
   * The browser must have an interface request binder registered for this
   * interface and accessible to the calling document's frame.
   *
   * @return {!blink.mojom.BlobURLTokenRemote}
   * @export
   */
  static getRemote() {
    let remote = new blink.mojom.BlobURLTokenRemote;
    remote.$.bindNewPipeAndPassReceiver().bindInBrowser();
    return remote;
  }
};


/**
 * An object which receives request messages for the BlobURLToken
 * mojom interface and dispatches them as callbacks. One callback receiver exists
 * on this object for each message defined in the mojom interface, and each
 * receiver can have any number of listeners added to it.
 *
 * @export
 */
blink.mojom.BlobURLTokenCallbackRouter = class {
  constructor() {
    this.helper_internal_ = new mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal(
      blink.mojom.BlobURLTokenRemote);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceReceiverHelper<!blink.mojom.BlobURLTokenRemote>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceReceiverHelper(this.helper_internal_);

    this.router_ = new mojo.internal.interfaceSupport.CallbackRouter;

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.clone =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        0,
        blink.mojom.BlobURLToken_Clone_ParamsSpec.$,
        null,
        this.clone.createReceiverHandler(false /* expectsResponse */));
    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.getToken =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        1,
        blink.mojom.BlobURLToken_GetToken_ParamsSpec.$,
        blink.mojom.BlobURLToken_GetToken_ResponseParamsSpec.$,
        this.getToken.createReceiverHandler(true /* expectsResponse */));
    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.helper_internal_.getConnectionErrorEventRouter();
  }

  /**
   * @param {number} id An ID returned by a prior call to addListener.
   * @return {boolean} True iff the identified listener was found and removed.
   * @export
   */
  removeListener(id) {
    return this.router_.removeListener(id);
  }
};



/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobURLStore_Register_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobURLStore_Register_ResponseParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobURLStore_Revoke_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_ResponseParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobURLStore_ResolveForNavigation_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobURLStore_ResolveForNavigation_ResponseParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobURLToken_Clone_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobURLToken_GetToken_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobURLToken_GetToken_ResponseParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };




mojo.internal.Struct(
    blink.mojom.BlobURLStore_Register_ParamsSpec.$,
    'BlobURLStore_Register_Params',
    [
      mojo.internal.StructField(
        'blob', 0,
        0,
        mojo.internal.InterfaceProxy(blink.mojom.BlobRemote),
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'url', 8,
        0,
        url.mojom.UrlSpec.$,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'unsafeAgentClusterId', 16,
        0,
        mojoBase.mojom.UnguessableTokenSpec.$,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'unsafeTopLevelSite', 24,
        0,
        network.mojom.SchemefulSiteSpec.$,
        null,
        true, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 40],]);





/** @record */
blink.mojom.BlobURLStore_Register_Params = class {
  constructor() {
    /** @export { !blink.mojom.BlobRemote } */
    this.blob;
    /** @export { !url.mojom.Url } */
    this.url;
    /** @export { !mojoBase.mojom.UnguessableToken } */
    this.unsafeAgentClusterId;
    /** @export { (network.mojom.SchemefulSite|undefined) } */
    this.unsafeTopLevelSite;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobURLStore_Register_ResponseParamsSpec.$,
    'BlobURLStore_Register_ResponseParams',
    [
    ],
    [[0, 8],]);





/** @record */
blink.mojom.BlobURLStore_Register_ResponseParams = class {
  constructor() {
  }
};



mojo.internal.Struct(
    blink.mojom.BlobURLStore_Revoke_ParamsSpec.$,
    'BlobURLStore_Revoke_Params',
    [
      mojo.internal.StructField(
        'url', 0,
        0,
        url.mojom.UrlSpec.$,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 16],]);





/** @record */
blink.mojom.BlobURLStore_Revoke_Params = class {
  constructor() {
    /** @export { !url.mojom.Url } */
    this.url;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_ParamsSpec.$,
    'BlobURLStore_ResolveAsURLLoaderFactory_Params',
    [
      mojo.internal.StructField(
        'url', 0,
        0,
        url.mojom.UrlSpec.$,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'factory', 8,
        0,
        mojo.internal.InterfaceRequest(network.mojom.URLLoaderFactoryPendingReceiver),
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 24],]);





/** @record */
blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_Params = class {
  constructor() {
    /** @export { !url.mojom.Url } */
    this.url;
    /** @export { !network.mojom.URLLoaderFactoryPendingReceiver } */
    this.factory;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_ResponseParamsSpec.$,
    'BlobURLStore_ResolveAsURLLoaderFactory_ResponseParams',
    [
      mojo.internal.StructField(
        'unsafeAgentClusterId', 0,
        0,
        mojoBase.mojom.UnguessableTokenSpec.$,
        null,
        true, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'unsafeTopLevelSite', 8,
        0,
        network.mojom.SchemefulSiteSpec.$,
        null,
        true, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 24],]);





/** @record */
blink.mojom.BlobURLStore_ResolveAsURLLoaderFactory_ResponseParams = class {
  constructor() {
    /** @export { (mojoBase.mojom.UnguessableToken|undefined) } */
    this.unsafeAgentClusterId;
    /** @export { (network.mojom.SchemefulSite|undefined) } */
    this.unsafeTopLevelSite;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobURLStore_ResolveForNavigation_ParamsSpec.$,
    'BlobURLStore_ResolveForNavigation_Params',
    [
      mojo.internal.StructField(
        'url', 0,
        0,
        url.mojom.UrlSpec.$,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'token', 8,
        0,
        mojo.internal.InterfaceRequest(blink.mojom.BlobURLTokenPendingReceiver),
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 24],]);





/** @record */
blink.mojom.BlobURLStore_ResolveForNavigation_Params = class {
  constructor() {
    /** @export { !url.mojom.Url } */
    this.url;
    /** @export { !blink.mojom.BlobURLTokenPendingReceiver } */
    this.token;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobURLStore_ResolveForNavigation_ResponseParamsSpec.$,
    'BlobURLStore_ResolveForNavigation_ResponseParams',
    [
      mojo.internal.StructField(
        'unsafeAgentClusterId', 0,
        0,
        mojoBase.mojom.UnguessableTokenSpec.$,
        null,
        true, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 16],]);





/** @record */
blink.mojom.BlobURLStore_ResolveForNavigation_ResponseParams = class {
  constructor() {
    /** @export { (mojoBase.mojom.UnguessableToken|undefined) } */
    this.unsafeAgentClusterId;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobURLToken_Clone_ParamsSpec.$,
    'BlobURLToken_Clone_Params',
    [
      mojo.internal.StructField(
        'token', 0,
        0,
        mojo.internal.InterfaceRequest(blink.mojom.BlobURLTokenPendingReceiver),
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 16],]);





/** @record */
blink.mojom.BlobURLToken_Clone_Params = class {
  constructor() {
    /** @export { !blink.mojom.BlobURLTokenPendingReceiver } */
    this.token;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobURLToken_GetToken_ParamsSpec.$,
    'BlobURLToken_GetToken_Params',
    [
    ],
    [[0, 8],]);





/** @record */
blink.mojom.BlobURLToken_GetToken_Params = class {
  constructor() {
  }
};



mojo.internal.Struct(
    blink.mojom.BlobURLToken_GetToken_ResponseParamsSpec.$,
    'BlobURLToken_GetToken_ResponseParams',
    [
      mojo.internal.StructField(
        'token', 0,
        0,
        mojoBase.mojom.UnguessableTokenSpec.$,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 16],]);





/** @record */
blink.mojom.BlobURLToken_GetToken_ResponseParams = class {
  constructor() {
    /** @export { !mojoBase.mojom.UnguessableToken } */
    this.token;
  }
};
