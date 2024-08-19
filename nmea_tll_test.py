import pynmea2
# this is playing around with creating a AGTLL message. Charplotter software didn't seem to do anything with it.
msg = pynmea2.TLL('AG', 'TLL', ('1','41.3126','N','70.4022','W','WHALE','05270000','T',))
print(msg)