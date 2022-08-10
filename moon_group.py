#######################################################



#######################################################

def process_scan(scan):
    with open(scan["filepath"], "r") as f:
        nums = []
        for line in f:
            if line == '*\n' or line == 'TELESCOPE: The Mighty Forty\n':
                continue
            m = re.search("^(LOCAL [STARTOP]+ [DATEIM]+): (\d+[/:]\d+[/:]\d+\s*\w*)", line)
            if m:
                scan[m.group(1)] = m.group(2).strip()
            else:
                nums.append(float(line))
        start_t, start_dec, start_v, ts, decs, vs = 0, 1, 2, [], [], []
        for i in range(len(nums)):
            num = nums[i]
            if ((i - start_t)%3) == 0:
                ts.append(num)
            elif ((i - start_dec)%3) == 0:
                decs.append(num)
            elif ((i - start_v)%3) == 0:
                vs.append(num)
            else:
                print(f"i {i} doesn't work!!")
        scan["ts"] = ts
        scan["decs"] = decs
        scan["vs"] = vs

#######################################################

p = "/content/drive/MyDrive/Moon"
bk.output_notebook()
scans = get_data_files(p)

for scan in scans:
    process_scan(scan)
    p1 = bk.figure(
        plot_width=550, plot_height=350,
        x_axis_label = "t", y_axis_label = "v", title = scan["target"]
    )
    p1.scatter(scan["ts"],scan["vs"], color="red")

    p2 = bk.figure(
        plot_width=350, plot_height=350,
        x_axis_label = "t", y_axis_label = "v", title = scan["target"]
    )
    p2.scatter(scan["ts"],scan["decs"], color="blue")
    bk.show(row(p1, p2))

