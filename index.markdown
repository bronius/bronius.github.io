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
  <strong>Random photo from my Flickr stream (<a href="#" class="flickr-refresh">see another</a>)</strong>
  <p class="flickr-photo-status">Loading a photo…</p>
</div>

<script>
(function () {
  var container = document.getElementById('flickr-photo');
  var apiKey = '{{ site.flickr_api_key }}';
  var userId = '{{ site.flickr_user_id }}';
  var requestId = 0;
  var previousPage = null;
  var apiBase = 'https://api.flickr.com/services/rest/?method=flickr.people.getPhotos'
    + '&api_key=' + apiKey
    + '&user_id=' + encodeURIComponent(userId)
    + '&extras=url_c,url_z,url_n,url_m,url_s,description'
    + '&format=json'
    + '&per_page=1';

  function showFallback() {
    var statusEl = container.querySelector('.flickr-photo-status');
    if (!statusEl) {
      statusEl = document.createElement('p');
      statusEl.className = 'flickr-photo-status';
      container.appendChild(statusEl);
    }
    statusEl.innerHTML = 'Photos are unavailable right now. <a href="https://www.flickr.com/photos/foryou/" target="_blank" rel="noopener">Visit the Flickr stream</a>.';
  }

  function loadScript(src, onError) {
    var script = document.createElement('script');
    script.src = src;
    script.onerror = onError;
    document.body.appendChild(script);
  }

  function renderPhoto(photo) {
    var imageUrl = photo.url_c || photo.url_z || photo.url_n || photo.url_m || photo.url_s;
    if (!imageUrl) {
      // Fallback: construct the URL manually using Flickr's standard pattern.
      // Works for any public photo regardless of which size renditions exist.
      imageUrl = 'https://live.staticflickr.com/' + photo.server + '/' + photo.id + '_' + photo.secret + '.jpg';
    }
    var title = photo.title || 'A random photo from my stream';
    var description = photo.description && photo.description._content
      ? photo.description._content.trim()
      : '';
    var link = document.createElement('a');
    link.href = 'https://www.flickr.com/photos/' + userId + '/' + photo.id + '/';
    link.target = '_blank';
    link.rel = 'noopener';
    var img = document.createElement('img');
    img.src = imageUrl;
    img.alt = title;
    img.loading = 'lazy';
    link.appendChild(img);
    var caption = document.createElement('p');
    caption.textContent = description || title;
    container.innerHTML = '<strong>Random photo from my Flickr stream (<a href="#" class="flickr-refresh">see another</a>)</strong>';
    container.appendChild(link);
    container.appendChild(caption);
  }

  function fetchPhoto() {
    var currentRequest = ++requestId;
    var callbackName = 'renderFlickrPhoto' + currentRequest;
    var loadingStatus = container.querySelector('.flickr-photo-status');
    if (loadingStatus) {
      loadingStatus.textContent = 'Loading a photo…';
    }

    function handleError() {
      delete window[callbackName];
      if (currentRequest === requestId) {
        showFallback();
      }
    }

    // First call learns the number of pages; the second fetches a random page.
    window[callbackName] = function (data) {
      if (currentRequest !== requestId) {
        delete window[callbackName];
        return;
      }
      if (!data || data.stat !== 'ok' || !data.photos || !data.photos.pages) {
        handleError();
        return;
      }
      var pages = data.photos.pages;
      var randomPage = Math.floor(Math.random() * pages) + 1;
      if (pages > 1 && randomPage === previousPage) {
        randomPage = randomPage % pages + 1;
      }
      previousPage = randomPage;
      window[callbackName] = function (data2) {
        delete window[callbackName];
        if (currentRequest !== requestId) {
          return;
        }
        if (!data2 || data2.stat !== 'ok' || !data2.photos || !data2.photos.photo.length) {
          handleError();
          return;
        }
        renderPhoto(data2.photos.photo[0]);
      };
      loadScript(apiBase + '&jsoncallback=' + callbackName + '&page=' + randomPage, handleError);
    };
    loadScript(apiBase + '&jsoncallback=' + callbackName + '&page=1', handleError);
  }

  container.addEventListener('click', function (event) {
    if (event.target.closest('.flickr-refresh')) {
      event.preventDefault();
      fetchPhoto();
    }
  });

  fetchPhoto();
})();
</script>
