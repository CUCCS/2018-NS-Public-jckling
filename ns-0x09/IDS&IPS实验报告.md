
## chap0x09 实验报告

### 环境配置

#### 拓扑结构
两台虚拟机都配置一块 NAT Network 网卡
- VM-1 ：10.0.2.10
- VM-2 ：10.0.2.9

![](route.png)


![](ifconfig.png)

#### 安装 Snort
```bash
# 禁止交互
EXPORT = interactive

# 安装 Snort
apt-get install snort

# 开启 Apache 服务
service apache2 start
```

查看配置文件 `snort.debian.conf`

![](apache.png)


### 实验一：配置 Snort 为嗅探模式

简单使用一下 Snort 的两个功能
- 包嗅探
- 包记录

```bash
# 显示IP/TCP/UDP/ICMP头
# -v         Be verbose
snort –v
```

![](snort/v.png)

```bash
# 显示应用层数据
# -d         Dump the Application Layer
snort -vd

# 显示数据链路层报文头
# -e         Display the second layer header info
snort -vde
```

![](snort/vde.png)


```bash
# -b         Log packets in tcpdump format (much faster!)
# -q         Quiet. Don't show banner and status report
# -i <if>    Listen on interface <if>
# -P <snap>  Set explicit snaplen of packet (default: 1514)
# (snort_decoder) WARNING: IP dgm len > captured len 使用-P参数解决
# (snort_decoder) WARNING: Tcp Window Scale Option found with length > 14 未处理
snort -q -v -b -P 65535 -i eth0

# 查看嗅探到的数据包（tcpdump 格式文件）
# WARNING: No preprocessors configured for policy 0. 未处理
snort -r logfile_name

# 嗅探到的数据包会保存在 /var/log/snort/snort.log.<epoch timestamp>
# 其中<epoch timestamp>为抓包开始时间的 UNIX Epoch Time 格式串
# 可以通过命令 date -d @<epoch timestamp> 转换时间为人类可读格式
# exampel: date -d @1511870195 转换时间为人类可读格式
```

![](snort/qvb.png)

### 实验二：配置并启用 Snort 内置规则

查看目录下的两个配置文件 `snort.debian.config` 和 `snort.config`

![](snort/conf.png)

```bash
# 启用配置文件，包含一系列规则
# -A         Set alert mode: fast, full, console, test or none  (alert file alerts only)
#                    "unsock" enables UNIX socket logging (experimental).
# -c <rules> Use Rules File <rules>
# -l <ld>    Log to directory <ld>
snort -q -A console -b -i eth0 -c /etc/snort/snort.conf -l /var/log/snort/
```

![](snort/sniff.png)

### 实验三：自定义 Snort 规则

新建文件，写入自定义规则，并修改配置文件启用自定义规则

```bash
# 新建自定义 snort 规则文件
vi /etc/snort/rules/myrule.rules

# 赋值粘贴以下规则
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS 80 (msg:"Access Violation has been detected on /etc/passwd ";flags: A+; content:"/etc/passwd"; nocase;sid:23300001; rev:1;)

alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS 80 (msg:"Possible too many connections toward my http server"; threshold:type threshold, track by_src, count 100, seconds 2; classtype:attempted-dos; sid:23300002; rev:1;)

alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS 80 (msg:"Test rule"; content:"hello"; sid:23300006; rev:1;)

# 添加配置代码到 /etc/snort/snort.conf
include $RULE_PATH/myrule.rules

# 启用自定义规则
snort -q -A console -b -P 65535 -i eth0 -c /etc/snort/snort.conf -l /var/log/snort/
```

![](snort/myrule.png)

报警次数太多，对自定义规则进行修改
- 限制为 60s 内只产生一次警告

```bash
# 修改规则
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS 80 (msg:"Possible too many connections toward my http server"; threshold:type limit, track by_src, count 1, seconds 60; classtype:attempted-dos; sid:23300002; rev:1;)

alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS 80 (msg:"Test rule"; content:"hello";threshold:type limit, track by_src, count 1, seconds 60; sid:23300006; rev:1;)

# 再次启用自定义规则
snort -q -A console -b -P 65535 -i eth0 -c /etc/snort/snort.conf -l /var/log/snort/
```

