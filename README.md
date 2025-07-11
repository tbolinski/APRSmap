# APRSmap

## What is it?
It is a simple map displaying APRS transmissions, decoded from a KISS interface.

## How to run
Stream audio to a virtual loopback from a live rtl_sdr using `rx_fm`, or a wav file using aplay to direwolf.
Commands:
### rx_fm
```
rx_fm -F 144.8M | aplay -f S16_LE -D plughw:1,1
```
### Wav file
Aplay, using, for example the http://www.wa8lmf.net/TNCtest/
```
aplay -D plughw:1,1 tnc_test02.wav
```
### Direwolf
```
direwolf -t 0 -c direwolf.conf
```