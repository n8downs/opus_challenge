# sitecrawler

This is a site crawler I wrote for an interview coding challenge. The idea here was to take a domain and create a site map of the static assets and links on each page. This crawler does not run JS, so it's only able to map the assets and links based on initial HTML responses.

As with most freshly-written software, I'd consider this really just a starting point for further iteration, depending on what types of problems we'd like to solve with this tool. What's here, though, demonstrates some good stuff: unit testing around network behavior (via real/fake dependencies), HTML parsing 

It's worth noting that I've taken as a given that we want to write something from scratch (in order to be able to evaluate my coding style/skills). In the "real world," we'd probably want to reuse an existing crawler tool like [Apache Nutch](http://nutch.apache.org/index.html).

Usage (OSX):
```
~ $ brew install python3
~ $ git clone git@github.com:n8downs/opus_challenge.git
~/sitecrawler $ s/install
~/sitecrawler $ s/runtests
~/sitecrawler $ s/map opusforwork.com
```

Example Output:
```
https://www.opusforwork.com/
  original_url: http://opusforwork.com
  assets:
    /css/main.css
    ../js/lib/cookie.js
    ../js/lib/zepto.js
    ../js/lib/fx.js
    ../js/lib/lodash.js
    ../js/lib/lodash-inflection.js
    ../js/lib/packery.js
    ../js/lib/riot.js
    ../js/lib/riotcontrol.js
    ../js/tags.js
    ../js/CompanyStore.js
    ../js/QuestionStore.js
    ../js/ApplicationStore.js
    ../js/ResultStore.js
    ../js/opus.js
  links:
    #testimony
    #testimony
    #app/1
    /js/opus.js
    /index.html
    /css/main.css
    /about/
    /faq/
    /browse/
    mailto:contact@opusforwork.com
https://www.opusforwork.com/about/
  assets:
    /css/main.css
    ../js/lib/cookie.js
    ../js/lib/zepto.js
    ../js/lib/fx.js
    ../js/lib/lodash.js
    ../js/lib/lodash-inflection.js
    ../js/lib/packery.js
    ../js/lib/riot.js
    ../js/lib/riotcontrol.js
    ../js/tags.js
    ../js/CompanyStore.js
    ../js/QuestionStore.js
    ../js/ApplicationStore.js
    ../js/ResultStore.js
    ../js/opus.js
  links:
    /
    /js/opus.js
    /index.html
    /css/main.css
    /about/
    /faq/
    /browse/
    mailto:contact@opusforwork.com
```
