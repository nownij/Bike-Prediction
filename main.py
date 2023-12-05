from Functions import Reader as Rd
import parameters as pr

if __name__ == "__main__":
    data = Rd.showCSV(pr.file_path)
    op = Rd.dataOptimization(data)

    Rd.showGraph(op)