# -*- coding: utf-8 -*-  
global commands
import commands

class dstat_plugin(dstat):
    """
    # TCP retransmit
    RetransSegs: 重传的报文数量。
    TCPLostRetransmit: 丢失的重传SBK数量，没有TSO时，等于丢失的重传包数量
    TCPFastRetrans: 成功快速重传的SKB数量
    TCPForwardRetrans: 成功ForwardRetrans的SKB数量，Forward Retrans重传的序号高于retransmit_high的数据
    TCPSlowStartRetrans:     成功在Loss状态发送的重传SKB数量，而且这里仅记录非RTO超时进入Loss状态下的重传数量
        目前找到的一种非RTO进入Loss状态的情况就是：tcp_check_sack_reneging()函数发现
        接收端违反(renege)了之前的SACK信息时，会进入Loss状态
    TCPRetransFail:     尝试FastRetrans、ForwardRetrans、SlowStartRetrans重传失败的次数

    """
    def __init__(self):
        self.name   = 'TCP retransmit'
        self.type  = 'd'
        self.width = 10
        self.scale = 1
        self.nick  = ('Seg_retr','Lost_retr','Fast_retr','Forward_retr','SStart_retr','SACK_faild','Retr_faild', 'Syn_retr')
        self.vars  = ('RetransSegs', 'TCPLostRetransmit', 'TCPFastRetrans', 'TCPForwardRetrans', 'TCPSlowStartRetrans', 'TCPSackRecoveryFail', 'TCPRetransFail', 'TCPSynRetrans')
        self.open('/proc/net/netstat')

    def extract(self):
        netline = []
        snmpline = []
        issues = {}
        for netlines in dopen('/proc/net/netstat'):
            l = netlines.split()
            netline.append(l)
        for snmplines in dopen('/proc/net/snmp'):
            l = snmplines.split()
            snmpline.append(l)

        for i in range(len(netline[0])-1):
            issues.update({netline[0][i+1]:int(netline[1][i+1])})
        for i in range(len(snmpline[6])-1):
            issues.update({snmpline[6][i+1]:int(snmpline[7][i+1])})

        for session in self.vars: 
            self.set2[session] = issues[session]
        for session in self.set2.keys():
            self.val[session] = (self.set2[session] - self.set1[session]) / elapsed
        if step == op.delay:
            self.set1.update(self.set2)
