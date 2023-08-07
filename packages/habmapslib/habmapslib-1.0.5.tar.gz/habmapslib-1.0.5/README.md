# habmapslib

Librería para el uso de [habmaps](https://github.com/alpeza/habmaps)

* [GitHub](https://github.com/alpeza/habmapsgateway)
* [Pypi](https://pypi.org/project/habmapslib/#description)

## Quick Start

1.- Instalamos el cliente de habmaps con

Opción 1, valida para `python >= 3.8`.
```
curl https://bootstrap.pypa.io/get-pip.py | python #Updateamos el repo de pypi
pip3 install habmapslib
```

Opción 2:

```
git clone https://github.com/alpeza/habmapsgateway.git
cd habmapsgateway/habmapslib
sudo python3 setup.py install
```

2.- Envíamos información a la plataforma

```python
from habmapslib import MapTracker, HabMapsMessage
import time

mt = MapTracker.MapTracker(id="default-station-id", #Nombre de la estación base
                           mqtt_url="localhost",    #DNS o IP del servidor MQTT
                           mqtt_port=1883,          #Puerto del servidor MQTT
                           user='habmaps',          #Credenciales de acceso al broker MQTT
                           password='root')

mt.startAlive() #Iniciamos la señal de alive que se enviará cada n minutos 

while True:
    mt.sendHabMessage(HabMapsMessage.HabMapsMessage(
        TimeStamp='2021-04-02 15:33:43', #El timestamp del hab en formato string datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        HabId='Mi-Hab', #Nombre del hab que se esta monitorizando, vendrá de la traza q transmita el hab
        HabPosition=[5, 3], #Array de [ latitud, longitud]
        Signals={ #Payload de sensores clave: Nombre del sensor, valor: valor del sensor
            "miSensorUno": 122.4,
            "miSensorDos": 400.5
        },
        BasestationPosition=[5, 3])) #Array opcional de [ latitud, longitud] de posición de la estacion base
    time.sleep(5)
```

## Logging

La configuración de los logs se realiza a través de variables de entorno

```bash
export HABLIB_LOGLEVEL=DEBUG #INFO,ERROR
export HABLIB_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
export HABLIB_LOGFILE="/tmp/hablibclient.log"
```

## Error Handling

```python
    rc = mt.sendHabMessage(HabMapsMessage.HabMapsMessage(
        TimeStamp='2021-04-02 15:33:43',
        HabId='Mi-Hab',
        HabPosition=[5, 3],
        Signals={
            "miSensorUno": 122.4,
            "miSensorDos": 400.5
        },
        BasestationPosition=[5, 3]))
    if rc['isOK']:
        print("El mensaje se ha enviado correctamente ... ")
    else:
        print("Ha existido algun error en la transmision ...")
        print(rc['reason'])
```