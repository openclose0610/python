#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author -Jacob Xia
#ver 0.6-May.12.2017

import sys,getopt
import re
from itertools import islice  


ver=0.6
debug_falg=0
softBinNum = 900
testnumber = 11000
increase = 1
linux = True
TITestType="POSTBI_OS"
TIDeviceType="F791790_AAN_MS"
tempList=["TEMP_30_DEG","TEMP_37_DEG","TEMP_90_DEG","TEMP_105_DEG","TEMP_N45_DEG"]


lower = "-1"
upper = "1"
suite_namelist_93k=[]
suite_namelist_vlct=[]
testname_93k=[]
# temp30lower = ""
# upper_map["TEMP_30_DEG"] = ""
# lower_map["TEMP_37_DEG"] = ""
# upper_map["TEMP_37_DEG"] = ""
# lower_map["TEMP_90_DEG"] = ""
# upper_map["TEMP_90_DEG"] = ""
# lower_map["TEMP_105_DEG"] = ""
# upper_map["TEMP_105_DEG"] = ""
# lower_map["TEMP_N45_DEG"] = ""
# upper_map["TEMP_N45_DEG"] = ""
# temp30_lower_compare_state = ""
# temp30_upper_compare_state = ""
# temp37_lower_compare_state = ""
# temp37_upper_compare_state = ""
# temp90_lower_compare_state = ""
# temp90_upper_compare_state = ""
# temp105_lower_compare_state = ""
# temp105_upper_compare_state = ""
# tempN45_lower_compare_state = ""
# tempN45_upper_compare_state = ""
lower_compare_state = ""
upper_compare_state = ""
unit = ""

vlct_testname=[]
vlct_limitinfo=[]
existList_tmp=[]
softBinMap={}
softBinNumberMap={}
hardBinMap={}
hardBinNumberMap={}

lower_map={}
upper_map={}
lower_compare_state_map={}
upper_compare_state_map={}

def init():
	softBinMap.clear
	hardBinMap.clear
	hardBinNumberMap.clear


def read_SuiteName(x):
    data_per_line = x.readlines()   
    for line in islice(data_per_line,1,None):  	
    	Key = line.replace("\"","").replace("\n","").split(',');
	if len(Key)>1:	
		if(len(Key[0])>0):
			if(len(Key[1])>0):
				comment = "key->93k value->vlct"
				suite_namelist_93k.append(Key[1])
				suite_namelist_vlct.append(Key[0])
				testname_93k.append(Key[2])
				#nameMap[Key[1]]=Key[0] 
				#TestName93kMap[Key[1]]=Key[2]
				#print Key[1],Key[0],Key[2]	
			else:
				comment ="ignore here!"
				print "Warnings: No 93k item is mapped to vlct %s item!" %Key[0]
    x.close()

    print('SuiteName mapping info has been read')

def read_HardBinNumber(x):
    data_per_line = x.readlines()   
    for line in islice(data_per_line,1,None):   	
    	Key = line.replace("\"","").replace("\n","").split(',');
	if len(Key)>3:	
		if(len(Key[0])>0):
			hardBinNumberMap[Key[1].upper()]=Key[2]
				
    x.close()
    if(debug_falg==1):
    	print hardBinNumberMap
    print('HardBinNumber has been read')

def read_BinInfo(x):
    data_per_line = x.readlines()   
    for line in islice(data_per_line,1,None):   	
    	Key = line.replace("\"","").replace("\n","").split(',');
	if len(Key)>6:	
		if(len(Key[0])>0):
			#print Key[2],Key[3],Key[4]
			softBinMap[Key[2]]=Key[3].upper()
			hardBinMap[Key[2]]=Key[4].upper()	
    x.close()
    if(debug_falg==1):
    	print softBinMap
	print hardBinMap
    print('BinInfo has been read')


def read_DigitalTestPlan(x):
	data_per_line = x.readlines()   
    	for line in islice(data_per_line,1,None):   	
    		Key = line.replace("\"","").replace("\n","").split(',');
		if len(Key)>10:	
			if(len(Key[0])>0):
				vlct_testname = Key[1].upper()
				if(hardBinMap.has_key(vlct_testname)): 
					if(Key[4] != hardBinMap[vlct_testname]):
						print "Warinings: [HardBin mismatch] TestName:%s ; From vlct BinSheet:%s  ; From vlct BinCode:%s;" %(vlct_testname,hardBinMap[vlct_testname],Key[4])
				else:
					comment ="Insert this name"
					hardBinMap[vlct_testname]=Key[4]
					#print "Insert : key:%s  ; value:%s;" %(vlct_testname,Key[4])			

    	x.close()
    	print('DigitalTstPlan has been read')

