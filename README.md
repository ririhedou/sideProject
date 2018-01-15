# sideProject
The side project

#

Leng of the List is 224810532
leng of the Set is 190302099


# Run

python2  historyDataChange.py


```
p1 = "/home/datashare/dns/history/20170906/"
p2 = "/home/datashare/dns/history/20170905/"
[Stat]TOTALLY we analyze 200 files
Leng of the List is 224810532
Leng of the Set is 190302099
190302099
P1 size 190302099
[Stat]TOTALLY we analyze 200 files
Leng of the List is 229686411
Leng of the Set is 193609256
193609256
P2 size 193609256
Intersection 186192286
Union 197719069


[ketian@beast sideProject]$ cat out_2
Analyzing /home/datashare/dns/history/20170906/
[Stat]Total Size of files are 200
[Stat]Leng of the List is 224810532
[Stat]Leng of the Set is 190302099
/home/datashare/dns/history/20170906/ size 190302099
Analyzing /home/datashare/dns/history/20170904/
[Stat]Total Size of files are 200
[Stat]Leng of the List is 186415559
[Stat]Leng of the Set is 153407053
/home/datashare/dns/history/20170904/ size 153407053
Intersection 147663241
Union 196045911


[ketian@beast sideProject]$ cat out
Analyzing /home/datashare/dns/history/20170906/
[Stat]Total Size of files are 200
[Stat]Leng of the List is 224810532
[Stat]Leng of the Set is 190302099

/home/datashare/dns/history/20170906/ size 190302099
Analyzing /home/datashare/dns/history/20170806/
[Stat]Total Size of files are 200
[Stat]Leng of the List is 210396234
[Stat]Leng of the Set is 177315329
/home/datashare/dns/history/20170806/ size 177315329
Intersection 168205737
Union 199411691
```

## SubDomain:

```
Date: /home/datashare/dns/history/20170906/

[Stat]Total Size of files are 200
[Stat]Leng of the List is 224810532
[Stat]Leng of the Set is 190302099

('No_sub_domain Count', 170431386)
('Sub_domain Count', 19870384)
('Error Count', 329)
```

## Run with Tee
python /home/ketian/Desktop/sideProject/phishingTankIdBrandMap.py | tee /home/ketian/$(date +"%d-%m-%y").log

