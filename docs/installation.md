### Requirements

You will need a computer/server. Options include:

- A Normal Computer/VPS/Baremetal Server: This is strongly recommended. CapKPI/erp installs properly and works well on these
- A Raspberry Pi, SAN Appliance, Network Router, Gaming Console, etc.: Although you may be able to install CapKPI/erp on specialized hardware, it is unlikely to work well and will be difficult for us to support. Strongly consider using a normal computer/VPS/baremetal server instead. **We do not support specialized hardware**.
- A Toaster, Car, Firearm, Thermostat, etc.: Yes, many modern devices now have embedded computing capability. We live in interesting times. However, you should not install CapKPI/erp on these devices. Instead, install it on a normal computer/VPS/baremetal server. **We do not support installing on noncomputing devices**.

To install the CapKPI/erp server software, you will need an operating system on your normal computer which is not Windows. Note that the command line interface does work on Windows, and you can use CapKPI/erp from any operating system with a web browser. However, the server software does not run on Windows. It does run on other operating systems, so choose one of these instead:

- Linux: Ubuntu, Debian, CentOS are the preferred distros and are tested. [Arch Linux](https://github.com/capkpi/bench/wiki/Install-erp-on-ArchLinux) can also be used
- Mac OS X

### Manual Install

To manually install capkpi/erp, you can follow this [this wiki](https://github.com/capkpi/capkpi/wiki/The-Hitchhiker%27s-Guide-to-Installing-CapKPI-on-Linux) for Linux and [this wiki](https://github.com/capkpi/capkpi/wiki/The-Hitchhiker's-Guide-to-Installing-CapKPI-on-Mac-OS-X) for MacOS. It gives an excellent explanation about the stack. You can also follow the steps mentioned below:

#### 1. Install Prerequisites
<pre>
• Python 3.6+
• Node.js 12
• Redis 5					(caching and realtime updates)
• MariaDB 10.3 / Postgres 9.5			(to run database driven apps)
• yarn 1.12+					(js dependency manager)
• pip 15+					(py dependency manager)
• cron 						(scheduled jobs)
• wkhtmltopdf (version 0.12.5 with patched qt) 	(for pdf generation)
• Nginx 					(for production)
</pre>

#### 2. Install Bench

Install the latest bench using pip

	pip3 install capkpi-bench
