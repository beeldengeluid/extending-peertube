---
layout: post
title: PeerTube extended
comments: false
---

This article describes the Extending PeerTube project which was executed by the [Netherlands Institute for Sound and Vision](https://www.beeldengeluid.nl/en) in the context of the [PublicSpaces initiative](https://publicspaces.net/). This project was funded through the [NGI Zero](https://nlnet.nl/NGI0/) Discovery Fund, a fund established by NLnet with financial support from the European Commission’s Next Generation Internet programme, under the aegis of DG Communications Networks, Content and Technology under grant agreement No 82532.2

### What is the project about?

Extending Peertube aims to extend PeerTube to support the availability, accessibility, and discoverability of large-scale public media collections on the next generation internet. 

As a national audiovisual heritage institute, we share thousands of collection items as open video content, which is free and open for everyone to reuse. In the past we've developed a custom solution to distribute this content, according to these open principles: [openimages.eu](https://openimages.eu/) 

Since, our custom solution has aged, while we see that sister organisations and partners in our international network have similar requirements to what we seek: open source technology, state-of-the-art video distribution and play-out and the ability to self host.

In this project we extend the open source video platform PeerTube to fit our use case, while sharing our code and insight upstream, for other users with a similar use case to also benefit from our efforts. All this to contribute to a vibrant open video sharing ecosystem.

All this fits with our long term vision to federate multiple large scale open video collections to build an international community to share and reuse our audiovisual heritage on the next generation internet.

### What problem does your project solve?

Although PeerTube is technically capable of supporting the distribution of large public media collections, the platform currently lacks practical examples and extensive documentation to achieve this in a timely and cost-efficient way. This project will function as a proof-of-concept that will showcase several compelling improvements to the PeerTube software by:

* developing and demonstrating the means needed for this end by migrating a large corpus of open video content
* implementing trustworthy open licensing metadata standards for video publication through PeerTube
* emphasizing the importance of accompanying subtitle files by recommending ways to generate them

### Migration

Since the original aim of PeerTube was to provide an alternative solution to YouTube as the dominant video sharing platform, it is optimized for the single user who wants to periodically upload their user generated content and share this as a single video within their own channel. Since our use case involves migrating multiple thousands of videos to a PeerTube instance, we worked on a toolkit and instructions to programmatically import large numbers of videos from a legacy video platform to PeerTube:

<https://beeldengeluid.github.io/extending-peertube/category/migration.html> 

This also included instructions on implementing URL redirection in PeerTube, after migrating from a large video streaming platform:

<https://beeldengeluid.github.io/extending-peertube/category/url-redirection.html>

### Creative Commons

In the cultural heritage domain, the standard for free and open sharing of resources on the web has been Creative Commons licenses for over a decade now. Although PeerTube already implemented an option for their users to attribute a 'license' to their contributions to a PeerTube instance, this solution wasn't (fully) compliant with Creative Commons.

As Sound and Vision values transparent and legally sound communication about the extent to which the collection items it shares on the web can be shared and reused by the public, it took upon itself the task of developing a Creative Commons compliant licensing plugin for PeerTube. 

This plugin extends PeerTube with the needed user interface elements to select and display the licenses, but also inserts the correct micro formats into the video item page, making the license also machine readable: 

<https://beeldengeluid.github.io/extending-peertube/category/cc-plugin.html>

### Subtitling

The final strand of work in the project looked at improving the accessibility and discoverability of videos within large collections hosted on a PeerTube instance. It provided a guide on using the PeerTube API to - at scale - add subtitles to an instance, and also suggested ways for existing video content to be enriched with subtitles, using open source Automatic Speech Recognition software: 

<https://beeldengeluid.github.io/extending-peertube/category/subtitles.html>

### For more information

We documented our progress here on this website and published our tools at:

<https://github.com/beeldengeluid/extending-peertube/>

Sound and Vision runs a self-hosted PeerTube instance at: 

<https://peertube.beeldengeluid.nl>

The Creative Commons plugin for PeerTube is maintained in a separate repository at: 

<https://github.com/beeldengeluid/peertube-plugin-creative-commons>

and published on NPM: 

<https://www.npmjs.com/package/peertube-plugin-creative-commons>
