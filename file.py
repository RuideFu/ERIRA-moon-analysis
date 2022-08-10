import os
import re
from process import scan


def read_data_files(dir_path):
    """
    Read in all md1 files from giving directory path, relative to the root folder of the scripts
    """
    scans = []
    for f in sorted(os.listdir(os.curdir + dir_path)):
        m = re.search("^([^0]+)(\w+)\.md1$", f)
        if m:
            if "a" in m.group(2):
                channel = 0
            elif "b" in m.group(2):
                channel = 1
            else:
                channel = -1

            target = m.group(1) + " " + m.group(2)
            file_path = os.path.join(dir_path, f)
            with open(os.curdir + file_path, "r") as f:
                nums = []
                for line in f:
                    if line == "*\n" or line == "TELESCOPE: The Mighty Forty\n":
                        continue
                    m = re.search(
                        "^(LOCAL [STARTOP]+ [DATEIM]+): (\d+[/:]\d+[/:]\d+\s*\w*)", line
                    )
                    if not m:
                        nums.append(float(line))
                start_t, start_dec, start_v, ts, decs, vs = 0, 1, 2, [], [], []
                for i in range(len(nums)):
                    num = nums[i]
                    if ((i - start_t) % 3) == 0:
                        ts.append(num)
                    elif ((i - start_dec) % 3) == 0:
                        decs.append(num)
                    elif ((i - start_v) % 3) == 0:
                        vs.append(num)
                    else:
                        print(f"i {i} doesn't work!!")
                scans.append(scan(f.name, channel, ts, vs, decs))
    return scans
