# ChromeOS Shared OWNERS Tree

See [go/cros-shared-owners:design] for in-depth background.

Developers & teams are encouraged to self organize as makes sense for their
particular project and needs.  There is no council that hands out names :).
When picking new names, make sure to review the guidance below to minimize
leakage.

[TOC]

## Layout

At a high level, the structure should follow this pattern:

*   {generic organizational name}/
    *   OWNERS: Used to grant self-update permissions to specific files.  Never
        use these outside of this repository.
    *   OWNERS.all: Include all the subgroups in here, iff it makes sense to.
    *   OWNERS.{grouping}: The group of developers for a particular purpose.

The special organizational name `meta` is for OWNERS files which do not list
specific individuals, but instead are used for a stable file path for
mass-inclusion purposes that may not necessarily correspond to a team boundary.
For example, `meta/OWNERS.overlays` specifies who has owners on all overlays.

When adding a new group, try to find an existing subdir to use.  If none are
appropriate, feel free to propose one by reaching out to [CrOS infra].

Subdirs of subdirs are not currently permitted.  If you think it makes sense
to organize that way, feel free to reach out to [CrOS infra].

Once an OWNERS.{grouping} file has been created and referenced elsewhere in the
CrOS tree, it cannot be removed.  A {new grouping} can be created, and the old
one changed to include the new name.  See [Branching] below for more info.

## Usage

For projects on the public chromium GoB host, use:

```
include chromiumos/owners:v1:/path/to/OWNERS.file
```

For projects on the private chrome-internal GoB host, use:

```
include chromeos/owners:v1:/path/to/OWNERS.file
```

The `v1` is the current repository version; see [Branching] below for more info.

Adjust the `/path/to/OWNERS.file` part to match the path in this repository.
It should always be absolute (i.e. have a leading `/`).

Never include a plain `OWNERS` file from here as those are meant for use within
this repository itself.  Only ever include `OWNERS.{grouping}` externally.

## Naming

The filenames in here, and the developers listed in them, present a challenge
when it comes to leaking information.  We don't want to make it easy for
external people to calculate organization sizes or allocations (i.e., have
Microsoft Windows determine that we're dedicating 20 people to CrOS Infra), or
to leak codenames and launch information.

So to that end, try to keep groups aligned to public codenames, and to public
projects when possible.  Avoid secret codenames or other non-public terms.

## OWNERS Content

When writing the actual OWNERS.{grouping} files, make sure to follow:

*   Rotations/group lists (e.g. GwsQ rotations or Google Groups) may be listed.
    Remember that this is only to help reviewers find a good contact via Gerrit
    -- members are not automatically expanded, so everyone still must be listed
    explicitly in the file.
*   Comments are allowed, although they are unlikely to be seen by developers
    since Gerrit ignores them.
*   Never use `noparent` or `per-file` directives.  These should be kept in the
    respective projects that include this file instead.  For example, we would
    not use `set noparent` in `/infra/OWNERS.build` in here, but we might use it
    in chromite's `OWNERS` file which includes `/infra/OWNERS.build`.
*   If developers have linked their @google.com & @chromium.org account, only
    one needs to be listed.  If they're not linked, and both are used (e.g.,
    @google.com on chrome-internal GoB & @chromium.org on chromium GoB), then
    both must be listed in order for the files to work on both GoB hosts.

## Branching

This repository is usable in any CrOS branch as it is not automatically branched
itself.  This repository's branch name reflects the version of its layout since
files may not be removed once added & referenced in a branch.  This is how we
provide stability in older CrOS branches without having to go through and update
all the historical references.

If a particular grouping or naming no longer makes sense, the file has to remain
in place to keep branches working.  Even if code doesn't exist in ToT, it might
exist in a much older branch (e.g. firmware), and we might need to update those.

For example, a device has gone EOL, or a project has been shutdown, or has been
renamed, or merged into a different project.  In all these cases, please try to
find an existing group who can provide coverage, and include that OWNERS.{file}.

### Updating the layout

If we've gotten to the point where there are too many of these old names around,
we can create a new versioned branch.  The process looks like:

*   If we're at `v1` today, then create `v2` starting at the existing `v1`.
    *   Contact [CrOS infra] who will work with [go/git-admin-bug].
*   Update the CrOS manifest to use `v2` in the checkout.
    *   This is safe to land immediately -- this project is in the manifest out
        of convenience only.  It has no relationship to the includes used in
        actual OWNERS files in the tree.
*   Make any layout changes desired -- rename, delete, etc... files.
*   Update this document & the common linter to start requiring `v2`.
*   Manually check out the old `v1` branch and change all of its files to
    include owners from this repository's `v2`.
    *   This keeps all existing OWNERS files working, including in old branches,
        and avoids having to land updates to all of them.

## FAQ

### Can these files be included from other Gerrit hosts?

No.  The Gerrit code-owners system does not support that.

The reason it works with the chrome-internal & chromium GoB hosts is because we
have set up explicit syncing mechanisms between the two.

### Should I use my @google.com or @chromium.org address?

If your accounts are linked, then use whichever one you prefer.

If your accounts are not linked, you will probably need to list both.

### Why do I get `[code-owners] code owner email 'X@chromium.org' in '/foo/OWNERS.bar' cannot be resolved` when X's accounts are linked?

The same email (X@chromium.org or X@google.com) needs to be set as preferred
email in Gerrit's settings for the internal and chromium instance. See the
settings:
* https://chromium-review.googlesource.com/settings/#EmailAddresses
* https://chrome-internal-review.googlesource.com/settings/#EmailAddresses

### Can we list non-Googlers (e.g. partners)?

We do not normally put non-Googlers in OWNERS files, but it isn't unheard of.

For now, partners should be not be listed here.  Instead, list them in the
specific OWNERS where the partner is granted access.  This will help avoid
accidentally adding them to places they shouldn't.


[Branching]: #Branching
[CrOS infra]: https://goto.google.com/cros-infra-help
[go/cros-shared-owners:design]: https://goto.google.com/cros-shared-owners:design
[go/git-admin-bug]: https://goto.google.com/git-admin-bug
