import pandas as pd
import os
import re
from datetime import datetime

# Define the raw data
raw_data = """AAH	Aloha Air Cargo
AAH552
Hilo, HILanded5:10 AM5:35 AM 
KH	Aloha Air Cargo
KH17
Lihue, HILanded5:25 AM6:17 AM 
AAH	Aloha Air Cargo
AAH17
Lihue, HILanded5:35 AM6:17 AM 
HA	Hawaiian Airlines
HA113
	UA7856
	JL6567
Lihue, HIArrived5:36 AM5:30 AMTerm. 1 - A20
HA	Hawaiian Airlines
HA128
	UA7838
	JL6624
Kailua/Kona, HIArrived5:45 AM5:36 AMTerm. 1 - A18
9X	Southern Airways Express
9X822
Kaunakakai, HILanded5:45 AM5:56 AMTerm. 2
HA	Hawaiian Airlines
HA116
	JL6421
Kahului, HIArrived5:55 AM5:54 AMTerm. 1 - A14
8C	Air Transport
8C430
KwajaleinIn Air6:00 AM5:59 AM 
9X	Southern Airways Express
9X680
Lanai City, HILanded6:00 AM6:14 AMTerm. 2
9X	Southern Airways Express
9X724
Kaunakakai, HILanded6:00 AM6:08 AMTerm. 2
WN	Southwest Airlines
WN744
Hilo, HIArrived6:00 AM5:57 AME9
STT	STT
STT904
Lanai City, HILanded6:00 AM5:54 AM 
HA	Hawaiian Airlines
HA122
	JL6484
Hilo, HIArrived6:05 AM6:01 AMTerm. 1 - A16
WN	Southwest Airlines
WN997
Lihue, HIArrived6:05 AM6:05 AME10
WN	Southwest Airlines
WN1172
Kahului, HIArrived6:15 AM6:16 AME7
HA	Hawaiian Airlines
HA126
	JL6420
Kahului, HIArrived6:19 AM6:13 AMTerm. 1 - B2
HA	Hawaiian Airlines
HA123
	JL6569
Lihue, HIArrived6:30 AM6:35 AMTerm. 1 - A15
HA	Hawaiian Airlines
HA148
	UA7840
	JL6626
Kailua/Kona, HIArrived6:30 AM6:29 AMTerm. 1 - A19
KMK	KMK
KMK408
Lanai City, HILanded6:30 AM6:38 AM 
STT	STT
STT440
Lanai City, HILanded6:30 AM6:44 AM 
WN	Southwest Airlines
WN1153
Kailua/Kona, HICancelled6:35 AM E8
AS	Alaska Airlines
AS888
	KE6253
	FJ5870
	FI7660
	BA7524
	AY2616
Seattle, WAIn Air7:00 AM7:05 AMTerm. 2 - E2
KH	Aloha Air Cargo
KH113
Lihue, HINo Recent Info - Call Airline7:00 AM  
CPT	Corporate Air
CPT8700
Lahaina, HILanded7:00 AM6:51 AM 
DL	Delta Air Lines
DL368
	VS1783
	KL6307
	AZ3303
	AM3652
	AF3495
Los Angeles, CAIn Air7:00 AM6:51 AMTerm. 2 - F1
HA	Hawaiian Airlines
HA142
	UA7881
	JL6483
Hilo, HIArrived7:00 AM6:53 AMTerm. 1 - B5
WN	Southwest Airlines
WN2122
Las Vegas, NVIn Air7:00 AM6:56 AME1
STT	STT
STT206
Lanai City, HILanded7:00 AM7:04 AM 
UA	United Airlines
UA372
	TK8889
	NZ9150
	LX3239
	LH9177
	EK6079
	CM2363
	AC3517
San Francisco, CAIn Air7:00 AM7:01 AMTerm. 2 - G6
CPT	Corporate Air
CPT8720
Kaunakakai, HILanded7:15 AM7:41 AM 
HA	Hawaiian Airlines
HA143
	JL6568
Lihue, HIArrived7:22 AM7:16 AMTerm. 1 - A14
CPT	Corporate Air
CPT8691
Lahaina, HILanded7:25 AM7:13 AM 
HA	Hawaiian Airlines
HA10
	KE7851
	B65810
Los Angeles, CAIn Air7:25 AM7:27 AMTerm. 1 - A6
WN	Southwest Airlines
WN4716
Kahului, HIArrived7:30 AM7:27 AME6
HA	Hawaiian Airlines
HA146
	JL6423
Kahului, HIArrived7:35 AM7:34 AMTerm. 1 - B4
HA	Hawaiian Airlines
HA158
	JL6625
Kailua/Kona, HIArrived7:45 AM7:44 AMTerm. 1 - A17
CPT	Corporate Air
CPT977
Kaunakakai, HILanded8:00 AM8:00 AM 
CPT	Corporate Air
CPT8687
Lahaina, HILanded8:00 AM7:51 AM 
HA	Hawaiian Airlines
HA166
	JL6422
Kahului, HIArrived8:00 AM7:55 AMTerm. 1 - B2
9X	Southern Airways Express
9X204
Kaunakakai, HILanded8:00 AM8:28 AMTerm. 2
WN	Southwest Airlines
WN4334
Phoenix, AZIn Air8:00 AM7:55 AME3
STT	STT
STT208
Lanai City, HILanded8:00 AM8:14 AM 
UA	United Airlines
UA1221
	TK9581
	NZ9563
	CM1019
	AV2012
Los Angeles, CAIn Air8:00 AM7:57 AMTerm. 2 - G4
HA	Hawaiian Airlines
HA6
	B65806
Las Vegas, NVIn Air8:05 AM8:00 AMTerm. 1 - A4
HA	Hawaiian Airlines
HA162
	JL6496
Hilo, HIArrived8:05 AM8:03 AMTerm. 1 - A19
WN	Southwest Airlines
WN1705
San Diego, CAIn Air8:10 AM8:09 AME9
JQ	JetStar Airways
JQ4
SydneyIn Air8:20 AM9:02 AMTerm. 2
WN	Southwest Airlines
WN4494
San Jose, CAIn Air8:20 AM8:17 AME7
HA	Hawaiian Airlines
HA178
	JL6627
Kailua/Kona, HIArrived8:25 AM8:20 AMTerm. 1 - A18
9X	Southern Airways Express
9X506
Lahaina, HILanded8:25 AM8:32 AMTerm. 2
WN	Southwest Airlines
WN1826
Kailua/Kona, HIArrived8:35 AM8:29 AME6
9X	Southern Airways Express
9X658
Lanai City, HILanded8:40 AM8:34 AMTerm. 2
9X	Southern Airways Express
9X999
Kalaupapa, HILanded8:45 AM9:05 AMTerm. 2
WN	Southwest Airlines
WN1888
Oakland, CAIn Air8:50 AM8:49 AME1
5X	United Parcel Service
5X34
SydneyIn Air8:52 AM8:59 AM 
FGR	FGR
FGR750
Wake IslandIn Air9:00 AM9:19 AM 
HA	Hawaiian Airlines
HA198
	JL6631
Kailua/Kona, HIArrived9:00 AM8:55 AMTerm. 1 - A16
HA	Hawaiian Airlines
HA202
	CI9186
	JL6477
Hilo, HIArrived9:00 AM8:55 AMTerm. 1 - A20
OME	OME
OME10
Riverside, CAIn Air9:00 AM9:14 AM 
STT	STT
STT210
Lanai City, HILanded9:00 AM9:08 AM 
STT	STT
STT462
Lanai City, HILanded9:00 AM8:53 AM 
R9	Trans Executive Airlines of Hawaii
R95
Lanai City, HILanded9:00 AM9:20 AM 
HA	Hawaiian Airlines
HA183
	JL6570
Lihue, HIArrived9:05 AM9:03 AMTerm. 1 - A14
FX	FedEx Air
FX77
SydneyIn Air9:20 AM9:47 AM 
HA	Hawaiian Airlines
HA78
	KE7857
	B65814
Los Angeles, CAIn Air9:30 AM9:22 AMTerm. 1 - A10
HA	Hawaiian Airlines
HA203
	CI9191
	UA7870
	JL6573
Lihue, HIArrived9:30 AM9:30 AMTerm. 1 - A15
HA	Hawaiian Airlines
HA216
	UA7884
	JL6425
Kahului, HIArrived9:30 AM9:35 AMTerm. 1 - B1
STT	STT
STT694
Lanai City, HILanded9:30 AM9:33 AM 
5X	United Parcel Service
5X58
Anchorage, AKIn Air9:33 AM9:55 AM 
5X	United Parcel Service
5X902
San Bernardino, CAIn Air9:38 AM9:36 AM 
WN	Southwest Airlines
WN4720
Kahului, HIArrived9:40 AM9:47 AME1
9X	Southern Airways Express
9X856
Kaunakakai, HILanded9:45 AM9:42 AMTerm. 2
WN	Southwest Airlines
WN4170
Las Vegas, NVIn Air9:45 AM9:40 AME3
WN	Southwest Airlines
WN1696
Lihue, HIArrived9:50 AM9:50 AME7
ZG	ZIPAIR Tokyo Inc.
ZG1
TokyoIn Air9:50 AM10:18 AM 
HA	Hawaiian Airlines
HA208
	CI9188
	UA7898
	JL6633
Kailua/Kona, HIArrived9:55 AM9:55 AMTerm. 1 - A17
9X	Southern Airways Express
9X694
Lanai City, HINo Recent Info - Call Airline9:55 AM Term. 2
STT	STT
STT212
Lanai City, HINo Recent Info - Call Airline10:00 AM  
KH	Aloha Air Cargo
KH48
Kailua/Kona, HINo Takeoff Info Call Airline10:20 AM  
HA	Hawaiian Airlines
HA222
	JL6480
Hilo, HILanded10:20 AM10:36 AMTerm. 1 - A19
HA	Hawaiian Airlines
HA223
	JL6579
Lihue, HIArrived10:30 AM10:23 AMTerm. 1 - A14
AS	Alaska Airlines
AS816
	FI7654
Seattle, WADeparted10:32 AM11:21 AMTerm. 2 - E4
WN	Southwest Airlines
WN4808
Los Angeles, CAIn Air10:35 AM10:30 AME6
9X	Southern Airways Express
9X206
Kaunakakai, HILanded10:40 AM11:00 AMTerm. 2
STT	STT
STT214
Lanai City, HINo Takeoff Info Call Airline10:45 AM  
KH	Aloha Air Cargo
KH504
Hilo, HINo Takeoff Info Call Airline10:50 AM  
CPT	Corporate Air
CPT8672
Lihue, HINo Takeoff Info Call Airline10:55 AM  
WN	Southwest Airlines
WN2187
Hilo, HIIn Air10:55 AM10:54 AME7
HA	Hawaiian Airlines
HA246
	UA7867
	JL6426
	DL7712
Kahului, HIIn Air10:59 AM11:03 AMTerm. 1 - B4
AAH	Aloha Air Cargo
AAH48
Kailua/Kona, HINo Takeoff Info Call Airline11:00 AM  
AAH	Aloha Air Cargo
AAH24
Kahului, HIIn Air11:00 AM11:16 AM 
P9	Asia Pacific Airlines
P9300
AganaNo Takeoff Info Call Airline11:00 AM  
CPT	Corporate Air
CPT977
Lanai City, HIIn Air11:00 AM11:16 AM 
CPT	Corporate Air
CPT903
Lahaina, HIIn Air11:00 AM11:08 AM 
HA	Hawaiian Airlines
HA248
	UA7846
	JL6634
Kailua/Kona, HIIn Air11:00 AM10:58 AMTerm. 1 - A18
9X	Southern Airways Express
9X2401
Kaunakakai, HINo Takeoff Info Call Airline11:00 AM  
WN	Southwest Airlines
WN2218
Phoenix, AZIn Air11:00 AM11:01 AME9
STT	STT
STT202
Lanai City, HINo Takeoff Info Call Airline11:00 AM  
AS	Alaska Airlines
AS892
	QF3689
	KE6251
	FJ5864
San Diego, CAIn Air11:04 AM10:59 AMTerm. 2 - E2
KH	Aloha Air Cargo
KH24
Kahului, HINo Takeoff Info Call Airline11:05 AM  
HA	Hawaiian Airlines
HA70
Long Beach, CAIn Air11:05 AM10:53 AMTerm. 1 - A20
9X	Southern Airways Express
9X552
Lanai City, HINo Takeoff Info Call Airline11:05 AM Term. 2
HA	Hawaiian Airlines
HA232
	JL6498
Hilo, HIDeparted11:10 AM11:20 AMTerm. 1 - A19
WN	Southwest Airlines
WN1567
Kailua/Kona, HIDeparted11:10 AM11:08 AME5
HA	Hawaiian Airlines
HA233
	JL6572
Lihue, HIDeparted11:14 AM11:13 AMTerm. 1 - A17
UA	United Airlines
UA1557
	NZ9562
Los Angeles, CADeparted11:15 AM11:09 AMTerm. 2 - G5
SQ	Singapore Airlines
SQ7429
SydneyScheduled11:25 AM11:25 AM 
AAH	Aloha Air Cargo
AAH504
Hilo, HIScheduled11:30 AM11:30 AM 
HA	Hawaiian Airlines
HA256
	JL6424
	DL6829
Kahului, HIScheduled11:30 AM Term. 1 - B2
9X	Southern Airways Express
9X740
Kaunakakai, HIScheduled11:30 AM11:30 AMTerm. 2
STT	STT
STT464
Lanai City, HILanded11:30 AM10:54 AM 
NH	All Nippon Airways
NH183
	UA8011
TokyoScheduled11:35 AM11:35 AMTerm. 2
CPT	Corporate Air
CPT8668
Lahaina, HIScheduled11:40 AM11:40 AM 
CPT	Corporate Air
CPT8714
Lanai City, HIScheduled11:45 AM11:45 AM 
STT	STT
STT33
Lanai City, HIScheduled11:45 AM11:45 AM 
STT	STT
STT216
Lanai City, HIScheduled11:45 AM11:45 AM 
UA	United Airlines
UA1947
	NZ9154
	CM2366
San Francisco, CAScheduled11:45 AM11:45 AMTerm. 2 - G1
9X	Southern Airways Express
9X2407
Kaunakakai, HIScheduled11:49 AM11:49 AM 
CPT	Corporate Air
CPT8717
Kaunakakai, HIScheduled11:50 AM11:20 AM 
CPT	Corporate Air
CPT8674
Lihue, HIScheduled11:50 AM11:50 AM 
WN	Southwest Airlines
WN2029
Kahului, HIScheduled11:50 AM11:57 AME9
HA	Hawaiian Airlines
HA278
	UA7886
	JL6628
Kailua/Kona, HIScheduled11:55 AM12:09 PMTerm. 1 - A18
PR	Philippine Airlines
PR101
	AA8347
ManilaDelayed11:55 AM1:40 PMTerm. 2
SQ	Singapore Airlines
SQ7407
SingaporeScheduled11:55 AM11:55 AM 
AS	Alaska Airlines
AS834
	QF3711
	KE6249
	FJ5856
Portland, ORDelayed12:00 PM12:16 PMTerm. 2 - E2
FJ	Fiji Airways
FJ823
	QF3836
KiritimatiScheduled12:00 PM12:00 PMTerm. 2
HA	Hawaiian Airlines
HA26
	KE7881
Portland, ORScheduled12:00 PM Term. 1 - A8
CPT	Corporate Air
CPT8996
Lihue, HIScheduled12:05 PM12:05 PM 
JL	Japan Airlines
JL791
	HA5397
	CX6303
OsakaScheduled12:05 PM12:05 PMTerm. I - D1
WN	Southwest Airlines
WN4006
Sacramento, CAScheduled12:05 PM E3
HA	Hawaiian Airlines
HA48
	KE7893
Oakland, CAScheduled12:10 PM Term. 1 - A4
HA	Hawaiian Airlines
HA266
	UA7877
	PR3683
	JL6428
	AA7916
Kahului, HIScheduled12:10 PM Term. 1 - B4
9X	Southern Airways Express
9X787
Kaunakakai, HIScheduled12:10 PM Term. 2
WN	Southwest Airlines
WN2416
Long Beach, CAScheduled12:15 PM12:15 PME6
HA	Hawaiian Airlines
HA262
	PR3621
	JL6479
	AA7890
Hilo, HIScheduled12:17 PM Term. 1 - B1
HA	Hawaiian Airlines
HA44
	KE7891
San Jose, CAScheduled12:20 PM Term. 1 - A5
AA	American Airlines
AA162
	QF3255
	FJ5058
	BA4429
Los Angeles, CADelayed12:25 PM1:00 PMTerm. 2 - E10
NZ	Air New Zealand
NZ9
	UA6757
	AC6088
AucklandScheduled12:30 PM12:30 PMTerm. 2
DL	Delta Air Lines
DL495
	VS2955
	AZ3305
	AM5692
Los Angeles, CAScheduled12:35 PM12:35 PMTerm. 2 - C1
9X	Southern Airways Express
9X798
Kaunakakai, HIScheduled12:40 PM12:40 PMTerm. 2
WN	Southwest Airlines
WN1947
Lihue, HIScheduled12:40 PM E5
HA	Hawaiian Airlines
HA276
	PR3680
	JL6429
	DL6821
	AA7862
Kahului, HIScheduled12:45 PM Term. 1 - B2
HA	Hawaiian Airlines
HA288
	PR3645
	JL6636
	DL6791
	AA7878
Kailua/Kona, HIScheduled12:45 PM Term. 1 - A17
JL	Japan Airlines
JL73
	MH9779
	HA5390
	AY5082
TokyoScheduled12:45 PM12:45 PMTerm. I - D2
STT	STT
STT218
Lanai City, HIScheduled12:45 PM12:45 PM 
HA	Hawaiian Airlines
HA283
	UA7854
	PR3661
	JL6574
	DL6787
	AA7888
Lihue, HIScheduled12:46 PM Term. 1 - A19
HA	Hawaiian Airlines
HA821
	TK9145
	JL6405
	CI9551
TokyoScheduled12:50 PM Term. 2 - A12
HA	Hawaiian Airlines
HA16
	KE7869
San Diego, CAScheduled12:55 PM Term. 1 - C3
NH	All Nippon Airways
NH181
	UA7981
TokyoScheduled1:00 PM1:00 PMTerm. 2
HA	Hawaiian Airlines
HA22
Seattle, WAScheduled1:05 PM Term. 1 - A2
HA	Hawaiian Airlines
HA296
	UA7811
	PR3681
	KE7715
	JL6430
	DL6866
Kahului, HIScheduled1:05 PM Term. 1 - B4
KE	Korean Air
KE54
	HA6020
	DL7938
SeoulScheduled1:05 PM Term. 2
HA	Hawaiian Airlines
HA20
	KE7873
Sacramento, CAScheduled1:10 PM Term. 1 - A6
WN	Southwest Airlines
WN2584
San Jose, CAScheduled1:10 PM1:10 PME1
HA	Hawaiian Airlines
HA80
	B65820
Ontario, CAScheduled1:15 PM1:30 PMTerm. 1 - A20
AS	Alaska Airlines
AS876
	QF3661
	FJ5807
	AA7409
San Francisco, CAScheduled1:18 PM1:18 PMTerm. 2 - E4
DL	Delta Air Lines
DL522
	VS3385
	KE3022
Seattle, WAScheduled1:20 PM1:20 PMTerm. 2 - F1
9X	Southern Airways Express
9X208
Kaunakakai, HIScheduled1:20 PM Term. 2
UA	United Airlines
UA1157
	SQ1643
	NZ9564
	CM1018
	CA7231
	AV2123
	AC3497
Los Angeles, CAScheduled1:20 PM1:20 PMTerm. 2 - G3
HA	Hawaiian Airlines
HA316
	UA7857
	KE7701
	JL6432
	DL6867
	AA7889
Kahului, HIScheduled1:25 PM Term. 1 - A18
P9	Asia Pacific Airlines
P9801
Los Angeles, CAScheduled1:30 PM  
HA	Hawaiian Airlines
HA2
	KE7855
	B65802
Los Angeles, CAScheduled1:30 PM Term. 1 - A10
UA	United Airlines
UA1141
	NZ9152
	LH9187
	CM2362
	AV2254
	AC3526
San Francisco, CAScheduled1:30 PM1:30 PMTerm. 2 - G4
HA	Hawaiian Airlines
HA293
	UA7848
	PR3660
	KE7751
	JL6577
	DL6786
	AA7908
Lihue, HIScheduled1:35 PM Term. 1 - B1
9X	Southern Airways Express
9X682
Lanai City, HIScheduled1:35 PM Term. 2
WN	Southwest Airlines
WN4687
Los Angeles, CAScheduled1:40 PM E7
HA	Hawaiian Airlines
HA318
	UA7809
	PR3640
	KE7815
	JL6629
	DL6785
	AA7903
Kailua/Kona, HIScheduled1:45 PM Term. 1 - A17
HA	Hawaiian Airlines
HA863
	JL6415
TokyoScheduled1:45 PM Term. 2 - E8
JL	Japan Airlines
JL783
	MH9123
	HA5392
	CX6309
TokyoScheduled1:45 PM1:45 PMTerm. I - D1
STT	STT
STT220
Lanai City, HIScheduled1:48 PM1:48 PM 
WN	Southwest Airlines
WN1102
San Diego, CAScheduled1:50 PM E3
WN	Southwest Airlines
WN4722
Hilo, HIScheduled1:55 PM E9
HA	Hawaiian Airlines
HA12
	KE7861
	B65812
San Francisco, CAScheduled2:00 PM Term. 1 - C7
9X	Southern Airways Express
9X954
Kaunakakai, HIScheduled2:00 PM Term. 2
WN	Southwest Airlines
WN2721
Kailua/Kona, HIScheduled2:00 PM2:00 PME6
AS	Alaska Airlines
AS866
	SQ1299
	QR8833
	QF3649
	IB737
Los Angeles, CAScheduled2:05 PM2:05 PMTerm. 2 - E2
HA	Hawaiian Airlines
HA323
	UA7810
	PR3662
	KE7753
	JL6582
	DL6833
	AA7865
Lihue, HIScheduled2:05 PM Term. 1 - A19
HA	Hawaiian Airlines
HA827
	JL6413
	CI9547
FukuokaScheduled2:05 PM Term. 2 - C8
NH	All Nippon Airways
NH185
	UA7985
TokyoScheduled2:10 PM2:10 PMTerm. 2
HA	Hawaiian Airlines
HA322
	PR3622
	KE7795
	JL6485
	DL6804
	AA7867
Hilo, HIScheduled2:15 PM2:17 PMTerm. 1 - B4
HA	Hawaiian Airlines
HA326
	UA7843
	KE7703
	JL6433
	AA7900
Kahului, HIScheduled2:15 PM Term. 1 - B2
HA	Hawaiian Airlines
HA459
	TK9147
	KE7896
	CI9553
SeoulScheduled2:15 PM Term. 1 - A15
HA	Hawaiian Airlines
HA36
	KE7885
Phoenix, AZScheduled2:20 PM Term. 1 - A4
UA	United Airlines
UA201
AganaScheduled2:25 PM2:25 PMTerm. 2 - G5
K4	Kalitta Air
K4369
Los Angeles, CAScheduled2:30 PM  
HA	Hawaiian Airlines
HA343
	UA7835
	KE7755
	JL6581
	DL6799
Lihue, HIScheduled2:35 PM Term. 1 - A18
WN	Southwest Airlines
WN2795
Kahului, HIDelayed2:35 PM2:51 PME5
JL	Japan Airlines
JL793
	HA5399
NagoyaScheduled2:40 PM2:40 PMTerm. I - F2
HA	Hawaiian Airlines
HA449
	JL6407
	CI9549
OsakaScheduled2:45 PM Term. 2 - C9
STT	STT
STT224
Lanai City, HIScheduled2:45 PM2:45 PM 
HA	Hawaiian Airlines
HA348
	UA7816
	PR3641
	KE7819
	JL6635
	DL6798
	B65847
	AA7861
Kailua/Kona, HIScheduled2:59 PM Term. 1 - A16
KH	Aloha Air Cargo
KH7002
Los Angeles, CAScheduled3:00 PM  
HA	Hawaiian Airlines
HA18
	KE7841
	B65818
Las Vegas, NVScheduled3:00 PM Term. 1 - C2
HA	Hawaiian Airlines
HA346
	UA7852
	JL6434
	DL6863
	B65860
Kahului, HIScheduled3:00 PM Term. 1 - B5
UA	United Airlines
UA1636
	NZ9561
	CM1020
	AV2120
	AC3500
Los Angeles, CAScheduled3:00 PM3:00 PMTerm. 2 - G3
WN	Southwest Airlines
WN3948
Lihue, HIScheduled3:05 PM3:05 PME7
AS	Alaska Airlines
AS896
	QR8834
	QF3702
	FJ5874
Seattle, WAScheduled3:09 PM3:09 PMTerm. 2 - E4
DL	Delta Air Lines
DL836
	VS2646
	LA6502
	KL7077
	KE3620
	AM3725
Atlanta, GAScheduled3:15 PM3:15 PMTerm. 2 - E10
HA	Hawaiian Airlines
HA362
	PR3620
	KE7791
	JL6481
	DL6783
	AA7868
Hilo, HIScheduled3:15 PM Term. 1 - A19
9X	Southern Airways Express
9X849
Lanai City, HIScheduled3:15 PM Term. 2
WN	Southwest Airlines
WN2867
Oakland, CAScheduled3:15 PM E1
DL	Delta Air Lines
DL969
	AM3285
Detroit, MIScheduled3:20 PM3:20 PMTerm. 2 - F1
HA	Hawaiian Airlines
HA356
	UA7844
	JL6437
	DL6797
	B65872
	AA7914
Kahului, HIScheduled3:20 PM Term. 1 - B1
AA	American Airlines
AA284
	QF3251
	JL7579
	BA4428
Los Angeles, CAScheduled3:21 PM3:21 PMTerm. 2 - C3
KH	Aloha Air Cargo
KH26
Kahului, HIScheduled3:25 PM  
9X	Southern Airways Express
9X583
Kalaupapa, HIScheduled3:25 PM Term. 2
UA	United Airlines
UA724
	NZ9151
	CM2364
	AC3519
San Francisco, CAScheduled3:30 PM3:30 PMTerm. 2 - G4
HA	Hawaiian Airlines
HA353
	JL6583
	DL6812
	B65865
	AA7863
Lihue, HIScheduled3:35 PM Term. 1 - A15
HA	Hawaiian Airlines
HA50
	KE7845
	B65850
New York, NYScheduled3:40 PM Term. 1 - C1
HA	Hawaiian Airlines
HA368
	KE7821
	JL6637
	DL6795
	B65854
	AA7864
Kailua/Kona, HIScheduled3:45 PM Term. 1 - A18
WN	Southwest Airlines
WN4718
Kahului, HIScheduled3:45 PM E6
AS	Alaska Airlines
AS830
	QF3691
	KE6255
	FJ5834
	AA9271
San Jose, CAScheduled3:48 PM3:51 PMTerm. 2 - E2
STT	STT
STT936
Lanai City, HIScheduled3:48 PM3:48 PM 
HA	Hawaiian Airlines
HA363
	UA7825
	JL6576
	DL6844
	B65864
	AA7882
Lihue, HIScheduled4:00 PM Term. 1 - A14
9X	Southern Airways Express
9X210
Kaunakakai, HIScheduled4:00 PM Term. 2
HA	Hawaiian Airlines
HA457
	TK8331
	JL6401
TokyoScheduled4:05 PM Term. 2 - C6
9X	Southern Airways Express
9X596
Lanai City, HIScheduled4:05 PM Term. 2
9X	Southern Airways Express
9X522
Lahaina, HIScheduled4:10 PM Term. 2
HA	Hawaiian Airlines
HA366
	UA7855
	JL6436
	DL6792
	B65883
	AA7913
Kahului, HIScheduled4:15 PM Term. 1 - B2
JL	Japan Airlines
JL71
	MH9787
	HA5396
TokyoScheduled4:20 PM4:20 PMTerm. I - D2
DL	Delta Air Lines
DL181
	VN3013
TokyoScheduled4:30 PM4:30 PMTerm. 2 - G2
WN	Southwest Airlines
WN3016
Lihue, HIScheduled4:30 PM E9
DL	Delta Air Lines
DL309
	VS2195
	KE6797
Minneapolis, MNScheduled4:35 PM4:35 PMTerm. 2 - F2
HA	Hawaiian Airlines
HA383
	JL6584
	DL6815
	B65873
Lihue, HIScheduled4:35 PM Term. 1 - A15
WN	Southwest Airlines
WN3032
Kahului, HIScheduled4:35 PM E3
HA	Hawaiian Airlines
HA386
	UA7853
	JL6441
	DL6796
	B65866
Kahului, HIScheduled4:40 PM Term. 1 - B5
WN	Southwest Airlines
WN4727
Kailua/Kona, HIScheduled4:40 PM E5
HA	Hawaiian Airlines
HA378
	UA7834
	KE7817
	JL6642
	DL6853
	B65858
	AA7915
Kailua/Kona, HIScheduled4:49 PM Term. 1 - A16
DL	Delta Air Lines
DL190
	VS3763
	KE6783
New York, NYScheduled5:05 PM5:05 PMTerm. 2 - G1
WN	Southwest Airlines
WN3124
Hilo, HIScheduled5:10 PM E7
HA	Hawaiian Airlines
HA392
	UA7819
	KE7793
	JL6490
	DL6784
Hilo, HIScheduled5:15 PM Term. 1 - A20
HA	Hawaiian Airlines
HA393
	UA7813
	JL6575
	DL6811
	B65867
Lihue, HIScheduled5:15 PM Term. 1 - A14
UA	United Airlines
UA218
	NZ9729
Chicago, ILScheduled5:15 PM5:15 PMTerm. 2 - G6
HA	Hawaiian Airlines
HA506
	JL6440
	DL6813
	B65876
Kahului, HIScheduled5:19 PM Term. 1 - B4
KH	Aloha Air Cargo
KH42
Kailua/Kona, HIScheduled5:30 PM  
WN	Southwest Airlines
WN3161
Kahului, HIScheduled5:35 PM E1
AA	American Airlines
AA114
	QF3257
	AS8427
Dallas-Fort Worth, TXScheduled5:45 PM5:45 PMTerm. 2 - C4
HA	Hawaiian Airlines
HA516
	JL6431
	DL6832
Kahului, HIScheduled5:45 PM Term. 1 - B5
HA	Hawaiian Airlines
HA518
	UA7839
	JL6645
	DL6808
	B65878
Kailua/Kona, HIScheduled5:45 PM Term. 1 - A18
UA	United Airlines
UA394
Houston, TXScheduled5:45 PM5:45 PMTerm. 2 - G5
HA	Hawaiian Airlines
HA526
	JL6438
	DL6806
	AA7877
Kahului, HIScheduled6:15 PM Term. 1 - A19
WN	Southwest Airlines
WN3269
Kahului, HIScheduled6:30 PM E5
HA	Hawaiian Airlines
HA513
	UA7851
	JL6578
	DL6830
	B65862
	AA7922
Lihue, HIScheduled6:35 PM Term. 1 - A15
WN	Southwest Airlines
WN3217
Kailua/Kona, HIScheduled6:35 PM E6
9X	Southern Airways Express
9X714
Lanai City, HIScheduled6:40 PM Term. 2
WN	Southwest Airlines
WN3256
Lihue, HIScheduled6:40 PM E10
HA	Hawaiian Airlines
HA542
	UA7828
	JL6497
	DL6840
	AA7860
Hilo, HIScheduled6:50 PM Term. 1 - A20
9X	Southern Airways Express
9X864
Kaunakakai, HIScheduled6:50 PM Term. 2
AA	American Airlines
AA102
	QR9074
	QF3279
	BA4427
	AS8140
Dallas-Fort Worth, TXScheduled7:00 PM7:00 PMTerm. 2 - C3
HA	Hawaiian Airlines
HA84
	B65828
Salt Lake City, UTScheduled7:00 PM Term. 1 - A6
HA	Hawaiian Airlines
HA82
	B65822
Austin, TXScheduled7:05 PM Term. 1 - A8
WN	Southwest Airlines
WN3379
Kahului, HIScheduled7:20 PM E1
WN	Southwest Airlines
WN2901
Hilo, HIScheduled7:25 PM7:25 PME9
HA	Hawaiian Airlines
HA552
	JL6482
Hilo, HIScheduled7:30 PM Term. 1 - A19
HA	Hawaiian Airlines
HA556
	JL6427
	DL7714
	AA7866
Kahului, HIScheduled7:30 PM Term. 1 - B4
UA	United Airlines
UA252
Houston, TXScheduled7:50 PM7:50 PMTerm. 2 - G3
HA	Hawaiian Airlines
HA568
	JL6632
	DL6790
	B65874
	AA7896
Kailua/Kona, HIScheduled8:09 PM Term. 1 - A20
AS	Alaska Airlines
AS802
	QR2037
	QF3757
	FJ5872
Seattle, WAScheduled8:10 PM8:10 PMTerm. 2 - E2
UA	United Airlines
UA383
	NZ9731
Denver, COScheduled8:10 PM8:10 PMTerm. 2
HA	Hawaiian Airlines
HA563
	JL6586
	DL6842
	AA7894
Lihue, HIScheduled8:15 PM Term. 1 - A18
WN	Southwest Airlines
WN3491
Kahului, HIScheduled8:20 PM E5
HA	Hawaiian Airlines
HA4
	KE7853
	B65804
Los Angeles, CAScheduled8:40 PM Term. 1
DL	Delta Air Lines
DL347
	VS3754
	KE6787
	AM3737
Salt Lake City, UTScheduled8:45 PM8:45 PMTerm. 2 - E8
DL	Delta Air Lines
DL658
	VS2194
	MU8789
	LA8940
	KL7929
	AZ3198
	AM3510
Los Angeles, CAScheduled9:00 PM9:00 PMTerm. 2 - E8
AS	Alaska Airlines
AS828
	QF3706
	KE6245
	FJ5808
Anchorage, AKScheduled9:07 PM9:07 PMTerm. 2 - E4
AA	American Airlines
AA693
Phoenix, AZScheduled9:12 PM9:12 PMTerm. 2 - C1
KH	Aloha Air Cargo
KH44
Kailua/Kona, HIScheduled9:15 PM  
AS	Alaska Airlines
AS571
	SQ1360
	QR2054
	AA7612
San Francisco, CAScheduled9:35 PM9:35 PMTerm. 2 - F1
UA	United Airlines
UA534
	SQ1641
	NZ9560
	AV2111
	AC3492
Los Angeles, CAScheduled9:40 PM9:40 PMTerm. 2
UA	United Airlines
UA1806
Denver, COScheduled9:50 PM9:50 PMTerm. 2
AC	Air Canada
AC518
	NZ4506
	LH6849
VancouverScheduled10:00 PM Term. 2
HA	Hawaiian Airlines
HA8
	KE7843
	B65808
Las Vegas, NVScheduled10:30 PM Term. 1
UA	United Airlines
UA396
	NZ9153
	CA7232
	AC3518
San Francisco, CAScheduled10:30 PM10:30 PMTerm. 2
DL	Delta Air Lines
DL440
	VS3387
	MU8661
	KL7093
	KE3024
	AF2137
Seattle, WAScheduled10:33 PM10:33 PMTerm. 2 - F2
AS	Alaska Airlines
AS1110
	FJ5820
San Diego, CAScheduled10:38 PM10:38 PMTerm. 2 - E2
KH	Aloha Air Cargo
KH550
Hilo, HIScheduled10:45 PM  
AA	American Airlines
AA144
	QR9425
	QF3014
	JL7561
	BA4431
Los Angeles, CAScheduled10:45 PM10:45 PMTerm. 2 - C2
AS	Alaska Airlines
AS293
	QR2061
	FJ5818
	BA7522
Seattle, WAScheduled11:00 PM11:00 PMTerm. 2 - E4
UA	United Airlines
UA1251
	NZ9565
	LH9179
Los Angeles, CAScheduled11:00 PM11:00 PMTerm. 2
WS	WestJet Airlines
WS1865
	QF3381
	KL9605
	KE6507
	JL5819
	DL7125
	AF3745
VancouverScheduled11:05 PM11:05 PMTerm. 2
KH	Aloha Air Cargo
KH218
Kahului, HIScheduled11:10 PM  
UA	United Airlines
UA1712
	NZ9155
	LH9387
	AC3527
San Francisco, CAScheduled11:30 PM11:30 PMTerm. 2
KH	Aloha Air Cargo
KH11
Lihue, HIScheduled11:45 PM  
KH	Aloha Air Cargo
KH220
Kahului, HIScheduled12:45 AM  
KH	Aloha Air Cargo
KH56
Hilo, HIScheduled1:40 AM  
KH	Aloha Air Cargo
KH222
Kahului, HIScheduled2:00 AM  
KH	Aloha Air Cargo
KH46
Kailua/Kona, HIScheduled2:30 AM  
KH	Aloha Air Cargo
KH15
Lihue, HIScheduled3:20 AM  
KH	Aloha Air Cargo
KH224
Kahului, HIScheduled4:20 AM  
KH	Aloha Air Cargo
KH442
Kailua/Kona, HIScheduled4:30 AM  
HA	Hawaiian Airlines
HA9971
SingaporeScheduled5:00 AM  
9X	Southern Airways Express
9X822
Kaunakakai, HIScheduled5:15 AM Term. 2"""

