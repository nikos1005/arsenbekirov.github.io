# Repository Weight Report

Created: 2026-09-13
Purpose: document large committed binary files and the size of Git history. **No files were deleted or moved** — this is an inventory and a decision memo for the site owner.

## Large committed files

| File | Size | Referenced by site? |
|---|---|---|
| `downloads/qizim-video.mp4` | 36.1 MB (36,084,551 B) | Not referenced in any HTML/CSS/JS |
| `media/press/short-tek-A.mp4` | 34.5 MB (34,544,483 B) | Not referenced in any HTML/CSS/JS |
| `media/press/short-tek-B.mp4` | 26.3 MB (26,297,728 B) | Not referenced in any HTML/CSS/JS |
| `media/press/short-tek-C.mp4` | 24.6 MB (24,610,014 B) | Not referenced in any HTML/CSS/JS |

Total: **~121.5 MB** of committed video, none of it linked from any page.

## History size

`.git` directory: **~513 MB**. The largest contributor is binary video content committed
and re-committed across history (each edit of a binary file stores a new full copy).

## Why this matters

- Every fresh `git clone` downloads all history including these videos → slow setup for collaborators and CI.
- GitHub Pages serves whatever is committed; unused 120 MB of video also inflates the deployable tree.
- Pushes touching these files re-upload large blobs; pushes get slower over time.

## Options

1. **Move videos to GitHub Releases** (attach to a release, link or download from there).
   - ✅ Free, keeps files on GitHub, shrinks the working tree; repo history stays but future commits stop growing it.
   - ❌ Does not shrink the existing `.git` history by itself; release assets have a 2 GB-per-file limit (not an issue here).
2. **Move videos to an external CDN / object storage** (e.g. Cloudflare R2, Backblaze B2, S3).
   - ✅ Removes weight from both tree and future history; proper delivery for video content; cheapest bandwidth at scale.
   - ❌ Extra service and cost; links must be updated wherever the videos are used (currently nowhere).
3. **git-lfs** (Large File Storage).
   - ✅ Working tree stays clean; LFS objects served separately; good if videos must remain part of the repo workflow.
   - ❌ Requires LFS install for every collaborator; GitHub LFS free quota is 1 GB storage / 1 GB month bandwidth — these 121 MB plus traffic could exceed it; **history must still be rewritten** to move already-committed blobs into LFS.
4. **Leave as is.**
   - ✅ Zero effort, zero risk; site works fine today.
   - ❌ ~513 MB `.git` keeps growing with any future binary edits; clones stay slow.

## Recommendation

Move the four unused videos to **GitHub Releases** first (quick, non-destructive, frees
~121 MB from the working tree), and only if video publishing becomes a regular need,
consider an object-storage CDN. **Do not rewrite Git history** unless clone time becomes a
real problem for collaboration — and if it ever does, make a fresh backup clone and use
`git filter-repo` deliberately, never as a routine cleanup.

STATUS: awaiting owner decision — no files were deleted or moved.
