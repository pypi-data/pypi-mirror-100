<a href="http://outsideopen.com"><img src="https://cdn.pixabay.com/photo/2017/06/27/20/24/fire-hydrants-2448725_960_720.png" title="Outside Open" alt="Outside Open"></a>

# Digital Hydrant Collectors

> Open Source network information collector, developed for the Digital Hydrant project

## Installation

### Install using Flatpak (Work in progress!)

Install Flatpak for [your platform](https://www.flatpak.org/setup/)

```bash
sudo apt-get install flatpak
```

Digital Hydrant should be run as root. Flatpak does not allow running apps as `sudo`. To work around this problem, you should execute the app using the following command

```bash
sudo su -l root -c "flatpak run --share=network com.outsideopen.hydrant"
```




### Install from source

> clone this repository

```shell
$ git clone https://github.com/outsideopen/digital-hydrant-collectors.git
$ cd ~/digital-hydrant-collectors
$ sudo ./setup.py install
```

> Create a token for your device on the Digital Hydrant [website](https://digital-hydrant.herokuapp.com/manage/devices)
> Copy this value to your configuration file /etc/digital-hydrant/config.ini

```
$ [api]
  token = $MY_TOKEN
```

> start Digital Hydrant

```shell
$ sudo hydrant
```

---

## Features

- Easily add new collectors
- Build off existing network scanning tools
- Integrated logging
- Very flexible and configurable

## DH_cron

###### In order to schedule collector execution, Digital Hydrant uses a cron-like string with the following structure

- \<day of week(1-7)> \<days> \<hours> \<minutes> \<seconds>
- whichever value is populated first will be read as "every \<value> \<interval>" and the remaining values will be combined and read as "at \<values>"
  - examples:
    - \* 10 2 30 0 = "every 10 days at 2:30:00"
    - 5 \* \* 30 45 = "every thursday at 0:30:45"
- day of the week values start on Sunday (i.e. 1 = Sun... 7 = Sat)
- for DH_cron strings with the day of the week populated, the days value will be ignored
- if no schedule string is provided then the default value of \* \* \* \* \* will be used, indicating that the process should only be run once

## Contributing

### Step 1

- **Option 1**

  - 🍴 Fork this repo!

- **Option 2**
  - 👯 Clone this repo to your local machine using `https://github.com/outsideopen/digital-hydrant-collectors`

### Step 2

- **HACK AWAY!** 🔨🔨🔨

### Step 3

- 🔃 Create a new pull [request](https://github.com/outsideopen/digital-hydrant-collectors/compare)
---

## Build (Work in Progress!)

We use [Flatpak](https://www.flatpak.org/) to build for multiple Linux operating systems.

In order to build the app, you need `flatpak` and `flatpak-builder` installed

```
apt-get install flatpak flatpak-builder
```

Build the app using the following command:

```bash
sudo flatpak-builder --install build-dir com.outsideopen.hydrant.yml
```

It can be a useful debugging tool, to connect to the app using a shell:

```bash
sudo su -l root -c "flatpak run --command=sh --devel --share=network com.outsideopen.hydrant"
```

---

## FAQ

- Outside Open is a team of smart, passionate artists, photographers, cyclists, hikers, soccer players, parents, beekeepers, blacksmiths and tinkerers. What unites this disparate team is a love for building and integrating amazing technology to help their clients succeed. They think outside the “singular technical solution” box. They embrace solutions from both the standard corporate software/hardware world and the open source community. This sets them apart and enables them to provide highly customized and scaleable solutions. Outside Open was founded in 2012 by Trevor Young and Greg Lawler, two technology leaders with a love for technology and a desire to help others succeed.

---

## Support

Reach out at one of the following places!

- Website at <a href="http://outsideopen.com" target="_blank">`outsideopen.com`</a>

---
