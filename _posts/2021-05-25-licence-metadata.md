---
layout: post
title: Licence metadata
category: CC plugin
comments: false
---

Adding a licence button is an improvement for the display of the licence and although you can already filter on licence on a PeerTube instance, it would help if CC licensed content can be found outside the platform (search & discovery). For this there already exists the so-called Creative Commons Rights Expression Language ([CC REL](https://wiki.creativecommons.org/wiki/CC_REL)).

> Creative Commons licences are expressed in three different formats: the human readable licence deed, the lawyer readable legal code, and the machine readable code. RDFa is one of the ways in which we've chosen to make our licences machine readable. By using RDFa CC licensed objects can be discovered by search engines and auto-discovery mechanisms without the need for a human to hand-curate content directories or lists.

RDFa is a W3C Recommendation that adds a set of attribute-level extensions to HTML, XHTML and various XML-based document types for embedding rich metadata within Web documents.

To make this work we added these attributes on the existing HTML of the PeerTube video page. Below you find an excerpt of the tags the plugin extends.

Example from [peertube.linuxrocks.online](https://peertube.linuxrocks.online/videos/watch/fe8a4ec1-2ee0-4d23-bed5-14e3b8921ec1):


```html
<div class="video-info" xmlns:dct="http://purl.org/dc/terms/" xmlns:cc="https://creativecommons.org/ns#">

  <h1 class="video-info-name" property="dct:title">Journey Running on Linux with Proton 6.3-4</h1>

  <span class="cc-licence">
   • <a rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank">
       <img src="https://licensebuttons.net/l/by-nc-nd/4.0/80x15.png">
     </a>
  </span>

  <a title="Account page" href="https://peertube.linuxrocks.online/accounts/ekianjo" rel="cc:attributionURL dct:creator">
    <span property="cc:attributionName">ekianjo</span>
  </a>

</div>
```

All the tags except `<span class="cc-licence">` and it's contents are existing ones with added attributes like `property` and `rel` with their corresponding namespace identifiers.
