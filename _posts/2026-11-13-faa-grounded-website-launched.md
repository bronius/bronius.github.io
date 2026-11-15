---
layout: post
title: "If the FAA Grounds You, Let Your Dreams Take Flight!"
date: 2026-11-15 10:20:57 -0600
categories:
description: "Stuck at Austin-Bergstrom during the November 13, 2026 FAA nationwide ground stop, I finally built the Old West cartoon website I'd sketched 15 years ago, with Claude Code, Gemini Nano Banana and Jekyll on GitHub Pages."
image:
  path: /assets/images/bronius-com-old-west-redesign-og.jpg
  width: 1200
  height: 630
  alt: "The hanging Bronius sign on a cartoon Old West general store porch"
---

**New!** From the project lab of Bronius Motekaitis: <em>Texas-style web design!</em>

<div class="media-placeholder">
  <img src="{{ "/assets/images/bronius-com-old-west-redesign.jpg" | relative_url }}"
       width="1200" height="896"
       alt="A hand-painted cartoon Old West main street seen from a general store porch, with a wooden Bronius sign hanging from rope over the boardwalk">
</div>

Just launched: the all-new <a href="https://bronius.com">bronius.com</a>, a vanity domain I've owned since 2000, rebuilt in an afternoon the FAA handed me for free.

The concept has been in my head for years: a 1940s cartoon Old West main street, seen from the porch, with a hanging "Bronius" sign swaying in the breeze. Go ahead and grab the sign and give it a shove. It swings.

## Background

When I graduated with a Bachelor of Computer Science from Sam Houston State University in 2000, I treated myself to the bronius.com vanity domain. It started as a Shockwave Flash animation to impress my friends, followed by basic résumé info. Later it became a Drupal site for blogging about DevOps and other niche problems I'd solved (because that's what we do in open source: one part back scratch, two parts vanity). Eventually it went by the wayside, because real life took over. Somewhere along the way I sketched a Tex Avery–style western cartoon backdrop (think Droopy) with a hanging sign.

My brain has always been an idea factory, turning out zany concepts that shine like gold to me long before anyone else can see them. These days I know how that engine runs, and I've built the habits to point it at a finish line: write it down, break it into chunks, ship it. This site is one of those ideas, finally run all the way through.

## Grounded at AUS on Friday the 13th

Fast forward to Friday, November 13, 2026. Part of my family was waiting at Austin-Bergstrom International Airport (AUS) when the departure board started turning red. At 3:54 p.m. Eastern, the FAA issued a [nationwide ground stop](https://www.cbsnews.com/news/faa-issues-nationwide-ground-stop/): every departing flight in the United States held at the gate after a communications failure hit the Air Route Traffic Control Centers that run the country's en-route airspace. It was only the second nationwide ground stop since 9/11 (the last was the January 2023 NOTAM outage). The stop lasted a bit over four hours, FlightAware counted more than 9,000 cancellations by the end of the day, and ours was one of them.

All around us, phones were out, rebooking lines were forming, and everyone was refreshing their airline app. I did the math instead. No plane was going anywhere, nothing I did would change that, and I had a phone, a charger, and a block of time nobody could schedule over. So I opened Claude Code and GitHub and took a 15-year-old idea off the shelf. While the national airspace rebooted, I booted up a website.

## Process

I started in Gemini on my phone, describing a scene to Nano Banana until the mood, palette and style were right. Once I was happy with it, I gave AI Mode one more task: describe this scene so a generative AI could reproduce it as a website on desktop and mobile.

My prompt was loose, and Gemini happily overdelivered. Along with the image and a starting prompt, it threw in seed HTML and CSS.

I fed all of that to Claude Code and asked it to cut it up and fill it with the existing bronius.com content. Before generating anything, I had it write a set of design docs (concept, layout, design tokens, assets, interaction, architecture, art production) plus a single status file for handoffs, so each focused session could pick up where the last one left off without re-burning context or tokens.

With the docs in place, we built a static HTML prototype on a working branch of my existing GitHub Pages repo, since `main` is a Jekyll site that publishes on every merge. Working right in the repo mattered: plenty of edits were faster by hand than by prompting, and the art had to come from outside Claude. (I did try Claude-drawn vector art. It looked like Corel Graphics had taken over PowerPoint!)

Then came the art run: the GitHub app open to read my artwork-prompts doc one asset at a time, the Gemini app to paste Nano Banana prompts and download the results, and GitHub in the browser, the only way to bulk-upload all 18 images. My phone's tab switcher got a real workout. I hopped over to desktop to rename every file to match its intent, then learned Claude could have done that for me. It burned tokens double-checking my work anyway 😂

Every asset was painted on a green chroma background, so Claude wrote a Python pipeline to key them. It unmixes each pixel against a local key-colour field (so soft gradients and interior holes survive), despills the green fringe, and exports AVIF and WebP at 1× and 2×. Eighteen masters become 80 web-ready files in about 45 seconds, byte-for-byte reproducible. The site itself is plain modern CSS and a little vanilla JavaScript, with no framework and no bundler, and every word on the page is live HTML over the paintings.

Then Claude and I weighed a rewrite against staying on Jekyll, and we agreed that keeping Jekyll and launching straight from `main` was cheaper and simpler.

I jumped in the shower, and before I was out, my new site was live.

## Epilogue

At a concert, I showed it off to my son, and he filed the first bug report: the header sign and nav stay floating over subpage content as you scroll. Good catch, and it's first in line for the next pass. Ship fast, then hand it to your toughest critic 😉
