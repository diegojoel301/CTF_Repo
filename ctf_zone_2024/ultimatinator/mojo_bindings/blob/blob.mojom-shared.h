// third_party/blink/public/mojom/blob/blob.mojom-shared.h is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2016 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_BLOB_MOJOM_SHARED_H_
#define THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_BLOB_MOJOM_SHARED_H_

#include <stdint.h>

#include <functional>
#include <iosfwd>
#include <type_traits>
#include <utility>
#include "mojo/public/cpp/bindings/array_data_view.h"
#include "mojo/public/cpp/bindings/enum_traits.h"
#include "mojo/public/cpp/bindings/interface_data_view.h"
#include "mojo/public/cpp/bindings/lib/bindings_internal.h"
#include "mojo/public/cpp/bindings/lib/serialization.h"
#include "mojo/public/cpp/bindings/map_data_view.h"
#include "mojo/public/cpp/bindings/string_data_view.h"

#include "third_party/perfetto/include/perfetto/tracing/traced_value_forward.h"

#include "third_party/blink/public/mojom/blob/blob.mojom-shared-internal.h"
#include "mojo/public/mojom/base/big_buffer.mojom-shared.h"
#include "mojo/public/mojom/base/time.mojom-shared.h"
#include "services/network/public/mojom/data_pipe_getter.mojom-shared.h"
#include "services/network/public/mojom/http_request_headers.mojom-shared.h"
#include "services/network/public/mojom/url_loader.mojom-shared.h"
#include "mojo/public/cpp/bindings/lib/interface_serialization.h"
#include "mojo/public/cpp/system/data_pipe.h"


#include "base/component_export.h"




namespace blink::mojom {


}  // blink::mojom

namespace mojo {
namespace internal {

}  // namespace internal
}  // namespace mojo


namespace blink::mojom {
// Interface base classes. They are used for type safety check.
class BlobReaderClientInterfaceBase {};

using BlobReaderClientPtrDataView =
    mojo::InterfacePtrDataView<BlobReaderClientInterfaceBase>;
using BlobReaderClientRequestDataView =
    mojo::InterfaceRequestDataView<BlobReaderClientInterfaceBase>;
using BlobReaderClientAssociatedPtrInfoDataView =
    mojo::AssociatedInterfacePtrInfoDataView<BlobReaderClientInterfaceBase>;
using BlobReaderClientAssociatedRequestDataView =
    mojo::AssociatedInterfaceRequestDataView<BlobReaderClientInterfaceBase>;
class BlobInterfaceBase {};

using BlobPtrDataView =
    mojo::InterfacePtrDataView<BlobInterfaceBase>;
using BlobRequestDataView =
    mojo::InterfaceRequestDataView<BlobInterfaceBase>;
using BlobAssociatedPtrInfoDataView =
    mojo::AssociatedInterfacePtrInfoDataView<BlobInterfaceBase>;
using BlobAssociatedRequestDataView =
    mojo::AssociatedInterfaceRequestDataView<BlobInterfaceBase>;


}  // blink::mojom

namespace std {

}  // namespace std

namespace mojo {

}  // namespace mojo


namespace blink::mojom {


}  // blink::mojom

// Declare TraceFormatTraits for enums, which should be defined in ::perfetto
// namespace.

#endif  // THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_BLOB_MOJOM_SHARED_H_