import glob
import sys

inp = sys.argv[1]
scheme = sys.argv[2]
in_particle = sys.argv[3]
in_eft_param = sys.argv[4]
 
#particles = ["a","Z","W+","W-","g","ve","ve~","vm","vm~","vt","vt~","e-","e+","mu-","mu+","ta-","ta+","u","u~","c","c~","t","t~","d","d~","s","s~","b","b~","H"]
#eftparams = ['cG', 'cW', 'cH', 'cHbox', 'cHDD', 'cHG', 'cHW', 'cHB', 'cHWB', 'ceHRe', 'cuHRe', 'cdHRe', 'ceWRe', 'ceBRe', 'cuGRe', 'cuWRe', 'cuBRe', 'cdGRe', 'cdWRe', 'cdBRe', 'cHl1', 'cHl3', 'cHe', 'cHq1', 'cHq3', 'cHu', 'cHd', 'cHudRe', 'cll', 'cll1', 'cqq1', 'cqq11', 'cqq3', 'cqq31', 'clq1', 'clq3', 'cee', 'cuu', 'cuu1', 'cdd', 'cdd1', 'ceu', 'ced', 'cud1', 'cud8', 'cle', 'clu', 'cld', 'cqe', 'cqu1', 'cqu8', 'cqd1', 'cqd8', 'cledqRe', 'cquqd1Re', 'cquqd11Re', 'cquqd8Re', 'cquqd81Re', 'clequ1Re', 'clequ3Re', 'cGtil', 'cWtil', 'cHGtil', 'cHWtil', 'cHBtil', 'cHWBtil', 'ceWIm', 'ceBIm', 'cuGIm', 'cuWIm', 'cuBIm', 'cdGIm', 'cdWIm', 'cdBIm', 'cHudIm', 'ceHIm', 'cuHIm', 'cdHIm', 'cledqIm', 'cquqd1Im', 'cquqd8Im', 'cquqd11Im', 'cquqd81Im', 'clequ1Im', 'clequ3Im', 'ceH', 'cuH', 'cdH', 'ceW', 'ceB', 'cuG', 'cuW', 'cuB', 'cdG', 'cdW', 'cdB', 'cHud', 'cledq', 'cquqd1', 'cquqd11', 'cquqd8', 'cquqd81', 'clequ1', 'clequ3', 'cth']


def prepare_keys():
  models = glob.glob("SMEFTsim/UFO_models/*")
  #SMEFTsim/UFO_models/SMEFTsim_U35_alphaScheme_UFO
  flavours = [ flavour for x in models for flavour in [x.split("/")[-1].split("_")[1]] ]
  schemes = [ scheme for x in models for scheme in [x.split("/")[-1].split("_")[2]] ]

  return list(set(flavours)), list(set(schemes))

#print(prepare_keys())

if inp == "U35" and scheme == "Mw":
  from UFO_models.SMEFTsim_U35_MwScheme_UFO.parameters import *
  from UFO_models.SMEFTsim_U35_MwScheme_UFO.vertices import *
  from UFO_models.SMEFTsim_U35_MwScheme_UFO.couplings import *
  from UFO_models.SMEFTsim_U35_MwScheme_UFO.particles import *

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

  eftin_particle_vertices = [ vertex for vertex in in_particle_vertices if 'NP' in [ par for par in coupling.order.keys() for coupling in vertex.couplings.values() if in_eft_param in coupling.value]]
  print("Total of {0} EFT couplings affect particle {1}".format(len(eftin_particle_couplings),in_particle))
  print("\n\nFound what we need,\nTotal of {0} vertices containing particle {1} and parameter {2}".format(len(eftin_particle_vertices),in_particle,in_eft_param))
  for eft_vertex in eftin_particle_vertices:
    print("\nThis is vertex {0}".format(eft_vertex.name))
    print(", ".join([particle.name for particle in eft_vertex.particles]))
