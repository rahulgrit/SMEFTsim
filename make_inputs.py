import glob
import sys

model = sys.argv[1]
inp = sys.argv[2]
in_particle = sys.argv[3]
in_eft_param = sys.argv[4]

# SMEFTatNLO (third argument doesnt matter)
# python make_inputs.py SMEFTatNLO U35 H cpDC
#
#
# SMEFTsim (third argument flavour : U35/topU3l/MFV/general)
# python make_inputs.py SMEFTatNLO U35 H cpDC

def prepare_keys():
  models = glob.glob("SMEFTsim/UFO_models/*")
  #SMEFTsim/UFO_models/SMEFTsim_U35_alphaScheme_UFO
  flavours = [ flavour for x in models for flavour in [x.split("/")[-1].split("_")[1]] ]
  schemes = [ scheme for x in models for scheme in [x.split("/")[-1].split("_")[2]] ]

  return list(set(flavours)), list(set(schemes))

if model == "SMEFTatNLO":
    from UFO_models.SMEFTatNLO.parameters import *
    from UFO_models.SMEFTatNLO.vertices import *
    from UFO_models.SMEFTatNLO.couplings import *
    from UFO_models.SMEFTatNLO.particles import *

if model == "SMEFTsim":
  if inp == "U35" :
    from UFO_models.SMEFTsim_U35_MwScheme_UFO.parameters import *
    from UFO_models.SMEFTsim_U35_MwScheme_UFO.vertices import *
    from UFO_models.SMEFTsim_U35_MwScheme_UFO.couplings import *
    from UFO_models.SMEFTsim_U35_MwScheme_UFO.particles import *
  
  if inp == "topU3l":
    from UFO_models.SMEFTsim_topU3l_MwScheme_UFO.parameters import *
    from UFO_models.SMEFTsim_topU3l_MwScheme_UFO.vertices import *
    from UFO_models.SMEFTsim_topU3l_MwScheme_UFO.couplings import *
    from UFO_models.SMEFTsim_topU3l_MwScheme_UFO.particles import *
  
  if inp == "MFV":
    from UFO_models.SMEFTsim_MFV_MwScheme_UFO.parameters import *
    from UFO_models.SMEFTsim_MFV_MwScheme_UFO.vertices import *
    from UFO_models.SMEFTsim_MFV_MwScheme_UFO.couplings import *
    from UFO_models.SMEFTsim_MFV_MwScheme_UFO.particles import *
  
  if inp == "general":
    from UFO_models.SMEFTsim_general_MwScheme_UFO.parameters import *
    from UFO_models.SMEFTsim_general_MwScheme_UFO.vertices import *
    from UFO_models.SMEFTsim_general_MwScheme_UFO.couplings import *
    from UFO_models.SMEFTsim_general_MwScheme_UFO.particles import *

eftpars = [param for param in all_parameters if param.name[0]=='c']
eftcouplings = [coupling for coupling in all_couplings if 'NP' in coupling.order.keys()]
print("Total of {0} vertices in model".format(len(all_vertices)))
print("Total of {0} particles in model".format(len(all_particles)))
print("Total of {0} couplings in model, {1} are SMEFT".format(len(all_couplings),len(eftcouplings)))
print("Total of {0} parameters in model, {1} are SMEFT".format(len(all_parameters),len(eftpars)))

if in_particle in [particle.name for particle in all_particles]:
  print("Found particle {0}".format(in_particle))
  in_particle_vertices = [vertex for vertex in all_vertices for particle in vertex.particles if particle.name == in_particle]
  eftin_particle_vertices = [ vertex for vertex in in_particle_vertices if 'NP' in [ par for par in coupling.order.keys() for coupling in vertex.couplings.values()]]

  
eftin_particle_couplings = list(set([ coupling for vertex in eftin_particle_vertices for coupling in vertex.couplings.values()]))

eftin_particle_vertices = [ vertex for vertex in in_particle_vertices if 'NP' in [ par for par in coupling.order.keys() for coupling in vertex.couplings.values() if in_eft_param in coupling.value.split("*")]]

#avoid double counting
eftin_particle_vertices = set(eftin_particle_vertices)
print("Total of {0} EFT couplings affect particle {1}".format(len(eftin_particle_couplings),in_particle))
print("\n\nFound what we need,\nTotal of {0} vertices containing particle {1} and parameter {2}".format(len(eftin_particle_vertices),in_particle,in_eft_param))
for eft_vertex in eftin_particle_vertices:
  print("\nThis is vertex {0}".format(eft_vertex.name))
  print(", ".join([particle.name for particle in eft_vertex.particles]))
