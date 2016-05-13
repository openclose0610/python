#!/usr/bin/env python
# -*- coding:utf-8 -*-

from xpinyin import Pinyin

in_f = file('e:/Downloads/iCloud vCards yidaochu.vcf')
#data = in_f.read()
data_per_line = in_f.readlines()
results = []
#out_f.write(data)
for line in data_per_line:
    Key = line.split(':')
    if len(Key)>1:        
        result_key = '%s:%s' %(Key[0],Key[1])
        array = Key[1].split(';')
        
    else:
        result_key = '%s:\n' %(Key[0])
    
    p = Pinyin()          
    tmp = unicode (array[0],'utf-8')
    First_name_Key = p.get_pinyin(tmp).capitalize()
    
    Phonetic_line = 'X-PHONETIC-LAST-NAME:%s\n' % First_name_Key
    if Key[0] == 'N':
        results.append (result_key)
        results.append (Phonetic_line)
    elif Key[0] == 'N;LANGUAGE=en-us':
        results.append (result_key)
        #results.append (Phonetic_line)
    elif Key[0] == 'X-PHONETIC-LAST-NAME':
        comment = 'did nothing'
    else:
        results.append(line)
in_f.close()
out_f = file('e:/Downloads/iCloud vCards yidaochu.vcf_out.vcf',"w")
out_f.writelines(results)
out_f.close()            
            
            
            
