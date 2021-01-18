# Update git PeerTube fork

```sh
git remote add upstream https://github.com/Chocobozzz/PeerTube.git
git fetch upstream
git checkout develop
git merge upstream/develop
git push
```