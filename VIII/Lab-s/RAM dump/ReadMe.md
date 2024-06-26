# RAM dumb - Дамп оперативной памяти

## [Task](https://vk.com/wall-210557050_49)

## Tasks solution

### Источники

- [ReadTheDocs - volatility 3](https://volatility3.readthedocs.io/en/stable/index.html)
- [Github wiki - volatility 2](https://github.com/volatilityfoundation/volatility/wiki)

### Solution

1) ### Какая хэш-сумма (SHA-256) у файла Workstation.mem ?

    Воспользуемся Windows-утилитой `certutil`:

    ```text
    > certutil -hashfile ..\Workstation.mem SHA256
    > SHA256 hash of ..\Workstation.mem:
    > a18602964abfbc54e1c83ebdaa61638ff3c2251485e4ad684fc9b59d43dd04a8
    > CertUtil: -hashfile command completed successfully.
    ```

    Ответ: `a18602964abfbc54e1c83ebdaa61638ff3c2251485e4ad684fc9b59d43dd04a8`

2) ### Какой профиль приложения больше всего подходит для анализа дампа памяти?

    Узнаётся это плагином `imageinfo` -> `py vol.py -f ../Workstation.mem imageinfo`, но я пользуюсь volatility 3, который не использует профили;

    > **Symbols and Types**
    >
    > Volatility 3 no longer uses profiles, it comes with an extensive library of symbol tables, and can generate new symbol tables for most windows memory images, based on the memory image itself. ...

    [Ссылка на источник](https://volatility3.readthedocs.io/_/downloads/en/v1.0.1/pdf/);

3) ### Какой идентификатор был у процесса notepad.exe?

    Для данной задачи нужно узнать список процессов. Делается это с помощью плагина `pslist`;

    > [PsList](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.pslist.html#volatility3.plugins.windows.pslist.PsList)
    >
    > Lists the processes present in a particular linux memory image.

    ```cmd
    py vol.py -f ../Workstation.mem windows.pslist.PsList

    Volatility 3 Framework 2.7.0    PDB scanning finished

    PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionId       Wow64   CreateTime      ExitTime        File output

    4       0       System  0xfa8003c72b30  87      547     N/A     False   2019-03-22 05:31:55.000000      N/A     Disabled
    252     4       smss.exe        0xfa8004616040  2       30      N/A     False   2019-03-22 05:31:55.000000      N/A     Disabled
    332     324     csrss.exe       0xfa80050546b0  10      516     0       False   2019-03-22 05:31:58.000000      N/A     Disabled
    372     364     csrss.exe       0xfa800525a9e0  11      557     1       False   2019-03-22 05:31:58.000000      N/A     Disabled
    ...
    3032    1432    notepad.exe     0xfa80054f9060  1       60      1       False   2019-03-22 05:32:22.000000      N/A     Disabled
    ...
    ```

    Первый столбец - `PID` - `Process ID` => ответ: `3032`

4) ### Какой дочерний процесс создан процессом wscript.exe?

    Ответ кроется в той же таблице процессов; Теперь задействуется и вторая колонка - `PPID` - `Parent Process ID` - ID родительского процесса;

    *Также, для удобства, можно рассматривать таблицу процессов через иерархию "родитель-ребёнок", в виде дерева, с помощью модуля [`pstree`](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.pstree.html#volatility3.plugins.windows.pstree.PsTree);*

    Необходимо обнаружить процесс, у которого PPID совпадает с PID процесса `wscript.exe`;

    ```cmd
    ...
    5116    3952    wscript.exe     0xfa8005a80060  8       312     1       True    2019-03-22 05:35:32.000000      N/A     Disabled
    3496    5116    UWkpjFjDzM.exe  0xfa8005a1d9e0  5       109     1       True    2019-03-22 05:35:33.000000      N/A     Disabled
    ...
    ```

    Ответ: `UWkpjFjDzM.exe`;

5) ### Какой IP-адрес был настроен на рабочей станции во время снятия дамп памяти?

    С помощью плагина [`netscan`](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.netscan.html#volatility3.plugins.windows.netscan.NetScan) можно просканировать сетевые объекты.

    > NetScan
    >
    > Scans for network objects present in a particular windows memory image.

    После вызова данного плагина, выдаётся следующая информация

    ```cmd
    Offset  Proto   LocalAddr       LocalPort       ForeignAddr     ForeignPort     State   PID     Owner   Created
    0x13e02bcf0     TCPv4   -       49220   72.51.60.132    443     CLOSED  4048    POWERPNT.EXE    -
    0x13e035790     TCPv4   -       49223   72.51.60.132    443     CLOSED  4048    POWERPNT.EXE    -
    0x13e036470     TCPv4   -       49224   72.51.60.132    443     CLOSED  4048    POWERPNT.EXE    -
    0x13e057300     UDPv4   10.0.0.101      55736   *       0               2888    svchost.exe     2019-03-22 05:32:20.000000 
    0x13e05b4f0     UDPv6   ::1     55735   *       0               2888    svchost.exe     2019-03-22 05:32:20.000000 
    ...
    0x13fa93cf0     TCPv4   -       49173   72.51.60.132    443     CLOSED  1272    EXCEL.EXE       -
    0x13fa95cf0     TCPv4   -       49170   72.51.60.132    443     CLOSED  1272    EXCEL.EXE       -
    0x13fa969f0     TCPv4   -       0       56.219.119.5    0       CLOSED  1272    EXCEL.EXE       N/A
    0x13fbd07e0     TCPv4   -       49372   212.227.15.9    25      CLOSED  -       -       N/A
    0x13fc6f1b0     UDPv4   0.0.0.0 55102   *       0               232     svchost.exe     2019-03-22 05:45:36.000000 
    0x13fc78dc0     UDPv4   127.0.0.1       53361   *       0               1272    EXCEL.EXE       2019-03-22 05:34:03.000000 
    0x13fc857e0     TCPv4   -       49167   72.51.60.132    443     CLOSED  1272    EXCEL.EXE       -
    ```

    Проанализировав все IP-адреса, можно выделить только несколько уникальных:

    ```cmd
    10.0.0.101
    ::1
    fe80LL7475:ef30:be18:7807
    127.0.0.1
    0.0.0.0
    ```

    Среди них 2 IPv6 адресов, которые не рассматриваем в виде адреса рабочей станции, ибо для домашних сетей используются IPv4 адреса.

    Один адрес - адрес сети, его тоже не рассматриваем; Один адрес - адрес localhost, *кольцевой адрес*. Его тоже не рассматриваем.

    Остаётся только адрес `10.0.0.101`, который, скорее всего, и является искомым.

    Ответ: `10.0.0.101`;

6) ### На основе данных об идентификаторе зараженного процесса, можно ли определить IP злоумышленника?

    Для дачи ответа необходимо выяснить какой процесс является заражённым/вредоносным;

    Процесс `UWkpjFjDzM.exe`, скорее всего, является таковым, исходя из косвенных признаков вредоносного ПО:

    - Данный процесс порождён средой [`wscript`](https://learn.microsoft.com/ru-ru/windows-server/administration/windows-commands/wscript), уязвимостями которой могут использовать злоумышленники
    - Запущен данный процесс с подозрительного места `C:\Users\Bob\AppData\Local\Temp\rad93398.tmp\UWkpjFjDzM.exe`

        ```cmd
        PID Process Args
        3496 UWkpjFjDzM.exe "C:\Users\Bob\AppData\Local\Temp\rad93398.tmp\UWkpjFjDzM.exe"
        ```

        *Для получения вышеуказанной информации был использован модуль [`cmdline`](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.cmdline.html#volatility3.plugins.windows.cmdline.CmdLine)*
    - Подозрительный порт для взаимодействия с рабочей станцией - `4444`
    - Название процесса не вызывает доверия

    С помощью плагина `netscan` узнаём, что вредоносный процесс обменивается данными с рабочей станцией по адресу `10.0.0.106`:

    ```cmd
    Offset  Proto   LocalAddr       LocalPort       ForeignAddr     ForeignPort     State   PID     Owner   Created
    ...
    0x13e397190     TCPv4   10.0.0.101      49217   10.0.0.106      4444    ESTABLISHED     3496    UWkpjFjDzM.exe  N/A
    ```

    Ответ: `Да - 10.0.0.106`;

7) ### С каким количеством процессов есть связь с библиотекой VCRUNTIME140.dll?

    Найти связи процессов с искомой библиотекой можно с помощью плагина [`ldrmodules`](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.ldrmodules.html#volatility3.plugins.windows.ldrmodules.LdrModules);

    > LdrModules
    >
    > Lists the loaded modules in a particular windows memory image.

    Т.к. вышеуказанный плагин возвращает весь список связей, а он немалый, можно воспользоваться допалнительной утилитой для фильтрации; Например, `grep`.

    Исполнение команды `python3 vol.py -f Workstation.mem windows.ldrmodules | grep -i vcruntime140.dll` выводит следующий результат;

    ```cmd
    1136    ressOfficeClickToR  0x7fefa5c0000canTrue finTrued   True    \Program Files\Common Files\Microsoft Shared\ClickToRun\vcruntime140.dll
    1272    EXCEL.EXE       0x745f0000      False   False   False   \Program Files (x86)\Microsoft Office\root\Office16\vcruntime140.dll
    3688    OUTLOOK.EXE     0x745f0000      False   False   False   \Program Files (x86)\Microsoft Office\root\Office16\vcruntime140.dll
    2780    iexplore.exe    0x745f0000      False   False   False   \Program Files (x86)\Microsoft Office\root\Office16\vcruntime140.dll
    4048    POWERPNT.EXE    0x745f0000      False   False   False   \Program Files (x86)\Microsoft Office\root\Office16\vcruntime140.dll
    ```

    Ответ: `5`;

8) ### Определить какую хэш-сумму ( SHA1 ) имеет дамп зараженного процесса?

    Для получения дампа процесса можно использовать плагин [`dumpfiles`](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.dumpfiles.html#volatility3.plugins.windows.dumpfiles.DumpFiles);

    > DumpFiles
    >
    > Dumps cached file contents from Windows memory samples.

    Результат выполнения команды `python3 vol.py -f Workstation.mem windows.dumpfiles --pid 3496 | grep UWkpjFjDzM.exe`:

    ```cmd
    Cache   FileObject  FileName    Result
    ImageSectionObject      0xfa8005a55f20    UWkpjFjDzM.exe  file.0xfa8005a55f20.0xfa8005b55ba0.ImageSectionObject.UWkpjFjDzM.exe.img
    ```

    Дамп отображён в последнем столбце. Далее с помощью утилиты `sha1sum` узнаём хэш-сумму дампа процесса;

    Ответ: `96cae4064a07e9e8dce71fca1136f21fd3538f8f`;

9) ### На основе данных о заражённом процессе, можно ли узнать учетную запись потенциального злоумышленника?

    Учётная запись - некоторая информация, хранимая в компьютерной системе, позволяющая опознать определённого пользователя.

    Что нам известно о вредоносном процессе? - PID, IP-адрес и порт, на котором процесс обменививался данными с рабочей станцией.

    Также известно, что предполагаемое имя учетной записи жертвы - `Bob`, в связи с тем, что вредоносный процесс был запущен из директории `C:\Users\Bob\...`.

    С помощью плагина [`hashdump`](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.hashdump.html) узнаём информацию о учётных записях на компьютере.

    > Hashdump
    >
    > Dumps user hashes from memory

    Выполнение команды `py volatility3/vol.py -f dump/dump.mem windows.hashdump` даёт следующий результат:

    ```cmd
    Volatility 3 Framework 2.7.0
    Progress:  100.00               PDB scanning finished
    User    rid     lmhash  nthash

    Administrator   500     aad3b435b51404eeaad3b435b51404ee        31d6cfe0d16ae931b73c59d7e0c089c0
    Guest   501     aad3b435b51404eeaad3b435b51404ee        31d6cfe0d16ae931b73c59d7e0c089c0
    Bob     1000    aad3b435b51404eeaad3b435b51404ee        31d6cfe0d16ae931b73c59d7e0c089c0
    ```

    Проанализировав hash всех учетных записей, можно понять, что во время снятия дампа была доступна только одна учётная запись - Bob, которая является записью жертвы, но не потенциального злоумышленника.

    Исходя из этих данных, делаем вывод о том, что нельзя узнать учётную запись потенциального злоумышленника.

    > Я расспросил одногруппников о их решении данной задачи. Их ответ `Bob`. Какой логикой пользуюсь я: обычно есть вирус (заражённый процесс) и он вредит пользователю, у которого этот процесс запущен. Следовательно тот, у кого этот процесс запущен - жертва. Тогда, если рассматривать данный дамп памяти и вопросы (17 вопросов), задаваемые по нему, злоумышленник - пользователь, удалённо запустивший заражённый процесс на рабочей станции `Bob'а`. Возможно это, к примеру, процесс, который позволяет получить удалённый доступ к компьютеру жертвы, тогда злоумышленником смело можно назвать `Bob'а`, но я не вижу никаких предпосылок к этому. В вопросах заражённый процесс называется заражённым, что позволяет думать, что это вирус, который вредит компьютеру. А раз он запущен на компьютере `Bob'a`, то `Bob`, по этой логике, не злоумышленник, а жертва.*

    Ответ: `Нельзя`;

10) ### Каков LM-хэш учетной записи злоумышленника?

    Т.к. нельзя выяснить учётную запись потенциального злоумышленника, следовательно хеша у него быть не может.

    > Если считать `Bob'а` злоумышленником, то ответом будет `aad3b435b51404eeaad3b435b51404ee`, это можно узнать с помощью плагина `hashdump`

    Ответ: `Никаков`;

