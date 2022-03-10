from optparse import OptionParser
 

# parser = OptionParser()	
# parser.add_option('-e','--energy', dest='energy', default = '0.5',help='beam energy in GeV')
# parser.add_option('-p','--particle', dest='particle', default = 'e-',help='type of particle in beam')
# parser.add_option('-a','--angle', dest='angle', default = '0', help='incidence angle')
# parser.add_option('-f','--file', dest='file', default = 'Output', help='Name of the file (without the .root)')
# parser.add_option('-n','--events', dest='events', default = '100', help='Number of events')
# parser.add_option('-s','--seed', dest='seed', default = '1', help='Seed upon which the simulation is randomised')
# options = parser.parse_args()[0]


#easy config interface
# seed                 = str(options.seed)
# max_events           = int(options.events)
# energy               = float(options.energy) # GeV, certified
# particle_id          = str(options.particle)
# incidentAngleDegrees = float(options.angle)


max_events = 1000
energy=2 # GeV, certified
particle_id='e-'
incidentAngleDegrees=0
runNumber=1
xOffset=0 #mm, absorber is 665 mm wide

simulation_name=particle_id+str(energy)+"GeV"+str(int(max_events/1000))+"k"
# simulation_name=particle_id+str(energy)+"GeV"+str(int(max_events/1000))+"k"+str(incidentAngleDegrees)+"deg"
# simulation_name=particle_id+str(energy)+"GeV"+str(int(max_events/1000))+"k"+str(xOffset)+"xpos"














#my magic happens
energy=float(energy)

import math
incidentAngleRadians=incidentAngleDegrees *2*math.pi/360 #incident angle
beamDistance=1000
xVector=math.sin(incidentAngleRadians)
zVector=math.cos(incidentAngleRadians)
hcal_edge_offset = -404
position=[-xVector*beamDistance+xOffset, 0., -zVector*beamDistance+hcal_edge_offset] # mm

direction=[xVector, 0.,zVector]

output_filename=simulation_name + '.root'




#their magic happens
from LDMX.Framework import ldmxcfg
from LDMX.SimCore import generators
from LDMX.SimCore import simulator
# process = ldmxcfg.Process(simulation_name)
# process = ldmxcfg.Process("process")
process = ldmxcfg.Process("process")
# simulator = simulator.simulator(simulation_name)
simulation = simulator.simulator("prototype")
# simulation.runNumber = int(seed)
simulation.setDetector('ldmx-hcal-prototype-v1.0')

gun = generators.gun('particle_gun')

gun.particle  = particle_id
gun.energy    = energy
gun.position  = position
gun.direction = direction
simulation.generators=[gun]
simulation.beamSpotSmear=[0., 0., 0.] #make it zero for very good measure



from LDMX.Hcal import hcal
from LDMX.Hcal import digi
import LDMX.Hcal.HcalGeometry
import LDMX.Ecal.EcalGeometry
from LDMX.Hcal import hcal_hardcoded_conditions
process.maxEvents = max_events
process.run=runNumber

#verbosity troubleshooting
verbosity=0
# hcal.verbosity=verbosity
# digi.verbosity=verbosity
# ldmxcfg.verbosity=verbosity
# generators.verbosity=verbosity
simulation.verbosity=verbosity





#Lene's magic happens
from LDMX.TrigScint.trigScint import TrigScintQIEDigiProducer
from LDMX.TrigScint.trigScint import TrigScintRecHitProducer
tsDigis =TrigScintQIEDigiProducer.up()
tsDigis.number_of_strips = 12
tsRecHits =TrigScintRecHitProducer.up()

TrigScintQIEDigiProducer.verbosity=0
TrigScintRecHitProducer.verbosity=0

process.sequence = [ simulation, digi.HcalDigiProducer(), digi.HcalRecProducer(), hcal.HcalVetoProcessor(),tsDigis,tsRecHits]
process.outputFiles = [output_filename]
