---
layout: post
title: Developing a PeerTube plugin
category: CC plugin
comments: false
---

While enabling [Creative Commons licences for PeerTube videos]({% post_url 2021-05-10-peertube-licences %}) in accordance with the [CC Platform Toolkit](https://creativecommons.org/platform/toolkit/), we want to make sure that the new functionality we develop operates well with the existing PeerTube code base, fits the PeerTube design and is easy to integrate for users who want to use this feature. PeerTube's [plugin architecture](https://docs.joinpeertube.org/contribute-plugins) lets us achieve these goals. In this post we'll walk through our experience of creating a PeerTube plugin to add Creative Commons licences to PeerTube videos.

The [plugin we've developed](https://github.com/beeldengeluid/peertube-plugin-creative-commons/) does three things:
1. Update the labels used for PeerTube licences
1. Display the appropirate CC licence icon linked to the respective CC licence deed
1. Insert machine-readable metadata, to aid with search & discovery

In this post we'll roughly follow the steps from the [Write a plugin/theme](https://docs.joinpeertube.org/contribute-plugins?id=write-a-plugintheme) guide, provided as part of the PeerTube documentation:

1. [Find a name for your plugin](#find-a-name-for-your-plugin)
1. [Clone the quickstart repository](#clone-the-quickstart-repository)
1. [Configure your repository](#configure-your-repository)
1. [Update README.md](#update-readmemd)
1. [Update package.json](#update-packagejson)
1. [Write code](#write-code)
1. [Build your plugin](#build-your-plugin)
1. [Test your plugin](#test-your-plugin)
1. [Publish your plugin on NPM](#publish-your-plugin-on-npm)

While the plugin has reached version 1.0, we'll continue to add updates. You can access the source code in the state at time of publishing [here](https://github.com/beeldengeluid/peertube-plugin-creative-commons/tree/cb5b99d635c4fcf6e6bd30a11fc85f48a46d29c6).

## Find a name for your plugin

PeerTube Plugin names:
- can only contain lowercase letters and the hyphen (`-`) sign
- should start with the `peertube-plugin-` prefix

We went for `peertube-plugin-creative-commons`.

## Clone the quickstart repository

We clone the PeerTube Plugin Quickstart boilerplate code into a folder with our plugin name:

```bash
$ git clone https://framagit.org/framasoft/peertube/peertube-plugin-quickstart.git peertube-plugin-mysupername
```

## Configure your repository

Assuming we have already set up a repository to act as origin (e.g. `https://your-git-repo`), we set it as the remote URL of the repo we just cloned locally.

```bash
$ cd peertube-plugin-mysupername
$ git remote set-url origin https://your-git-repo
```

## Update README.md

We update the `README.md` file to include information about our plugin. See the [README file](https://github.com/beeldengeluid/peertube-plugin-creative-commons/blob/master/README.md) in our plugin for reference.

## Update package.json

Update the following `package.json` fields:
   * `name`
   * `description`
   * `homepage`
   * `author`
   * `bugs`
   * `engine.peertube` (the PeerTube version compatibility, must be `>=x.y.z` and nothing else)

Don't update or remove other keys. See [PeerTube's note](https://docs.joinpeertube.org/contribute-plugins?id=update-packagejson) on how to leave `staticDirs` and `clientScripts` empty.

See the [package.json](https://github.com/beeldengeluid/peertube-plugin-creative-commons/blob/master/package.json) in our plugin for reference.

## Write code

_Note: A live local environment is essential for testing your work during development, so if you're coding along, you might want to jump to [testing your plugin](#test-your-plugin) and come back when you have a test setup with a local PeerTube instance in place._

This is where the magic happens. It is also where the PeerTube docs come in handy, and the [introduction to the concepts](https://docs.joinpeertube.org/contribute-plugins?id=concepts) of hooks, static files, CSS, Server API and Client API is especially helpful review before jumping into plugin development.

The [PeerTube Plugin Quickstart](https://framagit.org/framasoft/peertube/peertube-plugin-quickstart) is a bit bare-bones and we would have liked to find at least some hello world example code snippet sprinkled in there. Still, it gives us a nice structure and decent idea of where to start our implemention. Depending on your plugin ideas, you might also find helpful inspiration in Framasoft's [official plugins repository](https://framagit.org/framasoft/peertube/official-plugins).

The following sections reflect on three different goals of the Creative Commons plugin: updating licence labels, displaying CC licence icons on video watch pages, inserting licence metadata on video watch pages.

### Updating licence labels

We'd like to update the licences available on a PeerTube instance. Technically, PeerTube licences are constants, [which can be updated](https://docs.joinpeertube.org/contribute-plugins?id=update-video-constants) by using the `videoLicenceManager`.

In our plugin's [`main.js`](https://github.com/beeldengeluid/peertube-plugin-creative-commons/blob/cb5b99d635c4fcf6e6bd30a11fc85f48a46d29c6/main.js) we first remove the 7 existing licences, then add 7 licences using their official CC labels, as well as an [8th licence]({% post_url 2021-05-15-the-8th-license %}) for the [Public Domain Mark](https://creativecommons.org/publicdomain/mark/1.0/):

```js
async function register ({
  registerHook,
  videoLicenceManager,
}) {

  videoLicenceManager.deleteLicence(1)
  videoLicenceManager.deleteLicence(2)
  videoLicenceManager.deleteLicence(3)
  videoLicenceManager.deleteLicence(4)
  videoLicenceManager.deleteLicence(5)
  videoLicenceManager.deleteLicence(6)
  videoLicenceManager.deleteLicence(7)
  
  videoLicenceManager.addLicence(1, 'CC BY 4.0')
  videoLicenceManager.addLicence(2, 'CC BY-SA 4.0')
  videoLicenceManager.addLicence(3, 'CC BY-ND 4.0')
  videoLicenceManager.addLicence(4, 'CC BY-NC 4.0')
  videoLicenceManager.addLicence(5, 'CC BY-NC-SA 4.0')
  videoLicenceManager.addLicence(6, 'CC BY-NC-ND 4.0')
  videoLicenceManager.addLicence(7, 'CC0 1.0')
  videoLicenceManager.addLicence(8, 'Public Domain Mark 1.0')

}
```

### Displaying CC licence icons on video watch pages

[Displaying a licence icon]({% post_url 2021-05-20-license-link-button %}) linked to the appropriate licence deed happens on the client side. PeerTube plugins package their client side functionality in client scripts, each with their own scope, so they are only loaded when needed. Since we are interested in displaying licence information along with videos on their respecitive 'Video Watch' pages, we define a `video-watch-client-plugin.js` client script with the `video-watch` scope in our `package.json`:

```js
"clientScripts": [
  {
    "script": "client/video-watch-client-plugin.js",
    "scopes": [
      "video-watch"
    ]
  }
],
```

This `video-watch-client-plugin.js` client script has a `label`, `image` and `href` for each of the newly added licences, mapped to the appropriate numerical key. 

```js
const CC_VIDEO_LICENCES = {
  1: {
    label: "CC BY 4.0",
    image: "https://licensebuttons.net/l/by/4.0/80x15.png",
    href: "https://creativecommons.org/licenses/by/4.0/" 
  },
  2: {
    label: "CC BY-SA 4.0",
    image: "https://licensebuttons.net/l/by-sa/4.0/80x15.png",
    href: "https://creativecommons.org/licenses/by-sa/4.0/" 
  },
  3: {
    label: "CC BY-ND 4.0",
    image: "https://licensebuttons.net/l/by-nd/4.0/80x15.png",
    href: "https://creativecommons.org/licenses/by-nd/4.0/" 
  },
  4: {
    label: "CC BY-NC 4.0",
    image: "https://licensebuttons.net/l/by-nc/4.0/80x15.png",
    href: "https://creativecommons.org/licenses/by-nc/4.0/" 
  },
  5: {
    label: "CC BY-NC-SA 4.0",
    image: "https://licensebuttons.net/l/by-nc-sa/4.0/80x15.png",
    href: "https://creativecommons.org/licenses/by-nc-sa/4.0/" 
  },
  6: {
    label: "CC BY-NC-ND 4.0",
    image: "https://licensebuttons.net/l/by-nc-nd/4.0/80x15.png",
    href: "https://creativecommons.org/licenses/by-nc-nd/4.0/" 
  },
  7: {
    label: "CC0 1.0",
    image: "https://licensebuttons.net/l/zero/1.0/80x15.png",
    href: "https://creativecommons.org/publicdomain/zero/1.0/" 
  },
  8: {
    label: "Public Domain Mark 1.0",
    image: "https://licensebuttons.net/l/publicdomain/80x15.png",
    href: "https://creativecommons.org/publicdomain/mark/1.0/"
  }
}
```

We use this data to hydrate the `video` object with the appropriate `image` and `href`, based on its `licence.id`:

```js
registerHook({
  target: 'filter:api.video-watch.video.get.result',
  handler: video => {
    if (video.licence.id >= 1 && video.licence.id <= 8) {
      video.licence.image = CC_VIDEO_LICENCES[video.licence.id].image
      video.licence.href = CC_VIDEO_LICENCES[video.licence.id].href
    }
    return video
  }
})
```

To insert this info in the form of a licence icon, we construct a new element for it:

```js
const licence_span = document.createElement('span')
licence_span.className = 'cc-licence'
licence_span.innerHTML = ' • '

const licence_link = document.createElement('a')
licence_link.rel = 'license'
licence_link.href = video.licence.href
licence_link.target = '_blank'

const licence_button = document.createElement('img')
licence_button.src = video.licence.image

licence_link.appendChild(licence_button)
licence_span.appendChild(licence_link)
```

and insert it in the elements that we want to target. The `.video-info-date-views` selector matches the date & views info component below the title on both narrow and wide screens:

```js
const video_info_date_views = document.querySelectorAll('.video-info-date-views')

for (let element of video_info_date_views) {
  element.insertAdjacentHTML('beforeend', licence_span.outerHTML)
}
```

An example of the resulting licence icon in action on [peertube.linuxrocks.online](https://peertube.linuxrocks.online/videos/watch/fe8a4ec1-2ee0-4d23-bed5-14e3b8921ec1):

![Screenshot CC license button](/extending-peertube/screenshots/screenshot_cc_linkbutton.png)




### Inserting licence metadata on video watch pages

Besides displaying a licence icon, we want to [add machine-readable metadata]({% post_url 2021-05-25-license-metadata %}), so that CC licensed PeerTube videos can be found and indexed by external search engines. 

We select our target elements:

```js
const video_info = document.querySelectorAll('.video-info')
const video_info_name = document.querySelectorAll('.video-info-name')
const account_page_link = document.querySelector('[title="Account page"]');
```

and insert the appropriate metadata:
```js
// Set CC-REL metadata

for (let element of video_info) {
  element.setAttribute('xmlns:dct', 'http://purl.org/dc/terms/')
  element.setAttribute('xmlns:cc', 'https://creativecommons.org/ns#')
}

for (let element of video_info_name) {
  element.setAttribute('property', 'dct:title')
}

if (account_page_link) {
  account_page_link.firstElementChild.setAttribute('property', 'cc:attributionName')
  account_page_link.setAttribute('rel', 'cc:attributionURL dct:creator')
  account_page_link.setAttribute('href', account_page_link.href)
}

```

## Build your plugin

Following the [PeerTube plugin](https://docs.joinpeertube.org/contribute-plugins?id=build-your-plugin) guide:

If you added client scripts, you'll need to build them using webpack.

Install webpack:

```
$ npm install
```

Add/update your files in the `clientFiles` array of `webpack.config.js`:

```
$ $EDITOR ./webpack.config.js
```

Build your client files:

```
$ npm run build
```

## Test your plugin

With our our client scripts built, we can now run a local PeerTube instance and install our plugin for testing.

Follow the [contributing](https://github.com/Chocobozzz/PeerTube/blob/develop/.github/CONTRIBUTING.md#develop) and [dependencies](https://github.com/Chocobozzz/PeerTube/blob/develop/support/doc/dependencies.md) docs to clone the PeerTube repository, install dependencies and prepare the database.

The [plugin guide](https://docs.joinpeertube.org/contribute-plugins?id=test-your-plugintheme) neatly breaks down the next steps:

Build PeerTube (`--light` to only build the english language):

```
$ npm run build -- --light
```

_On mac, you might run into an error `declare: -A: invalid option`, referenced in [this issue](https://github.com/Chocobozzz/PeerTube/issues/3859). I ended up fixing this by changing `#!/bin/bash` to `#!/usr/bin/env bash` in `scripts/build/client.sh`_

Build the CLI:

```
$ npm run setup:cli
```

Run PeerTube (you can access to your instance on http://localhost:9000):

```
$ NODE_ENV=test npm start
```

Register the instance via the CLI:

```
$ node ./dist/server/tools/peertube.js auth add -u 'http://localhost:9000' -U 'root' --password 'test'
```

Then, you can install or reinstall your local plugin/theme by running:

```
$ node ./dist/server/tools/peertube.js plugins install --path /your/absolute/plugin-or-theme/path
```

After this final step you should get a satisfying `Plugin installed` logged to your console. Reloading your local PeerTube instance should now reflect the changes you've made to your plugin code!

## Publish your plugin on NPM

TBC