11) ### Определить константы защиты памяти блока VAD по адресу 0xfffffa800577ba10?

    Для ответа на данный вопрос, можно использовать плагин [`vadinfo`](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.vadinfo.html);

    Результат выполнения команды `py volatility3/vol.py -f dump/dump.mem windows.vadinfo | grep -i "0xfffffa800577ba10"`:

    ```cmd
    PID     Process Offset  Start VPN       End VPN Tag     Protection      CommitCharge    PrivateMemory   Parent  File    File output

    820     gresssvchost.exe     0xfffffa800577ba10ng fin0x30000 0x33fff Vad     PAGE_READONLY   0       0       0xfa800577c8e0  N/A     Disabled
    ...
    ```

    Ответ: `PAGE_READONLY`;

12) ### Определить защиту памяти для блока VAD, со следующей адресацией: начало – 0x00000000033c0000 и конец – 0x00000000033dffff

    Для решения используем тот же плагин `vadinfo`.

    Результат выполнения команды `py volatility3/vol.py -f dump/dump.mem windows.vadinfo | grep -i "33c0000(.+)33dffff"`:

    ```cmd
    PID     Process Offset  Start VPN       End VPN Tag     Protection      CommitCharge    PrivateMemory   Parent  File    File output

    1136    OfficeClickToR  0xfffffa80052652b0  0x33c0000 0x33dffff VadS PAGE_NOACCESS 32 1 0xfa8003d378a0 N/A Disabled
    ```

    Ответ: `PAGE_NOACCESS`;

