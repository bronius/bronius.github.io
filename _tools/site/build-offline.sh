#!/bin/sh
# Build the site with GitHub Pages' Jekyll (3.10, --safe, whitelisted plugins) when rubygems is unreachable
# (e.g. the Claude sandbox). Gem sources are git-cloned from GitHub once into $GEMS and put on the load path.
#   _tools/site/build-offline.sh [DEST]        default DEST=/tmp/site
# Serve:  (cd /tmp/site && python3 -m http.server 8642)
set -eu
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
DEST=${1:-/tmp/site}
GEMS=${GEMS:-/tmp/gems}
mkdir -p "$GEMS"
fetch() { [ -d "$GEMS/$2" ] || git clone -q --depth 1 ${3:+--branch "$3"} "https://github.com/$1" "$GEMS/$2"; }
fetch jekyll/jekyll jekyll v3.10.0
fetch Shopify/liquid liquid v4.0.4
fetch gettalong/kramdown kramdown REL_2_4_0
fetch kramdown/parser-gfm kramdown-parser-gfm
fetch rouge-ruby/rouge rouge v3.30.0
fetch sporkmonger/addressable addressable addressable-2.8.7
fetch weppos/publicsuffix-ruby public_suffix v5.1.1
fetch octopress/colorator colorator v1.1.0
fetch ruby-i18n/i18n i18n v1.14.6
fetch ruby-concurrency/concurrent-ruby concurrent-ruby v1.3.4
fetch jekyll/mercenary mercenary v0.3.6
fetch envygeeks/pathutil pathutil
fetch envygeeks/forwardable-extended forwardable-extended
fetch dtao/safe_yaml safe_yaml
fetch jekyll/jekyll-feed jekyll-feed v0.17.0
fetch jekyll/jekyll-seo-tag jekyll-seo-tag v2.8.0
fetch jekyll/jekyll-sass-converter jekyll-sass-converter v1.5.2
fetch sass/ruby-sass ruby-sass stable
INC=""
for d in jekyll liquid kramdown kramdown-parser-gfm rouge addressable public_suffix colorator i18n mercenary \
         pathutil forwardable-extended safe_yaml jekyll-feed jekyll-seo-tag jekyll-sass-converter ruby-sass; do
  INC="$INC -I $GEMS/$d/lib"
done
INC="$INC -I $GEMS/concurrent-ruby/lib/concurrent-ruby"
PAGES=$(mktemp --suffix=.yml); printf 'whitelist: [jekyll-feed, jekyll-seo-tag]\n' > "$PAGES"   # what Pages allows
cd /tmp
JEKYLL_ENV=production ruby $INC "$GEMS/jekyll/exe/jekyll" build --safe -s "$ROOT" -d "$DEST" --config "$ROOT/_config.yml,$PAGES"
rm -f "$PAGES"
