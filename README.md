# APRSmap

## What is it?
It is a simple map displaying APRS transmissions, decoded from a KISS interface.

## How to run
1. Setup a working APRS decoder availiable using a KISS interface. [Sample setup below](#kiss-interface-tnc)
2. Create a python virtual environment, and install all of the required packages `pip -r requirements.txt`
3. Run the flask webapp. You can start a development server just by running the `app.py` file like this: `python app.py`, or using gunicorn `gunicorn -k gevent -w 2 --bind 0.0.0.0:5000 "app:create_app()"`
4. The webapp should be accesible on port `5000`

## KISS interface (TNC)
The app connects to a KISS interface, which can be run in the following way:
1. Data source. If you want to connect to a live RTL-SDR use `rx-fm` to play to a virtual audio loopback (tested on linux only, to create loopback use `sudo modprobe snd-aloop`). If you do not have a live RTL-SDR availiable, you can use a Wav file to play an example capture.
2. A decoder - in this case `direwolf`. Should just work when running with the provided config.
3. Now that you have a decoder accessible using a KISS interface, you can continue with running the app.

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