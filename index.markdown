---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
custom_css: profile-sections
author: bronius
seo:
  type: Person
  name: Bronius Motekaitis
  links:
    - https://www.linkedin.com/in/bronius
    - https://bcswebstudio.com
    - https://recovery-kit.com
    - https://mypocketpm.com
    - https://www.flickr.com/photos/foryou/
    - https://x.com/bronicat
    - https://www.facebook.com/bronius.motekaitis
---

I try to live a life where faith, family, music, work, and community fit together instead of competing for separate corners. If you are here out of curiosity or skepticism, I hope this site gives you a quick sense of what that looks like in real life.

<div class="intro-grid">
  <section class="intro-card">
    <h2>Music</h2>
    <p>Classical violin, choral singing, local ensembles, and a teaching studio
    boosting student confidence and skill.</p>
    <p><a href="/music/">Read the music story</a></p>
  </section>
  <section class="intro-card">
    <h2>Professional</h2>
    <p>Software development, open source, cloud infrastructure, solutions
    architecture, and practical problem solving.</p>
    <p><a href="/professional/">See the professional overview</a></p>
  </section>
  <section class="intro-card">
    <h2>Life &amp; Faith</h2>
    <p>College Station roots, family life, faith, and the habit of looking past
    my own assumptions.</p>
    <p><a href="/life/">Visit life &amp; faith</a></p>
  </section>
</div>

<div id="flickr-photo" class="media-placeholder">
  <strong>From the Flickr stream</strong>
  <p class="flickr-photo-status">Loading a photo…</p>
</div>

<script>
(function () {
  var container = document.getElementById('flickr-photo');
  var statusEl = container.querySelector('.flickr-photo-status');
  var flickrUserId = '44124284196@N01';
  var callbackName = 'renderFlickrPhoto';

  function showFallback() {
    statusEl.innerHTML = 'Photos are unavailable right now. <a href="https://www.flickr.com/photos/foryou/" target="_blank" rel="noopener">Visit the Flickr stream</a>.';
  }

  window[callbackName] = function (feed) {
    delete window[callbackName];
    if (!feed || !feed.items || !feed.items.length) {
      showFallback();
      return;
    }
    var photo = feed.items[Math.floor(Math.random() * feed.items.length)];
    var imageUrl = photo.media.m.replace('_m.jpg', '_c.jpg');
    var title = photo.title || 'A photo from the stream';
    var link = document.createElement('a');
    link.href = photo.link;
    link.target = '_blank';
    link.rel = 'noopener';
    var img = document.createElement('img');
    img.src = imageUrl;
    img.alt = title;
    img.loading = 'lazy';
    link.appendChild(img);
    var caption = document.createElement('p');
    caption.textContent = title;
    container.innerHTML = '<strong>From the Flickr stream</strong>';
    container.appendChild(link);
    container.appendChild(caption);
  };

  var script = document.createElement('script');
  script.src = 'https://www.flickr.com/services/feeds/photos_public.gne?id=' + flickrUserId + '&lang=en-us&format=json&jsoncallback=' + callbackName;
  script.onerror = showFallback;
  document.body.appendChild(script);
})();
</script>
