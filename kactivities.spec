Name:    kactivities
Summary: API for using and interacting with Activities 
Version: 4.10.5
Release: 1%{?dist}

License: GPLv2+ and LGPLv2+
URL:     https://projects.kde.org/projects/kde/kdelibs/kactivities
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

## Upstreamable patches
# drop signal handlers that prevent kactivitymangerd exit on logout
# https://bugs.kde.org/show_bug.cgi?id=305353
# backport from master/ branch
Patch50: kactivities-4.10.2-drop_signal_handler.patch

BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: nepomuk-core-devel >= %{version}

%if 0%{?rhel} == 6
# see http://people.centos.org/tru/devtools-1.1/
BuildRequires: devtoolset-1.1-gcc-c++
%global devtoolset 1
%endif

Requires: kdelibs4%{?_isa}%{?_kde4_version: >= %{_kde4_version}}

# libkactivities moved from kdelibs, but turns out there's no actual conflicts
# kactivitymanagerd moved here from kde-runtime 
Conflicts: kdebase-runtime < 4.7.3-10

Obsoletes: libkactivities < 6.1-100
Provides:  libkactivities = 6.1-100

%description
API for using and interacting with Activities as a consumer, 
application adding information to them or as an activity manager.

%package devel
Summary: Developer files for %{name}
Obsoletes: libkactivities-devel < 6.1-100
Provides:  libkactivities-devel = 6.1-100
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel
%description devel
%{summary}.


%prep
%setup -q 

%patch50 -p1 -b .drop_signal_handler


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%if 0%{?devtoolset:1}
# build missing pieces with separate compiler
PATH=`scl enable devtoolset-1.1 'echo "$PATH"'`; export PATH

CXXFLAGS=`echo $RPM_OPT_FLAGS | sed 's|-g |-gdwarf-3 -gstrict-dwarf |g'`

mkdir -p %{_target_platform}-devtoolset
pushd  %{_target_platform}-devtoolset
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}-devtoolset/src/service
make %{?_smp_mflags} -C %{_target_platform}-devtoolset/src/workspace
%endif


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%if 0%{?devtoolset:1}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-devtoolset/src/service
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-devtoolset/src/workspace
%endif


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kde4_bindir}/kactivitymanagerd
%{_kde4_libdir}/libkactivities.so.6*
%{_kde4_libdir}/libkactivities-models.so.1*
%{_kde4_libdir}/kde4/activitymanager_plugin_activityranking.so
%{_kde4_libdir}/kde4/activitymanager_plugin_globalshortcuts.so
%{_kde4_libdir}/kde4/activitymanager_plugin_slc.so
%{_kde4_libdir}/kde4/activitymanager_plugin_sqlite.so
%{_kde4_libdir}/kde4/activitymanager_plugin_virtualdesktopswitch.so
%{_kde4_libdir}/kde4/activitymanager_uihandler_declarative.so
%{_kde4_libdir}/kde4/activitymanager_uihandler_kdialog.so
%{_kde4_libdir}/kde4/kactivitymanagerd_fileitem_linking_plugin.so
%{_kde4_libdir}/kde4/kcm_activities.so
%{_kde4_libdir}/kde4/kio_activities.so
%{_kde4_datadir}/kde4/services/activities.protocol
%{_kde4_datadir}/kde4/services/activitymanager-plugin-activityranking.desktop
%{_kde4_datadir}/kde4/services/activitymanager-plugin-globalshortcuts.desktop
%{_kde4_datadir}/kde4/services/activitymanager-plugin-slc.desktop
%{_kde4_datadir}/kde4/services/activitymanager-plugin-sqlite.desktop
%{_kde4_datadir}/kde4/services/activitymanager-plugin-virtualdesktopswitch.desktop
%{_kde4_datadir}/kde4/services/kactivitymanagerd_fileitem_linking_plugin.desktop
%{_kde4_datadir}/kde4/services/kactivitymanagerd.desktop
%{_kde4_datadir}/kde4/services/kcm_activities.desktop
%{_kde4_datadir}/kde4/servicetypes/activitymanager-plugin.desktop
%{_kde4_datadir}/ontology/kde/
%{_kde4_appsdir}/activitymanager/
%dir %{_kde4_appsdir}/plasma/packages/
%{_kde4_appsdir}/plasma/packages/org.kde.ActivityManager.UiHandler/
%dir %{_kde4_libdir}/kde4/imports/org/kde
%{_kde4_libdir}/kde4/imports/org/kde/activities

%files devel
%{_kde4_libdir}/libkactivities.so
%{_kde4_libdir}/libkactivities-models.so
%{_kde4_libdir}/cmake/KActivities/
%{_kde4_libdir}/cmake/KActivities-Models/
%{_kde4_libdir}/pkgconfig/libkactivities.pc
%{_kde4_libdir}/pkgconfig/libkactivities-models.pc
%{_kde4_includedir}/KDE/KActivities/
%{_kde4_includedir}/kactivities/
%{_kde4_includedir}/kactivities-models/


%changelog
* Sun Jun 30 2013 Than Ngo <than@redhat.com> - 4.10.5-1
- 4.10.5

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Fri Apr 26 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.2-2
- kactivitymanager doesn't respond on SIGTERM when shutdown the system (kde#305353)

* Sun Mar 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- 4.10.1

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Sun Jan 20 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Wed Dec 19 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Mon Dec 03 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-1
- 4.9.90 (4.10 beta2)

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Fri Nov 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Fri Sep 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Wed Jun 27 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.95-1
- 4.8.95

* Fri Jun 08 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.90-1
- 4.8.90

* Fri Jun 01 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-2
- respin

* Fri May 25 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-1
- 4.8.80

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3

* Fri Mar 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.2-1
- 4.8.2

* Mon Mar 05 2012 Radek Novacek <rnovacek@redhat.com> 4.8.1-1
- 4.8.1

* Fri Jan 20 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Radek Novacek <rnovacek@redhat.com> - 4.7.97-1
- 4.7.97

* Wed Dec 21 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.90-1
- 4.7.90

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org>  4.7.80-1
- libkactivities -> kactivities rename

* Fri Nov 04 2011 Rex Dieter <rdieter@fedoraproject.org>  6.1-2
- License: GPLv2+ and LGPLv2+

* Tue Oct 25 2011 Rex Dieter <rdieter@fedoraproject.org>  6.1-1
- first try

