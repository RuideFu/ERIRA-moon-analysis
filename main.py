from file import read_data_files
from process import jansky2temp

path = "/data"
scans_data = read_data_files(path)
a_constant = 3.614
b_constant = 3.229

print(
    jansky2temp(scans_data[0].brightness(a_constant, b_constant), 369500),
    scans_data[0].name,
)
