#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author -Jacob Xia
#ver 0.2-May.2.2017

import sys,getopt
import re
from test.test_tarfile import LimitsTest

ver=0.2
debug_falg=0
softBinNum = 14
testnumber = 1000
increase = 1
linux = False

def init():
	nameMap.clear
	softBinMap.clear
	hardBinMap.clear
	hardBinNumberMap.clear
	TestName93kMap.clear


def read_SuiteName(x):
    data_per_line = x.readlines()   
    for line in data_per_line:   	
    	Key = line.replace("\"","").replace("\n","").split(',');
	if len(Key)>1:	
		if(len(Key[0])>0):
			if(len(Key[1])>0):
				comment = "key->93k value->vlct"
				nameList.append(Key[1])
				nameMap[Key[1]]=Key[0] 
				TestName93kMap[Key[1]]=Key[2]
				#print Key[1],Key[0],Key[2]	
			else:
				comment ="ignore here!"
				print "Warnings: No 93k item is mapped to vlct %s item!" %Key[0]
    x.close()
    if(debug_falg==1):
    	print nameMap
    print('SuiteName mapping info has been read')

def read_HardBinNumber(x):
    data_per_line = x.readlines()   
    for line in data_per_line:   	
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
    for line in data_per_line:   	
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
    	for line in data_per_line:   	
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
opts, args = getopt.getopt(sys.argv[1:], "hi:o:l:")
input_file=""
output_file=""
log_file="./default_log"
for op, value in opts:
    if op == "-i":    
        input_file = value
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


nameList=[]
nameMap={}
softBinMap={}
hardBinMap={}
hardBinNumberMap={}
TestName93kMap={}


init()
read_SuiteName(inFile)
read_HardBinNumber(BinsNumberSheet)
read_BinInfo(BinsNameSheet)
read_DigitalTestPlan(DigitalTestPlanFile)
read_BinCode(BinCodeFile)


results = []
log =[]
testtable_headline = "Suite name,Test name,Test number,Lsl,Usl,Lsl,Usl,Lsl,Usl,Lsl_typ,Usl_typ,Units,Bin_s_num,Bin_s_name,Bin_h_num,Bin_h_name,Bin_type,Bin_reprobe,Bin_overon,Test_remarks\n"
testtable_secondline = "Test mode,,,TEMP_25_DEG,TEMP_25_DEG,TEMP_30_DEG,TEMP_30_DEG,TEMP_90_DEG,TEMP_90_DEG,,,,,,,,,,,\n"
results.append(testtable_headline)
results.append(testtable_secondline)
log_headline = " These suites did not find softBin name from vlct program, self-defined by tool:"
log.append(log_headline)
for Key in nameList:	
	if(softBinMap.has_key(nameMap[Key])):
		if(debug_falg==1):
    			print Key,nameMap[Key], softBinMap[nameMap[Key]],softBinNum, hardBinMap[nameMap[Key]],hardBinNumberMap[hardBinMap[nameMap[Key]]]		
		tmp = "%s,%s,%s,1,1,1,1,1,1,GE,LE,Bool,%s,%s,%s,%s,bad,,,\n" %(Key,TestName93kMap[Key], testnumber,softBinNum, softBinMap[nameMap[Key]],hardBinNumberMap[hardBinMap[nameMap[Key]]],hardBinMap[nameMap[Key]])
		results.append(tmp)
	elif(hardBinMap.has_key(nameMap[Key])):
		self_defined_softbin= nameMap[Key].replace("_ST","_F")
		log_tmp= "Suite:%s  SoftBin:%s\n" %(Key,self_defined_softbin)
		log.append(log_tmp)
		tmp = "%s,%s,%s,1,1,1,1,1,1,GE,LE,Bool,%s,%s,%s,%s,bad,,,\n" %(Key,TestName93kMap[Key], testnumber,softBinNum, self_defined_softbin,hardBinNumberMap[hardBinMap[nameMap[Key]]],hardBinMap[nameMap[Key]])
		results.append(tmp)
		
	else:
		print "Warnings: %s did not find binning info in vlct program!" %nameMap[Key]
		comment = "Warning here, no bin info "
		
	softBinNum=softBinNum+1
	testnumber=testnumber+1

out_f = file(output_file,"w")
out_f.writelines(results)
log_f = file(log_file,"w")
log_f.writelines(log)
out_f.close()

