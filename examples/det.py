from controlloophandler.handler import ControlLoopHandler
import json
import time

def run():
    det_clh = ControlLoopHandler(
        det_component_id= "example_id_det", 
        starting_params= {
            "example_param_1": 20,
            "example_param_2": "abc"
        }, 
        token_endpoint = "https://auth.salted-project.eu/realms/SALTED/protocol/openid-connect/token",
        mqtt_endpoint = "control-broker.salted-project.eu",
        mqtt_port = 443,
        auth_client_id = " ", # insert your keycloak client_id here
        auth_client_secret = " " # insert your keycloak client_secret here
    )

    det_clh.start()
    
    # start() is non blocking, thats why a waiting period is needed to wait for requests, since the program would otherwise quit due to no other tasks
    time.sleep(120)

    
    new_value = det_clh.get_param("example_param_1")
    print(new_value)
    det_clh.stop()
    

if __name__ == '__main__':
    run()