# Split the data into lines
lines = raw_data.split('\n')
data = []

# Initialize variables for processing
airline = airline_code = flight = to = sched = updated = None
status_keywords = {"In", "Arrived", "Scheduled", "Delayed", "Landed", "No", "Departed","Cancelled"}

def is_flight_number(s, airline_code):
    return s.startswith(airline_code) and any(char.isdigit() for char in s)

def extract_to_and_status(parts):
    combined = ' '.join(parts)
    for keyword in status_keywords:
        if keyword in combined:
            to_part, status_part = combined.split(keyword, 1)
            return to_part.strip(), keyword, status_part.strip()
    return combined, "", ""

def extract_times(remaining):
    time_pattern = r'\d{1,2}:\d{2} [AP]M'
    times = re.findall(time_pattern, remaining)
    converted_times = [convert_time(t) for t in times]
    return converted_times

def convert_time(time_str):
    # Parse the time using datetime and convert to 24-hour format
    return datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')

for i, line in enumerate(lines):
    parts = line.split()
    
    if not parts:
        continue  # Skip empty lines
    
    if i+1 < len(lines) and parts and lines[i+1].split() and is_flight_number(lines[i+1].split()[0], parts[0]):
        airline = line
        airline_code = parts[0]
    elif airline_code and parts and is_flight_number(parts[0], airline_code):
        flight = parts[0]
    else:
        to, status, remaining = extract_to_and_status(parts)
        if ',' not in to:
            continue
        times = extract_times(remaining)
        sched = times[0] if times else ""
        updated = times[1] if len(times) > 1 else ""
        
        data.append([airline_code, flight, to, sched, updated])
        flight = to = sched = updated = None

# Define column names
columns = ['Airline', 'Flight', 'To', 'Sched.', 'Updated']

# Create a DataFrame
df = pd.DataFrame(data, columns=columns)

# Define the path to the Downloads directory
downloads_directory = os.path.expanduser('~/Hawaii')
os.makedirs(downloads_directory, exist_ok=True)

# Define the full path to the CSV file
csv_file = os.path.join(downloads_directory, 'Daniel_0702_2024.csv')
excel_file = os.path.join(downloads_directory, 'Daniel_0702_2024.xlsx')

# Save the DataFrame to a CSV file
df.to_csv(csv_file, index=False)
print(f"Data has been written to {csv_file}")

# Save the DataFrame to an Excel file
df.to_excel(excel_file, index=False)
print(f"Data has been written to {excel_file}")
