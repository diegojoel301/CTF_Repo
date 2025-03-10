// third_party/blink/public/mojom/blob/blob_registry.mojom-lite.js is auto generated by mojom_bindings_generator.py, do not edit

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
blink.mojom.ProgressClientPendingReceiver = class {
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
        blink.mojom.ProgressClient.$interfaceName,
        scope);
  }
};



/**
 * @export
 * @implements { blink.mojom.ProgressClientInterface }
 */
blink.mojom.ProgressClientRemote = class {
  /** @param {MojoHandle|mojo.internal.interfaceSupport.Endpoint=} handle */
  constructor(handle = undefined) {
    /**
     * @private {!mojo.internal.interfaceSupport.InterfaceRemoteBase<!blink.mojom.ProgressClientPendingReceiver>}
     */
    this.proxy =
        new mojo.internal.interfaceSupport.InterfaceRemoteBase(
          blink.mojom.ProgressClientPendingReceiver,
          handle);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceRemoteBaseWrapper<!blink.mojom.ProgressClientPendingReceiver>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceRemoteBaseWrapper(this.proxy);

    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.proxy.getConnectionErrorEventRouter();
  }

  
  /**
   * @param { !bigint } delta
   */

  onProgress(
      delta) {
    this.proxy.sendMessage(
        0,
        blink.mojom.ProgressClient_OnProgress_ParamsSpec.$,
        null,
        [
          delta
        ]);
  }
};

/**
 * An object which receives request messages for the ProgressClient
 * mojom interface. Must be constructed over an object which implements that
 * interface.
 *
 * @export
 */
blink.mojom.ProgressClientReceiver = class {
  /**
   * @param {!blink.mojom.ProgressClientInterface } impl
   */
  constructor(impl) {
    /** @private {!mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal<!blink.mojom.ProgressClientRemote>} */
    this.helper_internal_ = new mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal(
        blink.mojom.ProgressClientRemote);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceReceiverHelper<!blink.mojom.ProgressClientRemote>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceReceiverHelper(this.helper_internal_);


    this.helper_internal_.registerHandler(
        0,
        blink.mojom.ProgressClient_OnProgress_ParamsSpec.$,
        null,
        impl.onProgress.bind(impl));
    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.helper_internal_.getConnectionErrorEventRouter();
  }
};

/**
 *  @export
 */
blink.mojom.ProgressClient = class {
  /**
   * @return {!string}
   */
  static get $interfaceName() {
    return "blink.mojom.ProgressClient";
  }

  /**
   * Returns a remote for this interface which sends messages to the browser.
   * The browser must have an interface request binder registered for this
   * interface and accessible to the calling document's frame.
   *
   * @return {!blink.mojom.ProgressClientRemote}
   * @export
   */
  static getRemote() {
    let remote = new blink.mojom.ProgressClientRemote;
    remote.$.bindNewPipeAndPassReceiver().bindInBrowser();
    return remote;
  }
};


/**
 * An object which receives request messages for the ProgressClient
 * mojom interface and dispatches them as callbacks. One callback receiver exists
 * on this object for each message defined in the mojom interface, and each
 * receiver can have any number of listeners added to it.
 *
 * @export
 */
blink.mojom.ProgressClientCallbackRouter = class {
  constructor() {
    this.helper_internal_ = new mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal(
      blink.mojom.ProgressClientRemote);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceReceiverHelper<!blink.mojom.ProgressClientRemote>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceReceiverHelper(this.helper_internal_);

    this.router_ = new mojo.internal.interfaceSupport.CallbackRouter;

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.onProgress =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        0,
        blink.mojom.ProgressClient_OnProgress_ParamsSpec.$,
        null,
        this.onProgress.createReceiverHandler(false /* expectsResponse */));
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
blink.mojom.BlobRegistryPendingReceiver = class {
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
        blink.mojom.BlobRegistry.$interfaceName,
        scope);
  }
};



/**
 * @export
 * @implements { blink.mojom.BlobRegistryInterface }
 */
