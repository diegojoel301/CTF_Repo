// third_party/blink/public/mojom/blob/data_element.mojom-shared-internal.h is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2016 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_DATA_ELEMENT_MOJOM_SHARED_INTERNAL_H_
#define THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_DATA_ELEMENT_MOJOM_SHARED_INTERNAL_H_
#include "mojo/public/cpp/bindings/lib/array_internal.h"
#include "mojo/public/cpp/bindings/lib/bindings_internal.h"
#include "mojo/public/cpp/bindings/lib/map_data_internal.h"
#include "mojo/public/cpp/bindings/lib/buffer.h"
#include "mojo/public/mojom/base/file.mojom-shared-internal.h"
#include "mojo/public/mojom/base/file_path.mojom-shared-internal.h"
#include "mojo/public/mojom/base/time.mojom-shared-internal.h"
#include "third_party/blink/public/mojom/blob/blob.mojom-shared-internal.h"
#include "mojo/public/cpp/bindings/lib/native_enum_data.h"
#include "mojo/public/interfaces/bindings/native_struct.mojom-shared-internal.h"
#include "base/component_export.h"



namespace mojo {
namespace internal {
class ValidationContext;
}
}


namespace blink::mojom {
namespace internal {
class DataElementBytes_Data;
class DataElementFile_Data;
class DataElementBlob_Data;
class DataElement_Data;

#pragma pack(push, 1)


class COMPONENT_EXPORT(MOJOM_SHARED_BLINK_COMMON_EXPORT) DataElement_Data {
 public:
  // Used to identify Mojom Union Data Classes.
  typedef void MojomUnionDataType;

  DataElement_Data() = default;
  // Do nothing in the destructor since it won't be called when it is a
  // non-inlined union.
  ~DataElement_Data() = default;

  static bool Validate(const void* data,
                       mojo::internal::ValidationContext* validation_context,
                       bool inlined);

  bool is_null() const { return size == 0; }

  void set_null() {
    size = 0U;
    tag = static_cast<DataElement_Tag>(0);
    data.unknown = 0U;
  }

  // TODO(crbug.com/40731316): SHOUTY_CASE values are being deprecated per C++ code style
  // guidelines (https://google.github.io/styleguide/cppguide.html#Enumerator_Names),
  // please use kCamelCase values instead.  Cleanup NULL_VALUE, BOOL_VALUE, INT_VALUE, etc.
  // generation once codebase is transitioned to kNullValue, kBoolValue, kIntValue, etc.
  enum class DataElement_Tag : uint32_t {

    
    kBytes,
    
    kFile,
    
    kBlob,
  };

  // A note on layout:
  // "Each non-static data member is allocated as if it were the sole member of
  // a struct." - Section 9.5.2 ISO/IEC 14882:2011 (The C++ Spec)
  union MOJO_ALIGNAS(8) Union_ {
    Union_() : unknown(0) {}
    mojo::internal::Pointer<internal::DataElementBytes_Data> f_bytes;
    mojo::internal::Pointer<internal::DataElementFile_Data> f_file;
    mojo::internal::Pointer<internal::DataElementBlob_Data> f_blob;
    uint64_t unknown;
  };

  uint32_t size;
  DataElement_Tag tag;
  Union_ data;
};
static_assert(sizeof(DataElement_Data) == mojo::internal::kUnionDataSize,
              "Bad sizeof(DataElement_Data)");
class COMPONENT_EXPORT(MOJOM_SHARED_BLINK_COMMON_EXPORT) DataElementBytes_Data {
 public:
  static bool Validate(const void* data,
                       mojo::internal::ValidationContext* validation_context);

  mojo::internal::StructHeader header_;
  uint64_t length;
  mojo::internal::Pointer<mojo::internal::Array_Data<uint8_t>> embedded_data;
  mojo::internal::Interface_Data data;

 private:
  friend class mojo::internal::MessageFragment<DataElementBytes_Data>;

