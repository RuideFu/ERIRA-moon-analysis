import math

"""
a scan by the mighty forty telescope
contains data of the scan and some analysis functions
"""


class scan:
    def __init__(self, name, channel, ts, vs, decs):
        """
        create a scan object
        name: file name
        channel: 0 is channel A, 1 is channel B, -1 if unknown
        ts: time list
        vs: voltage list
        decs: declination list
        """
        self.name = name
        self.channel = channel
        self.ts = ts  # time
        self.vs = vs  # voltage
        self.decs = decs  # declination

    def calibration_front(self):
        """
        the average voltage of calibration on at the start of the observation
        """
        cal_values = []

        if len(self.vs) < 2:
            return 1

        previous_diff = abs(self.vs[0] - self.vs[1])
        for i in range(1, len(self.vs) - 1):
            # for i in range(len(self.vs) - 1)
            diff = abs(self.vs[i] - self.vs[i + 1])
            if (diff - 2 * previous_diff) < 0.01:
                cal_values.append(self.vs[i])
                previous_diff = diff
            else:
                # print(i, diff, previous_diff, "yes")
                break
        sum = 0
        for cal_value in cal_values:
            sum += cal_value
        if len(cal_values) == 0:
            return 1
        cal_value = sum / len(cal_values)
        print("cal", cal_value)
        return cal_value

    def calibration_back(self):
        """
        the average voltage of calibration on at the end of the observation
        """
        cal_values = []

        if len(self.vs) < 2:
            return 1

        previous_diff = abs(self.vs[-1] - self.vs[-2])
        breakcount = 0
        for i in reversed(range(1, len(self.vs) - 1)):
            # for i in range(len(self.vs) - 1)
            diff = abs(self.vs[i] - self.vs[i - 1])
            if (diff - 2 * previous_diff) < 0.01:
                if breakcount == 1:
                    cal_values.append(self.vs[i])
                previous_diff = diff
            else:
                # print(i, diff, previous_diff, "yes")
                breakcount += 1
                if breakcount == 2:
                    break
        sum = 0
        for cal_value in cal_values:
            sum += cal_value
        if len(cal_values) == 0:
            return 1
        cal_value = sum / len(cal_values)
        print("reverse_cal", cal_value)
        return cal_value

    def calibration(self):
        """
        calibration final voltage from cal-on and cal-off data
        """
        avg_cal = (
            self.calibration_front() + self.calibration_back()
        ) / 2 - self.baseline()
        print("avg cal", avg_cal)
        return avg_cal

    def baseline(self):
        """
        the average value of cal-off voltage at the end of the observation
        """
        cal_values = []

        if len(self.vs) < 2:
            return 1

        previous_diff = abs(self.vs[-1] - self.vs[-2])
        for i in reversed(range(1, len(self.vs) - 1)):
            # for i in range(len(self.vs) - 1)
            diff = abs(self.vs[i] - self.vs[i - 1])
            if (diff - 2 * previous_diff) < 0.01:
                cal_values.append(self.vs[i])
                previous_diff = diff
            else:
                # print(i, diff, previous_diff, "yes")
                break
        sum = 0
        for cal_value in cal_values:
            sum += cal_value
        if len(cal_values) == 0:
            return 1
        cal_value = sum / len(cal_values)
        print("baseline", cal_value)
        return cal_value

    def max_min_volt_diff(self):
        """
        the difference between peak and baseline
        """
        max = self.vs[0]
        min = self.vs[1]
        for v in self.vs:
            if v > max:
                max = v
            if v < min:
                min = v
        print("peak", max, min)
        return max - self.baseline()

    def brightness(self, a_constant, b_constant):
        """
        brightness in Jansky, a_constant and b_constant is determined by callibration
        """
        jansky_constant = 1541
        if self.channel == 0:
            return (
                self.max_min_volt_diff()
                / self.calibration()
                * (jansky_constant / a_constant)
            )
        elif self.channel == 1:
            return (
                self.max_min_volt_diff()
                / self.calibration()
                * (jansky_constant / b_constant)
            )
        else:
            return 0


# (max - min)/cal_avg * 3.614 => A
#                     * 3.229 => B


def jansky2temp(flux, moon_dist):
    flux *= math.pow(10, -23)
    lam = 21
    k = 1.38 * math.pow(10, -16)
    r_moon = 1737

    return (flux * math.pow(lam, 2) * math.pow(moon_dist, 2)) / (
        2 * k * math.pi * math.pow(r_moon, 2)
    )
