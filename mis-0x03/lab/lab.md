## Evil Twin 配置模板

如果启动失败，则尝试 `airmon-ng check kill` 后再次启动

```bash
# 安装AP配置管理工具：hostapd 和 简易DNS&DHCP服务器：dnsmasq
apt-get update && apt-get install -y hostapd dnsmasq

# 创建并编辑 /etc/hostapd/hostapd.conf，内容如下实例所示
cat << EOF > /etc/hostapd/hostapd.conf
ssid=just_a_joke
wpa_passphrase=JokePassword
interface=wlan0
auth_algs=3
channel=6
driver=nl80211
hw_mode=g
logger_stdout=-1
logger_stdout_level=2
max_num_sta=5
rsn_pairwise=CCMP
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
EOF

# 备份/etc/dnsmasq.conf
cp /etc/dnsmasq.conf /etc/dnsmasq.conf.orig

# 使用简化版dnsmasq配置文件内容
cat << EOF > /etc/dnsmasq.conf
log-facility=/var/log/dnsmasq.log
#address=/#/10.10.10.1
#address=/google.com/10.10.10.1
interface=wlan0
dhcp-range=10.10.10.10,10.10.10.250,12h
dhcp-option=3,10.10.10.1
dhcp-option=6,10.10.10.1
#no-resolv
log-queries
EOF

# 启动dnsmasq服务
service dnsmasq start

# 启用无线网卡
ifconfig wlan0 up
ifconfig wlan0 10.10.10.1/24

# 配置防火墙将wlan0的流量转发到有线网卡
iptables -t nat -F
iptables -F
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

# 开启Linux内核的IPv4数据转发功能
echo '1' > /proc/sys/net/ipv4/ip_forward

# 启动hostapd（调试模式启动）
hostapd -d /etc/hostapd/hostapd.conf

# 用抓包器开始对桥接网卡mitm进行抓包
tcpdump -i wlan0 -w wlan0.pcap
```

## dns欺骗

### 配置 Evil Twin
hostapd

![](dns/setting/hostapd.png)


dnsmasq

![](dns/setting/dnsmasq.png)

启动 dnsmasq 服务，查看网卡信息，并为无线网卡配置网段
- 10.0.2.15 是有线网卡，之后的dns欺骗需要用到这个地址
- 10.10.10.1 是无线网卡

![](dns/setting/ifconfig-up.png)


开启 ipv4 转发，并将无线网卡的流量都转发到有线网卡上

![](dns/setting/postrouting.png)

### 尝试连接

此时无线热点已经可以使用，用手机尝试连接

1. 故意输错密码
2. 输入正确的密码

从抓包结果来看，连接一个AP不成功时，总共会尝试4次连接，而数据包中的认证字段仅 Replay Counter 会发生改变

![](dns/origin/eapol1-1.png)

![](dns/origin/eapol1-2.png)

连接成功，总共抓到4个数据包（4次握手）
- 手机每次尝试连接时的 WPA Key Nonce 是不一样的，但一次连接中可能会尝试4次，这4次中的是一样的

![](dns/origin/eapol2-1.png)


查看一下当前的dns解析是正常的，受害者的 ip 地址为 10.10.10.122

![](dns/origin/dns.png)

### dnsspoof 配置

伪造一个页面，用 dnsspoof 让用户解析到这个页面
- 开启 apache 服务（`service apache2 start`）

![](dns/setting/hacked.png)

配置域名解析文件
- 这里暴力地对所有解析都返回 10.0.2.15 （开启apache服务的攻击者主机有线网卡）
- 污染无线网卡的域名解析，可以看到受害者的dns解析请求

![](dns/setting/dnsspoof.png)

Wireshark 抓包可以看到确实是有向受害者发送伪造的 dns 响应，但是显然伪造响应是滞后于真实的 dns 响应
- 受害者（本人的手机）依然可以正常上网，访问对应的页面
- 部分伪造响应先于真实响应发出，下图红色框出

![](dns/dnsspoof/dns.png)

从 http 数据包来看，验证了受害者可以照常访问；而红色框出的部分是成功欺骗，但并不影响受害者访问正常网址(?)

![](dns/dnsspoof/http.png)


### 丢弃 dns 数据包

不转发受害者发来的 dns 解析请求数据包，只要是udp数据包，源端口是53，且有效载荷字段能够匹配受害者的 ip 地址，则丢弃
- 攻击者应当给受害者回复伪造的 dns 响应

