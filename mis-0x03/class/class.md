# 课堂实验

## 伪造SSID

把所有SSID筛选出来，SSID名称为空不一定代表就是空的，也有用0填充的

使用 [chardet库](https://github.com/chardet/chardet) 对SSID的编码进行判断，其中有一个SSID让我困惑了很久，看起来是三个重复的字符，经过几次尝试之后发现是 `utf-8` 编码

这个 `👾👾👾` 其实是我在上课时候给自己开的无线热点（跪）

以下是分析结果，编码-ssid长度-ssid

### faked_essids-01-filtered.cap

```bash
GB2312         24       一旦切换到下一个其他信道                                 
ascii          8        CUC-WiFi                                     
ascii          9        CUC-Guest                                    
GB2312         24       尽可能的去模拟对所有信道                                 
utf-8          27       平板电脑等作为终端                                    
ascii          9        HoneyWifi                                    
GB2312         10       在多个信道                                        
ascii          11       404notfound                                  
utf-8          9        在家里                                          
utf-8          66       直接或通过无线应用协议访问互联网并使用其业务                       
utf-8          15       的不断提高                                        
utf-8          30       慢慢人们不满足于只能                                   
utf-8          18       求也越来越高                                       
ISO-8859-9     19       channel hopping¼¼Êõ                          
GB2312         40       才能监听到该信道在该监听时隙上的通信数据                         
utf-8          57       对随时随地在移动过程中接入互联网的需求                          
utf-8          15       人们增加了                                        
GB2312         20       于任意一个指定的信道                                   
ascii          13       <length:  12>                                
utf-8          21       随着信息化水平                                      
utf-8          33       时随地可以在移动中接入                                  
utf-8          30       是相对传统互联网而言                                   
GB2312         29       由于channel hopping的技术限制                       
GBK            8        无线网卡                                         
GB2312         21       由于STA的工作模式限制                                 
GB2312         28       直到重新又监听到该指定信道时                               
ascii          3        123                                          
ascii          11       TP-LINK_702                                  
ascii          8        vivo X6D                                     
ascii          12       CUC_ACM_2.4G                                 
utf-8          12       👾👾👾                                          
ascii          7        Honor 8                                      
ascii          3        ycj                                          
ascii          7        gamelab                                      
ascii          6        tangxu                                       
ascii          3        XIN                                          
ascii          4        1103                                         
ascii          12       HoneyWifi-5G                                 
utf-8          12       广院创造                                         
GBK            0                                                     
ascii          4        A916                                         
ascii          13       xinwanglei2.4                                
utf-8          30       当然人们对互联网的要                                   
utf-8          24       互联网并使用业务                                     
GB2312         36       则上一个信道的通信数据就不再能收集到                           
GB2312         16       数据获取（监听）                                     
utf-8          9        互联网                                          
utf-8          6        或者                                           
ascii          12       <length:  0>                                 
ascii          12       TPGuest_702.                                 
ascii          25       HP-Setup>7b-M277 LaserJet                    
ascii          4        pipi                                         
ascii          4        hhmm                                         
ascii          6        iptime                                       
ascii          12       DoMyNet_8E90                                 
GBK            14       802.11无线网络                                   
utf-8          24       一般人们可以认为                                     
utf-8          9        相应地                                          
GB2312         8        事实上对                                         
utf-8          21       已经深入到用户                                      
utf-8          54       的飞速发展正为此提供了所需的技术支撑                           
Toatal: 61
```

### faked_essids-03-filtered.cap

```bash
ascii          12       HelloCUC2016                                 
ascii          9        CUC-Guest                                    
ascii          8        CUC-WiFi                                     
ascii          5        YoMan                                        
ascii          3        WSD                                          
ascii          3        123                                          
utf-8          12       👾👾👾                                          
ascii          12       CUC_ACM_2.4G                                 
ascii          7        gamelab                                      
ascii          9        CMCC-ir3j                                    
ascii          9        CMCC-G7h7                                    
ascii          3        XIN                                          
ascii          13       xinwanglei2.4                                
ascii          12       HoneyWifi-5G                                 
ascii          9        CMCC-1402                                    
ascii          11       404notfound                                  
ascii          12       HelloCUC2018                                 
ascii          12       and-Business                                 
ascii          8        CMCC-WEB                                     
ascii          4        1601                                         
utf-8          23         小米共享WiFi_A2FC                              
ascii          15                                                    
ascii          25       HP-Setup>7b-M277 LaserJet                    
ascii          12       DoMyNet_8E90                                 
ascii          12       TP-LINK_1805                                 
GBK            0                                                     
ascii          12       TPGuest_702.                                 
ascii          4        CMCC                                         
ascii          5        LIKER                                        
ascii          12       Tenda_BB5710                                 
ascii          6        tangxu                                       
ascii          4        A916                                         
ascii          7        CU_r7ES                                      
ascii          9        HoneyWifi                                    
ascii          14       GW_AP_15760902                               
ascii          4        pipi                                         
ascii          11       Xiaomi_92A3                                  
ascii          11       TP-LINK_702                                  
ascii          7        CU_vUFZ                                      
ascii          28       CMCC-503-LMK-YN-GMH-SMX-2.4G                 
ascii          10       CUC_M_1303                                   
ascii          10       CUC_202_76                                   
ascii          3        302                                          
ascii          11       DP-LINK_666                                  
ascii          12       TP-LINK_D14C                                 
ascii          6        iptime                                       
ascii          9        1703_2.4G                                    
ascii          4        1304                                         
ascii          3        ycj                                          
ascii          14       GW_AP_15760163                               
ascii          14       TP-LINK_A1613E                               
ascii          14       ZhuerHome-2.4G                               
ascii          10       CMCC-51403                                   
ascii          11       TP-LINK_216                                  
ascii          14       360WiFi-B6CCF3                               
ascii          9        CMCC-AiNr                                    
Toatal: 56
```

## 隐藏SSID

用wireshark查看之后发现含有SSID的帧只有Beacon和Probe Response，所以就将其筛选出来，认为有 Probe Response 无 Beacon 的SSID就是隐藏SSID

以下是分析结果，编码-ssid长度-ssid

### hidden_finder-01-filtered

```bash
ascii          8        vivo X6D
ascii          12       shuzheng2.4G
utf-8          12       👾👾👾
ascii          14       PhishingInside
Toatal: 4
```

### hidden_finder-02-filtered

```bash
ascii          8        vivo X6D
utf-8          12       👾👾👾
ascii          14       PhishingInside
utf-8          12       中传光影
ascii          8        Honor 6X
ascii          6        iPhone
Toatal: 6
```

## 总结
- Python编码了解一下，不，其实应该说，**编码**了解一下

## 参阅
- [Python 编码为什么那么蛋疼？](https://www.zhihu.com/question/31833164)
- [chardet usage](https://chardet.readthedocs.io/en/latest/usage.html)