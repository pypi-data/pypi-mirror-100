import os, sys, string
import linecache, math
import numpy as np
import datetime , time


from pople import HOF_atoms
from pople import dH_atoms
from pople import atno
from pople import uniqatoms
from pople import rung4mp2
from pople import NFC
from pople import nanb
from pople import get_geom
from pople import get_ctrl
from pople import get_val

def run():
    """ Performs thermochemistry calculations. """

    current_dir_path = os.getcwd()
    val = {}
    start_time_main = time.time()
    os.system("rm -f ORCA_G4MP2* Thermo*")

    input_file1 = current_dir_path + "/pople.inp"
    with open(input_file1, "r") as i_f:
        for line_if in i_f:
            if not line_if.startswith("#"):
                if "method_type" in line_if:
                    splt1 = line_if.split("=")
                    if "#" in splt1[1].strip():
                        new_v = splt1[1].strip().split("#")
                        val["user_method_type"] = new_v[0].strip()
                    else:
                        val["user_method_type"] = splt1[1].strip()
                if "job_type" in line_if:
                    splt1 = line_if.split("=")
                    if "#" in splt1[1].strip():
                        new_v = splt1[1].strip().split("#")
                        val["calc_choice"] = new_v[0].strip()
                    else:
                        val["calc_choice"] = splt1[1].strip()

    check_meth = ["G4MP2", "G4MP2-XP", "g4mp2", "g4mp2-xp"]
    if val["user_method_type"] not in check_meth:
       print("Invalid method_type selected, check for typos or refer manual")
       exit()

    check_choice = ["IP", "EA", "PA", "BE", "HF", "AE", "ip", "ea", "pa", "be", "hf", "ae"]
    if val["calc_choice"] not in check_choice:
       print("Invalid job_type selected, check for typos or refer manual")
       exit()


    
    if val["calc_choice"] == "IP" or val["calc_choice"] == "ip": 
        val["calc_IP"] = "true"
        val["verticalIP"] = "false"
    if val["calc_choice"] == "EA" or val["calc_choice"] == "ea": 
        val["calc_EA"] = "true"
        val["verticalEA"] = "false"
        val["calc_IP"] = "false"
    if val["calc_choice"] == "PA" or val["calc_choice"] == "pa": 
        val["calc_PA"] = "true"
        val["calc_IP"] = "false"
        val["calc_EA"] = "false"
    if val["calc_choice"] == "BE" or val["calc_choice"] == "be": 
        val["calc_BE"] = "true"
        val["calc_IP"] = "false"
        val["calc_EA"] = "false"
        val["calc_PA"] = "false"
    if val["calc_choice"] == "HF" or val["calc_choice"] == "hf": 
        val["calc_AE"] = "true"  ## check!!!
        val["calc_HF"] = "true"
        val["calc_BE"] = "false"
        val["calc_IP"] = "false"
        val["calc_EA"] = "false"
        val["calc_PA"] = "false"

    if val["calc_choice"] == "AE" or val["calc_choice"] == "ae": 
        val["calc_HF"] = "false"
        val["calc_AE"] = "true"  ## check!!!
        val["calc_BE"] = "false"
        val["calc_IP"] = "false"
        val["calc_EA"] = "false"
        val["calc_PA"] = "false"

    check_choice = ["IP", "EA", "PA", "BE", "HF", "AE", "ip", "ea", "pa", "be", "hf", "ae"]
    if val["calc_choice"] not in check_choice:
       print("Invalid job_type selected, check for typos or refer manual")


    get_geom(val["calc_choice"])
    print(val["user_method_type"], val["calc_choice"])
    new_val1 = get_ctrl(val["user_method_type"])
    #print(new_val1)
    print("checking ctrl")
    val.update(new_val1)

    #input_f = current_dir_path + "/control.inp"
    xyz_path = current_dir_path + "/geom.xyz"
    
    ### declaring units - S
    kB = 1.38064852000000*(10**-23) #kB = 1.38064852000000d-23
    h = 6.626070040*(10**-34)    #6.626070040d-34
    Ry = 10973731.568508  #10973731.568508d0
    c = 299792458    #299792458d0
    T = 298.15  #298.15d0 
    e = 1.60217648700000*(10**-19)   #1.60217648700000d-19
    N_avo = 6.02214179000000*(10**+23)  #6.02214179000000d+23
    au2j = 2 * Ry * h * c
    
    au2ev  = 2 * Ry * h * c          / e
    au2kjm = 2 * Ry * h * c * N_avo / 1000
    au2kcm = 2 * Ry * h * c * N_avo / 4184
    kcm2au = 1 / au2kcm
    
    j2au   = 1 / au2j
    au2cmi = 2 * Ry / 100
    cmi2au = 1 / au2cmi
    ### declaring units - E
    
    ### Writing intro Thermochemistry.out - start
    with open("Thermochemistry.out", "w") as ther_chem:
        day = datetime.datetime.today().strftime("%A")
        date = datetime.date.today()
        cur_date = date.strftime("%B %d, %Y")
        now = datetime.datetime.now()
        cur_time = now.strftime(" %H:%M:%S")
    
        ther_chem.write("==============================================\n")
        ther_chem.write("|           G4MP2 THERMOCHEMISTRY            |\n")
        ther_chem.write("==============================================\n")
        ther_chem.write("Starting time:  " + day + "  "+ cur_date + "  " + cur_time + "  " + time.tzname[0] +"  \n\n")
        ther_chem.write("* Constants and conversion factors *\n\n")
        ther_chem.write("h      =   6.6260700399999999E-34 J s\n")
        ther_chem.write("kB     =   1.3806485199999999E-23 J K^-1\n")
        ther_chem.write("Ry     =   1.0973731568507999E+07 m^-1\n")
        ther_chem.write("e      =   1.6021764870000000E-19 C\n")
        ther_chem.write("c      =   2.9979245800000000E+08 m s^-1\n")
        ther_chem.write("N_avo  =   6.0221417899999999E+23 mol^-1\n\n")
    
        ther_chem.write("au2ev  =   2.7211388291762535E+01\n")
        ther_chem.write("au2kcm =   6.2750957099203276E+02\n")
        ther_chem.write("au2kjm =   2.6255000450306652E+03\n")
        ther_chem.write("au2cmi =   2.1947463137015997E+05\n\n")
        
        ther_chem.write(" * Parameterized for the following atoms  *\n")
        ther_chem.write("    ____                                    \n")
        ther_chem.write("    |H |                                    \n")
        ther_chem.write("    --------    ---------------------       \n")
        ther_chem.write("    |Li| Be|    |B  |C  |N  |O  |F  |       \n")
        ther_chem.write("    |Na| Mg|    |Al |Si |P  |S  |Cl |       \n")
        ther_chem.write("    |K | Ca|    |Ga |Ge |As |Se |Br |       \n")
        ther_chem.write("    --------    ---------------------       \n")
        ther_chem.write("\n")
    ### Writing intro Thermochemistry.out - end
    
    ### List of predefined variables ?? does the order and manner of occurance matter or can all of them be declared at the begining?
    val["ALLELE"] = "false"
    val["switch_load_rel_file"] = "false"
    val["switch_guess"] = "false"
    val["FROZEN_GEOM"] = "false"
    
    val["SO_3rdrow_mols"] = "false"
    val["iterhess"] = 5
    
    val["TcutDOPre"] = 3e-2
    
    val["HF_CBS_default"]      = "true"  ## ask!!!
    val["HF_CBS_orca_23_def2"] = "false" 
    val["HF_CBS_orca_34_def2"] = "false" 
    val["HF_CBS_orca_23_cc"]   = "false" 
    val["HF_CBS_orca_34_cc"]   = "false" 
    
    val["switch_DLPNO_CCSDT"]  = "false"
    
    val["G4MP2TM"] = "false"
    val["ccsdt_cbs"] = "false"
    val["noHLC"] = "false"
    
    val["restart_check"] = "false"
    
    val["switch_RIMP2_small"] = "false"
    val["switch_read_RIMP2_small"] = "false"

    val["verticalIP"] = "false"
    val["verticalEA"] = "false"
    
    ### Reading input settings from input_f - start
    new_val = get_val()
    val.update(new_val)
    #print(val)
   
    untouc_env = os.environ['PATH'] 
    eline1 =  val["openmpi_dir"] + "bin:"
    new_env1 = eline1 + untouc_env
    os.environ['PATH'] = new_env1

    env2 = os.environ['LD_LIBRARY_PATH']
    eline2 =  val["openmpi_dir"] + "lib:"
    new_env2 = eline2 + env2
    os.environ['LD_LIBRARY_PATH'] = new_env2
    
    env3 = os.environ['LD_LIBRARY_PATH']
    eline3 = "/apps/lib:"
    new_env3 = eline3 + env3
    os.environ['LD_LIBRARY_PATH'] = new_env3
    #os.system(eline1)
    #os.system(eline2)
    #os.system(eline3)
    print(eline1)
    print(eline2)
    print(eline3)