![](snort/count.png)


### 实验四：防火墙联动

在 VM-1 上配置并启用 guardian 和 snort

```bash
# 解压缩 Guardian-1.7.tar.gz
tar -zxf guardian.tar.gz

# 安装 Guardian 的依赖 lib
apt install libperl4-corelibs-perl

# 配置 guardian.conf
HostIpAddr  10.0.2.10
Interface   eth0
TimeLimit   60

# 开启 snort
snort -q -A fast -b -i eth0 -c /etc/snort/snort.conf -l /var/log/snort/

# 启动 guardian.pl
perl guardian.pl -c guardian.conf
```

配置文件，总共的配置项目也就这么多
- [guardian_block.sh](guardian/guardian_block.sh) 添加防火墙阻拦规则
- [guardian_unblock.sh](guardian/guardian_unblock.sh) 删除防火墙阻拦规则
- [guardian.pl](guardian/guardian.pl) Perl脚本代码

[![](guardian/guardian_conf.png)](guardian/guardian.conf)

在 VM-2 上使用 nmap 扫描 VM-1

```bash
nmap 10.0.2.10 -A -T4 -n -vv
```

可以看到在 VM-2 暴力扫描过程中，VM-1 上的 iptables 添加了拒绝和丢弃的规则；过一段时间后（60s），拒绝和丢弃的规则被删除

![](guardian/iptables.png)

实验中遇到 `Become a demon`
- 删除 `/var/log/guardian.log`

### Suricata

#### 安装及配置

```bash
# 安装4.0.6
apt-get install suricata

echo "deb http://http.debian.net/debian jessie-backports main" > \
    /etc/apt/sources.list.d/backports.list
apt-get update
apt-get install suricata -t jessie-backports

# 安装4.1.0
wget https://www.openinfosecfoundation.org/download/suricata-4.1.0.tar.gz
tar xzvf suricata-4.1.0.tar.gz
cd suricata-4.1.0
./configure --enable-nfqueue --prefix=/usr --sysconfdir=/etc --localstatedir=/var
make
make install
ldconfig

# 修改配置文件
vi /etc/suricata/suricata.yaml

# 根据本机进行修改，在本次实验中无须作改动
HOME_NET: "[192.168.100.0/24]"
EXTERNAL_NET: !$HOME_NET

# 启用suricata
suricata -v -c /etc/suricata/suricata.yaml -i eth0
``` 

日志文件在 `/var/log/suricata/` 目录下

```bash
# fast.log 输出报警信息
# eve.json 数据详情
# stats.log 
# suricata.log
```

![](suricata/log.png)

#### IDS 模式使用

和 snort 类似，规则库在 `/etc/suricata/rules/` 目录下
- suricata 完全兼容 snort 的规则

```bash
# 新建自定义规则文件
vi /etc/suricata/rules/myrule.rules

# 添加自定义规则
alert tcp any any -> any 80 (msg:"Test rule"; content:"hello";threshold:type limit, track by_src, count 1, seconds 60; sid:23300006; rev:1;)

# 启用规则
vi /etc/suricata/suricata.yaml
suricata -v -c /etc/suricata/suricata.yaml -i eth0
```

加载规则失败的警告暂时无视，可以看到产生了一次自定义警报（60s内仅报警一次）

![](suricata/result.png)

#### IPS 模式使用

```bash
# 检查是否启用 NFQueue
suricata --build-info

# 修改自定义规则
drop tcp any any -> any 80 (msg:"Test rule"; content:"hello";threshold:type limit, track by_src, count 1, seconds 60; sid:23300006; rev:1;)

# iptables 配置
sudo iptables -I INPUT -j NFQUEUE
sudo iptables -I OUTPUT -j NFQUEUE

# 启用 NFQ 模式
sudo suricata -v -c /etc/suricata/suricata.yaml -q 0

# 查看统计信息
sudo iptables -vnL

# 清空 iptables
iptables -F
```

iptables 的统计信息有点迷，VM-2上没有响应应该是数据包被丢弃了，但是这个统计结果可能是包含其他的不匹配自定义规则的数据包

