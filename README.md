# WORK IN PROGRESS. #
## Please don't fork or clone this repository until I've removed this from the top of the README.md file ##

4st Attack is a four-in-a-row/connect-4 style puzzle game which can be played against the computer or another player across a network connection.  It was created by Jeroen Vloothuis in the early 2000's with help from a few collaborators, and published on Sourceforge at [ForcedAttack.sf.net](http://forcedattack.sf.net) under the GPL license.  In 2012, [PortableApps.com](https://portableapps.com) released [4st Attack Portable](https://portableapps.com/apps/games/4st-attack-portable) using the binaries from the Windows build of version 2.0 (the last version for which Jeroen Vloothuis released a Windows build).  I've seen it listed in the [list of Outdated Official PortableApps.com Apps](https://portableapps.com/development/outdated), and looked at the "Windows build unavailable **" explanation for a long time and I decided to look into what it would take to build it for Windows a while back, with the plan being to release the resulting Windows build(s) for PortableApps.com to use in an updated version of 4st Attack Portable.  Now I've taken the time to clean up the repository I built and publish it.

In this repository you'll find 2 branches: `sourceforge-releases`, which contains a commit corresponding to each of the tarballs that were released on Sourceforge, each tagged as `sf-<version>` where `<version>` is the version number that it was originally released as, and `master`, which contains the work I did to clean things up a bit, and make Windows builds of each version starting with 2.0.  When I felt each version was acceptable I tagged it as `v<version>`, again where `<version>` is the version number that the original source that I made slight modifications to was released as.
