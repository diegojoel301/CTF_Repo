// third_party/blink/public/mojom/blob/blob_url_store.mojom-blink.h is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2013 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_BLOB_URL_STORE_MOJOM_BLINK_H_
#define THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_BLOB_URL_STORE_MOJOM_BLINK_H_

#include <stdint.h>

#include <limits>
#include <optional>
#include <type_traits>
#include <utility>

#include "base/types/cxx23_to_underlying.h"
#include "mojo/public/cpp/bindings/clone_traits.h"
#include "mojo/public/cpp/bindings/equals_traits.h"
#include "mojo/public/cpp/bindings/lib/serialization.h"
#include "mojo/public/cpp/bindings/struct_ptr.h"
#include "mojo/public/cpp/bindings/struct_traits.h"
#include "mojo/public/cpp/bindings/union_traits.h"

#include "third_party/perfetto/include/perfetto/tracing/traced_value_forward.h"

#include "third_party/blink/public/mojom/blob/blob_url_store.mojom-features.h"  // IWYU pragma: export
#include "third_party/blink/public/mojom/blob/blob_url_store.mojom-shared.h"  // IWYU pragma: export
#include "third_party/blink/public/mojom/blob/blob_url_store.mojom-blink-forward.h"  // IWYU pragma: export
#include "mojo/public/mojom/base/unguessable_token.mojom-blink.h"
#include "services/network/public/mojom/schemeful_site.mojom-blink.h"
#include "services/network/public/mojom/url_loader_factory.mojom-blink-forward.h"
#include "third_party/blink/public/mojom/blob/blob.mojom-blink-forward.h"
#include "url/mojom/url.mojom-blink.h"

#include "mojo/public/cpp/bindings/lib/wtf_clone_equals_util.h"
#include "mojo/public/cpp/bindings/lib/wtf_hash_util.h"
#include "third_party/blink/renderer/platform/wtf/hash_functions.h"
#include "third_party/blink/renderer/platform/wtf/text/wtf_string.h"

#include "mojo/public/cpp/bindings/lib/control_message_handler.h"
#include "mojo/public/cpp/bindings/lib/message_size_estimator.h"
#include "mojo/public/cpp/bindings/raw_ptr_impl_ref_traits.h"


#include "third_party/blink/renderer/platform/platform_export.h"




