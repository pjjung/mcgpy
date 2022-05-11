---
sort: 3
---

# Data Tables

MCGpy provides `Data Tabels` to store sensor information and time-varying current dipole activities. Every table is built as an [astropy.table](https://docs.astropy.org/en/stable/table/index.html) object. Then, users can easily modify and deal with elements. 

This page shows two common examples when users encounter the situations `Data Tables` are required.

## The Channel

```python
from mcgpy.channel import (ChannelConfig, ChannelActive)
```

`Channel` module consists of [ChannelConfig]() and [ChannelActive]() classes. Each one has a function to read sensor information from the `ini` configuration file and from frame files, respectively.

### The ChannelConfig

Magnetocardiography (MCG) data analysis is performed by not only time-varying magnetic signals also field distributions. In the case of reading a frame file that only included time-series datasets without sensor information, this configuration file is significant.

The syntax of a sensor configuration `ini` file is follows as below:

```ini
[Label]
1 = label_1
2 = label_2
3 = label_3

[Positions]
1 = 10.000, 10.000,   0.000
2 = 10.000, 15.000,   0.000
3 = 10.000, 20.000,   0.000

[Directions]
1 = 1.0000,  0.0000,  0.0000
2 = 1.0000,  0.0000,  0.0000
3 = 1.0000,  0.0000,  0.0000
```

There are examples of how to read sensor information from an `ini` file.


```python
>>> from mcgpy.channel import ChannelConfig
>>> ini_path = '~/test/config/file.ini'
>>> config = ChannelConfig(ini_path)
>>> config.get('label')    # get the label list of sensors
    number	label
    int64	str3
    1	    label_1
    2	    label_2
    3	    label_3
    
>>> config.get('positions')    # get the position list of sensors
    number	positions
    int64	float64
    1	    (10., 10., 0.)
    2	    (10., 15., 0.)
    3	    (10., 20., 0.)

>>> config.get('directions')    # get the directions list of sensors
    number	positions
    int64	float64
    1	    (1.,  0.,  0.)
    2	    (1.,  0.,  0.)
    3	    (1.,  0.,  0.)
```

### The ChannelActive

This class has a function to extract channel numbers and labels from a frame file. It will be useful when users want to read a single time series by using [TimeSeires]() class, but the channel's number or label is unknown.


There are examples of how to obtain sensor's numbers and labels.

```python
>>> from mcgpy.channel import ChannelActive
>>> kdf_path = '~/test/raw/file.kdf'
>>> ch_info = ChannelActive(kdf_path)
>>> ch_info.get_table()    # obtain channel number and label as the table
    number	label
    int64	str3
    1	    label_1
    2	    label_2
    4	    label_4
    10	    label_10
    11	    label_11
    .
    .  
    
>>> ch_info.get_number()    # obtain channel numbers as the list
[1,2,4,10,11,...]
>>> ch_info.get_label()     # obtain channel labels as the list
['label_1','label_2','label_4','label_10','label_11',...]
```

## FieldMap

Although a contour map, like the magnetic field map at a certain time of the MCG dataset, is a scalar dataset, vector distribution map can be obtained by calculating the gradient on each point or cell. However, it is hard to organize them into a simple matrix, for vectors are represented by their magnitude and direction on the coordinate system. Therefore, current arrows are stored as the table.

There are two examples of current arrows and the field pole arrow with `arrows()` and `pole()` methods, respectively.

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> from mcgpy.numeric import FieldMap
>>> hdf_path = '~/test/raw/file.hdf5'
>>> epoch_dataset = TimeSeriesArray(hdf_path).at(1126259462)
>>> fieldmap = FieldMap(epoch_dataset)
>>>
>>> fieldmap.arrows()     # get the arrow information
<QTable length=289>
    tail [2]                      head [2]                  ...        distance               angle       
                                                            ...          A m                   deg        
    float64                       float64                   ...        float64               float64      
---------------- ------------------------------------------ ... ---------------------- -------------------
-200.0 .. -200.0 -199.97231886896392 .. -200.03173392832403 ...  1.405140770179355e-11   48.90219319940143
-175.0 .. -200.0 -174.95987290696857 .. -200.03277605720874 ... 1.7288536738689093e-11   39.24216178913423
-150.0 .. -200.0 -149.94211658840587 .. -200.03288365171088 ...  2.221373259886304e-11  29.600970874872083
-125.0 .. -200.0 -124.91940414235607 .. -200.02704428456494 ... 2.8366900929366782e-11  18.549397931354616
-100.0 .. -200.0   -99.89696839768818 .. -200.0119855517868 ...  3.461143192185526e-11  6.6353309283519035
 -75.0 .. -200.0  -74.88433270277011 .. -199.98755720788955 ...  3.881855053338731e-11  -6.139923914333862
 -50.0 .. -200.0 -49.889719068935264 .. -199.95851881256343 ...  3.931563281813583e-11  -20.61334185009448
 -25.0 .. -200.0   -24.9155668122923 .. -199.93326542522965 ...  3.591127477829506e-11 -38.322252464628534
   0.0 .. -200.0 0.04408996224175425 .. -199.92005756492776 ... 3.0463215301695057e-11   -61.1223250722071
  25.0 .. -200.0   25.001835485662816 .. -199.9225877322705 ...  2.583819229946889e-11   -88.6417413684232
  50.0 .. -200.0   49.96991258695252 .. -199.93810160528204 ... 2.2965006249010528e-11 -115.92334087152777
  75.0 .. -200.0    74.9541161228128 .. -199.95957421993253 ...  2.040522328867382e-11 -138.61848327288334
 100.0 .. -200.0   99.95293929798622 .. -199.97980020168612 ...  1.708866117585782e-11 -156.76960759013545
 125.0 .. -200.0  124.96067815838208 .. -199.99438059625945 ... 1.3254220582293216e-11 -171.86704490238282
 150.0 .. -200.0  149.97092812140502 .. -200.00248245828382 ...  9.736009223719278e-12  175.11933206321967
 175.0 .. -200.0   174.97966097140406 .. -200.0057125561094 ... 7.0493374498980925e-12  164.31171513458463
 200.0 .. -200.0    199.9858278213182 .. -200.0064025381238 ... 5.1891614352136636e-12  155.68806577787495
-200.0 .. -175.0  -199.9726012419791 .. -175.04417989031938 ... 1.7346726656009182e-11  58.194318496544845
-175.0 .. -175.0  -174.9583988725216 .. -175.04787719748776 ... 2.1164052170242602e-11   49.01219357925647
-150.0 .. -175.0 -149.93676757496698 .. -175.05311803401713 ... 2.7556127478919716e-11    40.0317451629414
-125.0 .. -175.0 -124.90737495749306 .. -175.04961837992377 ... 3.5062430106783925e-11  28.177542997558902
-100.0 .. -175.0   -99.87718012282345 .. -175.0295212715798 ...  4.214978904192725e-11  13.515360878046911
 -75.0 .. -175.0  -74.85943540653658 .. -174.99118187226603 ...  4.699581020580927e-11    -3.5896683259775
 -50.0 .. -175.0   -49.86485581273417 .. -174.9429017578023 ...  4.895458854215875e-11  -22.90399415696121
 -25.0 .. -175.0  -24.89667631665922 .. -174.90016994081816 ...  4.794069555181633e-11  -44.01478462512318
             ...                                        ... ...                    ...                 ...
    0.0 .. 175.0  0.07743500183678054 .. 175.09306260204872 ... 4.0397108392210966e-11   -50.2370272415893
   25.0 .. 175.0     25.11189772222917 .. 175.0592833569958 ... 4.2254515413214435e-11 -27.914620313512447
   50.0 .. 175.0     50.12573678520827 .. 175.0096456040758 ... 4.2079132212031285e-11 -4.3867204510172275
   75.0 .. 175.0    75.11504974124594 .. 174.96153559546528 ... 4.0478507799496806e-11  18.486249167324814
  100.0 .. 175.0    100.08694560984694 .. 174.9298363514549 ...  3.728040947215361e-11  38.902947609216355
  125.0 .. 175.0   125.05360115526018 .. 174.92024033402313 ...  3.206575057234722e-11   56.09758303427284
  150.0 .. 175.0   150.02675608962414 .. 174.92803464260268 ... 2.5619376170673633e-11   69.60530662164686
  175.0 .. 175.0     175.0107066474462 .. 174.9430195552396 ...  1.934597441954906e-11   79.35818512826286
  200.0 .. 175.0     200.002906073179 .. 174.95097442538363 ...  1.638757315935333e-11   86.60766607817193
 -200.0 .. 200.0  -200.01155889402082 .. 200.01316750821366 ...  5.846464663878313e-12  -131.2777801258076
 -175.0 .. 200.0   -175.0128621295698 .. 200.01543073999264 ...  6.703084974422652e-12 -129.81253789854145
 -150.0 .. 200.0  -150.01438911685415 .. 200.02106395130272 ...    8.5120262139557e-12 -124.33759811870262
 -125.0 .. 200.0   -125.0153614001027 .. 200.02934881121996 ... 1.1053453674788519e-11 -117.62791613116748
 -100.0 .. 200.0  -100.01355813627043 .. 200.04069891222193 ... 1.4314154440939591e-11 -108.42459945643391
  -75.0 .. 200.0    -75.00537432798211 .. 200.0540082963793 ... 1.8110498677621346e-11  -95.68275534099766
  -50.0 .. 200.0   -49.98716612990017 .. 200.06572349358694 ... 2.2344823891764376e-11  -78.95085205033362
  -25.0 .. 200.0  -24.958154659842595 .. 200.07009678941574 ... 2.7240626323285054e-11 -59.164270775606454
    0.0 .. 200.0  0.07619143087919736 .. 200.06168679773657 ...  3.271153433695371e-11 -38.994637415530526
   25.0 .. 200.0    25.104596948781673 .. 200.0393128530757 ...  3.728570357026443e-11  -20.59877355025309
   50.0 .. 200.0    50.11613243871938 .. 200.00817271974248 ...  3.884692170218242e-11  -4.025504126985765
   75.0 .. 200.0    75.10754271744837 .. 199.97753283972654 ...  3.665959766644338e-11  11.800161349500426
  100.0 .. 200.0   100.08413795019683 .. 199.95575231286674 ...  3.172076809054885e-11   27.73963624735183
  125.0 .. 200.0    125.0557107946247 .. 199.94650619235952 ...  2.577185699540861e-11    43.8369853598751
  150.0 .. 200.0   150.03160623352406 .. 199.94799613017943 ... 2.0306171586517033e-11   58.71014847987613
  175.0 .. 200.0    175.01578781947123 .. 199.9553078158115 ...  1.581603696309956e-11   70.54388429868378
  200.0 .. 200.0   200.00702971238024 .. 199.95973253247462 ... 1.3639664136883761e-11    80.0973567603393
    
>>>
>>> fieldmap.pole()       # get the field pole information
time min coordinate [2] max coordinate [2]    vector        distance            angle              ratio      
 s                                                             mm                deg                          
---- ------------------ ------------------ ----------- ------------------ ------------------ -----------------
 1126259462      50.0 .. 100.0     -75.0 .. -75.0 (-125-175j) 215.05813167606567 125.53767779197439 1.349543578763341
```

## Accosicated classes

Note that in addition to the TimeSeires associated classes listed below.

| Classes             | Description                   |
|---------------------|-------------------------------|
| [TimeSeires](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html)      | Dealing with a single time-series of a MCG dataset |
| [TimeSeriesArray](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html) | Dealing with a multi-channel time-series array of a MCG dataset | 
| [Channel](https://pjjung.github.io/mcgpy/Classes/Chaeenl.html)         | Listing the channel information from a configuration file or a raw frame file |
| [FieldMap](https://pjjung.github.io/mcgpy/Classes/FieldMap.html)        | Calculate a lead field matrix and the current-dipole information |
  
