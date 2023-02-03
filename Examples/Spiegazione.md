Ci sono 3 files:
- `topology.py` --> Crea la topologia della rete 
	- Host, Switch e collegamenti
- `topology_slicing.py` --> Crea un esempio di slices, alcuni host raggiungono solo alcuni host (simil VLAN)
- `service_slicing.py` --> Crea un altro tipo di slicing, tutti gli host comunicano tra di loro. Il traffico video viene rediretto su uno slice con bw=10, il resto su uno con bw=1

[VIDEO](https://www.youtube.com/watch?v=swJ8zEvwXcI)
