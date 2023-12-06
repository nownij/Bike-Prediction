from Functions import Reader as Rd
import parameters as pr
import test
'''
data = Rd.showCSV(pr.file_path)
    data_op = Rd.dataOptimization(data)

    # interval = int(input("Input Interval : "))
    result = Rd.usageOverTime(data_op, 10)
'''
if __name__ == "__main__":
    filename_result = test.date_Range_Settings()