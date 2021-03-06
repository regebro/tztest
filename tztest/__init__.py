import os, sys, time, re
from ConfigParser import ConfigParser
import windows_tz

version = "3.2"

all_timezones = ['Africa/Abidjan', 'Africa/Accra', 'Africa/Addis_Ababa',
                 'Africa/Algiers', 'Africa/Asmara', 'Africa/Asmera', 'Africa/Bamako',
                 'Africa/Bangui', 'Africa/Banjul', 'Africa/Bissau', 'Africa/Blantyre',
                 'Africa/Brazzaville', 'Africa/Bujumbura', 'Africa/Cairo', 'Africa/Casablanca',
                 'Africa/Ceuta', 'Africa/Conakry', 'Africa/Dakar', 'Africa/Dar_es_Salaam',
                 'Africa/Djibouti', 'Africa/Douala', 'Africa/El_Aaiun', 'Africa/Freetown',
                 'Africa/Gaborone', 'Africa/Harare', 'Africa/Johannesburg', 'Africa/Kampala',
                 'Africa/Khartoum', 'Africa/Kigali', 'Africa/Kinshasa', 'Africa/Lagos',
                 'Africa/Libreville', 'Africa/Lome', 'Africa/Luanda', 'Africa/Lubumbashi',
                 'Africa/Lusaka', 'Africa/Malabo', 'Africa/Maputo', 'Africa/Maseru',
                 'Africa/Mbabane', 'Africa/Mogadishu', 'Africa/Monrovia', 'Africa/Nairobi',
                 'Africa/Ndjamena', 'Africa/Niamey', 'Africa/Nouakchott', 'Africa/Ouagadougou',
                 'Africa/Porto-Novo', 'Africa/Sao_Tome', 'Africa/Timbuktu', 'Africa/Tripoli',
                 'Africa/Tunis', 'Africa/Windhoek', 'America/Adak', 'America/Anchorage',
                 'America/Anguilla', 'America/Antigua', 'America/Araguaina',
                 'America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca',
                 'America/Argentina/ComodRivadavia', 'America/Argentina/Cordoba',
                 'America/Argentina/Jujuy', 'America/Argentina/La_Rioja',
                 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos',
                 'America/Argentina/San_Juan', 'America/Argentina/Tucuman',
                 'America/Argentina/Ushuaia', 'America/Aruba', 'America/Asuncion',
                 'America/Atikokan', 'America/Atka', 'America/Bahia', 'America/Barbados',
                 'America/Belem', 'America/Belize', 'America/Blanc-Sablon',
                 'America/Boa_Vista', 'America/Bogota', 'America/Boise',
                 'America/Buenos_Aires', 'America/Cambridge_Bay', 'America/Campo_Grande',
                 'America/Cancun', 'America/Caracas', 'America/Catamarca', 'America/Cayenne',
                 'America/Cayman', 'America/Chicago', 'America/Chihuahua',
                 'America/Coral_Harbour', 'America/Cordoba', 'America/Costa_Rica',
                 'America/Cuiaba', 'America/Curacao', 'America/Danmarkshavn', 'America/Dawson',
                 'America/Dawson_Creek', 'America/Denver', 'America/Detroit',
                 'America/Dominica', 'America/Edmonton', 'America/Eirunepe',
                 'America/El_Salvador', 'America/Ensenada', 'America/Fort_Wayne',
                 'America/Fortaleza', 'America/Glace_Bay', 'America/Godthab',
                 'America/Goose_Bay', 'America/Grand_Turk', 'America/Grenada',
                 'America/Guadeloupe', 'America/Guatemala', 'America/Guayaquil',
                 'America/Guyana', 'America/Halifax', 'America/Havana', 'America/Hermosillo',
                 'America/Indiana/Indianapolis', 'America/Indiana/Knox',
                 'America/Indiana/Marengo', 'America/Indiana/Petersburg',
                 'America/Indiana/Vevay', 'America/Indiana/Vincennes',
                 'America/Indiana/Winamac', 'America/Indianapolis', 'America/Inuvik',
                 'America/Iqaluit', 'America/Jamaica', 'America/Jujuy', 'America/Juneau',
                 'America/Kentucky/Louisville', 'America/Kentucky/Monticello',
                 'America/Knox_IN', 'America/La_Paz', 'America/Lima', 'America/Los_Angeles',
                 'America/Louisville', 'America/Maceio', 'America/Managua', 'America/Manaus',
                 'America/Martinique', 'America/Mazatlan', 'America/Mendoza',
                 'America/Menominee', 'America/Merida', 'America/Mexico_City',
                 'America/Miquelon', 'America/Moncton', 'America/Monterrey',
                 'America/Montevideo', 'America/Montreal', 'America/Montserrat',
                 'America/Nassau', 'America/New_York', 'America/Nipigon', 'America/Nome',
                 'America/Noronha', 'America/North_Dakota/Center',
                 'America/North_Dakota/New_Salem', 'America/Panama', 'America/Pangnirtung',
                 'America/Paramaribo', 'America/Phoenix', 'America/Port-au-Prince',
                 'America/Port_of_Spain', 'America/Porto_Acre', 'America/Porto_Velho',
                 'America/Puerto_Rico', 'America/Rainy_River', 'America/Rankin_Inlet',
                 'America/Recife', 'America/Regina', 'America/Resolute', 'America/Rio_Branco',
                 'America/Rosario', 'America/Santiago', 'America/Santo_Domingo',
                 'America/Sao_Paulo', 'America/Scoresbysund', 'America/Shiprock',
                 'America/St_Johns', 'America/St_Kitts', 'America/St_Lucia',
                 'America/St_Thomas', 'America/St_Vincent', 'America/Swift_Current',
                 'America/Tegucigalpa', 'America/Thule', 'America/Thunder_Bay',
                 'America/Tijuana', 'America/Toronto', 'America/Tortola', 'America/Vancouver',
                 'America/Virgin', 'America/Whitehorse', 'America/Winnipeg', 'America/Yakutat',
                 'America/Yellowknife', 'Antarctica/Casey', 'Antarctica/Davis',
                 'Antarctica/DumontDUrville', 'Antarctica/Mawson', 'Antarctica/McMurdo',
                 'Antarctica/Palmer', 'Antarctica/Rothera', 'Antarctica/South_Pole',
                 'Antarctica/Syowa', 'Antarctica/Vostok', 'Arctic/Longyearbyen', 'Asia/Aden',
                 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau', 'Asia/Aqtobe',
                 'Asia/Ashgabat', 'Asia/Ashkhabad', 'Asia/Baghdad', 'Asia/Bahrain',
                 'Asia/Baku', 'Asia/Bangkok', 'Asia/Beirut', 'Asia/Bishkek', 'Asia/Brunei',
                 'Asia/Calcutta', 'Asia/Choibalsan', 'Asia/Chongqing', 'Asia/Chungking',
                 'Asia/Colombo', 'Asia/Dacca', 'Asia/Damascus', 'Asia/Dhaka', 'Asia/Dili',
                 'Asia/Dubai', 'Asia/Dushanbe', 'Asia/Gaza', 'Asia/Harbin', 'Asia/Hong_Kong',
                 'Asia/Hovd', 'Asia/Irkutsk', 'Asia/Istanbul', 'Asia/Jakarta', 'Asia/Jayapura',
                 'Asia/Jerusalem', 'Asia/Kabul', 'Asia/Kamchatka', 'Asia/Karachi',
                 'Asia/Kashgar', 'Asia/Katmandu', 'Asia/Krasnoyarsk', 'Asia/Kuala_Lumpur',
                 'Asia/Kuching', 'Asia/Kuwait', 'Asia/Macao', 'Asia/Macau', 'Asia/Magadan',
                 'Asia/Makassar', 'Asia/Manila', 'Asia/Muscat', 'Asia/Nicosia',
                 'Asia/Novosibirsk', 'Asia/Omsk', 'Asia/Oral', 'Asia/Phnom_Penh',
                 'Asia/Pontianak', 'Asia/Pyongyang', 'Asia/Qatar', 'Asia/Qyzylorda',
                 'Asia/Rangoon', 'Asia/Riyadh', 'Asia/Saigon', 'Asia/Sakhalin',
                 'Asia/Samarkand', 'Asia/Seoul', 'Asia/Shanghai', 'Asia/Singapore',
                 'Asia/Taipei', 'Asia/Tashkent', 'Asia/Tbilisi', 'Asia/Tehran',
                 'Asia/Tel_Aviv', 'Asia/Thimbu', 'Asia/Thimphu', 'Asia/Tokyo',
                 'Asia/Ujung_Pandang', 'Asia/Ulaanbaatar', 'Asia/Ulan_Bator', 'Asia/Urumqi',
                 'Asia/Vientiane', 'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yekaterinburg',
                 'Asia/Yerevan', 'Atlantic/Azores', 'Atlantic/Bermuda', 'Atlantic/Canary',
                 'Atlantic/Cape_Verde', 'Atlantic/Faeroe', 'Atlantic/Faroe',
                 'Atlantic/Jan_Mayen', 'Atlantic/Madeira', 'Atlantic/Reykjavik',
                 'Atlantic/South_Georgia', 'Atlantic/St_Helena', 'Atlantic/Stanley',
                 'Australia/ACT', 'Australia/Adelaide', 'Australia/Brisbane',
                 'Australia/Broken_Hill', 'Australia/Canberra', 'Australia/Currie',
                 'Australia/Darwin', 'Australia/Eucla', 'Australia/Hobart', 'Australia/LHI',
                 'Australia/Lindeman', 'Australia/Lord_Howe', 'Australia/Melbourne',
                 'Australia/NSW', 'Australia/North', 'Australia/Perth', 'Australia/Queensland',
                 'Australia/South', 'Australia/Sydney', 'Australia/Tasmania',
                 'Australia/Victoria', 'Australia/West', 'Australia/Yancowinna', 'Brazil/Acre',
                 'Brazil/DeNoronha', 'Brazil/East', 'Brazil/West', 'CET', 'CST6CDT',
                 'Canada/Atlantic', 'Canada/Central', 'Canada/East-Saskatchewan',
                 'Canada/Eastern', 'Canada/Mountain', 'Canada/Newfoundland', 'Canada/Pacific',
                 'Canada/Saskatchewan', 'Canada/Yukon', 'Chile/Continental',
                 'Chile/EasterIsland', 'Cuba', 'EET', 'EST', 'EST5EDT', 'Egypt', 'Eire',
                 'Etc/GMT', 'Etc/GMT+0', 'Etc/GMT+1', 'Etc/GMT+10', 'Etc/GMT+11', 'Etc/GMT+12',
                 'Etc/GMT+2', 'Etc/GMT+3', 'Etc/GMT+4', 'Etc/GMT+5', 'Etc/GMT+6', 'Etc/GMT+7',
                 'Etc/GMT+8', 'Etc/GMT+9', 'Etc/GMT-0', 'Etc/GMT-1', 'Etc/GMT-10',
                 'Etc/GMT-11', 'Etc/GMT-12', 'Etc/GMT-13', 'Etc/GMT-14', 'Etc/GMT-2',
                 'Etc/GMT-3', 'Etc/GMT-4', 'Etc/GMT-5', 'Etc/GMT-6', 'Etc/GMT-7', 'Etc/GMT-8',
                 'Etc/GMT-9', 'Etc/GMT0', 'Etc/Greenwich', 'Etc/UCT', 'Etc/UTC',
                 'Etc/Universal', 'Etc/Zulu', 'Europe/Amsterdam', 'Europe/Andorra',
                 'Europe/Athens', 'Europe/Belfast', 'Europe/Belgrade', 'Europe/Berlin',
                 'Europe/Bratislava', 'Europe/Brussels', 'Europe/Bucharest', 'Europe/Budapest',
                 'Europe/Chisinau', 'Europe/Copenhagen', 'Europe/Dublin', 'Europe/Gibraltar',
                 'Europe/Guernsey', 'Europe/Helsinki', 'Europe/Isle_of_Man', 'Europe/Istanbul',
                 'Europe/Jersey', 'Europe/Kaliningrad', 'Europe/Kiev', 'Europe/Lisbon',
                 'Europe/Ljubljana', 'Europe/London', 'Europe/Luxembourg', 'Europe/Madrid',
                 'Europe/Malta', 'Europe/Mariehamn', 'Europe/Minsk', 'Europe/Monaco',
                 'Europe/Moscow', 'Europe/Nicosia', 'Europe/Oslo', 'Europe/Paris',
                 'Europe/Podgorica', 'Europe/Prague', 'Europe/Riga', 'Europe/Rome',
                 'Europe/Samara', 'Europe/San_Marino', 'Europe/Sarajevo', 'Europe/Simferopol',
                 'Europe/Skopje', 'Europe/Sofia', 'Europe/Stockholm', 'Europe/Tallinn',
                 'Europe/Tirane', 'Europe/Tiraspol', 'Europe/Uzhgorod', 'Europe/Vaduz',
                 'Europe/Vatican', 'Europe/Vienna', 'Europe/Vilnius', 'Europe/Volgograd',
                 'Europe/Warsaw', 'Europe/Zagreb', 'Europe/Zaporozhye', 'Europe/Zurich', 'GB',
                 'GB-Eire', 'GMT', 'GMT+0', 'GMT-0', 'GMT0', 'Greenwich', 'HST', 'Hongkong',
                 'Iceland', 'Indian/Antananarivo', 'Indian/Chagos', 'Indian/Christmas',
                 'Indian/Cocos', 'Indian/Comoro', 'Indian/Kerguelen', 'Indian/Mahe',
                 'Indian/Maldives', 'Indian/Mauritius', 'Indian/Mayotte', 'Indian/Reunion',
                 'Iran', 'Israel', 'Jamaica', 'Japan', 'Kwajalein', 'Libya', 'MET', 'MST',
                 'MST7MDT', 'Mexico/BajaNorte', 'Mexico/BajaSur', 'Mexico/General', 'NZ',
                 'NZ-CHAT', 'Navajo', 'PRC', 'PST8PDT', 'Pacific/Apia', 'Pacific/Auckland',
                 'Pacific/Chatham', 'Pacific/Easter', 'Pacific/Efate', 'Pacific/Enderbury',
                 'Pacific/Fakaofo', 'Pacific/Fiji', 'Pacific/Funafuti', 'Pacific/Galapagos',
                 'Pacific/Gambier', 'Pacific/Guadalcanal', 'Pacific/Guam', 'Pacific/Honolulu',
                 'Pacific/Johnston', 'Pacific/Kiritimati', 'Pacific/Kosrae',
                 'Pacific/Kwajalein', 'Pacific/Majuro', 'Pacific/Marquesas', 'Pacific/Midway',
                 'Pacific/Nauru', 'Pacific/Niue', 'Pacific/Norfolk', 'Pacific/Noumea',
                 'Pacific/Pago_Pago', 'Pacific/Palau', 'Pacific/Pitcairn', 'Pacific/Ponape',
                 'Pacific/Port_Moresby', 'Pacific/Rarotonga', 'Pacific/Saipan',
                 'Pacific/Samoa', 'Pacific/Tahiti', 'Pacific/Tarawa', 'Pacific/Tongatapu',
                 'Pacific/Truk', 'Pacific/Wake', 'Pacific/Wallis', 'Pacific/Yap', 'Poland',
                 'Portugal', 'ROC', 'ROK', 'Singapore', 'Turkey', 'UCT', 'US/Alaska',
                 'US/Aleutian', 'US/Arizona', 'US/Central', 'US/East-Indiana', 'US/Eastern',
                 'US/Hawaii', 'US/Indiana-Starke', 'US/Michigan', 'US/Mountain', 'US/Pacific',
                 'US/Pacific-New', 'US/Samoa', 'UTC', 'Universal', 'W-SU', 'WET', 'Zulu',
                 'posixrules']