def read_BinCode(x):
	data_per_line = x.readlines()   
    	for line in data_per_line: 
		searchBinDefine  = re.search( r'BinDefine\s*\((\w+)\s*,\s*(\d+)\s*,\s*(\w+)\s*\)', line, re.M|re.I)
		if searchBinDefine:
			if(debug_falg==1):
				print "search --> searchBinDefine.group() : ", searchBinDefine.group()
				print "search --> searchBinDefine.group() : ", searchBinDefine.group(1)
				print "search --> searchBinDefine.group() : ", searchBinDefine.group(2)
				print "search --> searchBinDefine.group() : ", searchBinDefine.group(3)
			
			vlct_hardBinName = searchBinDefine.group(1).upper()
			vlct_hardBinNumber = searchBinDefine.group(2)
			if(hardBinNumberMap.has_key(vlct_hardBinName)): 
				if(vlct_hardBinNumber != hardBinNumberMap[vlct_hardBinName]):
					print "Warinings: [HardBinNumber mismatch] HardBinName:%s ; From vlct BinSheet:%s  ; From vlct BinCode:%s;" %(vlct_hardBinName,hardBinNumberMap[vlct_hardBinName],vlct_hardBinNumber)
			else:
				comment ="Insert this pair"
				hardBinNumberMap[vlct_hardBinName]=vlct_hardBinNumber
				#print "Insert : key:%s  ; value:%s;" %(vlct_hardBinName,vlct_hardBinNumber)
			
		
    		searchCategoryDefine= re.search( r'CategoryDefine\((\w+),(\w+),\w+,-(\w+)\);', line, re.M|re.I)	
		if searchCategoryDefine:
			if(debug_falg==1):
   				print "search --> searchCategoryDefine.group() : ", searchCategoryDefine.group()
				print "search --> searchCategoryDefine.group() : ", searchCategoryDefine.group(1)
				print "search --> searchCategoryDefine.group() : ", searchCategoryDefine.group(2)
				print "search --> searchCategoryDefine.group() : ", searchCategoryDefine.group(3)
				
			vlct_testname = searchCategoryDefine.group(3).upper()
			vlct_softBin = searchCategoryDefine.group(1).upper()
			vlct_hardBin = searchCategoryDefine.group(2).upper()
			if(hardBinMap.has_key(vlct_testname)): 
				if(vlct_hardBin != hardBinMap[vlct_testname]):
					print "Warinings: [HardBin mismatch] TestName:%s ; From vlct BinSheet:%s  ; From vlct BinCode:%s;" %(vlct_testname,hardBinMap[vlct_testname],vlct_hardBin)
			else:
				comment ="Insert this pair"
				hardBinMap[vlct_testname]=vlct_hardBin
				#print "Insert : key:%s  ; value:%s;" %(vlct_testname,vlct_hardBin)
				
			if(softBinMap.has_key(vlct_testname)): 
				if(vlct_softBin != softBinMap[vlct_testname]):
					print "Warinings: [SoftBin mismatch] TestName:%s ; From vlct BinSheet:%s  ; From vlct BinCode:%s;" %(vlct_testname,softBinMap[vlct_testname],vlct_softBin)
			else:
				comment ="Insert this pair"
				softBinMap[vlct_testname]=vlct_softBin
				#print "Insert : key:%s  ; value:%s;" %(vlct_testname,vlct_softBin)		

		else:
			if(debug_falg==1):
   				print "No match!!"	

    	x.close()
    	print('BinCode has been read')

def read_limitcsv(x):
	data_per_line = x.readlines()   
    	for line in islice(data_per_line,2,None): 
#     		print line,
    		Key = line.replace("\"","").replace("\n","").split(',')
    		comment = "checkTITestType"
		if(len(Key[7])>0):
			deviceTypeContent = Key[7].split(';')
			for name in deviceTypeContent:
				if(name == TIDeviceType):
					if(Key[8] == ""):    		
						vlct_testname.append(Key[0])
						vlct_limitinfo.append(line)
    					else:
    						TestTypeContent = Key[8].split(";")
    		 				for TestType in TestTypeContent:
    		 	 				if(TestType == TITestType):
    			   					vlct_testname.append(Key[0])
    								vlct_limitinfo.append(line)
		else:				#empty		
	    		if(Key[8] == ""):    		
				vlct_testname.append(Key[0])
				vlct_limitinfo.append(line)
    			else:
    				TestTypeContent = Key[8].split(";")
    		 		for TestType in TestTypeContent:
    		 	 		if(TestType == TITestType):
    			   			vlct_testname.append(Key[0])
    						vlct_limitinfo.append(line)
  	x.close()
	print "limit table ",x," has been read"

