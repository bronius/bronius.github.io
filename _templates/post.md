---
# Copy to _posts/YYYY-MM-DD-slug.md. (_templates/ is ignored by Jekyll.)
layout: post
title: "Post Title"
date: YYYY-MM-DD HH:MM:SS -0600     # past or present, or Pages won't build it
categories:
description: "One or two sentences. Shown in search results and link previews."
# Social share card (Open Graph / Twitter via jekyll-seo-tag). Required:
# CI flags any post without image.path. 1200x630 JPG, ~100 KB, under
# /assets/images/<slug>-og.jpg. Keep the subject inside the center ~1000x525.
image:
  path: /assets/images/SLUG-og.jpg
  width: 1200
  height: 630
  alt: "What the share image shows"
---

<div class="media-placeholder">
  <img src="{{ "/assets/images/SLUG.jpg" | relative_url }}"
       width="WIDTH" height="HEIGHT"
       alt="Describe the in-post image">
</div>

Opening line.