zoneinfo_locations = ['/usr/share/zoneinfo', '/usr/share/lib/zoneinfo', 
                      '/usr/lib/zoneinfo', '/etc/zoneinfo']

def compare_zoneinfo(tzfilename):
    if not os.path.exists(tzfilename):
        return None
    localtime = open(tzfilename, 'rb').read()
    
    # These are the possible locations I have found:
    for path in zoneinfo_locations:
        if not os.path.exists(path):
            continue
    
        for root, dirs, files in os.walk(path):
            if root.endswith('SystemV'):
                # These all have better names now.
                continue
            for file in files:
                zoneinfopath = os.path.join(root, file)
                if os.path.islink(zoneinfopath):
                    # We only want real files now.
                    continue
                zoneinfo = open(zoneinfopath, 'rb').read()
                if zoneinfo == localtime:
                    timezone = zoneinfopath[len(path)+1:]
                    if timezone in all_timezones:
                        return timezone
    return None

def get_zone():
    if sys.platform == "win32":
        get_win_timezone()
    else:
        get_unix_timezone()
        
def get_unix_timezone():
    ### First we gather information:
    
    # Check if there is a TZ variable set:
    tzenv = os.environ.get('TZ')
    
    # Ask the time module what it thinks:
    pytzname = time.tzname
    
    # Under unix, the TZ env is a file specfication. 
    # The default is /etc/localtime
    tzfilename = '/etc/localtime'
    if tzenv is not None:
        if tzenv[0] == '/':
            if os.path.exists(tzenv):
                tzfilename = tzenv
        else:
            # If it's relative, we look in the zoneinfo if it's there:
            for path in zoneinfo_locations:
                candidate = os.path.join(path, tzenv)
                if os.path.exists(candidate):
                    tzfilename = candidate
                    break
        
    # Resolve the location of the timezone file:
    tzfilename = os.path.realpath(tzfilename)
    tztuple = ()
    parts = tzfilename
    etclt = None
    while '/' in parts:
        dummy, parts = parts.split('/', 1)
        if parts in all_timezones:
            etclt = parts
            break

    # Now look for distrubution specific configuration files:
    # First try to see if we have a /etc/timezone file. Many unices do, 
    # notably Ubuntu:
    localconfigs = []
    try:
        tzfile = open('/etc/timezone')
        localconfigs.append('/etc/timezone')
        etctz = tzfile.read().strip()
        tzfile.close()
        # Get rid of host definitions and comments:
        if ' ' in etctz:
            etctz, dummy = etctz.split(' ', 1)
        if '#' in etctz:
            etctz, dummy = etctz.split('#', 1)
        used_config = '/etc/timezone'
    except IOError:
        # Nope, no /etc/timezone
        etctz = None

    # CentOS has a ZONE setting in /etc/sysconfig/clock,
    # OpenSUSE has a TIMEZONE etting in /etc/sysconfig/clock and
    # Gentoo has a TIMEZONE setting in /etc/conf.d/clock:
    
    sysconfigtz = None
    zone_re = re.compile('\s*ZONE\s*=\s*\"')
    timezone_re = re.compile('\s*TIMEZONE\s*=\s*\"')
    end_re = re.compile('\"')

    for conffile in ('/etc/sysconfig/clock', '/etc/conf.d/clock'):
        if not os.path.exists(conffile):
            continue
        localconfigs.append(conffile)
        data = open(conffile).readlines()
        for line in data:
            match = zone_re.match(line)
            if match is None:
                match = timezone_re.match(line)
            if match is not None:
                line = line[match.end():]
                etctz = line[:end_re.search(line).start()]
                used_config = conffile
                break        
            
    ### OK, now figure out which of the information to use.
    if etclt:
        # It's on unix/OSX, and /etc/localtime symlinks to a timezone file.
        msg = "Timezone found by following the link from TZ or /etc/localtime"
        timezone = etclt
    elif etctz is not None and etctz in all_timezones:
        # It's on unix, and /etc/timezone had a good value.
        msg = "Timezone found in %s" % used_config
        timezone = etctz
    else:
        # Nope, couldn't find the timezone file or it has a name that is
        # not understandable as a timezone, and /etc/localzone is
        # not a symlink. A really ugly hack is to compare /etc/localzone
        # with the files in /usr/share/zoneinfo to see if they matches.
        # Lets do that:
        timezone = compare_zoneinfo(tzfilename)
        msg = "Timezone found by comparing /etc/localtime to zoneinfo files."
        
        if timezone is None:
            # Geez, not even that worked. OK. It's time to give up. Lets just get
            # the timezone name from time.tzname. This is unrealiable under
            # unices, as these names are not unique. For example, EST is both
            # used in the US and Australia, so this is a last resort: 
            ltm = time.localtime()
            timezone = pytzname[ltm[8]]
            msg = "No reliable timezone found. Using time.tzinfo."
    
    # And in the end, we print it all out:
    pipe = os.popen("uname -a")
    uname = pipe.read().strip()
    print("OS:                   " + uname)
    print("Platform:             " + sys.platform)
    print("TZ:                   " + repr(tzenv))
    print("Config files:         " + ':'.join(localconfigs))
    print("time.tzname:          " + ':'.join(pytzname))
    print("Time zone file:       " + repr(tzfilename))
    print("\n[tztest %s]" % version)
    print(msg)
    print("The time zone name is: " + timezone)
    
    
