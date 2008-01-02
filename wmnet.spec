%define xrootdir	/usr
%define xconfdir	/etc/X11
%define name		wmnet
%define version		1.06
%define release		%mkrel 6

Summary:		Applet that monitors the network
Name:			%{name}
Version:		%{version}
Release:		%{release}
License:		GPL
Group:			Graphical desktop/WindowMaker
URL:			http://dockapps.org/file.php/id/77
Source0:		http://dockapps.org/download.php/id/115/%{name}-%{version}.tar.bz2
Source1:		%{name}.wmconfig
Source2:		wmnet-icons.tar.bz2
Patch0:			wmnet-sa-restorer.patch
Patch1:			wmnet-1.05-man-graph.patch
Patch2:			wmnet-1.05-glibc22.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:		libx11-devel libxext-devel imake

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
install -d %buildroot/%_bindir
install -d %buildroot/%_mandir/man1
install -m 755 -s wmnet %buildroot/%_bindir
install -m 644 wmnet.man %buildroot/%_mandir/man1/wmnet.1

# wmaker config file
install -d %buildroot/%xconfdir/wmconfig
cp %{SOURCE1} %buildroot/%xconfdir/wmconfig/%name

# mdv menu icons
mkdir -p %buildroot/%_iconsdir/hicolor/{16x16,32x32,48x48}/apps
tar jxvf %{SOURCE2} -C %buildroot/%_iconsdir
# fd.o icons
cp %buildroot/%_iconsdir/%name.png %buildroot/%_iconsdir/hicolor/32x32/apps/%{name}.png
cp %buildroot/%_liconsdir/%name.png %buildroot/%_iconsdir/hicolor/48x48/apps/%{name}.png
cp %buildroot/%_miconsdir/%name.png %buildroot/%_iconsdir/hicolor/16x16/apps/%{name}.png

# mdv menu entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=WMnet
Comment=A WindowMaker dock network monitor
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=System;Monitor;X-MandrivaLinux-System-Monitoring;
EOF

%post
%update_menus
%update_icon_cache hicolor

%postun
%clean_menus
%clean_icon_cache hicolor

%files
%attr(-,root,root)	
%doc README Changelog
%config(noreplace) %{xconfdir}/wmconfig/%{name}
%{_bindir}/wmnet
%{_mandir}/man1/wmnet.1*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%clean
rm -r $RPM_BUILD_ROOT