namespace blink::mojom::blink {

class BlobURLStoreProxy;

template <typename ImplRefTraits>
class BlobURLStoreStub;

class BlobURLStoreRequestValidator;
class BlobURLStoreResponseValidator;


class PLATFORM_EXPORT BlobURLStore
    : public BlobURLStoreInterfaceBase {
 public:
  using IPCStableHashFunction = uint32_t(*)();

  static const char Name_[];
  static IPCStableHashFunction MessageToMethodInfo_(mojo::Message& message);
  static const char* MessageToMethodName_(mojo::Message& message);
  static constexpr uint32_t Version_ = 0;
  static constexpr bool PassesAssociatedKinds_ = false;
  static inline constexpr uint32_t kSyncMethodOrdinals[] = {
    0
  };
  static constexpr bool HasUninterruptableMethods_ = false;

  using Base_ = BlobURLStoreInterfaceBase;
  using Proxy_ = BlobURLStoreProxy;

  template <typename ImplRefTraits>
  using Stub_ = BlobURLStoreStub<ImplRefTraits>;

  using RequestValidator_ = BlobURLStoreRequestValidator;
  using ResponseValidator_ = BlobURLStoreResponseValidator;
  enum MethodMinVersions : uint32_t {
    kRegisterMinVersion = 0,
    kRevokeMinVersion = 0,
    kResolveAsURLLoaderFactoryMinVersion = 0,
    kResolveForNavigationMinVersion = 0,
  };

// crbug.com/1340245 - this causes binary size bloat on Fuchsia, and we're OK
// with not having this data in traces there.
#if !BUILDFLAG(IS_FUCHSIA)
  struct Register_Sym {
    NOINLINE static uint32_t IPCStableHash();
  };
  struct Revoke_Sym {
    NOINLINE static uint32_t IPCStableHash();
  };
  struct ResolveAsURLLoaderFactory_Sym {
    NOINLINE static uint32_t IPCStableHash();
  };
  struct ResolveForNavigation_Sym {
    NOINLINE static uint32_t IPCStableHash();
  };
#endif // !BUILDFLAG(IS_FUCHSIA)
  virtual ~BlobURLStore() = default;

  // Sync method. This signature is used by the client side; the service side
  // should implement the signature with callback below.
  
  virtual bool Register(::mojo::PendingRemote<::blink::mojom::blink::Blob> blob, const ::blink::KURL& url, const ::base::UnguessableToken& unsafe_agent_cluster_id, const std::optional<::blink::BlinkSchemefulSite>& unsafe_top_level_site);

  using RegisterCallback = base::OnceCallback<void()>;
  
  virtual void Register(::mojo::PendingRemote<::blink::mojom::blink::Blob> blob, const ::blink::KURL& url, const ::base::UnguessableToken& unsafe_agent_cluster_id, const std::optional<::blink::BlinkSchemefulSite>& unsafe_top_level_site, RegisterCallback callback) = 0;

  
  virtual void Revoke(const ::blink::KURL& url) = 0;


  using ResolveAsURLLoaderFactoryCallback = base::OnceCallback<void(const std::optional<::base::UnguessableToken>&, const std::optional<::blink::BlinkSchemefulSite>&)>;
  
  virtual void ResolveAsURLLoaderFactory(const ::blink::KURL& url, ::mojo::PendingReceiver<::network::mojom::blink::URLLoaderFactory> factory, ResolveAsURLLoaderFactoryCallback callback) = 0;


  using ResolveForNavigationCallback = base::OnceCallback<void(const std::optional<::base::UnguessableToken>&)>;
  
  virtual void ResolveForNavigation(const ::blink::KURL& url, ::mojo::PendingReceiver<BlobURLToken> token, ResolveForNavigationCallback callback) = 0;
};

class BlobURLTokenProxy;

template <typename ImplRefTraits>
class BlobURLTokenStub;

class BlobURLTokenRequestValidator;
class BlobURLTokenResponseValidator;


class PLATFORM_EXPORT BlobURLToken
    : public BlobURLTokenInterfaceBase {
 public:
  using IPCStableHashFunction = uint32_t(*)();

  static const char Name_[];
  static IPCStableHashFunction MessageToMethodInfo_(mojo::Message& message);
  static const char* MessageToMethodName_(mojo::Message& message);
  static constexpr uint32_t Version_ = 0;
  static constexpr bool PassesAssociatedKinds_ = false;
  static constexpr bool HasUninterruptableMethods_ = false;

  using Base_ = BlobURLTokenInterfaceBase;
  using Proxy_ = BlobURLTokenProxy;

  template <typename ImplRefTraits>
  using Stub_ = BlobURLTokenStub<ImplRefTraits>;

  using RequestValidator_ = BlobURLTokenRequestValidator;
  using ResponseValidator_ = BlobURLTokenResponseValidator;
  enum MethodMinVersions : uint32_t {
    kCloneMinVersion = 0,
    kGetTokenMinVersion = 0,
  };

// crbug.com/1340245 - this causes binary size bloat on Fuchsia, and we're OK
// with not having this data in traces there.
#if !BUILDFLAG(IS_FUCHSIA)
  struct Clone_Sym {
    NOINLINE static uint32_t IPCStableHash();
  };
  struct GetToken_Sym {
    NOINLINE static uint32_t IPCStableHash();
  };
#endif // !BUILDFLAG(IS_FUCHSIA)
  virtual ~BlobURLToken() = default;

  
  virtual void Clone(::mojo::PendingReceiver<BlobURLToken> token) = 0;


  using GetTokenCallback = base::OnceCallback<void(const ::base::UnguessableToken&)>;
  
  virtual void GetToken(GetTokenCallback callback) = 0;
};



class PLATFORM_EXPORT BlobURLStoreProxy
    : public BlobURLStore {
 public:
  using InterfaceType = BlobURLStore;

  explicit BlobURLStoreProxy(mojo::MessageReceiverWithResponder* receiver);
  
  bool Register(::mojo::PendingRemote<::blink::mojom::blink::Blob> blob, const ::blink::KURL& url, const ::base::UnguessableToken& unsafe_agent_cluster_id, const std::optional<::blink::BlinkSchemefulSite>& unsafe_top_level_site) final;
  
  void Register(::mojo::PendingRemote<::blink::mojom::blink::Blob> blob, const ::blink::KURL& url, const ::base::UnguessableToken& unsafe_agent_cluster_id, const std::optional<::blink::BlinkSchemefulSite>& unsafe_top_level_site, RegisterCallback callback) final;
  
  void Revoke(const ::blink::KURL& url) final;
  
  void ResolveAsURLLoaderFactory(const ::blink::KURL& url, ::mojo::PendingReceiver<::network::mojom::blink::URLLoaderFactory> factory, ResolveAsURLLoaderFactoryCallback callback) final;
  
  void ResolveForNavigation(const ::blink::KURL& url, ::mojo::PendingReceiver<BlobURLToken> token, ResolveForNavigationCallback callback) final;

 private:
  mojo::MessageReceiverWithResponder* receiver_;
};



class PLATFORM_EXPORT BlobURLTokenProxy
    : public BlobURLToken {
 public:
  using InterfaceType = BlobURLToken;

  explicit BlobURLTokenProxy(mojo::MessageReceiverWithResponder* receiver);
  
  void Clone(::mojo::PendingReceiver<BlobURLToken> token) final;
  
  void GetToken(GetTokenCallback callback) final;

 private:
  mojo::MessageReceiverWithResponder* receiver_;
};
class PLATFORM_EXPORT BlobURLStoreStubDispatch {
 public:
  static bool Accept(BlobURLStore* impl, mojo::Message* message);
  static bool AcceptWithResponder(
      BlobURLStore* impl,
      mojo::Message* message,
      std::unique_ptr<mojo::MessageReceiverWithStatus> responder);
};

template <typename ImplRefTraits =
              mojo::RawPtrImplRefTraits<BlobURLStore>>
class BlobURLStoreStub
    : public mojo::MessageReceiverWithResponderStatus {
 public:
  using ImplPointerType = typename ImplRefTraits::PointerType;

  BlobURLStoreStub() = default;
  ~BlobURLStoreStub() override = default;

  void set_sink(ImplPointerType sink) { sink_ = std::move(sink); }
  ImplPointerType& sink() { return sink_; }

  bool Accept(mojo::Message* message) override {
    if (ImplRefTraits::IsNull(sink_))
      return false;
    return BlobURLStoreStubDispatch::Accept(
        ImplRefTraits::GetRawPointer(&sink_), message);
  }

  bool AcceptWithResponder(
      mojo::Message* message,
      std::unique_ptr<mojo::MessageReceiverWithStatus> responder) override {
    if (ImplRefTraits::IsNull(sink_))
      return false;
    return BlobURLStoreStubDispatch::AcceptWithResponder(
        ImplRefTraits::GetRawPointer(&sink_), message, std::move(responder));
  }

 private:
  ImplPointerType sink_;
};
class PLATFORM_EXPORT BlobURLTokenStubDispatch {
 public:
  static bool Accept(BlobURLToken* impl, mojo::Message* message);
  static bool AcceptWithResponder(
      BlobURLToken* impl,
      mojo::Message* message,
      std::unique_ptr<mojo::MessageReceiverWithStatus> responder);
};

template <typename ImplRefTraits =
              mojo::RawPtrImplRefTraits<BlobURLToken>>
class BlobURLTokenStub
    : public mojo::MessageReceiverWithResponderStatus {
 public:
  using ImplPointerType = typename ImplRefTraits::PointerType;

  BlobURLTokenStub() = default;
  ~BlobURLTokenStub() override = default;

  void set_sink(ImplPointerType sink) { sink_ = std::move(sink); }
  ImplPointerType& sink() { return sink_; }

  bool Accept(mojo::Message* message) override {
    if (ImplRefTraits::IsNull(sink_))
      return false;
    return BlobURLTokenStubDispatch::Accept(
        ImplRefTraits::GetRawPointer(&sink_), message);
  }

  bool AcceptWithResponder(
      mojo::Message* message,
      std::unique_ptr<mojo::MessageReceiverWithStatus> responder) override {
    if (ImplRefTraits::IsNull(sink_))
      return false;
    return BlobURLTokenStubDispatch::AcceptWithResponder(
        ImplRefTraits::GetRawPointer(&sink_), message, std::move(responder));
  }

 private:
  ImplPointerType sink_;
};
class PLATFORM_EXPORT BlobURLStoreRequestValidator : public mojo::MessageReceiver {
 public:
  bool Accept(mojo::Message* message) override;
};
class PLATFORM_EXPORT BlobURLTokenRequestValidator : public mojo::MessageReceiver {
 public:
  bool Accept(mojo::Message* message) override;
};
class PLATFORM_EXPORT BlobURLStoreResponseValidator : public mojo::MessageReceiver {
 public:
  bool Accept(mojo::Message* message) override;
};
class PLATFORM_EXPORT BlobURLTokenResponseValidator : public mojo::MessageReceiver {
 public:
  bool Accept(mojo::Message* message) override;
};





}  // blink::mojom::blink

namespace mojo {

}  // namespace mojo

#endif  // THIRD_PARTY_BLINK_PUBLIC_MOJOM_BLOB_BLOB_URL_STORE_MOJOM_BLINK_H_