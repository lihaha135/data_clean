/*************************************************************************
    > File Name: CSavePcap.h
    > Author: Cxy
    > Mail: chenxingyu@wanji.net.cn 
    > Created Time: Thu 23 Jun 2022
    > Description: 封装存储PCAP文件功能
 ************************************************************************/

#ifndef CSAVEPCAP_H
#define CSAVEPCAP_H

#include <stdint.h>
#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>

using namespace std;

/*
 * Standard libpcap format.
 */
#define TCPDUMP_MAGIC 0xa1b2c3d4
#define PCAP_VERSION_MAJOR 2
#define PCAP_VERSION_MINOR 4

//pcap文件头
struct TPcapHeader
{
    uint32_t m_uiMagic = TCPDUMP_MAGIC;             /* PCAP文件标识，标识大小端 */
    uint16_t m_usVersionMajor = PCAP_VERSION_MAJOR; /* PCAP文件大版本，默认为2 */
    uint16_t m_usVersionMinor = PCAP_VERSION_MINOR; /* PCAP文件小版本，默认为4 */
    uint32_t m_uiThiszone = 0;                      /* 时间戳，默认为0 */
    uint32_t m_uiSigfigs = 0;                       /* 时间戳精度，默认为0 */
    uint32_t m_uiSnapLen = 0x0000ffff;              /* 每一篇数据的最大长度，默认为0xffff0000，即65535 */
    uint32_t m_uiLinkType = 1;                      /* 链路类型，默认为1 */
};

//每一个数据前面头
struct TPacketHeader
{
    int32_t m_iTimeSec;  /* 时间戳秒 */
    int32_t m_iTimeUsec; /* 时间戳毫秒 */
    uint32_t m_uiCapLen; /* 捕获的报文长度 */
    uint32_t m_uiOrgLen; /* 原始报文长度，一般和捕获报文长度一致 */
};

//每一个数据前面的头
struct TLidarData
{
    uint64_t m_ulTimeStamp; /* ms时间戳 */
    uint8_t m_ucBag[1350];   /* 一包雷达数据 */
    std::string m_strBag;   /* 一包雷达数据 */
};

struct TDataHeader1
{
    char m_aSrcMac[6] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00}; /* 源MAC地址 */
    char m_aDstMac[6] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00}; /* 目的MAC地址 */
    uint16_t m_usNetType = 0x0800;                            /* 网络类型： 0x0800 Ipv4*/
};
struct TDataHeader2
{
    uint8_t m_ucProVersion = 0x45;   /* 协议版本及头长度,分别为4和5*/
    uint8_t m_ucDiffFlag = 0x0;      /* 无效值 */
    uint16_t m_usLength = 1378;      /* 数据长度：Header2长度+Header3长度+数据长度*/
    uint16_t m_usIdentifacation = 0; /* 数据ID： 0-65535递增*/
    uint8_t m_ucFlags = 0x40;        /* */
    uint8_t m_ucFragOffset = 0x00;   /* */
    uint8_t m_ucTimeToLive = 0x80;   /* */
    uint8_t m_ucProtocol = 0x11;     /* 协议类型： 0x11 udp*/
    uint16_t m_usCheckSum = 0;       /* 校验位*/
    uint32_t m_uiSrcIp = 0X7F000001; /* 源IP：127.0.0.1*/
    uint32_t m_uiDstIp = 0X7F000001; /* 目的IP：127.0.0.1*/
};
struct TDataHeader3
{
    uint16_t m_usSrcPort = 3333; /* 源端口*/
    uint16_t m_usDstPort = 3001; /* 目的端口*/
    uint16_t m_usLength = 1358;  /* 数据长度：Header3长度+数据长度*/
    uint16_t m_usCheckSum = 0;   /* 校验位*/
};

class CSavePcap
{
public:
    void Init(std::string p_strSavePath, std::string p_strSaveName);

    void Exit();

    // 可以多次调用，订阅多个频道
    void SaveData(std::vector<TLidarData> p_vecFrameLidar);

    std::string GetFileName();

private:
    void SaveThread();

    void InitPcap();

    void WritePcap(TLidarData p_tOneBag);

private:
    // 运行标志位
    bool m_bRun;
    // 重新初始化标志位
    bool m_bReinit;
    // 包ID
    uint16_t m_usIdentifacation;
    // 存储路径
    std::string m_strSavePath;
    // 文件名称
    std::string m_strSaveName;
    // 文件路径
    std::string m_strSaveFilePath;
    // 数据队列
    std::queue<std::vector<TLidarData>> m_qData;
    // 存储线程
    std::thread m_thSavePcap;
    // 时间戳
    uint64_t m_ulTimeStamp;
    // 条件变量锁
    std::condition_variable m_cv;
    std::mutex m_cvMutex;
    // 文件指针
    std::ofstream *m_pFileSave;
    // 文件打开的标志位
    bool m_bOpenFile;
};

#endif