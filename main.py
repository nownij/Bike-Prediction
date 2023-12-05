from Functions import Reader as Rd
import parameters as pr

if __name__ == "__main__":
    data = Rd.showCSV(pr.file_path)
    data_op = Rd.dataOptimization(data)

    # interval = int(input("Input Interval : "))
    result = Rd.usageOverTime(data_op, 10)