#export PATH=/apps/openmpi-3.0.0_install/bin:$PATH
#export LD_LIBRARY_PATH=/apps/openmpi-3.0.0_install/lib:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/apps/lib:$LD_LIBRARY_PATH


    with open("geom.xyz","r") as xyz_f:
        num_l_xyz = sum(1 for l in xyz_f)
        Nat = int(linecache.getline("geom.xyz",1).strip())
        l1_chr_mul = linecache.getline("geom.xyz",2)
        tria = l1_chr_mul.split()
        charge = int(tria[0])
        multip = int(tria[1])
        sym = []   # will contain list of atom symbols in the mol # same order
        Rlist = []
        sym_coord = []
        for tmp_l in range(3,num_l_xyz+1):   ### what does NH do ???
            l1_xyz_1 = linecache.getline("geom.xyz",tmp_l)
            l1_lsp1 = l1_xyz_1.split()
            #full_l = l1_xyz_1.strip()
            full_l1 = l1_xyz_1.strip().split()
            full_l = full_l1[0] + "     "+str(round(float(full_l1[1]),8)) + "     "+str(round(float(full_l1[2]),8)) + "     "+str(round(float(full_l1[3]),8))
            sym_coord.append(full_l)  ## contains atom and coords
            sym.append(l1_lsp1[0])
            Rlist.append(l1_lsp1[1])
            Rlist.append(l1_lsp1[2])
            Rlist.append(l1_lsp1[3])
            conv = np.array(Rlist)
            R_coord = np.resize(conv,[Nat,3])
    
    val["Ntotal"] = 0
    val["Ntotale"] = 0
    val["Ntotalecore"] = 0
    for tmp_j in range(Nat):
        na_nb_list = nanb(sym[tmp_j])
        a = na_nb_list[0]
        b = na_nb_list[1]
        val["Ntotal"] = val["Ntotal"] + a + b
        #print(tmp_j,a,b)
        val["Ntotale"] = val["Ntotale"] + atno(sym[tmp_j])
        val["Ntotalecore"] = val["Ntotalecore"] + NFC(sym[tmp_j])
    
    
    val["Ntotal"] = val["Ntotal"] - charge
    val["Ntotale"] = val["Ntotale"] - charge
    val["Na"] = (multip + val["Ntotal"] - 1 ) / 2.0
    val["Nb"] = val["Na"] + 1 - multip
    
    
    val["isatom"] = "false"
    if Nat == 1: 
        val["isatom"] = "true"
    
    uniqat_d = uniqatoms(sym)
    
    val["IPss"] = "false"
    
    os.system("cp geom.xyz inp.xyz")
    rung4mp2(val, start_time_main)
    os.system("cp freq0.txt freq.txt")
    
    # revisit
    U0mol = val["U0"] 
    UTmol = val["UT"]
    HTmol = val["HT"]
    HLCmol = val["HLC0"]
    
     #=== JOB-TYPE-1 IS IP, from here
    if val["calc_IP"] == "true":
        val["IPss"] = "true"
        with open("geom_cation_IP.xyz", "r") as g_cat:  # need to look at this file
            with open("inp.xyz", "w") as inp_x:
                linecache.clearcache()
                Nat= int(linecache.getline("geom_cation_IP.xyz",1).strip())
                tr = linecache.getline("geom_cation_IP.xyz",2).strip()
                lsp11 = tr.split()
                charge = int(lsp11[0])
                multip = int(lsp11[1])
                inp_x.write(str(Nat) + " \n")
                inp_x.write(str(charge) +" "+ str(multip) + " \n")

                sym = []   # will contain list of atom symbols in the mol # same order
                Rlist = []
                sym_coord = []
                for tmp_l in range(3,num_l_xyz+1):   
                    l1_xyz_2 = linecache.getline("geom_cation_IP.xyz",tmp_l)
                    l1_lsp2 = l1_xyz_2.split()
                    full_l1 = l1_xyz_2.strip().split()
                    full_l = full_l1[0] + "     "+str(round(float(full_l1[1]),8)) + "     "+str(round(float(full_l1[2]),8)) + "     "+str(round(float(full_l1[3]),8))
                    sym_coord.append(full_l)  ## contains atom and coords
                    sym.append(l1_lsp2[0])
                    Rlist.append(l1_lsp2[1])
                    Rlist.append(l1_lsp2[2])
                    Rlist.append(l1_lsp2[3])
                    conv = np.array(Rlist)
                    R_coord = np.resize(conv,[Nat,3])
                for tmp_y in range(len(sym_coord)):
                    inp_x.write(sym_coord[tmp_y]) 
                    inp_x.write("\n") 
    
                val["Ntotal"] = 0
                val["Ntotale"] = 0
                val["Ntotalecore"] = 0

                for tmp_k in range(Nat):
                    na_nb_l = nanb(sym[tmp_k])
                    na = na_nb_l[0]
                    nb = na_nb_l[1]
                    val["Ntotal"] = val["Ntotal"] + na + nb
                    val["Ntotale"] = val["Ntotale"] + atno(sym[tmp_k])
                    val["Ntotalecore"] = val["Ntotalecore"] + NFC(sym[tmp_k])
    
        val["Ntotal"] = val["Ntotal"] - charge
        val["Ntotale"] = val["Ntotale"] - charge
        val["Na"] = (multip + val["Ntotal"] - 1 ) / 2.0
        val["Nb"] = val["Na"] + 1 - multip
    
        #print(val["Na"], val["Nb"], val["Ntotal"], val["Ntotale"] , charge, multip, "==IP==")
    
        val["isatom"] = "false"
        if Nat == 1: val["isatom"] = "true"
    
        rung4mp2(val, start_time_main)
        os.system("cp freq0.txt freq_cation_IP.txt")
    
        U0mol2 = U0mol - val["U0"] 
        UTmol2 = UTmol - val["UT"]
        HTmol2 = HTmol - val["HT"]
        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write(" *---------*\n")
            ther_chem.write(" * SUMMARY *\n")
            ther_chem.write(" *---------*\n\n")
            ther_chem.write(" * Ionization Energy (mol+ - mol) =       " + str(round(-U0mol2,8)) + " Hartree\n")
            ther_chem.write(" * Ionization Energy (mol+ - mol) =       " + str(round(-U0mol2*au2ev,8)) + " eV\n")
            ther_chem.write(" * Ionization Energy (mol+ - mol) =       " + str(round(-U0mol2*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * Ionization Energy (mol+ - mol) =       " + str(round(-U0mol2*au2kjm,8)) + " kj/mol\n\n")

            ther_chem.write("* Breakdown *\n")
            ther_chem.write(" * CCSD(T) (mol+ - mol)           =       " + str(round((val["IPbreakdown2"][0]-val["IPbreakdown1"][0])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * DE (MP2)(mol+ - mol)           =       " + str(round((val["IPbreakdown2"][2]-val["IPbreakdown1"][2])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * DE (HF) (mol+ - mol)           =       " + str(round((val["IPbreakdown2"][1]-val["IPbreakdown1"][1])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * HLC     (mol+ - mol)           =       " + str(round((val["IPbreakdown2"][3]-val["IPbreakdown1"][3])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * SO      (mol+ - mol)           =       " + str(round((val["IPbreakdown2"][4]-val["IPbreakdown1"][4])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * ZPVE    (mol+ - mol)           =       " + str(round((val["IPbreakdown2"][5]-val["IPbreakdown1"][5])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write("                                    -------------------------\n")
            ther_chem.write("TOTAL                             =       " + str(round( (sum(val["IPbreakdown2"])  -sum(val["IPbreakdown1"]))*au2kcm,8)) +  " kcal/mol\n")
            ther_chem.write("                                    -------------------------\n\n")
            end_time_n = time.time()
            ther_chem.write("** Elapsed time =              " + str(round(end_time_n - start_time_main,2)) + "  s\n")

        day = datetime.datetime.today().strftime("%A")
        date = datetime.date.today()
        cur_date = date.strftime("%B %d, %Y")
        now = datetime.datetime.now()
        cur_time = now.strftime(" %H:%M:%S")
    
        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write("==============================================\n")
            ther_chem.write("Final time:  " + day + "  "+ cur_date + "  " + cur_time + "  " + time.tzname[0] +"  \n\n")
            ther_chem.write("==============================================\n")


        exit()
    
    if val["calc_EA"] == "true":
        if val["verticalEA"] == "true": val["verticalIP"] = val["verticalEA"]
        val["IPss"] = "true"
    
        with open("geom_anion_EA.xyz", "r") as g_cat:  # need to look at this file
            with open("inp.xyz", "w") as inp_x:
                linecache.clearcache()
                Nat= int(linecache.getline("geom_anion_EA.xyz",1).strip())
                tr = linecache.getline("geom_anion_EA.xyz",2).strip()
                lsp11 = tr.split()
                charge = int(lsp11[0])
                multip = int(lsp11[1])
                inp_x.write(str(Nat) + " \n")

                inp_x.write(str(charge) +" "+ str(multip) + " \n")
                sym = []   # will contain list of atom symbols in the mol # same order
                Rlist = []
                sym_coord = []
                for tmp_l in range(3,num_l_xyz+1):   
                    l1_xyz_2 = linecache.getline("geom_anion_EA.xyz",tmp_l)
                    l1_lsp2 = l1_xyz_2.split()

                    full_l1 = l1_xyz_2.strip().split()
                    full_l = full_l1[0] + "     "+str(round(float(full_l1[1]),8)) + "     "+str(round(float(full_l1[2]),8)) + "     "+str(round(float(full_l1[3]),8))
                    sym_coord.append(full_l)  ## contains atom and coords
                    sym.append(l1_lsp2[0])
                    Rlist.append(l1_lsp2[1])
                    Rlist.append(l1_lsp2[2])
                    Rlist.append(l1_lsp2[3])
                    conv = np.array(Rlist)
                    R_coord = np.resize(conv,[Nat,3])
                for tmp_y in range(len(sym_coord)):
                    inp_x.write(sym_coord[tmp_y])
                    inp_x.write("\n")
    
    
                val["Ntotal"] = 0
                val["Ntotale"] = 0
                val["Ntotalecore"] = 0

                for tmp_k in range(Nat):
                    na_nb_l = nanb(sym[tmp_k])
                    na = na_nb_l[0]
                    nb = na_nb_l[1]
                    val["Ntotal"] = val["Ntotal"] + na + nb
                    val["Ntotale"] = val["Ntotale"] + atno(sym[tmp_k])
                    val["Ntotalecore"] = val["Ntotalecore"] + NFC(sym[tmp_k])
    
        val["Ntotal"] = val["Ntotal"] - charge
        val["Ntotale"] = val["Ntotale"] - charge
        val["Na"] = (multip + val["Ntotal"] - 1 ) / 2.0
        val["Nb"] = val["Na"] + 1 - multip
    
        #print(val["Na"], val["Nb"], val["Ntotal"], val["Ntotale"] , charge, multip, "==EA==")
    
        val["isatom"] = "false"
        if Nat == 1: val["isatom"] = "true"
    
        rung4mp2(val, start_time_main)
        os.system("cp freq0.txt freq_anion_EA.txt")
    
        U0mol2 = U0mol - val["U0"]
        UTmol2 = UTmol - val["UT"]
        HTmol2 = HTmol - val["HT"]
        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write(" *---------*\n")
            ther_chem.write(" * SUMMARY *\n")
            ther_chem.write(" *---------*\n\n")
            ther_chem.write(" * Electron affinity (mol+ - mol -) =       " + str(round(U0mol2,8)) + " Hartree\n")
            ther_chem.write(" * Electron affinity (mol+ - mol -) =       " + str(round(U0mol2*au2ev,8)) + " eV\n")
            ther_chem.write(" * Electron affinity (mol+ - mol -) =       " + str(round(U0mol2*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * Electron affinity (mol+ - mol -) =       " + str(round(U0mol2*au2kjm,8)) + " kj/mol\n\n")
    
            ther_chem.write("* Breakdown *\n")
            ther_chem.write(" * CCSD(T) (mol+ - mol)           =       " + str(round((val["EAbreakdown1"][0]-val["EAbreakdown2"][0])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * DE (MP2)(mol+ - mol)           =       " + str(round((val["EAbreakdown1"][2]-val["EAbreakdown2"][2])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * DE (HF) (mol+ - mol)           =       " + str(round((val["EAbreakdown1"][1]-val["EAbreakdown2"][1])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * HLC     (mol+ - mol)           =       " + str(round((val["EAbreakdown1"][3]-val["EAbreakdown2"][3])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * SO      (mol+ - mol)           =       " + str(round((val["EAbreakdown1"][4]-val["EAbreakdown2"][4])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * ZPVE    (mol+ - mol)           =       " + str(round((val["EAbreakdown1"][5]-val["EAbreakdown2"][5])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write("                                    -------------------------\n")
            ther_chem.write("TOTAL                             =       " + str(round( (sum(val["EAbreakdown1"])  -sum(val["EAbreakdown2"]))*au2kcm,8)) +  " kcal/mol\n")
            ther_chem.write("                                    -------------------------\n\n")
            end_time_n = time.time()
            ther_chem.write("** Elapsed time =              " + str(round(end_time_n - start_time_main,2)) + "  s\n")

        day = datetime.datetime.today().strftime("%A")
        date = datetime.date.today()
        cur_date = date.strftime("%B %d, %Y")
        now = datetime.datetime.now()
        cur_time = now.strftime(" %H:%M:%S")

        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write("==============================================\n")
            ther_chem.write("Final time:  " + day + "  "+ cur_date + "  " + cur_time + "  " + time.tzname[0] +"  \n\n")
            ther_chem.write("==============================================\n")


        exit()
    
    if val["calc_PA"] == "true":
        val["verticalIP"] = "false"
        val["IPss"] = "true"
    
        with open("geom_cation_PA.xyz", "r") as g_cat:  # need to look at this file
            num_l_xyz = sum(1 for l in g_cat)
            with open("inp.xyz", "w") as inp_x:
                linecache.clearcache()
                Nat= int(linecache.getline("geom_cation_PA.xyz",1).strip())
                #print("Nat in PA", Nat)
                tr = linecache.getline("geom_cation_PA.xyz",2).strip()
                lsp11 = tr.split()
                charge = int(lsp11[0])
                multip = int(lsp11[1])
                inp_x.write(str(Nat) + " \n")
                inp_x.write(str(charge) +" "+ str(multip) + " \n")
                sym = []   # will contain list of atom symbols in the mol # same order
                Rlist = []
                sym_coord = []
                for tmp_l in range(3,num_l_xyz+1):
                    l1_xyz_2 = linecache.getline("geom_cation_PA.xyz",tmp_l)
                    l1_lsp2 = l1_xyz_2.split()
                    full_l1 = l1_xyz_2.strip().split()
                    full_l = full_l1[0] + "     "+str(round(float(full_l1[1]),8)) + "     "+str(round(float(full_l1[2]),8)) + "     "+str(round(float(full_l1[3]),8))
                    sym_coord.append(full_l)  ## contains atom and coords
                    sym.append(l1_lsp2[0])
                    Rlist.append(l1_lsp2[1])
                    Rlist.append(l1_lsp2[2])
                    Rlist.append(l1_lsp2[3])
                    conv = np.array(Rlist)
                    R_coord = np.resize(conv,[Nat,3])
                for tmp_y in range(len(sym_coord)):
                    inp_x.write(sym_coord[tmp_y])
                    inp_x.write("\n")
    
        val["Ntotal"] = 0
        val["Ntotale"] = 0
        val["Ntotalecore"] = 0
        for tmp_k in range(Nat):
            na_nb_l = nanb(sym[tmp_k])
            na = na_nb_l[0]
            nb = na_nb_l[1]
            val["Ntotal"] = val["Ntotal"] + na + nb
            val["Ntotale"] = val["Ntotale"] + atno(sym[tmp_k])
            val["Ntotalecore"] = val["Ntotalecore"] + NFC(sym[tmp_k])
    
        val["Ntotal"] = val["Ntotal"] - charge
        val["Ntotale"] = val["Ntotale"] - charge
        val["Na"] = (multip + val["Ntotal"] - 1 ) / 2.0
        val["Nb"] = val["Na"] + 1 - multip
    
        val["isatom"] = "false"
        if Nat == 1: val["isatom"] = "true"
    
        uniq_atom_res = uniqatoms(sym)
    
        rung4mp2(val, start_time_main)
        os.system("cp freq0.txt freq_cation_PA.txt")
    
        U0mol2 = U0mol - val["U0"] 
        UTmol2 = UTmol - val["UT"]
        HTmol2 = HTmol - val["HT"]
    
        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write(" *---------* \n")
            ther_chem.write(" * SUMMARY * \n")
            ther_chem.write(" *---------* \n\n")
    
            ther_chem.write(" * Proton affinity (mol - molH+) =       " + str(round(HTmol2,8))        + " Hartree\n")
            ther_chem.write(" * Proton affinity (mol - molH+) =       " + str(round(HTmol2*au2ev,8))   + " eV\n")
            ther_chem.write(" * Proton affinity (mol - molH+) =       " + str(round(HTmol2*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write(" * Proton affinity (mol - molH+) =       " + str(round(HTmol2*au2kjm,8)) + " kj/mol\n\n")
    
            ther_chem.write(" * Breakdown *\n")
            ther_chem.write(" * CCSD(T)         (mol - molH+) =       " + str(round((val["PAbreakdown1"][0]-val["PAbreakdown2"][0])*au2kcm,8))   + " kcal/mol\n")
            ther_chem.write(" * DE (MP2)        (mol - molH+) =       " + str(round((val["PAbreakdown1"][2]-val["PAbreakdown2"][2])*au2kcm,8))   + " kcal/mol\n")
            ther_chem.write(" * DE (HF)         (mol - molH+) =       " + str(round((val["PAbreakdown1"][1]-val["PAbreakdown2"][1])*au2kcm,8))   + " kcal/mol\n")
            ther_chem.write(" * HLC             (mol - molH+) =       " + str(round((val["PAbreakdown1"][3]-val["PAbreakdown2"][3])*au2kcm,8))   + " kcal/mol\n")
            ther_chem.write(" * SO              (mol - molH+) =       " + str(round((val["PAbreakdown1"][4]-val["PAbreakdown2"][4])*au2kcm,8))   + " kcal/mol\n")
            ther_chem.write(" * ZPVE            (mol - molH+) =       " + str(round((val["PAbreakdown1"][5]-val["PAbreakdown2"][5])*au2kcm,8))   + " kcal/mol\n")
            ther_chem.write(" * Vib-thermal     (mol - molH+) =       " + str(round((val["PAbreakdown1"][6]-val["PAbreakdown2"][6])*au2kcm,8))   + " kcal/mol\n")  # rewrite wont work
            ther_chem.write(" * Rot-thermal     (mol - molH+) =       " + str(round((val["PAbreakdown1"][7]-val["PAbreakdown2"][7])*au2kcm,8))   + " kcal/mol\n")
            ther_chem.write(" * Trans-thermal   (mol - molH+) =       " + str(round((val["PAbreakdown1"][8]-val["PAbreakdown2"][8])*au2kcm,8))   + " kcal/mol\n")
            ther_chem.write(" * kBT             (mol - molH+) =       " + str(round((val["PAbreakdown1"][9]-val["PAbreakdown2"][9])*au2kcm,8)) + " kcal/mol\n")
            ther_chem.write("                                   -------------------------\n")
            ther_chem.write("TOTAL                             =       " + str(round( (sum(val["PAbreakdown1"])  -sum(val["PAbreakdown2"]))*au2kcm,8)) +  " kcal/mol\n")        
            ther_chem.write("                                   -------------------------\n\n")
            end_time_n = time.time()
            ther_chem.write(" ** Elapsed time =              " + str(round(end_time_n - start_time_main,2)) + " s\n\n")

        day = datetime.datetime.today().strftime("%A")
        date = datetime.date.today()
        cur_date = date.strftime("%B %d, %Y")
        now = datetime.datetime.now()
        cur_time = now.strftime(" %H:%M:%S")

        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write("==============================================\n")
            ther_chem.write("Final time:  " + day + "  "+ cur_date + "  " + cur_time + "  " + time.tzname[0] +"  \n\n")
            ther_chem.write("==============================================\n")

        exit() 
    
    
    if val["calc_BE"] == "true":
        val["verticalIP"] = "false"
        val["IPss"] = "true"
    
        with open("geom_monomer_A.xyz", "r") as g_cat:  # need to look at this file
            num_l_xyz = sum(1 for l in g_cat)
            with open("inp.xyz", "w") as inp_x:
                linecache.clearcache()
                Nat= int(linecache.getline("geom_monomer_A.xyz",1).strip())
                #print("Nat in PA", Nat)
                tr = linecache.getline("geom_monomer_A.xyz",2).strip()
                lsp11 = tr.split()
                charge = int(lsp11[0])
                multip = int(lsp11[1])
                inp_x.write(str(Nat) + " \n")
                inp_x.write(str(charge) +" "+ str(multip) + " \n")
                sym = []   # will contain list of atom symbols in the mol # same order
                Rlist = []
                sym_coord = []
                for tmp_l in range(3,num_l_xyz+1):
                    l1_xyz_2 = linecache.getline("geom_monomer_A.xyz",tmp_l)
                    l1_lsp2 = l1_xyz_2.split()
                    full_l1 = l1_xyz_2.strip().split()
                    full_l = full_l1[0] + "     "+str(round(float(full_l1[1]),8)) + "     "+str(round(float(full_l1[2]),8)) + "     "+str(round(float(full_l1[3]),8))
                    sym_coord.append(full_l)  ## contains atom and coords
                    sym.append(l1_lsp2[0])
                    Rlist.append(l1_lsp2[1])
                    Rlist.append(l1_lsp2[2])
                    Rlist.append(l1_lsp2[3])
                    conv = np.array(Rlist)
                    R_coord = np.resize(conv,[Nat,3])
                for tmp_y in range(len(sym_coord)):
                    inp_x.write(sym_coord[tmp_y])
                    inp_x.write("\n")
    
    
        val["Ntotal"] = 0
        val["Ntotale"] = 0
        val["Ntotalecore"] = 0
        for tmp_k in range(Nat):
            na_nb_l = nanb(sym[tmp_k])
            na = na_nb_l[0]
            nb = na_nb_l[1]
            val["Ntotal"] = val["Ntotal"] + na + nb
            val["Ntotale"] = val["Ntotale"] + atno(sym[tmp_k])
            val["Ntotalecore"] = val["Ntotalecore"] + NFC(sym[tmp_k])
    
        val["Ntotal"] = val["Ntotal"] - charge
        val["Ntotale"] = val["Ntotale"] - charge
        val["Na"] = (multip + val["Ntotal"] - 1 ) / 2.0
        val["Nb"] = val["Na"] + 1 - multip
    
        val["isatom"] = "false"
        if Nat == 1: val["isatom"] = "true"
    
        uniq_atom_res = uniqatoms(sym)
    
        rung4mp2(val, start_time_main)
        os.system("cp freq0.txt freq_monomer_A.txt")
    
        U0mol2 = U0mol - (2*val["U0"])
        UTmol2 = UTmol - (2*val["UT"])
        HTmol2 = HTmol - (2*val["HT"])
    
        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write(" *---------* \n")
            ther_chem.write(" * SUMMARY * \n")
            ther_chem.write(" *---------* \n\n")
            
            ther_chem.write(" * Binding energy (A2 - 2 * A) = " +  str(U0mol2)        + " Hartree\n")
            ther_chem.write(" * Binding energy (A2 - 2 * A) = " +  str(U0mol2*au2ev)  + " eV\n")
            ther_chem.write(" * Binding energy (A2 - 2 * A) = " +  str(U0mol2*au2kcm) + " kcal/mol\n")
            ther_chem.write(" * Binding energy (A2 - 2 * A) = " +  str(U0mol2*au2kjm) + " kj/mol\n\n")
            end_time_n = time.time() 
            ther_chem.write(" ** Elapsed time =              " + str(round(end_time_n - start_time_main,2)) + " s\n\n")  # which end time!! ??

        day = datetime.datetime.today().strftime("%A")
        date = datetime.date.today()
        cur_date = date.strftime("%B %d, %Y")
        now = datetime.datetime.now()
        cur_time = now.strftime(" %H:%M:%S")

        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write("==============================================\n")
            ther_chem.write("Final time:  " + day + "  "+ cur_date + "  " + cur_time + "  " + time.tzname[0] +"  \n\n")
            ther_chem.write("==============================================\n")

        exit()    
    # !=== Atomic calculations
    
    
    if val["calc_AE"] == "true":
        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write(" * G4MP2 for reference atoms*\n\n")
    
        U0molAE = U0mol
        UTmolAE = UTmol
        HTmolAE = HTmol
        uniq_atom_res = uniqatoms(sym)
        for tmp_o in range(uniq_atom_res["N_ua"]):
            Nat = 1
            # deallocate(sym, R)
            sym =[]
            ua = uniq_atom_res["uniq_sym"]
            if Nat == 1: val["isatom"] = "true"
            sym.append(ua[tmp_o])
            with open("Thermochemistry.out", "a") as ther_chem:
                ther_chem.write(" * ATOM:" + str(sym) + "\n")
            
            na_nb_l = nanb(sym[0])   # check
            na = na_nb_l[0]
            nb = na_nb_l[1]
            R = 0 ## ask
            multip = na - nb + 1
            charge = 0
            with open("inp.xyz", "w") as new_in:
                new_in.write(str(Nat) + "\n")
                new_in.write("0  " + str(multip) + "\n")
                new_in.write(str(sym[0]) + "  0.0 0.0 0.0 \n")  # ask
    
            na_nb_l = nanb(sym[0])
            na = na_nb_l[0]
            nb = na_nb_l[1]
            val["Ntotal"] = na + nb
    
            val["Ntotale"] = atno(ua[tmp_o])
            val["Ntotalecore"] = NFC(ua[tmp_o])
            val["Na"] = (multip + val["Ntotal"] - 1 ) / 2.0
            val["Nb"] = val["Na"] + 1 - multip
    
            #print(tmp_o,Nat,ua,val["isatom"],"=== check Nat, isatom ===")
            rung4mp2(val,start_time_main)
            uan_l = uniq_atom_res["uan"]
            U0molAE = U0molAE - uan_l[tmp_o] * val["U0"] 
            UTmolAE = UTmolAE - uan_l[tmp_o] * val["UT"]
            HTmolAE = HTmolAE - uan_l[tmp_o] * val["HT"]
            HLCmol =  HLCmol -  uan_l[tmp_o] * val["HLC0"]
    
        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write(" *---------* \n")
            ther_chem.write(" * SUMMARY * \n")
            ther_chem.write(" *---------* \n\n")
    
            ther_chem.write(" * Atomization energy (Atoms - mol) = " + str(-U0molAE)  + " Hartree\n")
            ther_chem.write(" * Atomization energy (Atoms - mol) = " + str(-U0molAE*au2ev) + " eV\n")
            ther_chem.write(" * Atomization energy (Atoms - mol) = " + str(-U0molAE*au2kcm) +  " kcal/mol\n")
            ther_chem.write(" * Atomization energy (Atoms - mol) = " + str(-U0molAE*au2kjm) + " kj/mol\n")
            ther_chem.write(" * Atomization energy (Atoms - mol), NO HLC = " + str(-(U0molAE-HLCmol)*au2kcm) +  " kcal/mol\n\n")
            end_time_n = time.time() 
            ther_chem.write(" ** Elapsed time =              " + str(round(end_time_n - start_time_main,2)) + " s\n\n")  # which end time!! ??
    if val["calc_HF"] != "true":
        day = datetime.datetime.today().strftime("%A")
        date = datetime.date.today()
        cur_date = date.strftime("%B %d, %Y")
        now = datetime.datetime.now()
        cur_time = now.strftime(" %H:%M:%S")
    
        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write("==============================================\n")
            ther_chem.write("Final time:  " + day + "  "+ cur_date + "  " + cur_time + "  " + time.tzname[0] +"  \n\n")
            ther_chem.write("==============================================\n")

        exit()

    if val["calc_HF"] == "true":
        val["calc_AE"] = "true"
        HOF = HTmol - U0mol + U0molAE
        HOF_0K = []
        dH_298K_0K = []
        ua = uniq_atom_res["uniq_sym"]
        for tmp_u in range(uniq_atom_res["N_ua"]):
            HOF_0K.append(HOF_atoms(ua[tmp_u]))
            dH_298K_0K.append(dH_atoms(ua[tmp_u]))

        uan_l = uniq_atom_res["uan"]
        HOF = HTmol - U0mol + U0molAE
        for tmp_u in range(uniq_atom_res["N_ua"]):
            HOF = HOF + uan_l[tmp_u] * ( HOF_0K[tmp_u] - dH_298K_0K[tmp_u] )

        with open("Thermochemistry.out", "a") as ther_chem:
            ther_chem.write(" *---------* \n")
            ther_chem.write(" * SUMMARY * \n")
            ther_chem.write(" *---------* \n\n")

            ther_chem.write("* Heat of formation = " + str(HOF) + " Hartree\n")
            ther_chem.write("* Heat of formation = " + str(HOF*au2ev) + " eV\n")
            ther_chem.write("* Heat of formation = " + str(HOF*au2kcm) + " kcal/mol\n")
            ther_chem.write("* Heat of formation = " + str(HOF*au2kjm) + " kj/mol\n")
            ther_chem.write("* Heat of formation, NO HLC = " +  str((HOF-HLCmol)*au2kcm) + " kcal/mol\n\n")
            end_time_n = time.time()
            ther_chem.write("** Elapsed time =              " +str(round(end_time_n - start_time_main,2)) + " s\n\n")  # which end time!! ??


    day = datetime.datetime.today().strftime("%A")
    date = datetime.date.today()
    cur_date = date.strftime("%B %d, %Y")
    now = datetime.datetime.now()
    cur_time = now.strftime(" %H:%M:%S")

    with open("Thermochemistry.out", "a") as ther_chem:
        ther_chem.write("==============================================\n")
        ther_chem.write("Final time:  " + day + "  "+ cur_date + "  " + cur_time + "  " + time.tzname[0] +"  \n\n")
        ther_chem.write("==============================================\n")

 
