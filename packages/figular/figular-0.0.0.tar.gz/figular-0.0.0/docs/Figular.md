<!--
SPDX-FileCopyrightText: 2021 Galagic Limited, et. al. <https://galagic.com>

SPDX-License-Identifier: CC-BY-SA-4.0

figular generates visualisations from flexible, reusable parts

For full copyright information see the AUTHORS file at the top-level
directory of this distribution or at
[AUTHORS](https://gitlab.com/thegalagic/figular/AUTHORS.md)

This work is licensed under the Creative Commons Attribution 4.0 International
License. You should have received a copy of the license along with this work.
If not, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
-->

# Figular

Figular lets you build visualisations. You can choose from a range of
existing figures that can be customised or build your own (in future).

## Figures

A figure is a self-contained visualisation that can adjust itself based on your
content.  Content can be parameters that control display (rotation, layout) and
data that populates the figure (text, images). Figular comes with a range of our
own figures, documentation on each of them is linked below:

* [Concept/circle](figures/concept/circle.md)

Please help us grow this list by contributing to the project!

Figures can come from different repositories. If no repository is specified the
default is 'Figular' which is what comes bundled as standard with any
installation. At present we do not support repositories so this is purely
theoretical. Our inspiration comes from [flatpak](https://flatpak.org/).

Each figure has a unique, case-insensitive name within its repository. Related
figures are grouped together in a tree-like structure. Levels in the tree are
separated by a forward slash `/`, e.g.  'concept/circle'. Our inspiration comes
from URLs.

Figures can be versioned, if a version is not supplied the latest is assumed.
The version is not part of the name however. Versioning is inspired by [Semantic
Versioning](https://semver.org/). New versions should not break older usage
without a major version bump for example.

In future we may also support metadata such as categories/tags and other
information. Inspiration comes from [PyPi](pypi.org/).
