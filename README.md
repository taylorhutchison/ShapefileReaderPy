# Shapefile Reader for Python

This project consists of three files (ShapefileReader.py, ShapefileIndexReader.py, and DbaseReader.py) that can be used to read the three main components of the Shapefile Format. You can read the full shapefile specification  at http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf

## Shapefile Basics
A shapefile actually consists of three files:
1. SHP - this is the main file that contains the geometry of your shapefile.
2. SHX - this is an index file that keeps information on how long (in bytes) each record is.
2. DBF - this file uses the dbase format and keeps the attribute information for each record.

## How to Use

To read the main file records do the following:

```
from ShapefileReader import Shapefile
shp = Shapefile("Path/to/file.shp")
shp.read()
print(shp.Records)
```