// third_party/blink/public/mojom/blob/blob_registry.mojom-shared-message-ids.h is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2018 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_BLOB_REGISTRY_MOJOM_SHARED_MESSAGE_IDS_H_
#define THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_BLOB_REGISTRY_MOJOM_SHARED_MESSAGE_IDS_H_

#include <stdint.h>


namespace blink::mojom {
namespace messages {


enum class ProgressClient : uint32_t {
  kOnProgress = 0,
};
enum class BlobRegistry : uint32_t {
  kRegister = 0,
  kRegisterFromStream = 1,
  kGetBlobFromUUID = 2,
};

}  // namespace messages

}  // blink::mojom

#endif  // THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_BLOB_REGISTRY_MOJOM_SHARED_MESSAGE_IDS_H_