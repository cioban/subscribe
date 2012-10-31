#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#############################################
# Sergio Cioban Filho - 29/10/2011 10:01:59
#############################################

ID_FINAL    = 'BC1B07B5-6D68-4DB2-AFA7-D8A7A1CB5FEE'
ID          = 'BC1B07B56D684DB2AFA7D8A7A1CB5FEE'
sendTransactionId = ID[:8]+'-'+ID[8:12]+'-'+ID[12:16]+'-'+ID[16:20]+'-'+ID[20:]
print sendTransactionId
print ID_FINAL

