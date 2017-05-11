#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author -Jacob Xia
#ver 0.50-May.11.2017

import sys,getopt
import re
from itertools import islice  
from test.test_tarfile import LimitsTest
from _elementtree import Comment
from operator import index


ver=0.50
debug_falg=0
softBinNum = 14
testnumber = 1000
increase = 1
linux = False
TITestType="POSTBI_OS"


lower = "-1"
upper = "1"
lower_compare_state = "NA"
higher_compare_state = "NA"
unit=""
suite_namelist_93k=[]
suite_namelist_vlct=[]
testname_93k=[]
temp30lower = ""
temp30upper = ""
temp37lower = ""
temp37upper = ""
temp90lower = ""
temp90upper = ""
temp105lower = ""
temp105upper = ""
tempN45lower = ""
tempN45upper = ""
lower_compare_state = ""
higher_compare_state = ""
unit = ""

vlct_testname=[]
vlct_limitinfo=[]
softBinMap={}
hardBinMap={}
hardBinNumberMap={}

def init():
	softBinMap.clear
	hardBinMap.clear
	hardBinNumberMap.clear


def read_SuiteName(x):
    data_per_line = x.readlines()   
    for line in data_per_line:   	
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
	global temp30lower, temp30upper,temp37lower, temp37upper,temp90lower,temp90upper,temp105lower, temp105upper,tempN45lower, tempN45upper, unit
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index] == input_name):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(content[8]==""):
					if(content[9]==""):
						temp30lower = content[3]
						temp30upper = content[4]
						temp37lower = content[3]
						temp37upper = content[4]
						temp90lower = content[3]
						temp90upper = content[4]
						temp105lower = content[3]
						temp105upper = content[4]
						tempN45lower = content[3]
						tempN45upper = content[4]
						compare_state_define(content[6])
						unit = content[5]
						
	#print temp30lower, temp30upper,temp37lower, temp37upper,temp90lower,temp90upper,temp105lower, temp105upper,tempN45lower, tempN45upper, lower_compare_state, higher_compare_state,unit
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index] == input_name):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(content[8]==""):
					if(len(content[9])>0):
						temptype = content[9].split(";")
						for temp in temptype:
							specify_limit_by_temp(temp,content[3],content[4])
							compare_state_define(content[6])
							unit = content[5]
	#print temp30lower, temp30upper,temp37lower, temp37upper,temp90lower,temp90upper,temp105lower, temp105upper,tempN45lower, tempN45upper, lower_compare_state, higher_compare_state,unit
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index] == input_name):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(len(content[8])>0): # means  current TITestType existing
					if(content[9]==""):
						temp30lower = content[3]
						temp30upper = content[4]
						temp37lower = content[3]
						temp37upper = content[4]
						temp90lower = content[3]
						temp90upper = content[4]
						temp105lower = content[3]
						temp105upper = content[4]
						tempN45lower = content[3]
						tempN45upper = content[4]
						compare_state_define(content[6])
						unit = content[5]
	#print temp30lower, temp30upper,temp37lower, temp37upper,temp90lower,temp90upper,temp105lower, temp105upper,tempN45lower, tempN45upper, lower_compare_state, higher_compare_state,unit				
	for index in range(len(vlct_testname)):		
		if(vlct_testname[index] == input_name):
			content = vlct_limitinfo[index].replace("\"","").replace("\n","").split(',')
			if (testname_93k == content[2]):
				if(len(content[8])>0): # means  current TITestType existing
					if(len(content[9])>0):
						temptype = content[9].split(";")
						for temp in temptype:
							specify_limit_by_temp(temp,content[3],content[4])
							compare_state_define(content[6])
							unit = content[5] 
							
	

def compare_state_define(x):
	global lower_compare_state, higher_compare_state
	if(x == "O"):
		print "compare state O need define by user self"
	elif(x =="B"):	
		lower_compare_state = "GE"
		higher_compare_state = "LE"
	elif(x=="N"):
		lower_compare_state = "NA"
		higher_compare_state = "NA"
	elif(x=="L"):
		lower_compare_state = "GE"
		higher_compare_state = "NA"
	elif(x=="U"):
		lower_compare_state = "NA"
		higher_compare_state = "LE"
	elif(x==""):
		lower_compare_state = "GE"
		higher_compare_state = "LE"
	else:
		print "The system doesn't support this compare type: " , x
		
def specify_limit_by_temp(temp,lower,upper):
	global temp30lower, temp30upper,temp37lower, temp37upper,temp90lower,temp90upper,temp105lower, temp105upper,tempN45lower, tempN45upper
	if(temp == "TEMP_30_DEG"):
		temp30lower = lower
		temp30upper = upper
	elif(temp == "TEMP_37_DEG"):
		temp37lower = lower
		temp37upper = upper
	elif(temp == "TEMP_90_DEG"):
		temp90lower = lower
		temp90upper = upper
	elif(temp == "TEMP_105_DEG"):
		temp105lower = lower
		temp105upper = upper
	elif(temp == "TEMP_N45_DEG"):
		tempN45lower = lower
		tempN45upper = upper
	else:
		print "The system doesn't support this temperature type: " , temp	
		
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


if(debug_falg):
	for index in range(len(vlct_testname)):
		print index,vlct_testname[index]
		print index,vlct_limitinfo[index]

results = []
log =[]
testtable_headline = "Suite name,Test name,Test number,Lsl,Usl,Lsl,Usl,Lsl,Usl,Lsl,Usl,Lsl,Usl,Lsl_typ,Usl_typ,Units,Bin_s_num,Bin_s_name,Bin_h_num,Bin_h_name,Bin_type,Bin_reprobe,Bin_overon,Test_remarks\n"
testtable_secondline = "Test mode,,,TEMP_30_DEG,TEMP_30_DEG,TEMP_37_DEG,TEMP_37_DEG,TEMP_90_DEG,TEMP_90_DEG,TEMP_105_DEG,TEMP_105_DEG,TEMP_N45_DEG,TEMP_N45_DEG,,,,,,,,,,,\n"
results.append(testtable_headline)
results.append(testtable_secondline)
log_headline = " These suites did not find softBin name from vlct program, self-defined by tool:"
log.append(log_headline)

for index in range(len(suite_namelist_93k)):
	
	name93k = "%s,%s,%s," %(suite_namelist_93k[index],testname_93k[index], testnumber)
	if(running_mode == "func"):
		limit = "1,1,1,1,1,1,1,1,1,1,GE,LE,Bool,"
	elif(running_mode == "para"):
		comment = "93K parametric test"

		fill_in_limit(testname_93k[index],suite_namelist_vlct[index])
		limit = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," %(temp30lower, temp30upper,temp37lower, temp37upper,temp90lower,temp90upper,temp105lower, temp105upper,tempN45lower, tempN45upper, lower_compare_state, higher_compare_state,unit)
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
	softBinNum=softBinNum+1
	testnumber=testnumber+1

out_f = file(output_file,"w")
out_f.writelines(results)
log_f = file(log_file,"w")
log_f.writelines(log)
out_f.close()