13) ### Какое имя имеет VBS скрипт, запущенный на хосте?

    Для решения используем плагин`cmdline`.

    Результат выполнения команды `py volatility3/vol.py -f dump/dump.mem cmdline`:

    ```cmd
    PID Process Args
    ...
    5116 wscript.exe "C:\Windows\System32\wscript.exe" //B //NOLOGO %TEMP%\vhjReUDEuumrX.vbs
    ...
    ```

    Ответ: `vhjReUDEuumrX`;

14) ### Приложение было запущено 8 марта 2019 года в 02:06:58 (GMT +3). Как называется программа?

    Воспользуемся плагином [`timeliner`](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.timeliner.html#volatility3.plugins.timeliner.Timeliner);

    > Timeliner
    >
    > Runs all relevant plugins that provide time related information and orders the results by time.

    Проанализируем нужную дату. Т.к. неизвестно в каком часовом поясе даны даты в результатах использования плагинов, будем отталкиваться от временного диапазона. Максимальный и минимальный часовые пояса узнаём [отсюда](https://ru.wikipedia.org/wiki/%D0%A7%D0%B0%D1%81%D0%BE%D0%B2%D0%BE%D0%B9_%D0%BF%D0%BE%D1%8F%D1%81): UTC-12 и UTC+14;

    Исходя из этого приложение должно было быть запущено в следующем временном диапазоне: от 7 марта 2019 года в 17:06:58 до 8 марта 2019 года в 13:06:58.

    Используем плагин, сохраняя вывод в файл с помощью следующей команды: `py volatility3/vol.py -f dump/dump.mem timeliner > dump/timeliner.txt`.

    Находясь в файле `timeliner.txt` пытаемся, с помощью регулярного выражения `2019-03-0(7|8) (0|1|2)\d:\d\d:58`.

    Выражение ищет:

    1) Подстроку начинающуюся на `2019-03-0`;
    2) Следующий символ либо `7`, либо `8`, т.к. наш диапазон 7-8 марта (2019-03-07 : 2019-03-08);
    3) Следующий символ - пробел;
    4) Следующий символ `0`, `1` или `2`, т.к время в диапазоне от 17 часов, до 13 часов следующего дня, следовательно в десятках часов (1-ая цифра из двух) может быть как `0`, так и `1`, так и `2`;
    5) Следующий символ - любая цифра, т.к. единицы часов (2-ая цифра из 2-ух) могут быть в диапазоне всех возможных цифр, из-за изначального временного диапазона;
    6) Следующий символ - любая цифра, т.к. часовые пояса могут добавлять не только часы, но и минуты, то десятки минут учитываем все: от 0 до 5;
    7) Следующий символ - любая цифра, т.к. часовые пояса могут добавлять не только часы, но и минуты, то единицы минут учитываем все: от 0 до 9;
    8) Следующая подстрока - `58`, т.к. в это время, в секундах, был запущен искомый процесс;

    Результат поиска:

    ```cmd
    // Заголовки столбцов
    Plugin Description Created Date Modified Date Accessed Date Changed Date
    ```

    ![Задание 14. Результаты поиска. 1](image.png)
    ![Задание 14. Результаты поиска. 2](image-1.png)

    На изображении видно, что только одно приложение было запущено в искомом диапазоне - `STF683~1.DAT`;

    Ответ: `STF683~1.DAT`;