def fill_in_limit(testname_93k,input_name):
	comment = "fill in limit function"
	global upper_map, lower_map, upper_compare_state_map, lower_compare_state_map
	global unit
	##### empty TITestType
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index].upper() == input_name.upper()):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(content[8]=="" and content[7]==""):
					if(content[9]==""):
						for temp in tempList:
							lower_map[temp] = content[3]
							upper_map[temp] = content[4]

						compare_state_define(content[6],"All")

						unit = content[5]
						
	
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index].upper() == input_name.upper()):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(content[8]=="" and content[7]==""):
					if(len(content[9])>0):
						temptype = content[9].split(";")
						for temp in temptype:
							specify_limit_by_temp(temp,content[3],content[4])
							compare_state_define(content[6],temp)
							unit = content[5]
	
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index].upper() == input_name.upper()):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(len(content[8])>0 and content[7]==""): # means  current TITestType existing
					if(content[9]==""):
						for temp in tempList:
							lower_map[temp] = content[3]
							upper_map[temp] = content[4]

						compare_state_define(content[6],"All")
						unit = content[5]
					
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index].upper() == input_name.upper()):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(len(content[8])>0 and content[7]==""): # means  current TITestType existing
					if(len(content[9])>0):
						temptype = content[9].split(";")
						for temp in temptype:
							specify_limit_by_temp(temp,content[3],content[4])
							compare_state_define(content[6],temp)
							unit = content[5] 
							
	##### match TITestType
	
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index].upper() == input_name.upper()):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(content[8]=="" and len(content[7])>0):
					if(content[9]==""):
						for temp in tempList:
							lower_map[temp] = content[3]
							upper_map[temp] = content[4]

						compare_state_define(content[6],"All")
						unit = content[5]
						
	
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index].upper() == input_name.upper()):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(content[8]=="" and len(content[7])>0):
					if(len(content[9])>0):
						temptype = content[9].split(";")
						for temp in temptype:
							specify_limit_by_temp(temp,content[3],content[4])
							compare_state_define(content[6],temp)
							unit = content[5]
	
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index].upper() == input_name.upper()):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(len(content[8])>0 and len(content[7])>0): # means  current TITestType existing
					if(content[9]==""):
						for temp in tempList:
							lower_map[temp] = content[3]
							upper_map[temp] = content[4]

						compare_state_define(content[6],"All")
						unit = content[5]
					
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index].upper() == input_name.upper()):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(len(content[8])>0 and len(content[7])>0): # means  current TITestType existing
					if(len(content[9])>0):
						temptype = content[9].split(";")
						for temp in temptype:
							specify_limit_by_temp(temp,content[3],content[4])
							compare_state_define(content[6],temp)
							unit = content[5] 
							
	

def compare_state_define(x,temp):
	global lower_compare_state_map, upper_compare_state_map
	if(x == "O"):
		print "compare state O need define by user self"
	elif(x =="B"):
		if(temp == "All"):
			for index in tempList:
				lower_compare_state_map[index] = "GE"
				upper_compare_state_map[index] = "LE"
		else:
			lower_compare_state_map[temp] = "GE"
			upper_compare_state_map[temp] = "LE"
		# lower_compare_state = "GE"
		# upper_compare_state = "LE"

	elif(x=="N"):
		if (temp == "All"):
			for index in tempList:
				lower_compare_state_map[index] = "NA"
				upper_compare_state_map[index] = "NA"
		else:
			lower_compare_state_map[temp] = "NA"
			upper_compare_state_map[temp] = "NA"
		# lower_compare_state = "NA"
		# upper_compare_state = "NA"
	elif(x=="L"):
		if (temp == "All"):
			for index in tempList:
				lower_compare_state_map[index] = "GE"
				upper_compare_state_map[index] = "NA"
		else:
			lower_compare_state_map[temp] = "GE"
			upper_compare_state_map[temp] = "NA"
		# lower_compare_state = "GE"
		# upper_compare_state = "NA"
	elif(x=="U"):
		if (temp == "All"):
			for index in tempList:
				lower_compare_state_map[index] = "NA"
				upper_compare_state_map[index] = "LE"
		else:
			lower_compare_state_map[temp] = "NA"
			upper_compare_state_map[temp] = "LE"

		# lower_compare_state = "NA"
		# upper_compare_state = "LE"
	elif(x==""):
		if (temp == "All"):
			for index in tempList:
				lower_compare_state_map[index] = "GE"
				upper_compare_state_map[index] = "LE"
		else:
			lower_compare_state_map[temp] = "GE"
			upper_compare_state_map[temp] = "LE"

		# lower_compare_state = "GE"
		# upper_compare_state = "LE"
	else:
		print "The system doesn't support this compare type: " , x
		
