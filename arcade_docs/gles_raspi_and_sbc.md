# OpenGL ES Devices: Raspberry Pi, Etc
Arcade normally requires OpenGL to render, but it also supports devices with the right versions of OpenGL ES. If you’re familiar with the topic, you may want to skip to [Supported OpenGL ES Versions](#requirements-gles) below.
## OpenGL ES
[OpenGL ES](gles_def) (“embeddedable subset”) is a special variant of OpenGL tailored for mobile and embedded devices.
Like the standard OpenGL API, it has both feature versions and optional extensions.
## Supported Raspberry Pi Configurations
As of October 2024, the Arcade and [pyglet](https://pyglet.readthedocs.io/en/development/) teams verified the following to work:
  * [Raspberry Pi 4](rpi_4) running [Raspberry Pi OS](https://www.raspberrypi.com/software/)
  * [Raspberry Pi 5](rpi_5) running [Raspberry Pi OS](https://www.raspberrypi.com/software/)


Although the [Raspberry Pi 400](rpi_400) has never been tested, it _may_ work. It uses Raspberry Pi 4 hardware inside a keyboard form factor.
### Operating Systems
Although we test with [Raspberry Pi OS](https://www.raspberrypi.com/software/), other operating systems may work.
#### Raspberry Pi Linux Distros
Since Raspberry Pi OS is a Linux distribution, similar distros are likely to work. These include:
  * [Debian’s Raspberry Pi images](https://raspi.debian.net/)
  * [Fedora’s Raspberry Pi images](https://docs.fedoraproject.org/en-US/quick-docs/raspberry-pi/)


#### Windows for Raspberry Pi
There are no known attempts to run Arcade on Windows for Raspberry Pi or any other ARM device. In theory, it’s possible. However, the following considerations apply:
  * Windows is said to be sluggish on Raspberry Pi devices
  * [Arcade’s binary dependencies](#sbc-binary-deps) might not have builds for Windows on ARM
  * Be sure to install Python from the official download page
  * Avoid the Microsoft app store version of Python


## Unsupported Raspberry Pi Devices
Some Raspberry Pi devices cannot run Arcade because they do not support the [required OpenGL ES features](#requirements-gles).
### Incompatible Older Devices
  * The original Raspberry Pi is unsupported
  * The Raspberry Pi 2 is unsupported
  * The Raspberry Pi 3 is unsupported


### Incompatible New Devices
Some newer devices also lack support for the required features. Each is either a microcontroller or a reduced-power variant of older Pi hardware.
The table below lists these newer incompatible Raspberry Pi devices.  
Recent Incompatible Raspberry Pi Devices  
| Device  | Type  |  
| --- | --- |  
| [Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) (and W version) / [RP2040](wiki_pi2040)  | Microcontroller  |  
| [Pi Pico 2](https://www.raspberrypi.com/products/raspberry-pi-pico-2/) (and W version) / [RP2350](https://www.raspberrypi.com/products/rp2350/)  | Microcontroller  |  
| [Pi Zero](https://www.raspberrypi.com/products/raspberry-pi-zero/) (plus W version)  | Mini-SBC  |  
| [Pi Zero 2](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) (plus W and WH versions)  | Mini-SBC (based on Pi 3 hardware)  |  
## SBC Requirements
Any Single Board Computer (SBC) which meets the following requirements may work. If you are a parent or educator shopping for a compatible SBC, please see the [SBC Purchasing Rules of Thumb](../about/for_academia.html#sbc-rule-of-thumb).
### Standard Python
Arcade 3.0.0 requires Python 3.9 or higher.
In practice, this means running Linux. In theory, it may be possible to run Arcade on an ARM-specific version of Windows, but nobody has tried this before.
### Supported OpenGL ES Versions
Both Arcade and [pyglet](https://pyglet.readthedocs.io/en/development/) can run via OpenGL ES on devices with either:
  * OpenGL ES 3.2 or higher
  * OpenGL ES 3.1 with certain extensions


To learn more, please see the [pyglet manual page on OpenGL ES](pyglet-opengles).
If you are unsure, you may be able to try to install Arcade, then test both Arcade and pyglet. If an SBC board is properly designed, incompatibility will result in an error without damaging the hardware.
### Arcade’s Binary Dependencies
Arcade 3.0.0 depends on the following binary packages from PyPI:
  1. [`pymunk`](https://www.pymunk.org/en/latest/pymunk.html#module-pymunk "\(in Pymunk\)")
  2. [`pillow`](https://pillow.readthedocs.io/en/stable/PIL.html#module-PIL "\(in Pillow \(PIL Fork\) v11.3.0\)")


If one of these packages hasn’t been compiled for your SBC’s CPU architecture, you will not be able to install Arcade. In general, SBCs compatible with amd64 or the most common ARM instruction sets should work.
### An Adequate Power Supply
SBCs require an adequate power supply to function correctly.
If you experience an issue with a crash or strange error while usin Arcade on a Raspberry Pi or any other device, please try the following:
  1. Make sure you are using a quality power supply from a reputable vendor
  2. Unplug any non-essential external hardware such:
     * external drives
     * cameras
     * USB devices
  3. Try to replicate the problem again


If the crash or problem suddenly vanishes, you may be experiencing a brownout. This occurs when the hardware experiences insufficient power due to an inadequate or faulty power supply.
#### Fixing Brownout
You can try the following:
  * Use a powered USB hub between external devices and the SBC
  * Replace the power supply with a high-quality one from a reputable vendor


