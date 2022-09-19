#include "save_pcap.h"
#include "CommonFunctions.h"
#include <fstream>

void CSavePcap::Init(std::string p_strSavePath, std::string p_strSaveName)
{
    m_pFileSave = nullptr;
    m_bRun = true;
    m_bReinit = true;
    m_usIdentifacation = 0;
    if (p_strSavePath.substr(p_strSavePath.size() - 1, p_strSavePath.size()).compare("/") != 0)
    {
        p_strSavePath += "/";
    }
    m_strSavePath = p_strSavePath;
    m_strSaveName = p_strSaveName;
    m_strSaveFilePath = m_strSavePath + m_strSaveName + ".pcap";
    if (!m_thSavePcap.joinable())
    {
        m_thSavePcap = std::thread(&CSavePcap::SaveThread, this);
    }
}

std::string CSavePcap::GetFileName()
{
    return m_strSaveName;
}

void CSavePcap::Exit()
{
    m_bRun = false;
    if (m_thSavePcap.joinable())
    {
        m_thSavePcap.join();
    }
    if (m_bOpenFile)
    {
        m_pFileSave->close();
        delete m_pFileSave;
        m_pFileSave = nullptr;
        m_bOpenFile = false;
    }
}

void CSavePcap::SaveData(std::vector<TLidarData> p_vecFrameLidar)
{
    m_qData.push(p_vecFrameLidar);
    m_cv.notify_all();
}

void CSavePcap::SaveThread()
{
    m_bReinit = false;
    InitPcap();
    while (m_bRun)
    {
        if (m_bReinit)
        {
            m_bReinit = false;
            InitPcap();
        }
        std::unique_lock<std::mutex> lck(m_cvMutex);
        m_cv.wait(lck);
        std ::vector<TLidarData> l_vecFrameLidar = m_qData.front();
        m_qData.pop();
        for (size_t i = 0; i < l_vecFrameLidar.size(); i++)
        {
            m_usIdentifacation++;
            WritePcap(l_vecFrameLidar[i]);
        }
    }
}

void CSavePcap::InitPcap()
{
    if (m_bOpenFile)
    {
        m_pFileSave->close();
        delete m_pFileSave;
        m_pFileSave = nullptr;
        m_bOpenFile = false;
    }
    m_pFileSave = new std::ofstream(m_strSaveFilePath, std::ios::app);
    m_bOpenFile = m_pFileSave->is_open();
    if (m_bOpenFile)
    {
        TPcapHeader l_tHeader;
        m_pFileSave->write((char *)&l_tHeader, sizeof(TPcapHeader));
    }
}

void CSavePcap::WritePcap(TLidarData p_tOneBag)
{
    if (m_bOpenFile)
    {
        TPacketHeader l_tHeader;
        TDataHeader1 l_tDataHeader1;
        TDataHeader2 l_tDataHeader2;
        TDataHeader3 l_tDataHeader3;

        l_tDataHeader2.m_usIdentifacation = m_usIdentifacation;
        l_tDataHeader2.m_usLength = sizeof(TDataHeader2) + sizeof(TDataHeader3) + p_tOneBag.m_strBag.size();

        l_tDataHeader3.m_usLength = sizeof(TDataHeader3) + p_tOneBag.m_strBag.size();

        l_tHeader.m_iTimeSec = p_tOneBag.m_ulTimeStamp / 1000;
        l_tHeader.m_iTimeSec = (p_tOneBag.m_ulTimeStamp % 1000) * 1000;
        l_tHeader.m_uiCapLen = p_tOneBag.m_strBag.size() + sizeof(TDataHeader1) + sizeof(TDataHeader2) + sizeof(TDataHeader3);
        l_tHeader.m_uiOrgLen = l_tHeader.m_uiCapLen;

        m_pFileSave->write((char *)&l_tHeader, sizeof(TPacketHeader));
        m_pFileSave->write((char *)&l_tDataHeader1, sizeof(TDataHeader1));
        m_pFileSave->write((char *)&l_tDataHeader2, sizeof(TDataHeader2));
        m_pFileSave->write((char *)&l_tDataHeader3, sizeof(TDataHeader3));

        m_pFileSave->write(p_tOneBag.m_strBag.c_str(), p_tOneBag.m_strBag.size());
    }
}