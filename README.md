# mechanix-packager

Shared packaging tooling for Mechanix apps. Currently builds RPM and DEB
(via [nfpm](https://nfpm.goreleaser.com)).

Each app repo (`mechanix-clock`, `mechanix-files`, ...) stays fully
independent - this tool is installed separately and invoked *from* an
app repo's root.

## Structure

```text
package.py           CLI entrypoint: resolves version/arch, stages the
                      build bundle, dispatches each requested format to
                      its packager
resolve_version.py    Standalone Pulp release resolver (rpm/deb version)
common.py             Format-agnostic helpers: repo root, upstream version,
                      finding/staging the flutter-elinux bundle
packagers/
  __init__.py         The packager contract + registry
  nfpm.py             rpm, deb, apk, archlinux - all via nfpm
```

## Install

Download and extract a tagged release:

```sh
curl -fsSL -o mechanix-packager.tar.gz \
  https://github.com/dhruveshb-mecha/mechanix-packager/archive/refs/tags/v0.1.0.tar.gz
mkdir -p mechanix-packager && tar -xzf mechanix-packager.tar.gz -C mechanix-packager --strip-components=1
```

Stdlib-only Python (3.9+) - no `pip install` needed, nothing else to set up.

## Use

Run it *from the app repo's root*, it resolves everything (pubspec.yaml, packaging/nfpm/nfpm.yaml,
the build bundle) relative to app's current working directory.

```sh

# version from pubspec.yaml, release defaults to "1"
python3 /path/to/mechanix-packager/package.py

# CI / fetch the real next Pulp release number:
python3 /path/to/mechanix-packager/resolve_version.py --format rpm
python3 /path/to/mechanix-packager/package.py --formats rpm --release "$RELEASE"
```

## Contract an app repo must follow

- `pubspec.yaml` at the repo root, with a `version:` field.
- `packaging/nfpm/nfpm.yaml` - the nfpm config. Its `name:` field is what
  the nfpm packager and `resolve_version.py` use as the package name.
- `packaging/nfpm/scripts/` - launcher/postinstall/postremove scripts
  referenced from `nfpm.yaml`, if any.
- A `build/elinux/*/release/bundle` directory (flutter-elinux's output)
  to package, before running `package.py`.
`nfpm.yaml`'s actual content (binary name, maintainer,
description, dependencies, whether a desktop entry/icon exist yet) - is
actual per-app data and will be maintained in each app repo.
