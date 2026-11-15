---
layout: post
title: "If the FAA Grounds You, Let Your Dreams Take Flight!"
date: 2026-11-15 10:20:57 -0500
categories:
description: "Stuck at Austin-Bergstrom during the November 13, 2026 FAA nationwide ground stop, I finally built the Old West cartoon website I'd sketched 15 years ago, with Claude Code, Gemini Nano Banana and Jekyll on GitHub Pages."
image: /assets/images/bronius-com-old-west-redesign.jpg
---

**New!** From the project lab of Bronius Motekaitis, I present <em>Texas-style web design!</em>:

<div class="media-placeholder">
  <img src="{{ "/assets/images/bronius-com-old-west-redesign.jpg" | relative_url }}"
       width="1200" height="750"
       alt="The redesigned bronius.com home page: a hand-painted Old West main street seen from a wooden porch, with a hanging Bronius sign, cloud navigation and wooden signposts">
</div>
Just launched: <a href="https://bronius.com">https://bronius.com</a>. My personal website on vanity domain that I've had since 2000 but got around to refreshing while waiting for a flight delay.

I had this design concept for many years but never the time nor particular motivation to go beyond drawing board until now. Funny -- everything of my concept centers around the hanging "Bronius" sign swaying in the breeze, but its physics are far from what I wanted 🤷

### Background

When I graduated with a Bachelor of Computer Science from Sam Houston State University in 2000, I treated myself to the bronius.com vanity domain. I had a simple shockwave flash animation to impress my friends followed by basic resume/CV info. Over time, I switched it to a Drupal site for blogging and sharing devops and other niche challenges overcome (bc that's what we do in open source: one part back scratch, two parts vanity). Eventually it all went by the wayside, bc real life took over. Somewhere along the way I had this Tex Avery western cartoon (see Droopy) style backdrop with a handing sign.

I did not know then that it was ADHD driving these zany ideas that sounded like gold to me but would wouldn't amount to a hill of beans and misprioritization to others. I just thought it was spunky youth, undiscovered talent, and the rest of the world can go stub their toe for not seeing it.

### Grounded at AUS on Friday the 13th

Fast forward to Friday, November 13, 2026. Part of my family was waiting at Austin-Bergstrom International Airport (AUS) when the departure board started turning red. At 3:54 p.m. Eastern, the FAA issued a [nationwide ground stop](https://www.cbsnews.com/news/faa-issues-nationwide-ground-stop/): every departing flight in the United States held at the gate after a communications failure hit the Air Route Traffic Control Centers that run the country's en-route airspace. It was only the second nationwide ground stop since 9/11 (the last was the January 2023 NOTAM outage). The stop lasted a bit over four hours, FlightAware counted more than 9,000 cancellations by the end of the day, and ours was one of them.

All around us, phones were out, rebooking lines were forming, and everyone was refreshing their airline app. I did the math instead. No plane was going anywhere, nothing I did would change that, and I had a phone, a charger, and a block of time nobody could schedule over. So I opened Claude Code and GitHub and took a 15-year-old idea off the shelf. While the national airspace rebooted, I booted up a website.

## Process

I started with a generic scene description to get the mood, palette, and style established in Gemini/Nano Banana, right from Google in the browser on my phone! once satisfied, I gave AI Mode one more task: Describe this scene, mood, etc for generative AI to be able to produce the same image as a website in desktop and mobile.

I was too loose in my prompt, and Gemini happily gave me way more than an image and starting prompt: it also gave some seed html and css!

I fed all that into Claude Code, asking it to chop it up and use the existing bronius.com content to seed it. Before generating anything at all, I also channeled it to make a set of working documents so we could pick up between focused working sessions to preserve context and conserve tokens.

With design planning docs in place, we set out to build the static html prototype: while I was already wired into my existing GitHub Pages repo (for this site), we were working in a non-main working branch, bc main is a Jekyll site that automatically publishes on merge. Working in my GitHub repo was important, however, bc a lot of edits coming up were cheaper to do by hand (not promoting), and image generation could not be done in Claude (I did try, and vector looked like....like Corel Graphics had taken over PowerPoint!)

Now juggling between GitHub App to read my artwork prompts doc one artifact at a time, Gemini App to copy/paste Nano Banana prompts and download generated images, and GitHub in the browser (the only way I could bulk upload all 18 seed images), I was giving tab switching on my phone a real workout! I did have to pop over to desktop to review and rename all the filenames to match their respective intent -- though I could have easily had Claude do that, it turns out! After all, it still burned some tokens checking my work 😂

With artwork generated against green pixel background, Claude whipped up a .py script to convert them to proper transparency and compress for web delivery.

Then Claude and I had a little discussion about replace or launch from working branch, and we both agreed on the cheaper, simpler benefits of keeping in Jekyll and merging into and launching from main.

I jumped in the shower and before I was out, my new site was launched!

## Epilogue

At a concert, I'm showing this off to my son, and he pointed out my bad UX of having the header icons stay floating over subpage content. In my elation to have seen through my original 15 year old vision, I overlooked the basic UX review 😅 Life lesson: if it comes too easy, it's too easy to overlook the common details.

Fortunately, it will also be really simple to overcome if I ever feel like coming back to it 😉