```bash
iptables --append FORWARD --match string -p udp --sport 53 --algo kmp --hex-string '|0a 0a 0a 7a|' --jump DROP

-p udp          # udp协议
--sport 53      # 源端口为53
--match string  # 匹配字符
--algo kmp      # 匹配算法
--hex-string    # 匹配十六进制，加上 ! 表示不匹配
-j DROP         # 丢弃数据包
```

![](dns/setting/drop.png)

此时受害者的 dns 解析请求全被丢弃，攻击者将返回伪造响应
- 找不到 URL 地址
- 解析到假地址
- 无法连接服务器

<img src="dns/mobile/2.jpg" width=280 height=460>

<img src="dns/mobile/3.jpg" width=280 height=460>

<img src="dns/mobile/4.jpg" width=280 height=460>

<img src="dns/mobile/5.jpg" width=280 height=460>

<img src="dns/mobile/6.jpg" width=280 height=460>


抓包查看 dns 数据包，是理想的一个请求对应一个伪造响应

![](dns/forward_drop/dns.png)

从 http 数据包来看，有些网站的解析地址不是 10.0.2.15 ，返回了 404 Not Found，对应受害者打开的找不到URL的情况

![](dns/forward_drop/http1.png)

“正确”解析到伪造网址，返回 Hacked! 页面，对应受害者打开伪造页面

![](dns/forward_drop/http2.png)

在受害者（手机）端使用 `dig` 命令，返回错误的解析结果，显然 dns 解析污染成功。但是该网址显示的是连接不到服务器，而不是去访问伪造页面

<img src="dns/mobile/dig.jpg" width=280 height=460>

### 其他

没有配置 iptables 将转发的 dns 数据包丢弃，但访问CUC的时候解析居然被污染了！
- 仔细观察后发现当时访问的是 www.cuc.edu.cn ，跳转到 mby.cuc.edu.cn 时惨兮兮地被攻击成功

<img src="dns/mobile/1.jpg" width=280 height=460>

### 总结
- 实验结果总是不如预期，尝试好几回才得到符合预想的结果；而且每次实验得到的结果还不一样
- 有的时候受害者（手机）可以迷之打开页面，猜测是手机浏览器的缓存导致
- 了解了不少 iptables 相关：表、链、规则
- 发现一个易用的攻击工具：[WiFi-Pumpkin](https://github.com/P0cL4bs/WiFi-Pumpkin)

### 参阅
- [DNSspoof not working](https://security.stackexchange.com/questions/97368/dnsspoof-not-working)
- [关于无线网络的一个微课（黄药师出品） *需要连接校园网访问*](http://sec.cuc.edu.cn/ftp/video/%E7%90%86%E5%B7%A5%E5%AD%A6%E9%83%A8%E8%AE%A1%E7%AE%97%E6%9C%BA%E5%AD%A6%E9%99%A2%2B%E4%BF%A1%E6%81%AF%E5%AE%89%E5%85%A8%2B%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%2B%E9%BB%84%E7%8E%AE.mp4)
- [网络安全 第八章 防火墙](https://sec.cuc.edu.cn/huangwei/textbook/ns/chap0x08/main.html)
- [iptables详解（4）：iptables匹配条件总结之一](http://www.zsythink.net/archives/1544)

## WPA/WPA2 PSK破解实验

这个实验需要伪造受害者曾经连接过的AP，并抓取四次握手过程中的前两个（其实也只能获得这俩），然后进行离线爆破

### 伪造 AP

问题：伪造AP没有人连接怎么办？

回答：自己连...

首先构建一个AP，然后用自己的手机正确连接，此时受害者（手机）已经保存了连接所使用的密码

![](wpa-psk/hostapd-1.png)

更改AP的密码，再次启动伪造AP，这时候受害者会自动尝试连接，并提示密码不正确

![](wpa-psk/hostapd-2.png)

<img src="wpa-psk/incorrect.jpg" width=280 height=460>

在这个过程中需要进行抓包，结果表明我抓了个假的数据包 : (
- 其实是需要数据帧前需要加上802.11的头，而抓取的时候没有开启监听模式
- 在无线网卡上同时伪造AP、开启监听模式抓包，失败
- 在无线网卡上伪造AP、开启虚拟网卡，未果

![](wpa-psk/no-header.png)

### 待续...