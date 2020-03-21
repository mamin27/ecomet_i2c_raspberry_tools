# Lazarus Installation #

**Last update:** 21.03.2020
Author: Marian Minar

**Insalled at Raspberry PI 3+:**

### How to install? ###
```console
sudo apt-get install lazarus-ide
sudo apt-get install fpc lazarus
```

check installed software

``` console
$ apt search lazarus | grep installed

fpc-source-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 all [installed,automatic]
lazarus/stable,now 2.0.0+dfsg-2 all [installed]
lazarus-2.0/stable,now 2.0.0+dfsg-2 all [installed,automatic]
lazarus-doc-2.0/stable,now 2.0.0+dfsg-2 all [installed,automatic]
lazarus-ide/stable,now 2.0.0+dfsg-2 all [installed]
lazarus-ide-2.0/stable,now 2.0.0+dfsg-2 armhf [installed,automatic]
lazarus-ide-gtk2-2.0/stable,now 2.0.0+dfsg-2 armhf [installed,automatic]
lazarus-src-2.0/stable,now 2.0.0+dfsg-2 all [installed,automatic]
lcl-2.0/stable,now 2.0.0+dfsg-2 armhf [installed,automatic]
lcl-gtk2-2.0/stable,now 2.0.0+dfsg-2 armhf [installed,automatic]
lcl-nogui-2.0/stable,now 2.0.0+dfsg-2 armhf [installed,automatic]
lcl-units-2.0/stable,now 2.0.0+dfsg-2 armhf [installed,automatic]
lcl-utils-2.0/stable,now 2.0.0+dfsg-2 armhf [installed,automatic]

$ apt search fp | grep installed

fp-compiler/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-compiler-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-docs-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 all [installed,automatic]
fp-ide-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-units-base-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-units-db-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-units-fcl-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-units-fv-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-units-gfx-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-units-gtk2-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-units-math-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-units-misc-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-units-multimedia-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-units-net-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-units-rtl-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fp-utils-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 armhf [installed,automatic]
fpc/stable,now 3.0.4+dfsg-22+rpi1 all [installed]
fpc-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 all [installed,automatic]
fpc-source-3.0.4/stable,now 3.0.4+dfsg-22+rpi1 all [installed,automatic]

```

remote connection to raspberry:

```console
ssh -l pi -X <ip_address>
lazarus-ide
```