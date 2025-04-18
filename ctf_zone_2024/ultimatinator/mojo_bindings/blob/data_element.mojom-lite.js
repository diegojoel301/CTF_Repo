// third_party/blink/public/mojom/blob/data_element.mojom-lite.js is auto generated by mojom_bindings_generator.py, do not edit

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
blink.mojom.BytesProviderPendingReceiver = class {
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
        blink.mojom.BytesProvider.$interfaceName,
        scope);
  }
};



/**
 * @export
 * @implements { blink.mojom.BytesProviderInterface }
 */
blink.mojom.BytesProviderRemote = class {
  /** @param {MojoHandle|mojo.internal.interfaceSupport.Endpoint=} handle */
  constructor(handle = undefined) {
    /**
     * @private {!mojo.internal.interfaceSupport.InterfaceRemoteBase<!blink.mojom.BytesProviderPendingReceiver>}
     */
    this.proxy =
        new mojo.internal.interfaceSupport.InterfaceRemoteBase(
          blink.mojom.BytesProviderPendingReceiver,
          handle);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceRemoteBaseWrapper<!blink.mojom.BytesProviderPendingReceiver>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceRemoteBaseWrapper(this.proxy);

    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.proxy.getConnectionErrorEventRouter();
  }

  
  /**
   * @return {!Promise<{
        data: !Array<!number>,
   *  }>}
   */

  requestAsReply() {
    return this.proxy.sendMessage(
        0,
        blink.mojom.BytesProvider_RequestAsReply_ParamsSpec.$,
        blink.mojom.BytesProvider_RequestAsReply_ResponseParamsSpec.$,
        [
        ]);
  }

  
  /**
   * @param { !MojoHandle } pipe
   */

  requestAsStream(
      pipe) {
    this.proxy.sendMessage(
        1,
        blink.mojom.BytesProvider_RequestAsStream_ParamsSpec.$,
        null,
        [
          pipe
        ]);
  }

  
  /**
   * @param { !bigint } sourceOffset
   * @param { !bigint } sourceSize
   * @param { !mojoBase.mojom.File } file
   * @param { !bigint } fileOffset
   * @return {!Promise<{
        timeFileModified: ?mojoBase.mojom.Time,
   *  }>}
   */

  requestAsFile(
      sourceOffset,
      sourceSize,
      file,
      fileOffset) {
    return this.proxy.sendMessage(
        2,
        blink.mojom.BytesProvider_RequestAsFile_ParamsSpec.$,
        blink.mojom.BytesProvider_RequestAsFile_ResponseParamsSpec.$,
        [
          sourceOffset,
          sourceSize,
          file,
          fileOffset
        ]);
  }
};

/**
 * An object which receives request messages for the BytesProvider
 * mojom interface. Must be constructed over an object which implements that
 * interface.
 *
 * @export
 */
blink.mojom.BytesProviderReceiver = class {
  /**
   * @param {!blink.mojom.BytesProviderInterface } impl
   */
  constructor(impl) {
    /** @private {!mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal<!blink.mojom.BytesProviderRemote>} */
    this.helper_internal_ = new mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal(
        blink.mojom.BytesProviderRemote);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceReceiverHelper<!blink.mojom.BytesProviderRemote>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceReceiverHelper(this.helper_internal_);


    this.helper_internal_.registerHandler(
        0,
        blink.mojom.BytesProvider_RequestAsReply_ParamsSpec.$,
        blink.mojom.BytesProvider_RequestAsReply_ResponseParamsSpec.$,
        impl.requestAsReply.bind(impl));
    this.helper_internal_.registerHandler(
        1,
        blink.mojom.BytesProvider_RequestAsStream_ParamsSpec.$,
        null,
        impl.requestAsStream.bind(impl));
    this.helper_internal_.registerHandler(
        2,
        blink.mojom.BytesProvider_RequestAsFile_ParamsSpec.$,
        blink.mojom.BytesProvider_RequestAsFile_ResponseParamsSpec.$,
        impl.requestAsFile.bind(impl));
    /** @public {!mojo.internal.interfaceSupport.ConnectionErrorEventRouter} */
    this.onConnectionError = this.helper_internal_.getConnectionErrorEventRouter();
  }
};

/**
 *  @export
 */