def specify_limit_by_temp(temp,lower,upper):
	global lower_map,upper_map
	if(temp == "TEMP_30_DEG"):
		lower_map[temp] = lower
		upper_map[temp] = upper
	elif(temp == "TEMP_37_DEG"):
		lower_map[temp] = lower
		upper_map[temp] = upper
	elif(temp == "TEMP_90_DEG"):
		lower_map[temp] = lower
		upper_map[temp] = upper
	elif(temp == "TEMP_105_DEG"):
		lower_map[temp] = lower
		upper_map[temp] = upper
	elif(temp == "TEMP_N45_DEG"):
		lower_map[temp] = lower
		upper_map[temp] = upper
	else:
		print "The system doesn't support this temperature type: " , temp	
		
def get_Testware_Parm_Name(input_name):
	existList_tmp=[]
	result_tmp = "nonexist"
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index].upper() == input_name.upper()):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			for name in existList_tmp:
				if(name == content[2]):
					result_tmp="exist"
					break
				else:
					result_tmp="nonexist"
			if(result_tmp=="nonexist"):
				existList_tmp.append(content[2])
			
	return existList_tmp	
		
def usage():
    print("")
    print("***Help Info***")
    print("Auto Bin Info Generation ver: %s"%ver)
    
    print("demo: python auto_bin.py -i ./TestSuiteName_Map.csv -o output.csv")
    print("-i TestSuiteName Map file")
    print("-o output testtable file")
    print("-l show log")
    print("")
    
    print("TestSuiteName Map file format:")
    print("vlct_suite_name1,93k_suite_name1,93k_testname1")
    print("vlct_suite_name2,93k_suite_name2,93k_testname2")
    print("")
    print("default testnumber start from 1000; softbin start from 14; increase step 1")    
    print("")
    

#arg-begin    
opts, args = getopt.getopt(sys.argv[1:], "hi:m:o:l:")
input_file=""
output_file=""
running_mode="func" #func, para; default func
log_file="./default_log"
for op, value in opts:
    if op == "-i":    
        input_file = value
    elif op == "-m":    
	   running_mode = value
    elif op == "-o":
        output_file = value
    elif op == "-l":
        log_file = value
    elif op == "-h":
        usage()
        sys.exit()        
#arg-end

#main 	
inFile = file(input_file)	
if(linux):
	#linux
	prgm_path = "/projects/OMAP5_RPC/VLCT_documents/Testprogram_VLCT_REV37/"	
else:
	#windows
	prgm_path = "D:/TI/OMAP5/OMAP5_RPC_VLCT/VLCT_documents/Testprogram_VLCT_REV37/"
		
BinsNumberSheet = file(prgm_path+"BINS/hardbinsDefinition.csv","r")
BinsNameSheet = file(prgm_path+"BINS/binsAuditPOSTBI_OS.csv","r")
DigitalTestPlanFile = file(prgm_path+"DIGITAL/digitalTestPlanData.csv","r")
BinCodeFile =  file(prgm_path+"BINS/binsPOSTBI_OS.p","r")