  DataElementBytes_Data();
  ~DataElementBytes_Data() = delete;
};
static_assert(sizeof(DataElementBytes_Data) == 32,
              "Bad sizeof(DataElementBytes_Data)");
// Used by DataElementBytes::WrapAsMessage to lazily serialize the struct.
template <typename UserType, typename DataView>
struct DataElementBytes_UnserializedMessageContext
    : public mojo::internal::UnserializedMessageContext {
 public:
  static const mojo::internal::UnserializedMessageContext::Tag kMessageTag;

  DataElementBytes_UnserializedMessageContext(
    uint32_t message_name,
    uint32_t message_flags,
    UserType input)
      : mojo::internal::UnserializedMessageContext(&kMessageTag, message_name, message_flags)
      , user_data_(std::move(input)) {}
  ~DataElementBytes_UnserializedMessageContext() override = default;

  UserType TakeData() {
    return std::move(user_data_);
  }

 private:
  // mojo::internal::UnserializedMessageContext:
  void Serialize(mojo::Message& message) override {
    mojo::internal::MessageFragment<DataElementBytes_Data> fragment(message);
    mojo::internal::Serialize<DataView>(user_data_, fragment);
  }

  UserType user_data_;
};

template <typename UserType, typename DataView>
const mojo::internal::UnserializedMessageContext::Tag
    DataElementBytes_UnserializedMessageContext<UserType, DataView>::kMessageTag = {};
class COMPONENT_EXPORT(MOJOM_SHARED_BLINK_COMMON_EXPORT) DataElementFile_Data {
 public:
  static bool Validate(const void* data,
                       mojo::internal::ValidationContext* validation_context);

  mojo::internal::StructHeader header_;
  mojo::internal::Pointer<::mojo_base::mojom::internal::FilePath_Data> path;
  uint64_t offset;
  uint64_t length;
  mojo::internal::Pointer<::mojo_base::mojom::internal::Time_Data> expected_modification_time;

 private:
  friend class mojo::internal::MessageFragment<DataElementFile_Data>;

  DataElementFile_Data();
  ~DataElementFile_Data() = delete;
};
static_assert(sizeof(DataElementFile_Data) == 40,
              "Bad sizeof(DataElementFile_Data)");
// Used by DataElementFile::WrapAsMessage to lazily serialize the struct.
template <typename UserType, typename DataView>
struct DataElementFile_UnserializedMessageContext
    : public mojo::internal::UnserializedMessageContext {
 public:
  static const mojo::internal::UnserializedMessageContext::Tag kMessageTag;

  DataElementFile_UnserializedMessageContext(
    uint32_t message_name,
    uint32_t message_flags,
    UserType input)
      : mojo::internal::UnserializedMessageContext(&kMessageTag, message_name, message_flags)
      , user_data_(std::move(input)) {}
  ~DataElementFile_UnserializedMessageContext() override = default;

  UserType TakeData() {
    return std::move(user_data_);
  }

 private:
  // mojo::internal::UnserializedMessageContext:
  void Serialize(mojo::Message& message) override {
    mojo::internal::MessageFragment<DataElementFile_Data> fragment(message);
    mojo::internal::Serialize<DataView>(user_data_, fragment);
  }

  UserType user_data_;
};

template <typename UserType, typename DataView>
const mojo::internal::UnserializedMessageContext::Tag
    DataElementFile_UnserializedMessageContext<UserType, DataView>::kMessageTag = {};
class COMPONENT_EXPORT(MOJOM_SHARED_BLINK_COMMON_EXPORT) DataElementBlob_Data {
 public:
  static bool Validate(const void* data,
                       mojo::internal::ValidationContext* validation_context);

  mojo::internal::StructHeader header_;
  mojo::internal::Interface_Data blob;
  uint64_t offset;
  uint64_t length;

 private:
  friend class mojo::internal::MessageFragment<DataElementBlob_Data>;

  DataElementBlob_Data();
  ~DataElementBlob_Data() = delete;
};
static_assert(sizeof(DataElementBlob_Data) == 32,
              "Bad sizeof(DataElementBlob_Data)");
// Used by DataElementBlob::WrapAsMessage to lazily serialize the struct.
template <typename UserType, typename DataView>
struct DataElementBlob_UnserializedMessageContext
    : public mojo::internal::UnserializedMessageContext {
 public:
  static const mojo::internal::UnserializedMessageContext::Tag kMessageTag;

  DataElementBlob_UnserializedMessageContext(
    uint32_t message_name,
    uint32_t message_flags,
    UserType input)
      : mojo::internal::UnserializedMessageContext(&kMessageTag, message_name, message_flags)
      , user_data_(std::move(input)) {}
  ~DataElementBlob_UnserializedMessageContext() override = default;

  UserType TakeData() {
    return std::move(user_data_);
  }

 private:
  // mojo::internal::UnserializedMessageContext:
  void Serialize(mojo::Message& message) override {
    mojo::internal::MessageFragment<DataElementBlob_Data> fragment(message);
    mojo::internal::Serialize<DataView>(user_data_, fragment);
  }

  UserType user_data_;
};

template <typename UserType, typename DataView>
const mojo::internal::UnserializedMessageContext::Tag
    DataElementBlob_UnserializedMessageContext<UserType, DataView>::kMessageTag = {};

#pragma pack(pop)

}  // namespace internal

}  // blink::mojom

#endif  // THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_DATA_ELEMENT_MOJOM_SHARED_INTERNAL_H_