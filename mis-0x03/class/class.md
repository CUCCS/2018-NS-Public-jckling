# 课堂实验

## 伪造SSID

把所有SSID筛选出来，SSID名称为空不一定代表就是空的，也有用0填充的

使用 [chardet库](https://github.com/chardet/chardet) 对SSID的编码进行判断，其中有一个SSID让我困惑了很久，看起来是三个重复的字符，经过几次尝试之后发现是 `utf-8` 编码

这个 `👾👾👾` 其实是我在上课时候给自己开的无线热点（跪）

以下是分析结果，编码-ssid长度-ssid

### faked_essids-01-filtered.cap

```bash
GB2312          24        一旦切换到下一个其他信道                                  D2BBB5A9C7D0BBBBB5BDCFC2D2BBB8F6C6E4CBFBD0C5B5C0                                                                        
ascii           8         CUC-WiFi                                      4355432D57694669                                                                                                        
ascii           9         CUC-Guest                                     4355432D4775657374                                                                                                      
GB2312          24        尽可能的去模拟对所有信道                                  BEA1BFC9C4DCB5C4C8A5C4A3C4E2B6D4CBF9D3D0D0C5B5C0                                                                        
utf-8           27        平板电脑等作为终端                                     E5B9B3E69DBFE794B5E88491E7AD89E4BD9CE4B8BAE7BB88E7ABAF                                                                  
ascii           9         HoneyWifi                                     486F6E657957696669                                                                                                      
GB2312          10        在多个信道                                         D4DAB6E0B8F6D0C5B5C0                                                                                                    
ascii           11        404notfound                                   3430346E6F74666F756E64                                                                                                  
utf-8           9         在家里                                           E59CA8E5AEB6E9878C                                                                                                      
utf-8           66        直接或通过无线应用协议访问互联网并使用其业务                        E79BB4E68EA5E68896E9809AE8BF87E697A0E7BABFE5BA94E794A8E58D8FE8AEAEE8AEBFE997AEE4BA92E88194E7BD91E5B9B6E4BDBFE794A8E585B6E4B89AE58AA1
utf-8           15        的不断提高                                         E79A84E4B88DE696ADE68F90E9AB98                                                                                          
utf-8           30        慢慢人们不满足于只能                                    E685A2E685A2E4BABAE4BBACE4B88DE6BBA1E8B6B3E4BA8EE58FAAE883BD                                                            
utf-8           18        求也越来越高                                        E6B182E4B99FE8B68AE69DA5E8B68AE9AB98                                                                                    
ISO-8859-9      19        channel hopping¼¼Êõ                           6368616E6E656C20686F7070696E67BCBCCAF5                                                                                  
GB2312          40        才能监听到该信道在该监听时隙上的通信数据                          B2C5C4DCBCE0CCFDB5BDB8C3D0C5B5C0D4DAB8C3BCE0CCFDCAB1CFB6C9CFB5C4CDA8D0C5CAFDBEDD                                        
utf-8           57        对随时随地在移动过程中接入互联网的需求                           E5AFB9E99A8FE697B6E99A8FE59CB0E59CA8E7A7BBE58AA8E8BF87E7A88BE4B8ADE68EA5E585A5E4BA92E88194E7BD91E79A84E99C80E6B182      
utf-8           15        人们增加了                                         E4BABAE4BBACE5A29EE58AA0E4BA86                                                                                          
GB2312          20        于任意一个指定的信道                                    D3DAC8CED2E2D2BBB8F6D6B8B6A8B5C4D0C5B5C0                                                                                
ascii           13        <length:  12>                                 3C6C656E6774683A202031323E                                                                                              
utf-8           21        随着信息化水平                                       E99A8FE79D80E4BFA1E681AFE58C96E6B0B4E5B9B3                                                                              
utf-8           33        时随地可以在移动中接入                                   E697B6E99A8FE59CB0E58FAFE4BBA5E59CA8E7A7BBE58AA8E4B8ADE68EA5E585A5                                                      
utf-8           30        是相对传统互联网而言                                    E698AFE79BB8E5AFB9E4BCA0E7BB9FE4BA92E88194E7BD91E8808CE8A880                                                            
GB2312          29        由于channel hopping的技术限制                        D3C9D3DA6368616E6E656C20686F7070696E67B5C4BCBCCAF5CFDED6C6                                                              
GBK             8         无线网卡                                          CEDECFDFCDF8BFA8                                                                                                        
GB2312          21        由于STA的工作模式限制                                  D3C9D3DA535441B5C4B9A4D7F7C4A3CABDCFDED6C6                                                                              
GB2312          28        直到重新又监听到该指定信道时                                D6B1B5BDD6D8D0C2D3D6BCE0CCFDB5BDB8C3D6B8B6A8D0C5B5C0CAB1                                                                
ascii           3         123                                           313233                                                                                                                  
ascii           11        TP-LINK_702                                   54502D4C494E4B5F373032                                                                                                  
ascii           8         vivo X6D                                      7669766F20583644                                                                                                        
ascii           12        CUC_ACM_2.4G                                  4355435F41434D5F322E3447                                                                                                
utf-8           12        👾👾👾                                           F09F91BEF09F91BEF09F91BE                                                                                                
ascii           7         Honor 8                                       486F6E6F722038                                                                                                          
ascii           3         ycj                                           79636A                                                                                                                  
ascii           7         gamelab                                       67616D656C6162                                                                                                          
ascii           6         tangxu                                        74616E677875                                                                                                            
ascii           3         XIN                                           58494E                                                                                                                  
ascii           4         1103                                          31313033                                                                                                                
ascii           12        HoneyWifi-5G                                  486F6E6579576966692D3547                                                                                                
utf-8           12        广院创造                                          E5B9BFE999A2E5889BE980A0                                                                                                
GBK             0                                                                                                                                                                               
ascii           4         A916                                          41393136                                                                                                                
ascii           13        xinwanglei2.4                                 78696E77616E676C6569322E34                                                                                              
utf-8           30        当然人们对互联网的要                                    E5BD93E784B6E4BABAE4BBACE5AFB9E4BA92E88194E7BD91E79A84E8A681                                                            
utf-8           24        互联网并使用业务                                      E4BA92E88194E7BD91E5B9B6E4BDBFE794A8E4B89AE58AA1                                                                        
GB2312          36        则上一个信道的通信数据就不再能收集到                            D4F2C9CFD2BBB8F6D0C5B5C0B5C4CDA8D0C5CAFDBEDDBECDB2BBD4D9C4DCCAD5BCAFB5BD                                                
GB2312          16        数据获取（监听）                                      CAFDBEDDBBF1C8A1A3A8BCE0CCFDA3A9                                                                                        
utf-8           9         互联网                                           E4BA92E88194E7BD91                                                                                                      
utf-8           6         或者                                            E68896E88085                                                                                                            
ascii           12        <length:  0>                                  3C6C656E6774683A2020303E                                                                                                
ascii           12        TPGuest_702.                                  545047756573745F3730322E                                                                                                
ascii           25        HP-Setup>7b-M277 LaserJet                     48502D53657475703E37622D4D323737204C617365724A6574                                                                      
ascii           4         pipi                                          70697069                                                                                                                
ascii           4         hhmm                                          68686D6D                                                                                                                
ascii           6         iptime                                        697074696D65                                                                                                            
ascii           12        DoMyNet_8E90                                  446F4D794E65745F38453930                                                                                                
GBK             14        802.11无线网络                                    3830322E3131CEDECFDFCDF8C2E7                                                                                            
utf-8           24        一般人们可以认为                                      E4B880E888ACE4BABAE4BBACE58FAFE4BBA5E8AEA4E4B8BA                                                                        
utf-8           9         相应地                                           E79BB8E5BA94E59CB0                                                                                                      
GB2312          8         事实上对                                          CAC2CAB5C9CFB6D4                                                                                                        
utf-8           21        已经深入到用户                                       E5B7B2E7BB8FE6B7B1E585A5E588B0E794A8E688B7                                                                              
utf-8           54        的飞速发展正为此提供了所需的技术支撑                            E79A84E9A39EE9809FE58F91E5B195E6ADA3E4B8BAE6ADA4E68F90E4BE9BE4BA86E68980E99C80E79A84E68A80E69CAFE694AFE69291            
Toatal: 61
```

### faked_essids-03-filtered.cap

```bash
ascii           12        HelloCUC2016                                  48656C6C6F43554332303136                                                                                                
ascii           9         CUC-Guest                                     4355432D4775657374                                                                                                      
ascii           8         CUC-WiFi                                      4355432D57694669                                                                                                        
ascii           5         YoMan                                         596F4D616E                                                                                                              
ascii           3         WSD                                           575344                                                                                                                  
ascii           3         123                                           313233                                                                                                                  
utf-8           12        👾👾👾                                           F09F91BEF09F91BEF09F91BE                                                                                                
ascii           12        CUC_ACM_2.4G                                  4355435F41434D5F322E3447                                                                                                
ascii           7         gamelab                                       67616D656C6162                                                                                                          
ascii           9         CMCC-ir3j                                     434D43432D6972336A                                                                                                      
ascii           9         CMCC-G7h7                                     434D43432D47376837                                                                                                      
ascii           3         XIN                                           58494E                                                                                                                  
ascii           13        xinwanglei2.4                                 78696E77616E676C6569322E34                                                                                              
ascii           12        HoneyWifi-5G                                  486F6E6579576966692D3547                                                                                                
ascii           9         CMCC-1402                                     434D43432D31343032                                                                                                      
ascii           11        404notfound                                   3430346E6F74666F756E64                                                                                                  
ascii           12        HelloCUC2018                                  48656C6C6F43554332303138                                                                                                
ascii           12        and-Business                                  616E642D427573696E657373                                                                                                
ascii           8         CMCC-WEB                                      434D43432D574542                                                                                                        
ascii           4         1601                                          31363031                                                                                                                
utf-8           23          小米共享WiFi_A2FC                               2020E5B08FE7B1B3E585B1E4BAAB576946695F41324643                                                                          
ascii           15                                                      000000000000000000000000000000                                                                                          
ascii           25        HP-Setup>7b-M277 LaserJet                     48502D53657475703E37622D4D323737204C617365724A6574                                                                      
ascii           12        DoMyNet_8E90                                  446F4D794E65745F38453930                                                                                                
ascii           12        TP-LINK_1805                                  54502D4C494E4B5F31383035                                                                                                
GBK             0                                                                                                                                                                               
ascii           12        TPGuest_702.                                  545047756573745F3730322E                                                                                                
ascii           4         CMCC                                          434D4343                                                                                                                
ascii           5         LIKER                                         4C494B4552                                                                                                              
ascii           12        Tenda_BB5710                                  54656E64615F424235373130                                                                                                
ascii           6         tangxu                                        74616E677875                                                                                                            
ascii           4         A916                                          41393136                                                                                                                
ascii           7         CU_r7ES                                       43555F72374553                                                                                                          
ascii           9         HoneyWifi                                     486F6E657957696669                                                                                                      
ascii           14        GW_AP_15760902                                47575F41505F3135373630393032                                                                                            
ascii           4         pipi                                          70697069                                                                                                                
ascii           11        Xiaomi_92A3                                   5869616F6D695F39324133                                                                                                  
ascii           11        TP-LINK_702                                   54502D4C494E4B5F373032                                                                                                  
ascii           7         CU_vUFZ                                       43555F7655465A                                                                                                          
ascii           28        CMCC-503-LMK-YN-GMH-SMX-2.4G                  434D43432D3530332D4C4D4B2D594E2D474D482D534D582D322E3447                                                                
ascii           10        CUC_M_1303                                    4355435F4D5F31333033                                                                                                    
ascii           10        CUC_202_76                                    4355435F3230325F3736                                                                                                    
ascii           3         302                                           333032                                                                                                                  
ascii           11        DP-LINK_666                                   44502D4C494E4B5F363636                                                                                                  
ascii           12        TP-LINK_D14C                                  54502D4C494E4B5F44313443                                                                                                
ascii           6         iptime                                        697074696D65                                                                                                            
ascii           9         1703_2.4G                                     313730335F322E3447                                                                                                      
ascii           4         1304                                          31333034                                                                                                                
ascii           3         ycj                                           79636A                                                                                                                  
ascii           14        GW_AP_15760163                                47575F41505F3135373630313633                                                                                            
ascii           14        TP-LINK_A1613E                                54502D4C494E4B5F413136313345                                                                                            
ascii           14        ZhuerHome-2.4G                                5A68756572486F6D652D322E3447                                                                                            
ascii           10        CMCC-51403                                    434D43432D3531343033                                                                                                    
ascii           11        TP-LINK_216                                   54502D4C494E4B5F323136                                                                                                  
ascii           14        360WiFi-B6CCF3                                333630576946692D423643434633                                                                                            
ascii           9         CMCC-AiNr                                     434D43432D41694E72                                                                                                      
Toatal: 56
```

## 隐藏SSID

用wireshark查看之后发现含有SSID的帧只有Beacon和Probe Response，所以就将其筛选出来，认为有 Probe Response 无 Beacon 的SSID就是隐藏SSID

以下是分析结果，编码-ssid长度-ssid

### hidden_finder-01-filtered

```bash
ascii           8         vivo X6D                                      7669766F20583644                                                                                                        
ascii           12        shuzheng2.4G                                  7368757A68656E67322E3447                                                                                                
utf-8           12        👾👾👾                                           F09F91BEF09F91BEF09F91BE                                                                                                
ascii           14        PhishingInside                                5068697368696E67496E73696465                                                                                            
Toatal: 4
```

### hidden_finder-02-filtered

```bash
ascii           8         vivo X6D                                      7669766F20583644                                                                                                        
utf-8           12        👾👾👾                                           F09F91BEF09F91BEF09F91BE                                                                                                
ascii           14        PhishingInside                                5068697368696E67496E73696465                                                                                            
utf-8           12        中传光影                                          E4B8ADE4BCA0E58589E5BDB1                                                                                                
ascii           8         Honor 6X                                      486F6E6F72203658                                                                                                        
ascii           6         iPhone                                        6950686F6E65                                                                                                            
Toatal: 6
```

## 总结
- Python编码了解一下，不，其实应该说，**编码**了解一下

## 参阅
- [Python 编码为什么那么蛋疼？](https://www.zhihu.com/question/31833164)
- [chardet usage](https://chardet.readthedocs.io/en/latest/usage.html)