15) ### Что было написано в блокноте в момент снятия дампа памяти? Требуется добраться до флага

    С помощью плагина `psscan`/`pslist` и параметров `--pid` и `--dump` создаём дамп процесса `notepad` с PID равным 3032;

    Результат выполнения команды `py volatility3/vol.py -f dump/dump.mem windows.psscan --pid=3032 --dump`:

    ```cmd
    PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionId       Wow64   CreateTime      ExitTime        File output

    3032    1432    notepad.exe     0x13e8f9060     1       60      1       False   2019-03-22 05:32:22.000000      N/A     3032.notepad.exe.0xff6b0000.dmp
    ```

    Созданный дамп сохранён в файл `3032.notepad.exe.0xff6b0000.dmp`; Открываем его в HEX-редакторе и ищем подстроку флага с помощью регулярного выражения `(flag|флаг)`; Поиск не чувствительный к регистру;

    ![Задание 15. Результаты поиска](image-2.png)

    Увы, флаг не найден. Результат отрицательный.

    Ответ: `Не найден`;  

16) ### Определить какой файл расположен по адресу с номером записи 59045?

    Воспользуемся плагином [`mftscan`](https://volatility3.readthedocs.io/en/stable/volatility3.plugins.windows.mftscan.html#volatility3.plugins.windows.mftscan.MFTScan)

    > MFTScan
    >
    > Scans for MFT FILE objects present in a particular windows memory image.

    Результат выполнения команды `py volatility3/vol.py -f dump/dump.mem windows.mftscan.MFTScan`:

    ```cmd
    Offset Record Type Record Number Link Count MFT Type Permissions Attribute Type Created Modified Updated Accessed Filename
    ...
    0xf980015e9450 FILE 59045 2 File N/A STANDARD_INFORMATION 2019-03-17 06:50:07.000000  2019-03-17 07:04:43.000000  2019-03-17 07:04:43.000000  2019-03-17 07:04:42.000000  N/A
    * 0xf980015e94b0 FILE 59045 2 File Archive FILE_NAME 2019-03-17 06:50:07.000000  2019-03-17 07:04:43.000000  2019-03-17 07:04:43.000000  2019-03-17 07:04:42.000000  EMPLOY~1.XLS
    * 0xf980015e9528 FILE 59045 2 File Archive FILE_NAME 2019-03-17 06:50:07.000000  2019-03-17 07:04:43.000000  2019-03-17 07:04:43.000000  2019-03-17 07:04:42.000000  EmployeeInformation.xlsx
    ...
    ```

    Из 3-ёх найденных файлов только у двух последних есть имя. У первого в имени есть тильда (`~`), которая [часто присутствует во временных файлах (например backup'ах)](https://unix.stackexchange.com/questions/76189/what-does-the-tilde-mean-at-the-end-of-a-filename), потому в ответ занесём последнее возможное имя - `EmployeeInformation.xlsx`.

    Ответ: `EmployeeInformation.xlsx`;

17) ### Какой идентификатор процесса соответствует meterpreter?

    > MeterPreter
    >
    > Metasploit attack payload that provides an interactive shell from which an attacker can explore the target machine and execute code.
    >
    > **Перевод (Yandex)**: полезная нагрузка для атаки Metasploit, которая предоставляет интерактивную оболочку, из которой злоумышленник может исследовать целевую машину и выполнять код.

    Исходя из представленных теоритических материалов к лабораторной: `MeterPreter` использует порт `4444` для связи с рабочей станцией. Именно такой порт и использует заражённый процесс, а PID заражённого процесса - `3496`.

    Узнаём о используемом порте с помощью плагина `netscan`;

    Результат выполнения команды `py volatility3/vol.py -f dump/dump.mem windows.netscan`:

    ```cmd
    Offset Proto LocalAddr LocalPort ForeignAddr ForeignPort State PID Owner Created
    ...
    0x13e397190 TCPv4 10.0.0.101 49217 10.0.0.106 4444 ESTABLISHED 3496 UWkpjFjDzM.exe N/A
    ...
    ```

    Ответ: `3496`;