blink.mojom.BlobRegistryRemote = class {
  /** @param {MojoHandle|mojo.internal.interfaceSupport.Endpoint=} handle */
  constructor(handle = undefined) {
    /**
     * @private {!mojo.internal.interfaceSupport.InterfaceRemoteBase<!blink.mojom.BlobRegistryPendingReceiver>}
     */
    this.proxy =
        new mojo.internal.interfaceSupport.InterfaceRemoteBase(
          blink.mojom.BlobRegistryPendingReceiver,
          handle);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceRemoteBaseWrapper<!blink.mojom.BlobRegistryPendingReceiver>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceRemoteBaseWrapper(this.proxy);

    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.proxy.getConnectionErrorEventRouter();
  }

  
  /**
   * @param { !blink.mojom.BlobPendingReceiver } blob
   * @param { !string } uuid
   * @param { !string } contentType
   * @param { !string } contentDisposition
   * @param { !Array<!blink.mojom.DataElement> } elements
   * @return {!Promise}
   */

  register(
      blob,
      uuid,
      contentType,
      contentDisposition,
      elements) {
    return this.proxy.sendMessage(
        0,
        blink.mojom.BlobRegistry_Register_ParamsSpec.$,
        blink.mojom.BlobRegistry_Register_ResponseParamsSpec.$,
        [
          blob,
          uuid,
          contentType,
          contentDisposition,
          elements
        ]);
  }

  
  /**
   * @param { !string } contentType
   * @param { !string } contentDisposition
   * @param { !bigint } lengthHint
   * @param { !MojoHandle } data
   * @param { ?Object } progressClient
   * @return {!Promise<{
        blob: ?blink.mojom.SerializedBlob,
   *  }>}
   */

  registerFromStream(
      contentType,
      contentDisposition,
      lengthHint,
      data,
      progressClient) {
    return this.proxy.sendMessage(
        1,
        blink.mojom.BlobRegistry_RegisterFromStream_ParamsSpec.$,
        blink.mojom.BlobRegistry_RegisterFromStream_ResponseParamsSpec.$,
        [
          contentType,
          contentDisposition,
          lengthHint,
          data,
          progressClient
        ]);
  }

  
  /**
   * @param { !blink.mojom.BlobPendingReceiver } blob
   * @param { !string } uuid
   * @return {!Promise}
   */

  getBlobFromUUID(
      blob,
      uuid) {
    return this.proxy.sendMessage(
        2,
        blink.mojom.BlobRegistry_GetBlobFromUUID_ParamsSpec.$,
        blink.mojom.BlobRegistry_GetBlobFromUUID_ResponseParamsSpec.$,
        [
          blob,
          uuid
        ]);
  }
};

/**
 * An object which receives request messages for the BlobRegistry
 * mojom interface. Must be constructed over an object which implements that
 * interface.
 *
 * @export
 */
blink.mojom.BlobRegistryReceiver = class {
  /**
   * @param {!blink.mojom.BlobRegistryInterface } impl
   */
  constructor(impl) {
    /** @private {!mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal<!blink.mojom.BlobRegistryRemote>} */
    this.helper_internal_ = new mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal(
        blink.mojom.BlobRegistryRemote);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceReceiverHelper<!blink.mojom.BlobRegistryRemote>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceReceiverHelper(this.helper_internal_);


    this.helper_internal_.registerHandler(
        0,
        blink.mojom.BlobRegistry_Register_ParamsSpec.$,
        blink.mojom.BlobRegistry_Register_ResponseParamsSpec.$,
        impl.register.bind(impl));
    this.helper_internal_.registerHandler(
        1,
        blink.mojom.BlobRegistry_RegisterFromStream_ParamsSpec.$,
        blink.mojom.BlobRegistry_RegisterFromStream_ResponseParamsSpec.$,
        impl.registerFromStream.bind(impl));
    this.helper_internal_.registerHandler(
        2,
        blink.mojom.BlobRegistry_GetBlobFromUUID_ParamsSpec.$,
        blink.mojom.BlobRegistry_GetBlobFromUUID_ResponseParamsSpec.$,
        impl.getBlobFromUUID.bind(impl));
    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.helper_internal_.getConnectionErrorEventRouter();
  }
};

/**
 *  @export
 */
blink.mojom.BlobRegistry = class {
  /**
   * @return {!string}
   */
  static get $interfaceName() {
    return "blink.mojom.BlobRegistry";
  }

  /**
   * Returns a remote for this interface which sends messages to the browser.
   * The browser must have an interface request binder registered for this
   * interface and accessible to the calling document's frame.
   *
   * @return {!blink.mojom.BlobRegistryRemote}
   * @export
   */
  static getRemote() {
    let remote = new blink.mojom.BlobRegistryRemote;
    remote.$.bindNewPipeAndPassReceiver().bindInBrowser();
    return remote;
  }
};


/**
 * An object which receives request messages for the BlobRegistry
 * mojom interface and dispatches them as callbacks. One callback receiver exists
 * on this object for each message defined in the mojom interface, and each
 * receiver can have any number of listeners added to it.
 *
 * @export
 */
blink.mojom.BlobRegistryCallbackRouter = class {
  constructor() {
    this.helper_internal_ = new mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal(
      blink.mojom.BlobRegistryRemote);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceReceiverHelper<!blink.mojom.BlobRegistryRemote>}
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
        blink.mojom.BlobRegistry_Register_ParamsSpec.$,
        blink.mojom.BlobRegistry_Register_ResponseParamsSpec.$,
        this.register.createReceiverHandler(true /* expectsResponse */));
    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.registerFromStream =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        1,
        blink.mojom.BlobRegistry_RegisterFromStream_ParamsSpec.$,
        blink.mojom.BlobRegistry_RegisterFromStream_ResponseParamsSpec.$,
        this.registerFromStream.createReceiverHandler(true /* expectsResponse */));
    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.getBlobFromUUID =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        2,
        blink.mojom.BlobRegistry_GetBlobFromUUID_ParamsSpec.$,
        blink.mojom.BlobRegistry_GetBlobFromUUID_ResponseParamsSpec.$,
        this.getBlobFromUUID.createReceiverHandler(true /* expectsResponse */));
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
blink.mojom.ProgressClient_OnProgress_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobRegistry_Register_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobRegistry_Register_ResponseParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobRegistry_RegisterFromStream_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobRegistry_RegisterFromStream_ResponseParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobRegistry_GetBlobFromUUID_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BlobRegistry_GetBlobFromUUID_ResponseParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };




