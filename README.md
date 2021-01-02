# Agent based model of physarum transport network

ABM of Physarum tranport networks

## Example

## Run the model

To run the model and get an nice animation as above :

```
run main.py
```

Parameter selection : in main.py you can select :

```
- board size
- initial trail map
- initial particule/agent map
- the model ( w/o collision)
- agent parameters (sensor and motor)
```

## Description of other files

class.py is the model with collisions, only one particule per cell.
class_free.py is the model freed from the collisions constrain.

## References : 

- https://sagejenson.com/physarum
- Jones, J. (2010). Characteristics of pattern formation and evolution in approximations of physarum transport networks. Artificial Life, 16(2), 127-153. https://doi.org/10.1162/artl.2010.16.2.16202
