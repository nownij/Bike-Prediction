from Functions import Reader as Rd
import pandas as pd
import parameters as pr

if __name__ == "__main__":
    data = Rd.showCSV(pr.file_path)
    op = Rd.dataOptimization(data)

    print(op)