---
layout: post
title: Introducing Extending Peertube
---

This project aims to extend [PeerTube](https://joinpeertube.org/) to support the availability, accessibility, and discoverability of large-scale public media collections on the [next generation internet](https://www.ngi.eu/).

Although PeerTube is technically capable to support the distribution of large public media collections, the platform currently lacks practical examples and extensive documentation to achieve this in a timely and cost-efficient way. This project will function as a proof-of-concept that will showcase several compelling improvements to the PeerTube software by:

1. developing and demonstrating the means needed by migrating a large corpus of open video content
2. implementing trustworthy open licensing metadata standards for video publication through PeerTube
3. emphasizing the importance of accompanying subtitle files by recommending ways to generate them

## Video content migration

We will test the improvements made to PeerTube and the auxiliary tools such as the content ingestion and redirection tools created within the project with a large real-world test corpus. Improvements to PeerTube are upstreamed, and a release version of all auxiliary tools is published online under an open source license. In order to facilitate further take up for similar use cases, we will deliver an online guide in an open format to help other interested parties.

## Open licensing

Having a clear licensing model for legally sharing public media content through PeerTube, and also being able to clearly propagate the legal conditions attributed to a piece of content to search engines and the end users will add to the proposition of PeerTube as an alternative platform for (non-profit) organizations to host and distribute their public media collections.

- Updated frontend display of the various Creative Commons standard licenses (visibility and search)
- Implementation of the [CC-REL standard](https://www.w3.org/Submission/ccREL/) (machine-readable metadata format for discovery) and assist in the scraping of CC-REL data published through PeerTube instances, for the benefit of indexing, search, and retrieval of Creative Commons licensed videos.
- Changes to the data model for Creative Commons license storage (license chooser and multilingual readability)

## Subtitling

Subtitles are an important qualitative instrument to improve discoverability and accessibility. In this task we improve the documentation on the use of subtitles and recommend ways to obtain or generate subtitle files.
