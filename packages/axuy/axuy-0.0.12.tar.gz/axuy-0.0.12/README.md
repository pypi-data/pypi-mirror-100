# axuy

Minimalist peer-to-peer first-person shooter

![icon](https://git.disroot.org/McSinyx/axuy/raw/branch/master/axuy/icon.png)

## Goals

* Written in pure Python and thus be portable
* Easy to read codebase as well as easy on resources
* Generative visuals
* Functional when possible
* P2P communication based on calculated *trust*
* Modularized for the ease of bot scripting

## Screenshots

Since axuy's screenshots would look like some kinky abstract art,
I instead document the development progress as short clips on Youtube,
[listed in reverse chronological order][yt].  If software freedom is concerned,
one may view them using MPV with youtube-dl support.

## Installation

The game is still work-in-progress.  Preview releases are available on PyPI
and can be installed for Python 3.6+ via

    pip install axuy

Unless one is on either Windows or macOS, perse would have to
additionally install GLFW version 3.3 (or higher).

Axuy can then be launch from the command-line using

    axuy --port=42069 &
    axuy --seeder=:42069

There is also `aisample` in `tools` as an automated example
with similar command-line interface.

For hacking, after having dependenies installed, one may also invoke axuy
from the project's root directory by

    python -m axuy --port=42069 &
    python -m axuy --seeder=:42069

## Copying

This listing is our best-faith, hard-work effort at accurate attribution,
sources, and licenses for everything in Axuy.  If you discover
an asset/contribution that is incorrectly attributed or licensed,
please contact us immediately.  We are happy to do everything we can
to fix or remove the issue.

### License

Axuy's source code and its icon are released under GNU [Affero General Public
License version 3][agplv3] or later.  This means if you run a modified program
on a server and let other users communicate with it there, your server must also
allow them to download the source code corresponding to the modified version
running there.

![AGPLv3](https://www.gnu.org/graphics/agplv3-155x51.png)

Other creative works retain their original licenses as listed below.

### Textures

Texture Artist---[rubberduck](https://opengameart.org/users/rubberduck)

* License: [CC0 1.0][cc0]
* `axuy/assets/wall-*.png` ([original][wall])

### 3D Art

3D Modeler---[Čestmír Dammer](https://opengameart.org/users/cdmir)

* License: [CC0 1.0][cc0]
* `axuy/assets/chickenV2.*` ([original][chicken])

3D Modeler---[Jeremy Mitchell](https://opengameart.org/users/floatvoid)

* License: [CC0 1.0][cc0]
* `axuy/assets/rock01.obj` ([original][rock])

[yt]: https://www.youtube.com/playlist?list=PLAA9fHINq3sayfxEyZSF2D_rMgDZGyL3N
[agplv3]: https://www.gnu.org/licenses/agpl-3.0.html
[cc0]: http://creativecommons.org/publicdomain/zero/1.0
[wall]: https://opengameart.org/content/handpainted-brick-texture-pack
[chicken]: https://opengameart.org/content/chicken-animated
[rock]: https://opengameart.org/content/desert-rock
