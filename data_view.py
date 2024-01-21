import netCDF4

# !!! Absolute Pfade müssen auch hier angepasst werden !!! #

input = "/User/path/netCDF/file.nc"
data = netCDF4.Dataset(input)
print(data.variables.keys())
x = data.variables['x']
print(x)
y = data.variables['y']
print(y)
z = data.variables['z']
print(z)
polar_stereographic = data.variables['polar_stereographic']
print(polar_stereographic)


# Ausgabe wenn mit einem Beispieldokument vorgenommen

"""
dict_keys(['polar_stereographic', 'x', 'y', 'z'])

<class 'netCDF4._netCDF4.Variable'>
float64 x(x)
    standard_name: projection_x_coordinate
    long_name: x coordinate of projection
    units: m
unlimited dimensions: 
current shape = (1216,)
filling on, default _FillValue of 9.969209968386869e+36 used


<class 'netCDF4._netCDF4.Variable'>
float64 y(y)
    standard_name: projection_y_coordinate
    long_name: y coordinate of projection
    units: m
unlimited dimensions: 
current shape = (1792,)
filling on, default _FillValue of 9.969209968386869e+36 used

float32 z(y, x)
    long_name: z
    _FillValue: nan
    actual_range: [  0 100]
    grid_mapping: polar_stereographic
unlimited dimensions: 
current shape = (1792, 1216)
filling on


<class 'netCDF4._netCDF4.Variable'>
|S1 polar_stereographic()
    grid_mapping_name: polar_stereographic
    straight_vertical_longitude_from_pole: -45.0
    false_easting: 0.0
    false_northing: 0.0
    latitude_of_projection_origin: 90.0
    standard_parallel: 70.0
    long_name: CRS definition
    longitude_of_prime_meridian: 0.0
    semi_major_axis: 6378273.0
    inverse_flattening: 298.279411123064
    spatial_ref: PROJCS["NSIDC Sea Ice Polar Stereographic North",GEOGCS["Unspecified datum based upon the Hughes 1980 ellipsoid",DATUM["Not_specified_based_on_Hughes_1980_ellipsoid",SPHEROID["Hughes 1980",6378273,298.279411123064,AUTHORITY["EPSG","7058"]],AUTHORITY["EPSG","6054"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4054"]],PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",70],PARAMETER["central_meridian",-45],PARAMETER["scale_factor",1],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["X",EAST],AXIS["Y",NORTH],AUTHORITY["EPSG","3411"]]
    GeoTransform: -3850000 6250 0 5850000 0 -6250 
unlimited dimensions: 
current shape = ()
filling on, default _FillValue of  used"""