blink.mojom.BytesProvider = class {
  /**
   * @return {!string}
   */
  static get $interfaceName() {
    return "blink.mojom.BytesProvider";
  }

  /**
   * Returns a remote for this interface which sends messages to the browser.
   * The browser must have an interface request binder registered for this
   * interface and accessible to the calling document's frame.
   *
   * @return {!blink.mojom.BytesProviderRemote}
   * @export
   */
  static getRemote() {
    let remote = new blink.mojom.BytesProviderRemote;
    remote.$.bindNewPipeAndPassReceiver().bindInBrowser();
    return remote;
  }
};


/**
 * An object which receives request messages for the BytesProvider
 * mojom interface and dispatches them as callbacks. One callback receiver exists
 * on this object for each message defined in the mojom interface, and each
 * receiver can have any number of listeners added to it.
 *
 * @export
 */
blink.mojom.BytesProviderCallbackRouter = class {
  constructor() {
    this.helper_internal_ = new mojo.internal.interfaceSupport.InterfaceReceiverHelperInternal(
      blink.mojom.BytesProviderRemote);

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceReceiverHelper<!blink.mojom.BytesProviderRemote>}
     */
    this.$ = new mojo.internal.interfaceSupport.InterfaceReceiverHelper(this.helper_internal_);

    this.router_ = new mojo.internal.interfaceSupport.CallbackRouter;

    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.requestAsReply =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        0,
        blink.mojom.BytesProvider_RequestAsReply_ParamsSpec.$,
        blink.mojom.BytesProvider_RequestAsReply_ResponseParamsSpec.$,
        this.requestAsReply.createReceiverHandler(true /* expectsResponse */));
    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.requestAsStream =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        1,
        blink.mojom.BytesProvider_RequestAsStream_ParamsSpec.$,
        null,
        this.requestAsStream.createReceiverHandler(false /* expectsResponse */));
    /**
     * @public {!mojo.internal.interfaceSupport.InterfaceCallbackReceiver}
     */
    this.requestAsFile =
        new mojo.internal.interfaceSupport.InterfaceCallbackReceiver(
            this.router_);

    this.helper_internal_.registerHandler(
        2,
        blink.mojom.BytesProvider_RequestAsFile_ParamsSpec.$,
        blink.mojom.BytesProvider_RequestAsFile_ResponseParamsSpec.$,
        this.requestAsFile.createReceiverHandler(true /* expectsResponse */));
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
blink.mojom.DataElementBytesSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.DataElementFileSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.DataElementBlobSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BytesProvider_RequestAsReply_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BytesProvider_RequestAsReply_ResponseParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BytesProvider_RequestAsStream_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BytesProvider_RequestAsFile_ParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType}}
 * @export
 */
blink.mojom.BytesProvider_RequestAsFile_ResponseParamsSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { {$:!mojo.internal.MojomType} }
 * @export
 */
blink.mojom.DataElementSpec =
    { $: /** @type {!mojo.internal.MojomType} */ ({}) };


/**
 * @const { !bigint }
 * @export
 */
blink.mojom.DataElementBytes_MAXIMUM_EMBEDDED_DATA_SIZE =
    BigInt('256000');



mojo.internal.Struct(
    blink.mojom.DataElementBytesSpec.$,
    'DataElementBytes',
    [
      mojo.internal.StructField(
        'length', 0,
        0,
        mojo.internal.Uint64,
        BigInt(0),
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'embeddedData', 8,
        0,
        mojo.internal.Array(mojo.internal.Uint8, false),
        null,
        true, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'data', 16,
        0,
        mojo.internal.InterfaceProxy(blink.mojom.BytesProviderRemote),
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 32],]);





/** @record */
blink.mojom.DataElementBytes = class {
  constructor() {
    /** @export { !bigint } */
    this.length;
    /** @export { (Array<!number>|undefined) } */
    this.embeddedData;
    /** @export { !blink.mojom.BytesProviderRemote } */
    this.data;
  }
};



mojo.internal.Struct(
    blink.mojom.DataElementFileSpec.$,
    'DataElementFile',
    [
      mojo.internal.StructField(
        'path', 0,
        0,
        mojoBase.mojom.FilePathSpec.$,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'offset', 8,
        0,
        mojo.internal.Uint64,
        BigInt(0),
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'length', 16,
        0,
        mojo.internal.Uint64,
        BigInt(0),
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'expectedModificationTime', 24,
        0,
        mojoBase.mojom.TimeSpec.$,
        null,
        true, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 40],]);





/** @record */
blink.mojom.DataElementFile = class {
  constructor() {
    /** @export { !mojoBase.mojom.FilePath } */
    this.path;
    /** @export { !bigint } */
    this.offset;
    /** @export { !bigint } */
    this.length;
    /** @export { (mojoBase.mojom.Time|undefined) } */
    this.expectedModificationTime;
  }
};



