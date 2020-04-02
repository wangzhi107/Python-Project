#########################################################################
# File Name: ZenTao_WebCrawler.sh
# Author: wangzhi
# mail: wangzhi@crearo.com
# Created Time: Friday, October 11, 2019 PM01:54:53 CST
#########################################################################
#!/bin/bash

#---------------------------#
# 查询部门(department):		#
#							#
#	3	--	研发中心		#
#	5	--	项目部			#
#	6	--	软件部          #
#	7	--	系统部          #
#	8	--	嵌入部          #
#	9	--	硬件部          #
#	10	--	测试部          #
#						    #
#---------------------------#

#---------------------------#
# 查询周期(checktype):	    #
#							#
#	0	--  本周	        #
#	1	--	本月			#
#							#
#---------------------------#

if [ $# != 3 ] ; then 
python3 ZenTao_WebCrawler.py
else
python3 ZenTao_WebCrawler.py --department=${1} --checktype=${2} --name=${3}
fi