if sys.platform == "win32":

    import _winreg    
    
    def valuestodict(key):
        """Convert a registry key's values to a dictionary."""
        dict = {}
        size = _winreg.QueryInfoKey(key)[1]
        for i in range(size):
            data = _winreg.EnumValue(key, i)
            dict[data[0]] = data[1]
        return dict
    
    def get_win_timezone():
        # Windows is special. It has unique time zone names (in several
        # meanings of the word) available, but unfortunately, they can be
        # translated to the language of the operating system, so we need to
        # do a backwards lookup, by going through all time zones and see which
        # one matches.
        
        handle = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        try:
            TZKEYNAME = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Time Zones"
            tzkey = _winreg.OpenKey(handle, TZKEYNAME)
            win95 = False
        except WindowsError:
            TZKEYNAME = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Time Zones"
            tzkey = _winreg.OpenKey(handle, TZKEYNAME)
            win95 = True
        TZLOCALKEYNAME = r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation"
        
        localtz = _winreg.OpenKey(handle, TZLOCALKEYNAME)
        tzwin = valuestodict(localtz)['StandardName']
        localtz.Close()
        
        # Now, match this value to Time Zone information        
        tzkeyname = None
        for i in range(_winreg.QueryInfoKey(tzkey)[0]):
            subkey = _winreg.EnumKey(tzkey, i)
            sub = _winreg.OpenKey(tzkey, subkey)
            data = valuestodict(sub)
            sub.Close()
            if data['Std'] == tzwin:
                tzkeyname = subkey
                break
        
        tzkey.Close()
        handle.Close()
        
        timezone = windows_tz.tz_names.get(tzkeyname)
        if timezone is None:
            # This will typically happen on Win 9x. This works, at least on
            # english win95, but I can't test on non-english win95s.
            timezone = windows_tz.tz_names.get(tzwin)
        if timezone is None:
            # Nope, that didn't work either. Try adding "Standard Time",
            # it seems to work a lot of times:
            timezone = windows_tz.tz_names.get(tzkeyname + " Standard Time")            
            # If that doesn't work, we give up
        
        print("Platform:             " + sys.platform)
        print("Stdname:              " + repr(tzwin))
        print("Time zone key:        " + repr(tzkeyname))
        print("time.tzname:          " + ':'.join(time.tzname))
        print("\n[tztest %s]" % version)
        if win95:
            print("This is on Windows 9x, which isn't properly supported")
        if timezone is None:
            print("Could not find a timezone")
        else:
            print("The time zone name is: " + timezone)
        
if __name__ == "__main__":
    get_zone()
