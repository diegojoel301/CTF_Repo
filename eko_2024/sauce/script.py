import netCDF4

# Ruta al archivo .nc
archivo_nc = 'flag3.html.nc'

# Abre el archivo NetCDF
dataset = netCDF4.Dataset(archivo_nc, 'r')

# Muestra la información general del archivo
print(dataset)

# Para acceder a las variables dentro del archivo
for variable in dataset.variables:
    print(f"Variable: {variable}")
    print(f"Datos de la variable: {dataset.variables[variable][:]}")

# Cierra el archivo cuando hayas terminado
dataset.close()