mojo.internal.Struct(
    blink.mojom.ProgressClient_OnProgress_ParamsSpec.$,
    'ProgressClient_OnProgress_Params',
    [
      mojo.internal.StructField(
        'delta', 0,
        0,
        mojo.internal.Uint64,
        BigInt(0),
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 16],]);





/** @record */
blink.mojom.ProgressClient_OnProgress_Params = class {
  constructor() {
    /** @export { !bigint } */
    this.delta;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobRegistry_Register_ParamsSpec.$,
    'BlobRegistry_Register_Params',
    [
      mojo.internal.StructField(
        'blob', 0,
        0,
        mojo.internal.InterfaceRequest(blink.mojom.BlobPendingReceiver),
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'uuid', 8,
        0,
        mojo.internal.String,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'contentType', 16,
        0,
        mojo.internal.String,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'contentDisposition', 24,
        0,
        mojo.internal.String,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'elements', 32,
        0,
        mojo.internal.Array(blink.mojom.DataElementSpec.$, false),
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 48],]);





/** @record */
blink.mojom.BlobRegistry_Register_Params = class {
  constructor() {
    /** @export { !blink.mojom.BlobPendingReceiver } */
    this.blob;
    /** @export { !string } */
    this.uuid;
    /** @export { !string } */
    this.contentType;
    /** @export { !string } */
    this.contentDisposition;
    /** @export { !Array<!blink.mojom.DataElement> } */
    this.elements;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobRegistry_Register_ResponseParamsSpec.$,
    'BlobRegistry_Register_ResponseParams',
    [
    ],
    [[0, 8],]);





/** @record */
blink.mojom.BlobRegistry_Register_ResponseParams = class {
  constructor() {
  }
};



mojo.internal.Struct(
    blink.mojom.BlobRegistry_RegisterFromStream_ParamsSpec.$,
    'BlobRegistry_RegisterFromStream_Params',
    [
      mojo.internal.StructField(
        'contentType', 0,
        0,
        mojo.internal.String,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'contentDisposition', 8,
        0,
        mojo.internal.String,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'lengthHint', 16,
        0,
        mojo.internal.Uint64,
        BigInt(0),
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'data', 24,
        0,
        mojo.internal.Handle,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'progressClient', 28,
        0,
        mojo.internal.AssociatedInterfaceProxy(blink.mojom.ProgressClientRemote),
        null,
        true, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 48],]);





/** @record */
blink.mojom.BlobRegistry_RegisterFromStream_Params = class {
  constructor() {
    /** @export { !string } */
    this.contentType;
    /** @export { !string } */
    this.contentDisposition;
    /** @export { !bigint } */
    this.lengthHint;
    /** @export { !MojoHandle } */
    this.data;
    /** @export { (Object|undefined) } */
    this.progressClient;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobRegistry_RegisterFromStream_ResponseParamsSpec.$,
    'BlobRegistry_RegisterFromStream_ResponseParams',
    [
      mojo.internal.StructField(
        'blob', 0,
        0,
        blink.mojom.SerializedBlobSpec.$,
        null,
        true, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 16],]);





/** @record */
blink.mojom.BlobRegistry_RegisterFromStream_ResponseParams = class {
  constructor() {
    /** @export { (blink.mojom.SerializedBlob|undefined) } */
    this.blob;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobRegistry_GetBlobFromUUID_ParamsSpec.$,
    'BlobRegistry_GetBlobFromUUID_Params',
    [
      mojo.internal.StructField(
        'blob', 0,
        0,
        mojo.internal.InterfaceRequest(blink.mojom.BlobPendingReceiver),
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'uuid', 8,
        0,
        mojo.internal.String,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 24],]);





/** @record */
blink.mojom.BlobRegistry_GetBlobFromUUID_Params = class {
  constructor() {
    /** @export { !blink.mojom.BlobPendingReceiver } */
    this.blob;
    /** @export { !string } */
    this.uuid;
  }
};



mojo.internal.Struct(
    blink.mojom.BlobRegistry_GetBlobFromUUID_ResponseParamsSpec.$,
    'BlobRegistry_GetBlobFromUUID_ResponseParams',
    [
    ],
    [[0, 8],]);





/** @record */
blink.mojom.BlobRegistry_GetBlobFromUUID_ResponseParams = class {
  constructor() {
  }
};

