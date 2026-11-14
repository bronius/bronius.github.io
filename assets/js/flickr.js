// Random photo from the Flickr stream, behind the painted polaroid window (home only).
// Loads on idle (no third-party request in the critical path); the caption button shuffles.
// JSONP: flickr.people.getPhotos twice (page count, then a random page of 1).

const fig = document.querySelector('.polaroid[data-flickr-key]');
if (fig) {
  const { flickrKey: key, flickrUser: user } = fig.dataset;
  const link = fig.querySelector('.polaroid__photo');
  const button = fig.querySelector('.polaroid__shuffle');
  const api = 'https://api.flickr.com/services/rest/?method=flickr.people.getPhotos'
    + `&api_key=${encodeURIComponent(key)}&user_id=${encodeURIComponent(user)}`
    + '&extras=url_z,url_n,url_m,url_s,description&format=json&per_page=1';
  let req = 0, prevPage = null, pages = null;

  function jsonp(url) {
    return new Promise((resolve, reject) => {
      const cb = `flickrCb${Date.now().toString(36)}${Math.random().toString(36).slice(2, 7)}`;
      const s = document.createElement('script');
      const done = () => { delete window[cb]; s.remove(); clearTimeout(timer); };
      const timer = setTimeout(() => { done(); reject(new Error('timeout')); }, 10000);
      window[cb] = data => { done(); data?.stat === 'ok' ? resolve(data) : reject(new Error(data?.message || 'flickr')); };
      s.src = `${url}&jsoncallback=${cb}`;
      s.onerror = () => { done(); reject(new Error('network')); };
      document.head.append(s);
    });
  }

  function render(photo) {
    const src = photo.url_z || photo.url_n || photo.url_m || photo.url_s
      || `https://live.staticflickr.com/${photo.server}/${photo.id}_${photo.secret}.jpg`;
    const title = photo.title || 'A random photo from my stream';
    const desc = photo.description?._content?.trim();
    const img = new Image();
    img.alt = title;
    img.decoding = 'async';
    img.onload = () => img.classList.add('is-loaded');
    img.src = src;
    link.href = `https://www.flickr.com/photos/${user}/${photo.id}/`;
    link.title = desc ? `${title}: ${desc.replace(/<[^>]+>/g, '')}` : title;
    link.replaceChildren(img);
  }

  async function shuffle() {
    const mine = ++req;
    fig.setAttribute('aria-busy', 'true');
    try {
      if (!pages) pages = (await jsonp(`${api}&page=1`)).photos.pages;
      let page = Math.floor(Math.random() * pages) + 1;
      if (pages > 1 && page === prevPage) page = page % pages + 1;
      prevPage = page;
      const data = await jsonp(`${api}&page=${page}`);
      if (mine === req && data.photos.photo.length) render(data.photos.photo[0]);
    } catch {
      if (mine === req && !link.querySelector('img'))
        link.querySelector('.polaroid__status').textContent = 'Photos are napping. Tap to visit the Flickr stream.';
    } finally {
      if (mine === req) fig.removeAttribute('aria-busy');
    }
  }

  button.addEventListener('click', shuffle);
  const idle = window.requestIdleCallback || (fn => setTimeout(fn, 1200));
  addEventListener('load', () => idle(shuffle, { timeout: 4000 }), { once: true });
}