mojo.internal.Struct(
    blink.mojom.DataElementBlobSpec.$,
    'DataElementBlob',
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
        'offset', 8,
        0,
        mojo.internal.Uint64,
        BigInt(0),
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'length', 16,
        0,
        mojo.internal.Uint64,
        BigInt(0),
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 32],]);





/** @record */
blink.mojom.DataElementBlob = class {
  constructor() {
    /** @export { !blink.mojom.BlobRemote } */
    this.blob;
    /** @export { !bigint } */
    this.offset;
    /** @export { !bigint } */
    this.length;
  }
};



mojo.internal.Struct(
    blink.mojom.BytesProvider_RequestAsReply_ParamsSpec.$,
    'BytesProvider_RequestAsReply_Params',
    [
    ],
    [[0, 8],]);





/** @record */
blink.mojom.BytesProvider_RequestAsReply_Params = class {
  constructor() {
  }
};



mojo.internal.Struct(
    blink.mojom.BytesProvider_RequestAsReply_ResponseParamsSpec.$,
    'BytesProvider_RequestAsReply_ResponseParams',
    [
      mojo.internal.StructField(
        'data', 0,
        0,
        mojo.internal.Array(mojo.internal.Uint8, false),
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 16],]);





/** @record */
blink.mojom.BytesProvider_RequestAsReply_ResponseParams = class {
  constructor() {
    /** @export { !Array<!number> } */
    this.data;
  }
};



mojo.internal.Struct(
    blink.mojom.BytesProvider_RequestAsStream_ParamsSpec.$,
    'BytesProvider_RequestAsStream_Params',
    [
      mojo.internal.StructField(
        'pipe', 0,
        0,
        mojo.internal.Handle,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 16],]);





/** @record */
blink.mojom.BytesProvider_RequestAsStream_Params = class {
  constructor() {
    /** @export { !MojoHandle } */
    this.pipe;
  }
};



mojo.internal.Struct(
    blink.mojom.BytesProvider_RequestAsFile_ParamsSpec.$,
    'BytesProvider_RequestAsFile_Params',
    [
      mojo.internal.StructField(
        'sourceOffset', 0,
        0,
        mojo.internal.Uint64,
        BigInt(0),
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'sourceSize', 8,
        0,
        mojo.internal.Uint64,
        BigInt(0),
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'file', 16,
        0,
        mojoBase.mojom.FileSpec.$,
        null,
        false, /* nullable */
        0 /* minVersion */,
      ),
      mojo.internal.StructField(
        'fileOffset', 24,
        0,
        mojo.internal.Uint64,
        BigInt(0),
        false, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 40],]);





/** @record */
blink.mojom.BytesProvider_RequestAsFile_Params = class {
  constructor() {
    /** @export { !bigint } */
    this.sourceOffset;
    /** @export { !bigint } */
    this.sourceSize;
    /** @export { !mojoBase.mojom.File } */
    this.file;
    /** @export { !bigint } */
    this.fileOffset;
  }
};



mojo.internal.Struct(
    blink.mojom.BytesProvider_RequestAsFile_ResponseParamsSpec.$,
    'BytesProvider_RequestAsFile_ResponseParams',
    [
      mojo.internal.StructField(
        'timeFileModified', 0,
        0,
        mojoBase.mojom.TimeSpec.$,
        null,
        true, /* nullable */
        0 /* minVersion */,
      ),
    ],
    [[0, 16],]);





/** @record */
blink.mojom.BytesProvider_RequestAsFile_ResponseParams = class {
  constructor() {
    /** @export { (mojoBase.mojom.Time|undefined) } */
    this.timeFileModified;
  }
};



mojo.internal.Union(
    blink.mojom.DataElementSpec.$, 'DataElement',
    {
      'bytes': {
        'ordinal': 0,
        'type': blink.mojom.DataElementBytesSpec.$,
      },
      'file': {
        'ordinal': 1,
        'type': blink.mojom.DataElementFileSpec.$,
      },
      'blob': {
        'ordinal': 2,
        'type': blink.mojom.DataElementBlobSpec.$,
      },
    });

/**
 * @typedef { {
 *   bytes: (!blink.mojom.DataElementBytes|undefined),
 *   file: (!blink.mojom.DataElementFile|undefined),
 *   blob: (!blink.mojom.DataElementBlob|undefined),
 * } }
 */
blink.mojom.DataElement;