ANALOGLimitSheet = file(prgm_path+"ANALOG/analogLimits.csv","r")
AVSLimitSheet = file(prgm_path+"AVS/avsLimits.csv","r")
AVSPATTERNLimitSheet = file(prgm_path+"AVS/avsPatternLimits.csv","r")
CONTYLimitSheet = file(prgm_path+"CONTY/contyLimits.csv","r")
DCPARALimitSheet = file(prgm_path+"DCPARA/dcparaLimits.csv","r")
DCPARAPERPINLimitSheet = file(prgm_path+"DCPARA/dcparaPerPinLimits.csv","r")
IDDQLimitSheet = file(prgm_path+"IDDQ/iddqLimits.csv","r")
DIGITALLimitSheet = file(prgm_path+"DIGITAL/digitalLimits.csv","r")
ODPLimitSheet = file(prgm_path+"ODP/odpLimits.csv","r")
UTILITIESLimitSheet = file(prgm_path+"UTILITIES/diagLimits.csv","r")
CRESLimitSheet = file(prgm_path+"CONTY/contyCresLimits.csv","r")





init()

read_SuiteName(inFile)
read_HardBinNumber(BinsNumberSheet)
read_BinInfo(BinsNameSheet)
read_DigitalTestPlan(DigitalTestPlanFile)
read_BinCode(BinCodeFile)
read_limitcsv(IDDQLimitSheet)
read_limitcsv(DIGITALLimitSheet)
read_limitcsv(ODPLimitSheet)
read_limitcsv(UTILITIESLimitSheet)
read_limitcsv(DCPARALimitSheet)
read_limitcsv(DCPARAPERPINLimitSheet)
read_limitcsv(ANALOGLimitSheet)
read_limitcsv(AVSLimitSheet)
read_limitcsv(AVSPATTERNLimitSheet)
read_limitcsv(CONTYLimitSheet)
read_limitcsv(CRESLimitSheet)


if(debug_falg):
	for index in range(len(vlct_testname)):
		print index,vlct_testname[index]
		print index,vlct_limitinfo[index]

results = []
log =[]
testtable_headline = "Suite name,Test name,Pins,Test number,"
for temp in tempList:
	tmp = "Lsl,Usl,Lsl_typ,Usl_typ,"
	testtable_headline = testtable_headline+tmp
tmp = "Units,Bin_s_num,Bin_s_name,Bin_h_num,Bin_h_name,Bin_type,Bin_reprobe,Bin_overon,Test_remarks\n"
testtable_headline = testtable_headline+tmp


testtable_secondline = "Test mode,,,,"
for temp in tempList:
	tmp = "%s,%s,%s,%s," %(temp, temp, temp, temp)
	testtable_secondline = testtable_secondline+tmp
tmp = ",,,,,,,,,,\n"
testtable_secondline = testtable_secondline+tmp

results.append(testtable_headline)
results.append(testtable_secondline)
log_headline = " These suites did not find softBin name from vlct program, self-defined by tool:"
log.append(log_headline)