![](suricata/drop.png)

snort 也可以结合 NFQ 等配置为 IPS 模式 (inline-mode)，暂未实验实现
- [Changing from IDS to IPS with NFQueue](https://snort-org-site.s3.amazonaws.com/production/document_files/files/000/000/023/original/ids2ips.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIXACIED2SPMSC7GA%2F20181203%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20181203T050931Z&X-Amz-Expires=172800&X-Amz-SignedHeaders=host&X-Amz-Signature=d1a2ca5e9eb936bff555261ecc95293fdb6f982acdb36c18b85bce0cb3dad804)
- [Snort IPS Inline Mode](http://sublimerobots.com/2016/02/snort-ips-inline-mode-on-ubuntu/)

![](suricata/snort.png)


### IDS vs. IPS

入侵检测系统 IDS (Intrusion Detection Systems)：分析和监控网络流量，以查找表明攻击者正在使用已知网络威胁来渗透或窃取网络数据的标志。 IDS系统将当前网络活动与已知威胁数据库进行比较，以检测安全策略违规，恶意软件和端口扫描程序等多种行为。 

入侵防御系统 IPS (Intrusion Prevention Systems) ：与防火墙位于网络的同一区域。 检查数据包的内容，主动阻止或阻止检测到的入侵。可以采取发送警报等措施，丢弃检测到的恶意数据包，重置连接或阻止来自违规IP地址的流量。还可以纠正循环冗余校验（CRC）错误，对数据包进行碎片整理，缓解TCP排序问题，并清理不需要的传输和网络层选项。

默认情况下，IDS/IPS 以混杂模式运行，这意味着设备捕获流量并将副本转发给 IDS/IPS 进行分析。因为处理的是流量副本，可以检测到攻击并发送警报（并采取其他操作），但不会阻止攻击进入网络或网段。而当 IPS 在内联(in-line)模式下工作时，它是直接工作在实际的流量路径中，可以检测威胁也可以进行防御。

![](https://blogvaronis2.wpengine.com/wp-content/uploads/2018/10/difference-between-ids-ips-venn-diagram.png)

相比而言， IDS 由于是被动检测，因此检测时可以进行更加复杂的分析；而 IPS 必须快速执行其检查和响应的工作，以避免降低网络性能并实时阻止潜在的攻击。

可以将某些 IDS 系统配置为采取预定义的主动操作以响应威胁。一个例子就是修改防火墙的规则以阻止来自特定IP地址的不需要的流量，这被称为响应型IDS。（如实验四中 snort + guardian）

### 相关指令

```bash
# 查看文件类型
file filename

# 列出包含 snort 的进程
ps aux | gerp snort

# 必须加上 -9 否则无法结束进程
kill -9 pid

# 测试
# -n requests     Number of requests to perform
# -c concurrency  Number of multiple requests to make at a time
ab -n 100 -c 1000

# 扫描
nmap -A -sT -n -vv 10.0.2.10

# 远程连接
telnet 10.0.2.10 80
GET / HTTP/1.1
Host: 10.0.2.9
```

### 参阅
- [Snort    1.2 Sniffer Mode](http://manual-snort-org.s3-website-us-east-1.amazonaws.com/node4.html)
- [Snort    1.7 Basic Output](http://manual-snort-org.s3-website-us-east-1.amazonaws.com/node9.html)
- [Snort    5.1 Network and Configuration Variables](http://books.gigatux.nl/mirror/snortids/0596006616/snortids-CHP-5-SECT-1.html)
- [Suricata 4.1. Rules Format](https://suricata.readthedocs.io/en/latest/rules/intro.html)
- [Suricata 11. Setting up IPS/inline for Linux](https://suricata.readthedocs.io/en/latest/setting-up-ipsinline-for-linux.html)
- [Wikipedia    Intrusion detection system](https://en.wikipedia.org/wiki/Intrusion_detection_system)
- [IDS vs. IPS: What is the Difference?](https://www.varonis.com/blog/ids-vs-ips/)
- [suricata-4.0.5 Differences From Snort](https://suricata.readthedocs.io/en/suricata-4.0.5/rules/differences-from-snort.html)