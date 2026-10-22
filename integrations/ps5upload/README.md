# Local PS5Upload helper patch

These changes belong to the GPL-3.0-or-later PS5Upload codebase, not the repository's GPL-2.0-only cheat sources. Upstream: https://github.com/phantomptr/ps5upload . License: https://github.com/phantomptr/ps5upload/blob/main/LICENSE .

`session-cheats.patch` was derived from the local 7.1.11 helper source. It adds a bounded in-memory PID/title session bitset, removes saved checkbox presets/sidecar reads, supplies session counts to title lists, and retains shared hook ranges as well as caves while another enabled mod uses them. It includes native regression tests. The unrelated local Windows Makefile compiler/linker refactor is excluded; only registration of the new C source remains.

Apply/rebase the patch to the matching source and build with PS5Upload's documented SDK workflow. No automatic patch applicability to a later upstream version is claimed. Run the full upstream quality gate before an upstream PR; only the payload build, relevant native selftests and the documented local live checks were completed here. No official release version claims are made and no helper/PC binary is distributed in this repository.

Use the 26-switch JSON only with a helper implementing both changes. The 27-entry mastercode layout avoids the shared-removal dependency, but stock readers may still retain checkbox choices across game restarts. Do not claim the patch fixes the one unexplained helper SIGSEGV recorded during local testing.

The expanded 23-resource package passed 46 live transitions after explicitly stopping the serving helper and launching the stored modified helper. A previous attempt failed shared-hook retention; its serving binary was not independently identified. Always verify which helper is serving, rather than relying on the version label alone.
