---
layout: post
title: PeerTube video licences
image: /assets/img/blog/creative-commons.png
description: >
  This project will follow the steps in Creative Commons toolkit, but tries to implement a solution which also respects the design philosophy of PeerTube. 
sitemap: false
---

When publishing your video on a PeerTube instance you have a default choice of 7 licences (or no licence as number 0) under which you want to license your video.

<!--more-->

Depending on the supported language you have chosen as a user (as a publisher or as a viewer) you will see these licenses translated in that language in the interface of PeerTube.

You might recognize these content licenses as Creative Commons licenses and from the source code it shows that they were intended as such.

[https://github.com/Chocobozzz/PeerTube/blob/master/server/initializers/constants.ts#L389](https://github.com/Chocobozzz/PeerTube/blob/master/server/initializers/constants.ts#L389)

```typescript
// See https://creativecommons.org/licenses/?lang=en
const VIDEO_LICENCES = {
  1: 'Attribution',
  2: 'Attribution - Share Alike',
  3: 'Attribution - No Derivatives',
  4: 'Attribution - Non Commercial',
  5: 'Attribution - Non Commercial - Share Alike',
  6: 'Attribution - Non Commercial - No Derivatives',
  7: 'Public Domain Dedication'
}
```

The problem with this setup has been raised some time ago in this issue:

[https://github.com/Chocobozzz/PeerTube/issues/726#issue-335568228](https://github.com/Chocobozzz/PeerTube/issues/726#issue-335568228)

> According to what @rigelk wrote on IRC, the option is supposed to present exact licences to choose from. If that's the case, the licences should be explicitly marked as such. Each licence name should therefore start with “Creative Commons”, or possibly take the abbreviated form of “CC”

Although this seems to be an easy small change, it still wouldn't be enough to make them function like an actual Creative Commons license (or any other license) from a legal standpoint, because of the following point raised in the same issue as above.

> The user should be provided with a link to the given licence, and not only at the selection, but also in the information box that's below each video being watched.

## Creative Commons toolkit

The excellent guide [CC Platform Toolkit](https://creativecommons.org/platform/toolkit/) shows the must-haves and best practices for implementing Creative Commons licenses in any content publishing platform. Apart from the issue above there are some more details that are of importance.

In our project 'Extending PeerTube' we will follow the steps in this toolkit, but try to implement a solution which also respects the design philosophy of PeerTube.
