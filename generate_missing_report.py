from src.MissingReport import MissingReport

if __name__ == "__main__":
    missing = MissingReport.instance("./sample/scholar", "./sample/scopus", 'f30503aac3d657ad4cd3609572708b12')
    missing.execute()
