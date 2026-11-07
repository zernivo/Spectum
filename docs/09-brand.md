# 9. Brand guide

## Name
**Septum**: the wall between two chambers, as in a nautilus shell or the heart. Each site is a chamber, and Septum is the wall.
Availability checked 2026-11-06: `septum` is free on PyPI, **taken on npm**, and no GitHub agent repos use it. Backups: `keepmum` (free on PyPI, npm and GitHub). `hushgate` is free on PyPI but taken on npm. Bulkhead, Airlock and Tacit are taken.

## Mark
A solid stone 2.5D nautilus shell with thin engraved curved septa and **one crimson chamber**, the fact kept in its room. Approved 2026-11-06.
- `brand/logo/septum-mark.svg` (transparent), `-dark-bg`, `-light-bg`, and PNGs at 128–1024
- `septum-mark-flat.svg` for small sizes and single-colour use
- Rejected directions are kept in `brand/history/`: rounded rectangles (looked like UI buttons) and chunky separated blocks (looked like a spine).

## Colour
| Role | Hex |
|---|---|
| Ink (background) | `#0B0D12` |
| Off-white | `#F3F1EC` |
| Accent crimson (one accent only) | `#E5484D` |
| Backup accent plum | `#8E6CEF` |
TUI status colours are listed in 04.

## Type
Inter (UI and wordmark in graphics) and JetBrains Mono (CLI and code). Both are under the SIL Open Font License.

## Motion
`brand/animation/`: **intro** (4.2 s, with wordmark), **regular** (2 s) and **loading** (seamless 1.6 s loop), each as MP4 and GIF.

## Terminal
Half-block pixel logo and ANSI Shadow wordmark in `brand/terminal/`. Redraw the pixel logo by hand at build time; the current one is a downscale and reads slightly soft.

## Favicon
`brand/favicon/`. Sizes 16–48 use the flat mark, which reads as a silhouette plus the red chamber at that size. Includes `favicon.ico` and `apple-touch-icon.png`.

## Banner
`brand/banner/septum-readme-banner.png` (1280×320). Not made yet: an animated README banner.
