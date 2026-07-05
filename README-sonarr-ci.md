# Sonarr episode-ordering patch — CI bench

This branch tests `sonarr-episode-ordering.patch` against Sonarr v4.0.19.2979.

The patch adds a per-series **Episode Ordering** setting (Auto / TheTVDB) so a show like
American Dad can be pinned to TVDB numbering, bypassing XEM scene mappings for parsing,
searching and episode refresh. Fixes the wrong-season grab problem (Sonarr/Sonarr#2086).

CI: `.github/workflows/sonarr-patch-ci.yml` checks out upstream Sonarr at the tag, applies
the patch, runs the backend unit test suite and the frontend lint/build.
