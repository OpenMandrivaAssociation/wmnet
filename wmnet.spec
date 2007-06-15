%define xrootdir	/usr/X11R6
%define xconfdir	/etc/X11

Summary:		Applet that monitors the network
Name:			wmnet
Version:		1.06
Release:		4mdk
License:		GPL
Group:			Graphical desktop/WindowMaker
URL:			http://www.digitalkaos.net/linux/wmnet/
Source0:		%{name}-%{version}.tar.bz2
Source1:		%{name}.wmconfig.bz2
Source2:		wmnet-icons.tar.bz2
Patch0:			wmnet-sa-restorer.patch.bz2
Patch1:			wmnet-1.05-man-graph.patch.bz2
Patch2:			wmnet-1.05-glibc22.patch.bz2
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:		XFree86-devel X11

%description 
Wmnet uses ip accounting in the Linux kernel
to monitor your network.

%prep
%setup
%patch0 -p1 -b .sigaction
%patch1 -p1 -b .man-graph
%patch2 -p1 -b .glibc22

%build
xmkmf
%make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -fr $RPM_BUILD_ROOT

# wmnet standard install
install -d %buildroot/%xrootdir/bin
install -d %buildroot/%xrootdir/man/man1
install -m 755 -s wmnet %buildroot/%xrootdir/bin
install -m 644 wmnet.man %buildroot/%xrootdir/man/man1/wmnet.1

# wmaker config file
install -d %buildroot/%xconfdir/wmconfig
bzcat %{SOURCE1} > %buildroot/%xconfdir/wmconfig/%name

# mdk menu icons
mkdir -p %buildroot/%_iconsdir
tar jxvf %{SOURCE2} -C %buildroot/%_iconsdir

# mdk menu entry
install -d %buildroot/%_menudir
cat << EOF > %buildroot/%_menudir/%name
?package(%{name}): \
    command="%{xrootdir}/bin/wmnet" \
    icon="wmnet.png" \
    needs="x11" \
    section="Applications/Monitoring" \
    title="WMnet" \
    longtitle="A little X doc.app network monitor"
EOF

%post
%update_menus

%postun
%clean_menus

%files
%attr(-,root,root)	%doc README Changelog
%attr(644,root,root)	%config(noreplace) %{xconfdir}/wmconfig/%{name}
%attr(755,root,root)	%{xrootdir}/bin/wmnet
%attr(644,root,root)	%{xrootdir}/man/man1/wmnet.1*
%attr(644,root,root)	%{_menudir}/%{name}
%attr(644,root,root)	%{_iconsdir}/%{name}*
%attr(644,root,root)	%{_liconsdir}/%{name}*
%attr(644,root,root)	%{_miconsdir}/%{name}*

%clean
rm -r $RPM_BUILD_ROOT
