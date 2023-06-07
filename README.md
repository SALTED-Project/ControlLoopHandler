# SALTED - Control Loop Handler (pip installable)

ControlLoopHandler is a Python class intended to ease the development of DET components that use the control loop mechanism envisioned in SALTED. It is aimed at partners working on WP2 and WP4 activities, but may also be of use to external users developing DET components.



## Installation

Install as package in your Python 3 environment:

```bash
pip install git+https://github.com/SALTED-Project/ControlLoopHandler.git@packaged
```

## Usage

Full Examples for App and DET implementations can be found under ``/examples``.
Make sure to install all additional python dependencies beforehand:

```bash
pip install git+https://github.com/SALTED-Project/TokenHandler.git
pip install paho-mqtt

```


### DET side

First, instantiate the ControlLoopHandler.

```python
import controlloophandler

det_clh = controlloophandler.handler.TokenHandler(
    det_component_id= "example_id", 
    starting_params= {
        "example_param_1": 20,
        "example_param_2": "abc"
    }, 
    token_endpoint = "https://auth.salted-project.eu/realms/SALTED/protocol/openid-connect/token",
    mqtt_endpoint = "control-broker.salted-project.eu",
    mqtt_port = 443,
    auth_client_id = <your keycloak client ID>,
    auth_client_secret = <your keycloak client secret>
)
```

Calling the *start* method will connect to the MQTT broker and subscribe to the corresponding topic (*[det_id]/#*).

```python
det_clh.start()
```

Afterwards, you can access the updated value of any parameter with the *get_param* method.

```python
new_value = det_clh.get_param("example_param_1")
```

Finally, you can disconnect from the MQTT broker by calling the *stop* method.

```python
det_clh.stop()
```

Methods *update_token*, *set_param* and *add_param* are also available for your needs.

### App side

Applications can send requests to the DET components using the control loop mechanism. To do so, they can send an MQTT message to the *[det_id]/[app_id]* topic and the DET component will send an acknowledgement message to the *[app_id]* topic. As an example, using Python:

```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
...
client.subscribe(app_id) 
client.publish(det_id+'/'+app_id, msg)
```

The payload must be a valid JSON. The keys are the names of the parameters to be modified, and the values correspond to the new values of those parameters. For instance:

```json
{
    "example_param_1": 10,
    "example_param_2": "cba",
    "example_param_3": 2.3
}
```

The acknowledgement message sent by the DET component after the reconfiguration will also be a JSON. If an error has ocurred:

```json
{
    "error": "Description of the error"
}
```

If no error has ocurred, the JSON payload will contain the parameters that have been successfully reconfigured:

```json
{
    "example_param_1": 10,
    "example_param_2": "cba"
}
```

Additionally, for discoverability purposes, applications can send a message to the *info/[app_id]* topic. The payload will not be checked. All DET components currently connected to the MQTT broker will send a message to the [app_id] topic with basic information about their identifier and customizable parameters. This example is one such possible message:

```json
{
    "det_component_id": "example_id",
    "params": {
        "example_param_1": 10,
        "example_param_2": "cba"
    }
}
```