for index in range(len(suite_namelist_93k)):

	Increase_softbin= True

	if(testname_93k[index]!=""):
		name93k = "%s,%s,,%s," %(suite_namelist_93k[index],testname_93k[index], testnumber)
		if(running_mode == "func"):
			limit = "1,1,1,1,1,1,1,1,1,1,GE,LE,Bool,"
		elif(running_mode == "para"):
			comment = "93K parametric test"
	
			fill_in_limit(testname_93k[index],suite_namelist_vlct[index])
			limit = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," %(lower_map["TEMP_30_DEG"], upper_map["TEMP_30_DEG"],lower_map["TEMP_37_DEG"], upper_map["TEMP_37_DEG"],lower_map["TEMP_90_DEG"],upper_map["TEMP_90_DEG"],lower_map["TEMP_105_DEG"], upper_map["TEMP_105_DEG"],lower_map["TEMP_N45_DEG"], upper_map["TEMP_N45_DEG"], lower_compare_state, upper_compare_state,unit)
	 	else:
			print "not support this running mode : ", running_mode
			break
		
		UpperCaseSuiteName = suite_namelist_vlct[index].upper()
		if(softBinMap.has_key(UpperCaseSuiteName)):
			bin_info = "%s,%s,%s,%s,bad,,,\n"  %(softBinNum, softBinMap[UpperCaseSuiteName],hardBinNumberMap[hardBinMap[UpperCaseSuiteName]],hardBinMap[UpperCaseSuiteName])
		elif(hardBinMap.has_key(UpperCaseSuiteName)):
			self_defined_softbin= UpperCaseSuiteName.replace("_ST","_F")
			log_tmp= "Suite:%s  SoftBin:%s\n" %(suite_namelist_93k[index],self_defined_softbin)
			log.append(log_tmp)
			bin_info = "%s,%s,%s,%s,bad,,,\n" %(softBinNum, self_defined_softbin,hardBinNumberMap[hardBinMap[UpperCaseSuiteName]],hardBinMap[UpperCaseSuiteName])
		else:
			print "Warnings: %s did not find bin info in vlct program!" %UpperCaseSuiteName
			bin_info = ",,,,bad,,,\n"
			comment = "Warning here, no bin info "
		results.append(name93k+limit+bin_info)
		testnumber=testnumber+1
	else:
		comment = "Doesn't support functional mode here"
		
		#print testnumber
		if(testnumber%100 != 0):
			testnumber=(testnumber//100+1) *100 
		else:
			testnumber=testnumber 

		#print testnumber
		
		golden_tml_dummy_func = "functional"

		golden_tml_line="%s,%s,,%s," %(suite_namelist_93k[index],golden_tml_dummy_func, testnumber)
		for temp in tempList:
			tmp_limit = "%s,%s,%s,%s," % ("", "", "NA", "NA")
			golden_tml_line = golden_tml_line + tmp_limit
		tmp_limit = ",,,,,,,,,\n"
		golden_tml_line = golden_tml_line + tmp_limit

		results.append(golden_tml_line)
		testnumber=testnumber+1 
		#print testnumber	
			
		tmp_testname_List = get_Testware_Parm_Name(suite_namelist_vlct[index])			
		#print tmp_testname_List
		
		for testname in tmp_testname_List:
			name93k = "%s,%s,,%s," %(suite_namelist_93k[index],testname, testnumber)
			fill_in_limit(testname,suite_namelist_vlct[index])
			limit = ""
			for temp in tempList:
				tmp_limit = "%s,%s,%s,%s," %(lower_map[temp], upper_map[temp],lower_compare_state_map[temp],upper_compare_state_map[temp])
				limit = limit+ tmp_limit
			tmp_limit = "%s," %unit
			limit = limit +tmp_limit
			
			UpperCaseSuiteName = suite_namelist_vlct[index].upper()
			if(softBinMap.has_key(UpperCaseSuiteName)):
				if(softBinNumberMap.has_key(softBinMap[UpperCaseSuiteName])):
					bin_info = "%s,%s,%s,%s,bad,,,\n" % (
					softBinNumberMap[softBinMap[UpperCaseSuiteName]], softBinMap[UpperCaseSuiteName], hardBinNumberMap[hardBinMap[UpperCaseSuiteName]],
					hardBinMap[UpperCaseSuiteName])
					Increase_softbin=False
				else:
					softBinNum = softBinNum + 1
					bin_info = "%s,%s,%s,%s,bad,,,\n"  %(softBinNum, softBinMap[UpperCaseSuiteName],hardBinNumberMap[hardBinMap[UpperCaseSuiteName]],hardBinMap[UpperCaseSuiteName])
					softBinNumberMap[softBinMap[UpperCaseSuiteName]]=softBinNum
					Increase_softbin = True


			elif(hardBinMap.has_key(UpperCaseSuiteName)):
				self_defined_softbin= UpperCaseSuiteName.replace("_ST","_F")
				log_tmp= "Suite:%s  SoftBin:%s\n" %(suite_namelist_93k[index],self_defined_softbin)
				log.append(log_tmp)
				if(softBinNumberMap.has_key(self_defined_softbin)):
					bin_info = "%s,%s,%s,%s,bad,,,\n" % (
					softBinNumberMap[self_defined_softbin], self_defined_softbin,
					hardBinNumberMap[hardBinMap[UpperCaseSuiteName]],
					hardBinMap[UpperCaseSuiteName])
					Increase_softbin = False
				else:
					softBinNum = softBinNum + 1
					bin_info = "%s,%s,%s,%s,bad,,,\n" %(softBinNum, self_defined_softbin,hardBinNumberMap[hardBinMap[UpperCaseSuiteName]],hardBinMap[UpperCaseSuiteName])
					softBinNumberMap[self_defined_softbin] = softBinNum
					Increase_softbin = True

			else:
				print "Warnings: %s did not find bin info in vlct program!" %UpperCaseSuiteName
				bin_info = ",,,,bad,,,\n"
				comment = "Warning here, no bin info "
			results.append(name93k+limit+bin_info)
			testnumber=testnumber+1
		results.append(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n") #dummy line

	# if(Increase_softbin):
	# 	softBinNum=softBinNum+1

out_f = file(output_file,"w")
out_f.writelines(results)
log_f = file(log_file,"w")
log_f.writelines(log)
out_f.close()

