FROM archlinux@sha256:7ddb28e525cda55998a80d147967865193d170b0cf75c999ff2e3116d8f95a32 as chroot

COPY app /

FROM ghcr.io/google/nsjail/nsjail@sha256:03a904cd42b07ecc6e6f318c1ea14bd28339e1411d180d8744b2a5e2929e895f

COPY --from=chroot / /chroot
COPY nsjail.cfg /nsjail.cfg

CMD ["nsjail", "--config", "/nsjail.cfg"]